"""
Art Director Loop — Iterative Creative Revision System.

This is the KEY DIFFERENCE between V1 (linear pipeline) and V2 (creative loop).

V1 Flow: Topic → Write → Critic → Render → Done
V2 Flow: Topic → Write → Critic Panel → Art Director Revises → Re-Critic → Render → Verify

The Art Director:
1. Receives slides + all 5 critic scores
2. Identifies the WEAKEST dimension
3. Generates specific revision instructions
4. Writer revises based on instructions
5. Critics re-evaluate
6. Loop continues until MASTERPIECE or max iterations

This is what makes the system try to produce a MASTERPIECE every time,
not just "good enough."
"""
import json
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.llm_client import get_client
from src.visual.topic_dna import get_topic_dna


ART_DIRECTOR_SYSTEM = """You are an ART DIRECTOR for Instagram carousels.

Your job: When critics flag issues, you generate SPECIFIC REVISION INSTRUCTIONS
that the writer can execute. You don't write content — you DIRECT the revision.

Your instructions must be:
1. SPECIFIC: "Change slide 2 headline from X to Y" not "improve headline"
2. ACTIONABLE: The writer should know exactly what to change
3. PRIORITIZED: Focus on the WEAKEST dimension first
4. TOPIC-AWARE: Use the topic's metaphor and language

You receive:
- All 5 critic scores
- The slides with their current content
- The TopicDNA (metaphor, tone, key insight)

You output:
- Priority list of revisions (most impactful first)
- Specific instructions per slide
- What to KEEP (don't break what works)
- Target score after revisions

RULES:
1. NEVER tell the writer to "make it better" — always specific
2. NEVER revise more than 3 slides per iteration (focus, not scatter)
3. ALWAYS preserve what's working (if narrative is 9/10, don't touch it)
4. FOCUS on the lowest-scoring dimension first
5. If concept score is low, provide VISUAL BRIEFS, not just text changes"""


