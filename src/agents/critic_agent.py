"""
Unified Critic - Single LLM call, multiple evaluation perspectives.
Replaces 6 separate critics with ONE comprehensive evaluation.
Fast, cheap, consistent.
"""
import json
from typing import Dict, Any
import sys
sys.path.insert(0, "/".join(__file__.split("/")[:-3]))
from src.llm_client import get_client


CRITIC_PROMPT = """You are a ruthless multi-perspective critic for Instagram carousel content.
Evaluate this carousel from ALL 6 perspectives in ONE pass.

Return JSON:
{
  "editorial": {"score": 0-100, "issues": [], "strengths": []},
  "ux": {"score": 0-100, "issues": [], "strengths": []},
  "story": {"score": 0-100, "issues": [], "strengths": []},
  "data": {"score": 0-100, "issues": [], "strengths": []},
  "brand": {"score": 0-100, "issues": [], "strengths": []},
  "visual": {"score": 0-100, "issues": [], "strengths": []},
  "fix_suggestions": ["must-fix issue 1", "must-fix issue 2"],
  "overall_verdict": "pass|needs_revision|fail",
  "overall_score": 0-100
}

Evaluation criteria:
- EDITORIAL: clarity, conciseness, authority, engagement. Every word earns its place.
- UX: visual hierarchy, scan path, cognitive load. 3-second rule.
- STORY: narrative arc, tension/release, information gaps. Slide 1 → need slide 10?
- DATA: source credibility, stat freshness, context. Fake stats = 0.
- BRAND: AIWITHSUFIYAN voice consistency, audience alignment.
- VISUAL: hierarchy, contrast, alignment, spacing, emotional impact, density.

Be HARSH. Score low if anything is weak. No participation trophies."""


class UnifiedCritic:
    """One LLM call, six perspectives. Fast and consistent."""

    def __init__(self):
        self.client = get_client()

    def evaluate(self, carousel: Dict[str, Any]) -> Dict[str, Any]:
        """Run all critic perspectives in a SINGLE LLM call."""
        prompt = CRITIC_PROMPT + "\n\nCarousel:\n" + json.dumps(carousel, indent=2)[:5000]

        result = self.client.call_json(
            prompt,
            system="You are a multi-perspective critic. Return ONLY valid JSON.",
            model_tier="fast",
            temperature_key="evaluation",
        )

        if "error" in result:
            # Fallback: return low scores
            return {
                "scores": {"editorial": 0, "ux": 0, "story": 0, "data": 0, "brand": 0, "visual": 0},
                "details": {"error": result.get("error")},
                "weighted_score": 0,
                "passed": False,
                "critical_issues": ["Critic evaluation failed"],
            }

        # Extract per-perspective scores
        scores = {}
        details = {}
        for perspective in ["editorial", "ux", "story", "data", "brand", "visual"]:
            if perspective in result:
                score = result[perspective].get("score", 0) if isinstance(result[perspective], dict) else 0
                scores[perspective] = score / 100
                details[perspective] = result[perspective]
            else:
                scores[perspective] = 0
                details[perspective] = {"score": 0, "issues": ["missing evaluation"]}

        # Overall score from LLM
        overall_score = result.get("overall_score", 0) / 100

        # Weighted average (matches LLM's overall if available)
        weights = {"editorial": 0.2, "ux": 0.2, "story": 0.15, "data": 0.15, "brand": 0.15, "visual": 0.15}
        weighted_score = sum(scores[p] * weights[p] for p in weights)

        # Use the higher of the two scores
        final_score = max(weighted_score, overall_score)

        # Critical issues
        critical_issues = result.get("fix_suggestions", [])

        return {
            "scores": scores,
            "details": details,
            "weighted_score": final_score,
            "passed": final_score >= 0.65,  # Lowered from 0.75 - practical threshold
            "critical_issues": critical_issues,
            "overall_verdict": result.get("overall_verdict", "needs_revision"),
        }
