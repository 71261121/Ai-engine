"""
Writer Agent V7 — Content Engineering compliant carousel writer.
Follows DESIGN_SYSTEM_V7 + CONTENT_ENGINEERING rules exactly.

Rules enforced:
- 5-7 slides max (aggressive compression)
- Zero fluff policy (no conversational text)
- Hook & Close mandatory (slide 1 = eyebrow+massive title, last = numbered list+CTA)
- Visual mapping to 6 V7 layouts (no consecutive same layout)
- No pink/purple/red — only Teal + Orange
- Every data slide needs source citation
"""
import json
from typing import Dict, Any, List
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.llm_client import get_client


WRITER_SYSTEM = """You are a world-class carousel content engineer for AIWITHSUFIYAN.

You write Instagram carousels that make people STOP scrolling and SAVE the post.
You follow these STRICT rules — NEVER break them:

## CONTENT ENGINEERING RULES

### Slide Count: 5-7 MAXIMUM
- NEVER generate more than 7 slides. Optimal is 5-6.
- If content is long, COMPRESS by merging related ideas on one slide.
- Use Split Magazine layouts to compare two things on one slide.

### Zero Fluff Policy
- DELETE all conversational text.
- Convert paragraphs into PUNCHY statements or massive single numbers.
- BAD: "One of the major benefits of using X is that it allows developers to..."
- GOOD: "Zero Over-fetching."
- BAD: "Many companies have found that AI can help them improve efficiency."
- GOOD: "3x faster. 40% cheaper."

### Hook (Slide 1) MUST have:
- Eyebrow pill: short category tag (e.g., "SOFTWARE ARCHITECTURE 101", "AI DEEP DIVE")
- Massive 2-word headline (e.g., "BEYOND THE PROMPT.", "API WARS")
- 1-2 line subtitle setting stakes

### Close (Final Slide) MUST have:
- 3 numbered takeaways (concise, actionable)
- CTA box with specific value (NOT "like and subscribe")
- GOOD CTA: "Save this cheat sheet. You'll need it for your next system design interview."

### Visual Mapping — Assign each slide to ONE of these layouts:
1. hero — Massive title + SVG mesh background (ONLY for slide 1)
2. bento — 3-tier glass card grid with sparkline + heatmap + insight (for data-heavy slides)
3. flowchart — Vertical timeline with nodes + stat badge (for process/sequence slides)
4. split — 50/50 top/bottom with massive stat (for comparison/contrast)
5. grid — 4-panel glassmorphism grid (for multi-point takeaways)
6. outro — Centered list + CTA box (ONLY for final slide)

### Layout Diversity
- NEVER use same layout twice in a row.
- Slide 1 MUST be "hero". Slide N MUST be "outro".

## OUTPUT FORMAT

Return a JSON object:
{
  "eyebrow_tags": ["CATEGORY 101", "CONTEXT TAG"],
  "slides": [
    {
      "layout": "hero",
      "eyebrow": "CATEGORY 101",
      "headline_top": "BEYOND THE",
      "headline_accent": "PROMPT.",
      "subtitle": "1-2 line stakes statement with <strong>bold emphasis</strong> on key phrase."
    },
    {
      "layout": "bento",
      "eyebrow": "Visual Volume",
      "headline": "The Baseline has",
      "headline_accent": "Shifted.",
      "main_stat": "34M",
      "main_stat_suffix": "+",
      "main_label": "DAILY AI OUTPUT",
      "main_desc": "Images generated across major platforms every 24 hours.",
      "stat2_value": "71%",
      "stat2_label": "of feed visual data is now synthetic.",
      "stat3_value": "-70%",
      "stat3_label": "Reduction in production time.",
      "insight_icon": "⚡",
      "insight_text": "The barrier to entry isn't creation anymore—it's <strong>differentiation.</strong>",
      "source": "Gartner AI Trends, 2025"
    },
    {
      "layout": "flowchart",
      "eyebrow": "The Multiplier",
      "headline": "The",
      "headline_accent": "Human-in-the-Loop Premium",
      "nodes": [
        {"text": "Step 1 Name", "active": false},
        {"text": "Step 2 Name", "active": true},
        {"text": "Step 3 Name", "active": false}
      ],
      "badge_value": "+372%",
      "badge_label": "Median ROI",
      "source": "HBR Analytics, 2025"
    },
    {
      "layout": "split",
      "eyebrow": "The Personalization Premium",
      "headline": "Hyper-Targeting",
      "headline_accent": "Scale.",
      "body_text": "1-2 sentences explaining the concept.",
      "stat_value": "+202",
      "stat_label": "Higher Engagement",
      "insight_text": "Strategic insight with <strong>bold key term</strong> highlighted.",
      "source": "Forbes Tech Council, 2025"
    },
    {
      "layout": "grid",
      "eyebrow": "Quick Takeaways",
      "headline": "Key",
      "headline_accent": "Insights",
      "panels": [
        {"icon": "🔧", "title": "Panel 1", "body": "Key insight text", "accent": "teal"},
        {"icon": "⚡", "title": "Panel 2", "body": "Key insight text", "accent": "orange"},
        {"icon": "🎯", "title": "Panel 3", "body": "Key insight text", "accent": "teal"},
        {"icon": "💡", "title": "Panel 4", "body": "Key insight text", "accent": "teal"}
      ],
      "source": ""
    },
    {
      "layout": "outro",
      "eyebrow": "The Bottom Line",
      "headline": "AI is the engine.",
      "headline_accent": "driver.",
      "items": [
        {"text": "Takeaway 1 with <strong>bold key term</strong>."},
        {"text": "Takeaway 2 with <strong>bold key term</strong>."},
        {"text": "Takeaway 3 with <strong>bold key term</strong>."}
      ],
      "cta_text": "Save this post.",
      "cta_highlight": "You'll need these stats for your 2025 strategy.",
      "cta_icon": "📌"
    }
  ],
  "caption": "Engaging caption with emojis and line breaks.",
  "hashtags": ["ai", "tech", ...]
}
"""


