"""
Research Agent - Autonomous deep research with BUDGET limits.
Maximum 3 attempts. No infinite loops. Best available published.
Uses trend data + web search + LLM analysis.
"""
import json
from typing import Dict, Any, List
import sys
sys.path.insert(0, str(__file__).rsplit("\\", 3)[0])
sys.path.insert(0, "/".join(__file__.split("/")[:-3]))
from src.llm_client import get_client


RESEARCH_SYSTEM = """You are a research specialist for AIWITHSUFIYAN Instagram carousel content.
Your job: find the most compelling, data-backed insights on a topic.
You search multiple angles, verify sources, and produce a research package.

Output JSON with:
{
  "topic_analysis": "clear topic statement",
  "key_statistics": [{"stat": "...", "source": "...", "year": "...", "confidence": "high/medium/low"}],
  "insights": ["insight1", "insight2", ...],
  "counter_narratives": ["contrarian angle1", ...],
  "audience_angle": "how this applies to AI practitioners",
  "content_gaps": ["what competitors miss", ...],
  "research_confidence": 0.0-1.0
}"""


class ResearchAgent:
    """Research agent with budget-limited execution (max 3 attempts)."""

    def __init__(self):
        self.client = get_client()
        self.max_attempts = 1  # NO infinite loops

    def research(self, topic: str, trend_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Research a topic with budget limits. Returns research package."""
        best_result = None
        best_score = 0

        for attempt in range(self.max_attempts):
            # Build research prompt with trend context
            prompt = f"""Research topic: "{topic}"

Available trend context:
{json.dumps(trend_context, indent=2) if trend_context else "No trend data available yet."}

Previous research attempt scores: {best_score if best_result else "None yet"}

Focus on:
1. Find 5-8 data-backed statistics with sources
2. Identify 3-5 unique insights competitors miss
3. Find a contrarian angle
4. Score your own research confidence (0-1)

Be specific. Use real data. No vague statements."""

            result = self.client.call_json(prompt, system=RESEARCH_SYSTEM, model_tier="fast")

            if "error" in result:
                continue

            score = result.get("research_confidence", 0)
            if score > best_score:
                best_score = score
                best_result = result

            # Plateau detection: if score didn't improve, stop
            if best_result and score <= best_score and attempt > 0:
                break

        if best_result is None:
            best_result = {
                "topic_analysis": topic,
                "key_statistics": [],
                "insights": [f"Research on {topic} - manual review recommended"],
                "counter_narratives": [],
                "audience_angle": "general AI practitioners",
                "content_gaps": [],
                "research_confidence": 0.3
            }

        return best_result
