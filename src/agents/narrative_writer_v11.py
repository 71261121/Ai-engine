"""
Narrative Writer V9 — Narrative-first carousel content generation.
REPLACES the template-filling writer with intelligent story-structure generation.

Core difference from V7:
- V7: Fixed layout sequence → fill content into templates
- V9: Topic → narrative arc → information flow → layouts serve the story

Each carousel tells a DIFFERENT story based on what the topic needs.
"""
import json
from typing import Dict, Any, List
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.llm_client import get_client
from src.agents.narrative_arcs_v11 import (
    classify_topic, get_arc, get_slide_blueprint,
    get_density_for_position,
    get_cta_variant, NARRATIVE_ARCS
)


NARRATIVE_WRITER_SYSTEM = """You are a world-class narrative content strategist for AIWITHSUFIYAN Instagram carousels.

You do NOT fill templates. You CREATE stories and independent masterpieces.

## YOUR PROCESS
1. Understand the TOPIC deeply — what is it really about?
2. Identify the NARRATIVE ARC — what story structure fits this topic?
3. Plan the INFORMATION FLOW — what order should ideas appear?
4. CHOOSE A LAYOUT for each slide dynamically based on the required density and content purpose. 
5. Write each slide as a NARRATIVE BEAT — not a template field.

## CRITICAL RULES: END THE "BIG STAT" OBSESSION
- DO NOT force massive numbers or percentages onto slides if the content requires deep explanation.
- If a slide requires deep explanation (e.g., explaining a concept, a process, or a comparison), use text-dense layouts like 'concept_deepdive', 'process_detail', or 'comparative_text'.
- Ensure every slide has substantial, human-readable educational value. Do not leave slides mostly empty.

### Content Substance (ZERO TOLERANCE for empty/placeholder content)
- EVERY slide MUST contain actual topic-specific content.
- Every stat MUST have a real number from research.
- Every body_text MUST explain something specific about the topic.

### Visual Mapping (CHOOSE DYNAMICALLY)
Assign layouts based on WHAT the content needs:
- hero: Single powerful message (Slide 1 ONLY)
- concept_deepdive: For detailed text explanation of concepts (High Density Text)
- process_detail: For step-by-step deep text explanations (High Density Text)
- comparative_text: For comparing two things with deep text (Medium/High Density Text)
- outro: CTA and takeaways (Last slide ONLY)

### Layout Diversity
- NEVER use same layout twice in a row.
- Slide 1 MUST be "hero".
- Last slide MUST be "outro".
- Middle slides: CHOOSE FREELY from 'concept_deepdive', 'process_detail', and 'comparative_text' based on content needs.

## OUTPUT FORMAT

Return a JSON object with EXACTLY this structure at the root level:
{
  "narrative_arc": "the_arc_id",
  "topic_analysis": "brief analysis of why this arc fits",
  "slides": [
    // Array of slide objects based on the layouts below
  ]
}

### HERO layout:
{
  "layout": "hero",
  "narrative_role": "hook",
  "eyebrow": "CATEGORY",
  "headline_top": "FIRST LINE",
  "headline_accent": "SECOND LINE.",
  "subtitle": "25 words max. Explain what this carousel covers."
}

### CONCEPT_DEEPDIVE layout (NEW):
{
  "layout": "concept_deepdive",
  "narrative_role": "explanation",
  "eyebrow": "THE CONCEPT",
  "headline": "The Wipeout",
  "headline_accent": "Effect.",
  "box1_title": "The Concept",
  "box1_body": "20-30 words explaining the core idea deeply.",
  "box2_title": "Performance",
  "box2_body": "20-30 words explaining performance or secondary trait.",
  "box3_title": "Warning",
  "box3_body": "20-30 words explaining risks, warnings, or constraints."
}

### PROCESS_DETAIL layout (NEW):
{
  "layout": "process_detail",
  "narrative_role": "process",
  "eyebrow": "HOW IT WORKS",
  "headline": "The Engine",
  "headline_accent": "Internals.",
  "steps": [
    {"title": "Step 1", "body": "15-20 words explaining exactly what happens here.", "icon": "⚙️"},
    {"title": "Step 2", "body": "15-20 words explaining exactly what happens here.", "icon": "⚡"},
    {"title": "Step 3", "body": "15-20 words explaining exactly what happens here.", "icon": "🔒"}
  ]
}

### COMPARATIVE_TEXT layout (NEW):
{
  "layout": "comparative_text",
  "narrative_role": "comparison",
  "eyebrow": "VS BATTLE",
  "headline": "Choosing",
  "headline_accent": "Wisely.",
  "left_title": "Option A",
  "left_body": "30-40 words detailing the strengths and use cases.",
  "right_title": "Option B",
  "right_body": "30-40 words detailing the strengths and use cases.",
  "bottom_insight": "15 words on the ultimate deciding factor."
}


### OUTRO layout:
{
  "layout": "outro",
  "narrative_role": "cta",
  "eyebrow": "NEXT STEPS",
  "headline": "The Bottom Line.",
  "headline_accent": "The Strategy.",
  "items": [
    {"text": "Takeaway 1 with <strong>bold key term</strong>."},
    {"text": "Takeaway 2 with <strong>bold key term</strong>."},
    {"text": "Takeaway 3 with <strong>bold key term</strong>."}
  ],
  "cta_text": "Save this post.",
  "cta_highlight": "You'll need these stats.",
  "cta_icon": "📌"
}

IMPORTANT: Write as a NARRATIVE BEAT. CHOOSE the layout that BEST fits the depth of explanation required. Avoid big stats unless you have a real, impactful number. Use text-dense layouts for deep concepts.
"""