class ArtDirector:
    """
    Iterative creative revision system.

    The Art Director receives critic feedback and generates specific
    revision instructions. The writer executes revisions. Critics re-evaluate.
    Loop until MASTERPIECE or max iterations.
    """

    def __init__(self, max_iterations: int = 3, masterpiece_threshold: float = 7.5):
        self.client = get_client()
        self.max_iterations = max_iterations
        self.masterpiece_threshold = masterpiece_threshold

    def run_revision_loop(self, slides: List[Dict], topic: str, arc_id: str,
                          writer_fn=None, critics_fn=None) -> Tuple[List[Dict], Dict]:
        """
        Run the iterative revision loop.

        Args:
            slides: Initial slides from narrative writer
            topic: The carousel topic
            arc_id: The narrative arc
            writer_fn: Function to revise slides (slides, instructions) -> revised_slides
            critics_fn: Function to evaluate slides (slides) -> {critic_name: score_dict}

        Returns:
            (final_slides, revision_report)
        """
        current_slides = slides
        revision_log = []

        for iteration in range(self.max_iterations):
            # Step 1: Evaluate with critics
            scores = critics_fn(current_slides)

            # Step 2: Calculate overall score
            overall = self._calculate_overall(scores)

            revision_log.append({
                "iteration": iteration + 1,
                "scores": scores,
                "overall": overall,
                "slide_count": len(current_slides)
            })

            # Step 3: Check if masterpiece
            if overall >= self.masterpiece_threshold:
                return current_slides, {
                    "iterations": iteration + 1,
                    "final_score": overall,
                    "verdict": "MASTERPIECE",
                    "log": revision_log
                }

            # Step 4: Generate revision instructions
            instructions = self._generate_revision_instructions(
                current_slides, topic, arc_id, scores, overall
            )

            # Step 5: Execute revisions
            if writer_fn:
                current_slides = writer_fn(current_slides, instructions)
            else:
                current_slides = self._apply_revision_instructions(
                    current_slides, instructions, topic
                )

        # Final evaluation
        final_scores = critics_fn(current_slides)
        final_overall = self._calculate_overall(final_scores)

        return current_slides, {
            "iterations": self.max_iterations,
            "final_score": final_overall,
            "verdict": "MASTERPIECE" if final_overall >= self.masterpiece_threshold else "STRONG" if final_overall >= 6.0 else "NEEDS_WORK",
            "log": revision_log
        }

    def _calculate_overall(self, scores: Dict) -> float:
        """Calculate overall score from all critic scores."""
        all_scores = []
        for critic_name, score_data in scores.items():
            if isinstance(score_data, dict):
                for key, val in score_data.items():
                    if isinstance(val, (int, float)) and key.endswith("_score"):
                        all_scores.append(val)
                    elif isinstance(val, dict) and "score" in val:
                        all_scores.append(val["score"])

        if not all_scores:
            return 5.0

        return sum(all_scores) / len(all_scores)

    def _generate_revision_instructions(self, slides: List[Dict], topic: str,
                                         arc_id: str, scores: Dict,
                                         overall: float) -> Dict:
        """Generate specific revision instructions using LLM."""
        dna = get_topic_dna(topic)

        scores_summary = []
        for critic, data in scores.items():
            if isinstance(data, dict):
                score_val = data.get(f"overall_{critic.split('_')[0]}_score",
                                    data.get("overall_narrative_score",
                                    data.get("overall_concept_score",
                                    data.get("overall_data_score",
                                    data.get("overall_voice_score",
                                    data.get("overall_novelty_score", 5))))))
                scores_summary.append(f"  {critic}: {score_val}/10")
                if "critical_fix" in data:
                    scores_summary.append(f"    Critical fix: {data['critical_fix']}")

        slides_summary = []
        for i, s in enumerate(slides):
            headline = s.get("headline", s.get("headline_top", s.get("main_stat", "")))
            layout = s.get("layout", "?")
            slides_summary.append(f"  Slide {i+1} [{layout}]: {headline[:60]}")

        prompt = f"""ART DIRECTOR REVISION INSTRUCTIONS

TOPIC: "{topic}"
ARC: {arc_id}
OVERALL SCORE: {overall}/10 (target: {self.masterpiece_threshold}/10)

CRITIC SCORES:
{chr(10).join(scores_summary)}

CURRENT SLIDES:
{chr(10).join(slides_summary)}

TOPICDNA:
- Metaphor: {dna['visual_metaphor']['core']}
- Tone: {dna.get('tone', 'professional')}
- Key insight: {dna.get('key_insight', '')}

Generate SPECIFIC revision instructions. Focus on the WEAKEST dimension.

Return JSON:
{{
  "priority_dimension": "narrative|concept|data|voice|novelty",
  "overall_strategy": "One sentence on the main improvement needed",
  "slide_revisions": [
    {{
      "slide": 1,
      "change": "SPECIFIC change to make",
      "before": "current text/approach",
      "after": "revised text/approach",
      "reason": "why this improves the score"
    }}
  ],
  "keep_doing": ["things that are working well"],
  "target_score": 8.0,
  "estimated_iterations_remaining": 1
}}"""

        result = self.client.call_json(
            prompt, system=ART_DIRECTOR_SYSTEM, model_tier="smart"
        )

        if "error" in result:
            return {"priority_dimension": "narrative", "slide_revisions": [], "overall_strategy": "Focus on narrative improvement"}

        return result

    def _apply_revision_instructions(self, slides: List[Dict], instructions: Dict,
                                      topic: str) -> List[Dict]:
        """Apply revision instructions to slides without LLM (rule-based fallback)."""
        revised = [dict(s) for s in slides]
        revisions = instructions.get("slide_revisions", [])

        for rev in revisions:
            slide_idx = rev.get("slide", 1) - 1
            if 0 <= slide_idx < len(revised):
                slide = revised[slide_idx]
                change = rev.get("change", "")
                after = rev.get("after", "")

                # Apply specific changes based on what's being revised
                if "headline" in change.lower():
                    slide["headline"] = after
                elif "stat" in change.lower():
                    slide["main_stat"] = after
                elif "insight" in change.lower():
                    slide["insight_text"] = after
                elif "subtitle" in change.lower():
                    slide["subtitle"] = after
                elif "body" in change.lower():
                    slide["body_text"] = after

                revised[slide_idx] = slide

        return revised


