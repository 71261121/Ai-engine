"""
5 Specialized Critics — Replaces UnifiedCritic with domain-expert evaluators.

Each critic has:
- Domain expertise (narrative, visual, data, voice, novelty)
- Topic-aware criteria (evaluates Kafka differently than Rust)
- Specific fix suggestions (not generic "improve quality")
- Verdict: PASS / REVISION_NEEDED / FAIL with detailed reasoning

The critics work in sequence:
1. NarrativeCritic → Does the story make sense? Is there tension?
2. ConceptCritic → Does the visual serve the concept? Metaphor quality?
3. DataCritic → Are stats contextualized? Source quality?
4. VoiceCritic → Does this sound like Sufiyan? Opinionated? Direct?
5. NoveltyCritic → Have I seen this exact approach before?
"""
import json
from typing import Dict, List, Any, Tuple
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.llm_client import get_client
from src.visual.topic_dna import get_topic_dna


class NarrativeCritic:
    """
    Evaluates: Does the STORY work?
    - Is there a clear narrative arc (hook → tension → resolution)?
    - Does each slide build on the previous one?
    - Is there information hierarchy (easy → medium → advanced)?
    - Would I want to swipe to the next slide?
    - Does the CTA feel earned, not forced?
    """

    def __init__(self):
        self.client = get_client()

    def evaluate(self, slides: List[Dict], topic: str, arc_id: str = "") -> Dict:
        dna = get_topic_dna(topic)
        slide_summary = self._summarize_slides(slides)

        prompt = f"""You are a NARRATIVE CRITIC for Instagram carousels.

TOPIC: "{topic}"
ARC: {arc_id}
TONE: {dna.get('tone', 'professional')}

SLIDES:
{slide_summary}

Evaluate these 5 criteria (0-10 each):

1. HOOK_STRENGTH: Does slide 1 make you NEED to swipe? Is it specific, not generic?
2. TENSION_BUILD: Does each slide build on the previous? Is there progressive disclosure?
3. INFORMATION_HIERARCHY: Easy → Medium → Advanced? Or random order?
4. PAYOFF_QUALITY: Does the outro feel earned? Are takeaways specific (not "AI is changing everything")?
5. SWIPE_URGENCY: After each slide, would you swipe to the next? Rate 1-5.

Return JSON:
{
  "hook_strength": {"score": 0-10, "verdict": "...", "fix": "..."},
  "tension_build": {"score": 0-10, "verdict": "...", "fix": "..."},
  "info_hierarchy": {"score": 0-10, "verdict": "...", "fix": "..."},
  "payoff_quality": {"score": 0-10, "verdict": "...", "fix": "..."},
  "swipe_urgency": {"score": 1-5, "per_slide": [1,2,3,4,5,6]},
  "overall_narrative_score": 0-10,
  "critical_fix": "The ONE thing that must change to improve narrative",
  "verdict": "PASS|REVISION_NEEDED|FAIL"
}"""

        result = self.client.call_json(prompt, system="You are a ruthless narrative critic. Return ONLY valid JSON.", model_tier="smart")

        if "error" in result:
            return {"overall_narrative_score": 5, "verdict": "PASS", "critical_fix": "Critic unavailable"}

        return result

    def _summarize_slides(self, slides: List[Dict]) -> str:
        parts = []
        for i, s in enumerate(slides):
            layout = s.get("layout", "?")
            role = s.get("narrative_role", "?")
            headline = s.get("headline", s.get("headline_top", ""))
            body = s.get("body_text", s.get("main_desc", s.get("subtitle", "")))
            parts.append(f"Slide {i+1} [{layout}/{role}]: \"{headline}\" — {body[:100]}")
        return "\n".join(parts)