class NarrativeWriter:
    def __init__(self):
        self.client = get_client()
        self.max_attempts = 3

    def write(self, research: Dict, topic: str, arc_id: str = None) -> Dict:
        # Step 1: Use provided arc or classify
        if arc_id is None:
            arc_id = classify_topic(topic)
        arc = get_arc(arc_id)
        print(f"  📖 Narrative arc: {arc['name']} ({arc_id})")
        print(f"     Topic fits because: {[k for k in arc['best_for'] if k in topic.lower()][:3]}")

        # Step 2: Build arc blueprint for the prompt
        blueprint = self._build_blueprint(arc_id)

        # Step 3: Generate content with narrative intelligence
        best = None
        best_score = 0

        for attempt in range(self.max_attempts):
            result = self._generate(research, topic, arc_id, blueprint, attempt + 1)

            if result is None:
                continue

            score = self._evaluate_narrative_quality(result, arc_id)
            print(f"  📊 Attempt {attempt + 1}: narrative_score={score:.2f}")

            if score > best_score:
                best_score = score
                best = result

        if best is None or len(best.get("slides", [])) == 0:
            print("  ⚠️ Using fallback structure")
            best = self._fallback(topic, arc_id)

        # Step 4: Enforce narrative rules
        best = self._enforce_rules(best, arc_id)

        return best

    def _build_blueprint(self, arc_id: str) -> str:
        """Build a readable blueprint from the arc definition."""
        arc = get_arc(arc_id)
        lines = [
            f"NARRATIVE ARC: {arc['name']}", 
            f"Description: {arc['description']}", 
            "",
            "SLIDE STRUCTURE RULES:",
            "- You must design a 6 to 7 slide flow that best explains this topic.",
            "- Slide 1 MUST be 'hero'. Last slide MUST be 'outro'.",
            "- For the middle slides, use 'concept_deepdive', 'process_detail', and 'comparative_text' for deep educational value.",
            "- NEVER use the same layout twice in a row."
        ]
        return "\n".join(lines)

    def _generate(self, research: Dict, topic: str, arc_id: str, blueprint: str, attempt: int) -> Dict:
        """Generate carousel content using narrative blueprint."""
        research_summary = json.dumps(research, indent=2)[:3000]

        prompt = f"""Create a narrative-driven Instagram carousel for AIWITHSUFIYAN.

TOPIC: "{topic}"
NARRATIVE ARC: {arc_id}

{blueprint}

RESEARCH DATA:
{research_summary}

CRITICAL INSTRUCTIONS:
1. The narrative blueprint ABOVE is just a SUGGESTED structure. You MUST adapt the slide purposes and flow to best explain this specific TOPIC.
2. Write DATA WITH CONTEXT — never raw numbers without comparison/baseline
3. Each slide is a NARRATIVE BEAT — what does the viewer need to understand NOW?
4. Layouts serve the STORY — CHOOSE a layout for each slide from the Visual Mapping list based on its actual PURPOSE and DENSITY. Do not use the same layout twice in a row.
5. Information must be PROGRESSIVE — easy → medium → advanced
6. Zero fluff — every word earns its place
7. <strong> tags for bold emphasis

ATTEMPT {attempt}/3 — make each word count.

Return ONLY the JSON object."""

        result = self.client.call_json(
            prompt, system=NARRATIVE_WRITER_SYSTEM, model_tier="fast"
        )

        if "error" in result:
            print(f"  ⚠️ Attempt {attempt} error: {result['error'][:80]}")
            return None

        return result

    def _evaluate_narrative_quality(self, result: Dict, arc_id: str) -> float:
        """
        Evaluate content quality from a narrative perspective.
        Goes beyond format validation to assess story quality.
        """
        score = 0.0
        slides = result.get("slides", [])
        expected_arc = result.get("narrative_arc", arc_id)

        # 1. Arc match (15%) — did the writer follow the narrative structure?
        if expected_arc == arc_id:
            score += 0.15

        # 2. Slide count matches arc (10%)
        arc = get_arc(arc_id)
        expected_count = arc["slide_count"]["optimal"]
        actual_count = len(slides)
        if actual_count == expected_count:
            score += 0.10
        elif abs(actual_count - expected_count) <= 1:
            score += 0.05

        # 3. Layout diversity (10%)
        layouts = [s.get("layout", "") for s in slides]
        diverse = all(layouts[i] != layouts[i + 1] for i in range(len(layouts) - 1))
        if diverse:
            score += 0.10

        # 4. Hero + Outro (10%)
        if slides and slides[0].get("layout") == "hero":
            score += 0.05
        if slides and slides[-1].get("layout") == "outro":
            score += 0.05

        # 5. Data context quality (20%) — check if stats have context
        data_slides = [s for s in slides if s.get("layout") in ("bento", "split")]
        context_count = 0
        for ds in data_slides:
            for field in ["main_desc", "stat2_label", "stat3_label", "insight_text", "insight"]:
                val = str(ds.get(field, ""))
                if len(val) > 20:  # Has meaningful context
                    context_count += 1
                    break
        if data_slides:
            context_ratio = context_count / len(data_slides)
            score += 0.20 * context_ratio

        # 6. Narrative variety check (15%) — avoid same-y content patterns
        headlines = [str(s.get("headline", "") + s.get("headline_top", "")) for s in slides]
        unique_words = set()
        for h in headlines:
            unique_words.update(h.lower().split())
        if len(unique_words) > 15:
            score += 0.15
        elif len(unique_words) > 8:
            score += 0.10

        # 7. Narrative role assignment (10%) — did writer think about slide purpose?
        roles = [s.get("narrative_role", "") for s in slides]
        if any(r for r in roles):
            score += 0.10

        # 7b. Content substance check — penalize empty/placeholder slides (20%)
        substance_score = 0
        for s in slides:
            layout = s.get("layout", "")
            has_substance = False
            # Check key content fields for actual topic-related content
            for field in ["body_text", "subtitle", "main_desc", "main_stat", "stat_value",
                          "insight_text", "headline_accent"]:
                val = str(s.get(field, "")).strip()
                if val and len(val) > 3 and val.lower() not in ("—", "data pending", "key", ""):
                    has_substance = True
                    break
            # Check nodes, panels, items for substance
            for key in ["nodes", "panels", "items"]:
                for item in s.get(key, []):
                    for ik in ["text", "title", "body", "content"]:
                        val = str(item.get(ik, "")).strip()
                        if val and len(val) > 5 and val.lower() not in ("step 1", "step 2", "point 1", "research needed"):
                            has_substance = True
                            break
            if has_substance:
                substance_score += 1
        if slides:
            substance_ratio = substance_score / len(slides)
            score += 0.20 * substance_ratio

        # 8. Content depth (10%) — longer substantive content = deeper thinking
        total_content_len = sum(
            len(str(s.get("main_desc", "")) + str(s.get("insight_text", "")) +
                str(s.get("body_text", "")) + str(s.get("subtitle", "")))
            for s in slides
        )
        if total_content_len > 400:
            score += 0.10
        elif total_content_len > 200:
            score += 0.05

        return min(score, 1.0)

    def _enforce_rules(self, result: Dict, arc_id: str) -> Dict:
        """Post-process to ensure narrative rules are met."""
        slides = result.get("slides", [])

        # Enforce max 7 slides
        if len(slides) > 7:
            slides = slides[:7]
            if slides[-1].get("layout") != "outro":
                slides[-1]["layout"] = "outro"
            result["slides"] = slides

        # Ensure first is hero
        if slides and slides[0].get("layout") != "hero":
            slides[0]["layout"] = "hero"

        # Ensure last is outro
        if slides and slides[-1].get("layout") != "outro":
            slides[-1]["layout"] = "outro"

        # Fix consecutive same layouts
        for i in range(1, len(slides)):
            if slides[i]["layout"] == slides[i - 1]["layout"]:
                alternatives = ["concept_deepdive", "process_detail", "comparative_text"]
                current = slides[i]["layout"]
                for alt in alternatives:
                    if alt != current:
                        slides[i]["layout"] = alt
                        break

        # Inject narrative arc if missing
        if not result.get("narrative_arc"):
            result["narrative_arc"] = arc_id

        return result

    def _fallback(self, topic: str, arc_id: str) -> Dict:
        """Emergency fallback — minimal valid narrative structure."""
        arc = get_arc(arc_id)
        slides_blueprint = arc["slides"]

        slides = []
        for bp in slides_blueprint[:6]:
            slide = {
                "layout": "concept_deepdive",
                "narrative_role": bp["position"],
                "eyebrow": topic.upper()[:30],
            }
            if bp["position"] == "hook":
                slide["layout"] = "hero"
                slide["headline_top"] = topic.split()[0].upper() if topic else "TOPIC"
                slide["headline_accent"] = " ".join(topic.split()[1:3]).upper() if len(topic.split()) > 1 else "OVERVIEW"
                slide["subtitle"] = f"A deep technical breakdown of {topic}."
            elif bp["position"] == "cta":
                slide["layout"] = "outro"
                slide["eyebrow"] = "The Bottom Line"
                slide["headline"] = "Key Insight"
                slide["headline_accent"] = "Here."
                cta = get_cta_variant(arc_id)
                slide["items"] = cta["items"]
                slide["cta_text"] = cta["cta_text"]
                slide["cta_highlight"] = cta["cta_highlight"]
                slide["cta_icon"] = cta["cta_icon"]
            else:
                # Middle slides fallback to concept_deepdive
                slide["layout"] = "concept_deepdive"
                slide["headline"] = "Core Concept"
                slide["headline_accent"] = bp["position"].replace("_", " ").title()
                slide["box1_title"] = "The Concept"
                slide["box1_body"] = f"Understanding the fundamental mechanics behind {topic} and why it matters."
                slide["box2_title"] = "Performance"
                slide["box2_body"] = "How this architecture impacts scalability, speed, and overall system efficiency."
                slide["box3_title"] = "Constraints"
                slide["box3_body"] = "Every technical choice comes with trade-offs. Knowing when not to use it is key."
            slides.append(slide)

        return {
            "narrative_arc": arc_id,
            "topic_analysis": f"Fallback structure for {topic}",
            "slides": slides,
            "caption": f"#{topic.replace(' ', '_')}",
            "hashtags": ["ai", "tech", "data"],
        }
