"""
Writer Agent - Generates carousel narrative with budget limits.
Maximum 5 hook attempts. Picks best hook, then generates narrative.
Single LLM, multiple prompts (NOT multiple models).
"""
import json
from typing import Dict, Any, List
import sys
sys.path.insert(0, "/".join(__file__.split("/")[:-3]))
from src.llm_client import get_client


WRITER_SYSTEM = """You are a world-class content writer for AIWITHSUFIYAN Instagram carousel.
Your job: turn research into a compelling carousel narrative.
Write hooks that make people STOP scrolling. Write narratives that make people SAVE the post.

Output JSON:
{
  "hooks": [{"text": "...", "style": "curiosity_gap|pattern_interrupt|authority|data_hook", "score": 0-100}],
  "selected_hook": 0,
  "narrative_structure": "problem_solution|data_reveal|contrarian|step_by_step",
  "slides": [
    {"type": "hook", "headline": "...", "subtext": "..."},
    {"type": "data", "headline": "...", "stat": "...", "context": "...", "source": "..."},
    {"type": "insight", "headline": "...", "body": "..."},
    {"type": "contrarian", "headline": "...", "body": "..."},
    {"type": "cta", "headline": "...", "body": "...", "cta_type": "save|share|follow"}
  ],
  "caption": "...",
  "first_comment": "...",
  "hashtags": ["tag1", "tag2", ...],
  "engagement_prediction": {"save_rate": 0.0, "share_rate": 0.0, "completion_rate": 0.0}
}"""


class WriterAgent:
    """Writer with budget-limited hook generation (max 5 attempts)."""

    def __init__(self):
        self.client = get_client()
        self.max_hook_attempts = 5

    def write(self, research: Dict[str, Any], topic: str) -> Dict[str, Any]:
        """Generate carousel narrative from research. Budget-limited."""
        best_narrative = None
        best_score = 0

        for attempt in range(self.max_hook_attempts):
            prompt = f"""Based on this research:
{json.dumps(research, indent=2)[:3000]}

Generate a complete Instagram carousel for topic: "{topic}"

Brand: AIWITHSUFIYAN
Audience: AI practitioners, founders, engineers
Style: Data-driven, bold, no fluff
Slides: 8-10 slides (1080x1350 format)

Attempt {attempt + 1}/{self.max_hook_attempts}
Previous best engagement prediction score: {best_score}

Generate hooks with variety:
- Attempt 1: Curiosity gap hook
- Attempt 2: Data/stat hook
- Attempt 3: Contrarian hook
- Attempt 4: Authority hook
- Attempt 5: Emotional hook

Score each hook 0-100 on:
- Curiosity (would you swipe?)
- Specificity (is it vague or concrete?)
- Shareability (would you send to a friend?)
- Brand fit (does it match AIWITHSUFIYAN voice?)

Then write the full carousel with the best hook."""

            result = self.client.call_json(prompt, system=WRITER_SYSTEM, model_tier="fast")

            if "error" in result:
                continue

            # Score the narrative
            score = self._score_narrative(result)
            if score > best_score:
                best_score = score
                best_narrative = result

        if best_narrative is None:
            best_narrative = {
                "hooks": [],
                "selected_hook": 0,
                "narrative_structure": "data_reveal",
                "slides": [],
                "caption": "",
                "hashtags": [],
                "engagement_prediction": {"save_rate": 0.0, "share_rate": 0.0, "completion_rate": 0.0}
            }

        return best_narrative

    def _score_narrative(self, narrative: dict) -> float:
        """Score a narrative based on hook quality and completeness."""
        score = 0
        hooks = narrative.get("hooks", [])
        if hooks:
            best_hook = max(hooks, key=lambda h: h.get("score", 0))
            score = best_hook.get("score", 50) / 100
        slides = narrative.get("slides", [])
        score += min(len(slides) / 10, 0.3)  # More slides = more complete
        if narrative.get("caption"):
            score += 0.1
        if narrative.get("hashtags"):
            score += 0.1
        return min(score, 1.0)