class ConceptCritic:
    """
    Evaluates: Does the VISUAL serve the CONCEPT?
    - Does each slide have a unique visual identity (not just different text in same box)?
    - Is the TopicDNA metaphor actually used, or ignored?
    - Do the SVG elements add meaning, or just noise?
    - Is the visual hierarchy clear: eye → concept → data → insight?
    - Would a viewer REMEMBER this slide's visual?
    """

    def __init__(self):
        self.client = get_client()

    def evaluate(self, slides: List[Dict], topic: str) -> Dict:
        dna = get_topic_dna(topic)

        slide_details = []
        for i, s in enumerate(slides):
            concept = s.get("visual_concept", "NONE")
            elements = s.get("visual_elements", [])
            layout = s.get("layout", "?")
            slide_details.append(f"Slide {i+1} [{layout}]: concept=\"{concept[:120]}\", elements={len(elements)}")

        prompt = f"""You are a VISUAL CONCEPT CRITIC for Instagram carousels.

TOPIC: "{topic}"
TOPIC METAPHOR: {dna['visual_metaphor']['core']}
COLOR LANGUAGE: {json.dumps(dna.get('color_language', {}))}

SLIDES:
{chr(10).join(slide_details)}

Evaluate these 5 criteria (0-10 each):

1. CONCEPT_CLEARS: Does each slide have a unique visual concept (not just "glass card with text")?
2. METAPHOR_USAGE: Does the visual actually use the topic's metaphor? Or is it generic?
3. SVG_MEANING: Do the SVG elements add conceptual meaning, or just decoration?
4. VISUAL_HIERARCHY: Eye path: concept → data → insight. Clear or cluttered?
5. MEMORABILITY: Would a viewer REMEMBER any slide's visual approach?

Return JSON:
{
  "concept_clarity": {"score": 0-10, "per_slide": [1-10 for each], "verdict": "..."},
  "metaphor_usage": {"score": 0-10, "verdict": "...", "fix": "..."},
  "svg_meaning": {"score": 0-10, "verdict": "...", "fix": "..."},
  "visual_hierarchy": {"score": 0-10, "verdict": "..."},
  "memorability": {"score": 0-10, "verdict": "...", "most_memorable_slide": "..."},
  "overall_concept_score": 0-10,
  "critical_fix": "The ONE visual change that would transform this carousel",
  "verdict": "PASS|REVISION_NEEDED|FAIL"
}"""

        result = self.client.call_json(prompt, system="You are a ruthless visual concept critic. Return ONLY valid JSON.", model_tier="smart")

        if "error" in result:
            return {"overall_concept_score": 5, "verdict": "PASS", "critical_fix": "Critic unavailable"}

        return result


class DataCritic:
    """
    Evaluates: Are statistics USED WELL?
    - Every stat has a comparison baseline (not naked numbers)
    - Source citations are specific and recent
    - Numbers are in context (what does this MEAN for the viewer?)
    - No fake/hallucinated statistics
    - Data density is appropriate (not too sparse, not overwhelming)
    """

    def __init__(self):
        self.client = get_client()

    def evaluate(self, slides: List[Dict], topic: str) -> Dict:
        stats_found = []
        for i, s in enumerate(slides):
            for field in ["main_stat", "stat2_value", "stat3_value", "stat_value", "stat_label",
                          "main_desc", "insight_text", "body_text"]:
                val = s.get(field, "")
                if val and any(c.isdigit() for c in str(val)):
                    stats_found.append(f"Slide {i+1}.{field}: {val[:80]}")

        prompt = f"""You are a DATA CRITIC for Instagram carousels.

TOPIC: "{topic}"

STATS FOUND IN CAROUSEL:
{chr(10).join(stats_found) if stats_found else "No numeric data found"}

Evaluate these 4 criteria (0-10 each):

1. STAT_CONTEXT: Every number has a comparison baseline? (e.g., "80%" alone = BAD, "80% of Fortune 100 = GOOD")
2. SOURCE_QUALITY: Citations specific? Recent? Credible? (e.g., "Confluent 2023" = GOOD, "some study" = BAD)
3. DATA_DENSITY: Right amount of data? Not too sparse, not overwhelming?
4. HALLUCINATION_RISK: Any stats that seem made up? Too round? Too perfect?

Return JSON:
{
  "stat_context": {"score": 0-10, "naked_stats": ["list of stats without context"], "verdict": "..."},
  "source_quality": {"score": 0-10, "issues": ["specific issues"], "verdict": "..."},
  "data_density": {"score": 0-10, "verdict": "..."},
  "hallucination_risk": {"score": 0-10 (10=low risk), "suspect_stats": ["list"], "verdict": "..."},
  "overall_data_score": 0-10,
  "critical_fix": "The ONE data improvement that would transform this carousel",
  "verdict": "PASS|REVISION_NEEDED|FAIL"
}"""

        result = self.client.call_json(prompt, system="You are a ruthless data critic. Return ONLY valid JSON.", model_tier="smart")

        if "error" in result:
            return {"overall_data_score": 5, "verdict": "PASS", "critical_fix": "Critic unavailable"}

        return result