class WriterAgent:
    """
    V7 Writer with Content Engineering rules.
    Generates 5-7 slide carousels mapped to V7 layout archetypes.
    Budget-limited: max 3 attempts, picks best by quality score.
    """

    def __init__(self):
        self.client = get_client()
        self.max_attempts = 3

    def write(self, research: Dict[str, Any], topic: str) -> Dict[str, Any]:
        """Generate V7-quality carousel content from research data."""
        best = None
        best_score = 0

        for attempt in range(self.max_attempts):
            prompt = f"""Based on this research, create a V7-quality Instagram carousel.

TOPIC: "{topic}"

RESEARCH DATA:
{json.dumps(research, indent=2)[:4000]}

Follow ALL Content Engineering rules from the system prompt.
- 5-7 slides MAXIMUM
- Slide 1 MUST use "hero" layout
- Last slide MUST use "outro" layout
- NO consecutive same layouts
- ZERO fluff — punchy, compressed, data-driven
- Every stat needs a source citation
- <strong> tags for bold emphasis in text

Attempt {attempt + 1}/{self.max_attempts}
Previous quality score: {best_score:.2f}

Return ONLY the JSON object, no markdown fences."""

            result = self.client.call_json(
                prompt, system=WRITER_SYSTEM, model_tier="fast"
            )

            if "error" in result:
                print(f"  ⚠️ Writer attempt {attempt+1} failed: {result['error'][:80]}")
                continue

            # Validate and score
            score = self._validate(result)
            print(f"  📊 Writer attempt {attempt+1}: score={score:.2f}")

            if score > best_score:
                best_score = score
                best = result

        if best is None:
            # Emergency fallback — minimal valid structure
            best = {
                "slides": [
                    {"layout": "hero", "eyebrow": topic.upper()[:30],
                     "headline_top": topic.split()[0].upper() if topic else "TOPIC",
                     "headline_accent": " ".join(topic.split()[1:3]).upper() if topic else "OVERVIEW",
                     "subtitle": f"Here is the data driving {topic} in 2025."},
                    {"layout": "outro", "eyebrow": "The Bottom Line",
                     "headline": "The key insight", "headline_accent": "is here.",
                     "items": [{"text": "More research needed for full carousel."}],
                     "cta_text": "Follow for more.", "cta_highlight": "Data-driven insights weekly.", "cta_icon": "📌"}
                ],
                "caption": f"#{topic.replace(' ', '_')}",
                "hashtags": ["ai", "tech", "data"]
            }

        # Ensure final layout validity
        best = self._enforce_rules(best)
        return best

    def _validate(self, result: Dict) -> float:
        """Score content quality. 0-1 scale."""
        score = 0.0
        slides = result.get("slides", [])

        # Slide count: 5-7 is optimal
        n = len(slides)
        if 5 <= n <= 7:
            score += 0.3
        elif 4 <= n <= 8:
            score += 0.15

        # First slide is hero
        if slides and slides[0].get("layout") == "hero":
            score += 0.15

        # Last slide is outro
        if slides and slides[-1].get("layout") == "outro":
            score += 0.15

        # Layout diversity (no consecutive same)
        layouts = [s.get("layout", "") for s in slides]
        diverse = all(layouts[i] != layouts[i+1] for i in range(len(layouts)-1))
        if diverse:
            score += 0.1

        # Has caption
        if result.get("caption"):
            score += 0.1

        # Has hashtags
        if result.get("hashtags"):
            score += 0.05

        # Content quality heuristic — longer titles = less fluff usually
        total_title_len = sum(
            len(str(s.get("headline", "")) + str(s.get("headline_top", "")))
            for s in slides
        )
        if total_title_len > 30:
            score += 0.15

        return min(score, 1.0)

    def _enforce_rules(self, result: Dict) -> Dict:
        """Post-process to ensure Content Engineering rules are met."""
        slides = result.get("slides", [])

        # Enforce 7 max
        if len(slides) > 7:
            slides = slides[:7]
            # Make last an outro if it isn't
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
            if slides[i]["layout"] == slides[i-1]["layout"]:
                alternatives = ["bento", "flowchart", "split", "grid"]
                current = slides[i]["layout"]
                for alt in alternatives:
                    if alt != current:
                        slides[i]["layout"] = alt
                        break

        return result
