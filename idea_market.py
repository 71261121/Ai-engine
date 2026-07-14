"""
Idea Market - Generates 20 distinct ideas, runs tournament, picks top 5.
Evolutionary approach: many candidates → competitive evaluation → winner.
"""
import json
from typing import Dict, Any, List
import sys
sys.path.insert(0, "/".join(__file__.split("/")[:-3]))
from src.llm_client import get_client


IDEA_GEN_SYSTEM = """You are an idea generator for AIWITHSUFIYAN carousels.
Generate DISTINCT, SPECIFIC, DATA-BACKED carousel concepts.
Each idea must have: unique angle, specific hook, target statistic, audience pain point.
No generic ideas. No "AI is changing everything" BS.

Output JSON:
{"ideas": [{"title": "...", "hook": "...", "angle": "contrarian|data_reveal|step_by_step|framework|case_study", 
            "key_stat": "...", "pain_point": "...", "target_audience": "founders|engineers|leaders|all", 
            "differentiator": "what makes this unique vs competitors", "est_engagement": 0-100}]}"""


TOURNAMENT_SYSTEM = """You are a tournament judge.
Compare two carousel ideas head-to-head.
Return JSON: {"winner": "A" or "B", "reasoning": "...", "score_a": 0-100, "score_b": 0-100}"""


class IdeaMarket:
    """Generates many ideas, runs tournament, outputs top 5."""

    def __init__(self):
        self.client = get_client()
        self.population_size = 20
        self.tournament_rounds = 3

    def generate_ideas(self, topic: str, trend_context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate 20 distinct ideas."""
        prompt = f"""Topic: "{topic}"

Trend context: {json.dumps(trend_context, indent=2) if trend_context else "None"}

Generate {self.population_size} DISTINCT carousel ideas.
Each idea must be fundamentally different in:
- Hook style (curiosity, data, authority, contrarian, emotional, pattern interrupt)
- Narrative structure (problem-solution, data-reveal, framework, case study, step-by-step)
- Target audience segment (founders, engineers, AI leaders, general)
- Key statistic/insight (different data point each)

Output JSON with all 20 ideas. Be ruthless - kill generic ideas."""

        result = self.client.call_json(prompt, system=IDEA_GEN_SYSTEM, model_tier="fast")
        if "error" in result:
            return self._fallback_ideas(topic)
        return result.get("ideas", self._fallback_ideas(topic))

    def run_tournament(self, ideas: List[Dict[str, Any]], topic: str) -> List[Dict[str, Any]]:
        """Run elimination tournament to find top ideas."""
        if len(ideas) <= 5:
            return ideas

        current_round = ideas.copy()

        for round_num in range(self.tournament_rounds):
            next_round = []
            # Pair up
            for i in range(0, len(current_round), 2):
                if i + 1 < len(current_round):
                    a, b = current_round[i], current_round[i + 1]
                    winner = self._judge_matchup(a, b, topic)
                    next_round.append(winner)
                else:
                    # Odd number - auto-advance
                    next_round.append(current_round[i])

            current_round = next_round
            if len(current_round) <= 5:
                break

        # If still too many, score all and take top 5
        if len(current_round) > 5:
            scored = [(self._score_idea(idea, topic), idea) for idea in current_round]
            scored.sort(key=lambda x: x[0], reverse=True)
            current_round = [idea for _, idea in scored[:5]]

        return current_round

    def _judge_matchup(self, a: dict, b: dict, topic: str) -> dict:
        """Judge two ideas against each other."""
        prompt = f"""Compare these two carousel ideas for topic: "{topic}"

Idea A: {json.dumps(a)}
Idea B: {json.dumps(b)}

Which is BETTER for Instagram engagement (saves, shares, completion)?
Consider: hook strength, uniqueness, data credibility, shareability, brand fit.
Return JSON with winner, reasoning, and scores."""

        result = self.client.call_json(prompt, system=TOURNAMENT_SYSTEM, model_tier="fast")
        if "error" in result:
            return a  # default to first
        winner = result.get("winner", "A")
        return a if winner == "A" else b

    def _score_idea(self, idea: dict, topic: str) -> float:
        """Quick score for final ranking."""
        prompt = f"""Score this carousel idea 0-100 for: "{topic}"
Idea: {json.dumps(idea)}
Consider: hook, uniqueness, data, shareability, brand fit. Return just the number."""
        result = self.client.call(prompt, system=TOURNAMENT_SYSTEM, model_tier="fast", temperature_key="evaluation", max_tokens=50)
        try:
            return float(result.get("content", "50").strip()) / 100
        except:
            return 0.5

    def _fallback_ideas(self, topic: str) -> list:
        """Fallback ideas if generation fails."""
        return [
            {"title": f"{topic}: The Data", "hook": f"5 numbers that explain {topic}", "angle": "data_reveal", "key_stat": "TBD", "pain_point": "Confusion", "target_audience": "all", "differentiator": "Pure data", "est_engagement": 70},
            {"title": f"{topic}: The Contrarian Take", "hook": f"Everyone's wrong about {topic}", "angle": "contrarian", "key_stat": "TBD", "pain_point": "Groupthink", "target_audience": "engineers", "differentiator": "Contrarian", "est_engagement": 80},
            {"title": f"{topic}: Step-by-Step", "hook": f"How to actually do {topic}", "angle": "step_by_step", "key_stat": "TBD", "pain_point": "No clear path", "target_audience": "founders", "differentiator": "Actionable", "est_engagement": 75},
        ]

    def get_top_ideas(self, topic: str, trend_context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Full pipeline: generate → tournament → top 5."""
        ideas = self.generate_ideas(topic, trend_context)
        return self.run_tournament(ideas, topic)