class VoiceCritic:
    """
    Evaluates: Does this SOUND like Sufiyan/AIWITHSUFIYAN?
    - Direct, opinionated, not corporate-speak
    - Uses concrete language, not abstract buzzwords
    - Has personality (not interchangeable with any other tech page)
    - CTA feels personal, not template-generated
    - Vocabulary matches the audience (engineers, not marketing)
    """

    def __init__(self):
        self.client = get_client()

    def evaluate(self, slides: List[Dict], topic: str, caption: str = "") -> Dict:
        all_text = []
        for i, s in enumerate(slides):
            texts = [str(s.get(f, "")) for f in
                     ["headline", "headline_top", "headline_accent", "subtitle",
                      "body_text", "main_desc", "insight_text", "eyebrow"]]
            texts = [t for t in texts if t and t != "None"]
            if texts:
                all_text.append(f"Slide {i+1}: {' | '.join(texts)}")

        if caption:
            all_text.append(f"\nCAPTION: {caption[:200]}")

        prompt = f"""You are a VOICE CRITIC for AIWITHSUFIYAN Instagram carousels.

BRAND VOICE: Direct, opinionated, technical, no fluff. Like a senior engineer talking to peers.
AUDIENCE: Software engineers, backend devs, data engineers.
AVOID: Corporate buzzwords, "leverage", "utilize", "in today's fast-paced world", "game-changer".

SLIDES TEXT:
{chr(10).join(all_text)}

Evaluate these 4 criteria (0-10 each):

1. AUTHENTICITY: Does this sound like a real engineer sharing knowledge, or a marketing team?
2. OPINION: Is there a clear point of view? Or is it neutral/informational?
3. BUZZWORD_FREE: Zero corporate speak? No "leverage", "utilize", "streamline"?
4. PERSONALITY: Could you remove "AIWITHSUFIYAN" and tell it's Sufiyan's? Or is it generic?

Return JSON:
{
  "authenticity": {"score": 0-10, "issues": ["buzzword found: '...'"], "verdict": "..."},
  "opinion": {"score": 0-10, "verdict": "...", "suggestion": "..."},
  "buzzword_free": {"score": 0-10, "offenders": ["list of buzzwords found"], "verdict": "..."},
  "personality": {"score": 0-10, "verdict": "..."},
  "overall_voice_score": 0-10,
  "critical_fix": "The ONE voice change that would make this sound more like Sufiyan",
  "verdict": "PASS|REVISION_NEEDED|FAIL"
}"""

        result = self.client.call_json(prompt, system="You are a ruthless voice critic. Return ONLY valid JSON.", model_tier="smart")

        if "error" in result:
            return {"overall_voice_score": 5, "verdict": "PASS", "critical_fix": "Critic unavailable"}

        return result