class VoiceEngine:
    """
    Embeds Sufiyan's actual writing style.

    Uses the 2 manual Vault posts as reference examples.
    Detects and corrects:
    - Corporate buzzwords
    - Generic statements
    - Missing opinion
    - Template-sounding CTAs
    """

    BUZZWORDS = [
        "leverage", "utilize", "utilise", "streamline", "optimize", "synergy",
        "paradigm", "ecosystem", "holistic", "robust", "scalable", "innovative",
        "cutting-edge", "game-changer", "revolutionary", "transformative",
        "in today's fast-paced", "the world of", "it's worth noting",
        "it goes without saying", "at the end of the day", "moving forward",
        "in conclusion", "needless to say", "as we all know"
    ]

    OPINION_MARKERS = [
        "actually", "honestly", "here's the truth", "most people get this wrong",
        "hot take", "unpopular opinion", "the reality is", "let me be clear",
        "here's what nobody tells you", "stop doing", "start doing",
        "this is why", "the problem with", "the fix is"
    ]

    def __init__(self):
        self.client = get_client()

    def check_voice(self, slides: List[Dict], topic: str) -> Dict:
        """Check slides for voice compliance."""
        issues = []
        all_text = []

        for i, s in enumerate(slides):
            texts = [str(s.get(f, "")) for f in
                     ["headline", "headline_top", "headline_accent", "subtitle",
                      "body_text", "main_desc", "insight_text", "eyebrow"]]
            texts = [t for t in texts if t and t != "None"]
            slide_text = " ".join(texts)
            all_text.append(slide_text)

            # Check for buzzwords
            for buzzword in self.BUZZWORDS:
                if buzzword.lower() in slide_text.lower():
                    issues.append({
                        "slide": i + 1,
                        "type": "buzzword",
                        "word": buzzword,
                        "severity": "high"
                    })

        # Check for opinion (at least one slide should have opinion markers)
        full_text = " ".join(all_text)
        has_opinion = any(marker.lower() in full_text.lower() for marker in self.OPINION_MARKERS)

        if not has_opinion:
            issues.append({
                "slide": 0,
                "type": "no_opinion",
                "severity": "medium",
                "suggestion": "Add at least one opinionated statement (e.g., 'Here's the truth:' or 'Most people get this wrong')"
            })

        return {
            "issues": issues,
            "buzzword_count": sum(1 for i in issues if i["type"] == "buzzword"),
            "has_opinion": has_opinion,
            "text_length": len(full_text),
            "compliant": len([i for i in issues if i["severity"] == "high"]) == 0
        }

    def fix_buzzwords(self, text: str) -> str:
        """Replace buzzwords with direct language."""
        fixes = {
            "leverage": "use",
            "utilize": "use",
            "utilise": "use",
            "streamline": "simplify",
            "synergy": "combination",
            "paradigm": "approach",
            "holistic": "complete",
            "robust": "reliable",
            "scalable": "expandable",
            "innovative": "new",
            "cutting-edge": "latest",
            "game-changer": "major improvement",
            "revolutionary": "major",
            "transformative": "significant",
        }

        fixed = text
        for buzzword, replacement in fixes.items():
            fixed = fixed.replace(buzzword, replacement)
            fixed = fixed.replace(buzzword.capitalize(), replacement.capitalize())

        return fixed