class NoveltyCritic:
    """
    Evaluates: Is this carousel VISUALLY UNIQUE?
    - Different from last 10 carousels on same topic
    - Not the same "big number at slide 2" pattern
    - Layout sequence is varied (not always hero→bento→split→grid→outro)
    - Visual approach is fresh (not recycled SVG patterns)
    - Topic-specific visuals, not generic dark theme
    """

    def __init__(self):
        self.client = get_client()

    def evaluate(self, slides: List[Dict], topic: str, recent_runs: List[Dict] = None) -> Dict:
        layout_seq = [s.get("layout", "?") for s in slides]
        roles = [s.get("narrative_role", "?") for s in slides]

        recent_summary = ""
        if recent_runs:
            for r in recent_runs[-5:]:
                recent_summary += f"  - {r.get('topic', '?')}: layouts={r.get('layouts', '?')}\n"

        prompt = f"""You are a NOVELTY CRITIC for Instagram carousels.

TOPIC: "{topic}"
THIS CAROUSEL LAYOUTS: {' → '.join(layout_seq)}
THIS CAROUSEL ROLES: {' → '.join(roles)}

RECENT CAROUSELS:
{recent_summary if recent_summary else "No recent runs"}

Evaluate:

1. LAYOUT_NOVELTY: Is this layout sequence different from recent ones? (0-10)
2. PATTERN_BREAK: Does slide 2 break the "big number reveal" pattern? (0-10)
3. VISUAL_FRESHNESS: Does this use topic-specific visuals or generic dark theme? (0-10)
4. ROLE_DIVERSITY: Are narrative roles varied across slides? (0-10)

Return JSON:
{
  "layout_novelty": {"score": 0-10, "verdict": "..."},
  "pattern_break": {"score": 0-10, "uses_big_number_slide2": true/false, "verdict": "..."},
  "visual_freshness": {"score": 0-10, "topic_specific": true/false, "verdict": "..."},
  "role_diversity": {"score": 0-10, "unique_roles": N, "verdict": "..."},
  "overall_novelty_score": 0-10,
  "critical_fix": "The ONE change that would make this feel genuinely new",
  "verdict": "PASS|REVISION_NEEDED|FAIL"
}"""

        result = self.client.call_json(prompt, system="You are a ruthless novelty critic. Return ONLY valid JSON.", model_tier="smart")

        if "error" in result:
            return {"overall_novelty_score": 5, "verdict": "PASS", "critical_fix": "Critic unavailable"}

        return result


class MasterpieceCritic:
    """
    FINAL CRITIC — Evaluates the OVERALL masterpiece potential.

    Combines signals from all 5 specialized critics.
    Asks: "Is this carousel going to STOP someone mid-scroll?"

    This is the ULTIMATE quality gate.
    """

    def __init__(self):
        self.client = get_client()

    def evaluate(self, slides: List[Dict], topic: str,
                 narrative_score: float, concept_score: float,
                 data_score: float, voice_score: float,
                 novelty_score: float) -> Dict:

        avg = (narrative_score + concept_score + data_score + voice_score + novelty_score) / 5
        lowest = min(narrative_score, concept_score, data_score, voice_score, novelty_score)
        highest = max(narrative_score, concept_score, data_score, voice_score, novelty_score)

        # Determine verdict based on scores
        if avg >= 8.0 and lowest >= 6.0:
            verdict = "MASTERPIECE"
        elif avg >= 6.5 and lowest >= 5.0:
            verdict = "STRONG"
        elif avg >= 5.0:
            verdict = "ACCEPTABLE"
        else:
            verdict = "NEEDS_MAJOR_REVISION"

        return {
            "scores": {
                "narrative": narrative_score,
                "concept": concept_score,
                "data": data_score,
                "voice": voice_score,
                "novelty": novelty_score
            },
            "average": round(avg, 2),
            "lowest": lowest,
            "highest": highest,
            "spread": round(highest - lowest, 2),
            "verdict": verdict,
            "masterpiece_probability": min(100, max(0, int(avg * 10))),
            "recommendation": self._get_recommendation(avg, lowest, narrative_score, concept_score, data_score, voice_score, novelty_score)
        }

    def _get_recommendation(self, avg, lowest, nav, con, data, voice, nov):
        if lowest == nav:
            return "Focus on narrative: improve hook, tension, and swipe urgency"
        elif lowest == con:
            return "Focus on visuals: use topic-specific metaphors, not generic dark theme"
        elif lowest == data:
            return "Focus on data: add context to every stat, verify sources"
        elif lowest == voice:
            return "Focus on voice: remove buzzwords, add opinion, be direct"
        elif lowest == nov:
            return "Focus on novelty: break the big-number pattern, use fresh layouts"
        elif avg < 5:
            return "MAJOR OVERHAUL needed — content, visuals, and voice all need work"
        else:
            return "Solid foundation — polish the weakest dimension to reach masterpiece"
