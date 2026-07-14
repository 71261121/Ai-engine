"""
Meta-Loop - Self-improvement from ACTUAL Instagram data.
Learns from: save_rate, share_rate, watch_time, completion_rate, CTR,
comments, followers_gained, negative_feedback.
NOT from LLM confidence - from OUTCOME metrics.
"""
import json
from typing import Dict, Any, List
from pathlib import Path
import sys
sys.path.insert(0, "/".join(__file__.split("/")[:-3]))
from src.llm_client import get_client
from src.memory.experience_db import get_experience_db


METRICS_FOCUS = [
    "save_rate", "share_rate", "completion_rate", "ctr",
    "comments", "followers_gained", "negative_feedback",
    "reach", "engagement_rate"
]


class MetaLoop:
    """Learns from actual post performance. Detects patterns. Auto-improves."""

    def __init__(self):
        self.client = get_client()
        self.db = get_experience_db()

    def analyze_performance(self, days: int = 30) -> Dict[str, Any]:
        """Analyze what worked and what didn't over last N days."""
        recent = self.db.load_recent(days=days)

        if not recent:
            return {"status": "insufficient_data", "min_samples": 50}

        successful = [e for e in recent if e.metrics and e.metrics.get("engagement_rate", 0) > 0.02]
        failed = [e for e in recent if e.metrics and e.metrics.get("engagement_rate", 0) <= 0.02]

        analysis = {
            "total_posts": len(recent),
            "success_rate": len(successful) / len(recent),
            "top_performers": self._extract_patterns(successful),
            "bottom_performers": self._extract_patterns(failed),
            "metric_averages": self._average_metrics(recent),
            "prompt_effectiveness": self._analyze_prompts(recent),
            "visual_patterns": self._analyze_visuals(successful),
            "topic_performance": self._analyze_topics(recent),
        }

        # Generate improvement recommendations
        analysis["improvements"] = self._generate_improvements(analysis)
        return analysis

    def _extract_patterns(self, experiences: List) -> Dict[str, Any]:
        """Extract common patterns from a group of experiences."""
        hooks = [e.hook for e in experiences if e.hook]
        narratives = [e.narrative_structure for e in experiences if e.narrative_structure]
        visuals = [e.visual_system for e in experiences if e.visual_system]

        return {
            "common_hooks": list(set(hooks)),
            "common_narratives": list(set(narratives)),
            "common_visuals": list(set(visuals)),
            "sample_size": len(experiences),
        }

    def _average_metrics(self, experiences: List) -> Dict[str, float]:
        """Calculate average metrics across experiences."""
        if not experiences:
            return {}
        totals = {}
        counts = {}
        for e in experiences:
            for metric, value in (e.metrics or {}).items():
                if isinstance(value, (int, float)):
                    totals[metric] = totals.get(metric, 0) + value
                    counts[metric] = counts.get(metric, 0) + 1
        return {m: totals[m] / counts[m] for m in totals if counts[m] > 0}

    def _analyze_prompts(self, experiences: List) -> Dict[str, Any]:
        """Analyze which prompts performed best."""
        prompt_perf = {}
        for e in experiences:
            for key, version in (e.prompt_versions or {}).items():
                if key not in prompt_perf:
                    prompt_perf[key] = {"versions": [], "avg_engagement": 0}
                prompt_perf[key]["versions"].append({
                    "version": version,
                    "engagement": e.metrics.get("engagement_rate", 0) if e.metrics else 0,
                })
                prompt_perf[key]["avg_engagement"] += e.metrics.get("engagement_rate", 0) if e.metrics else 0
        for key in prompt_perf:
            count = len(prompt_perf[key]["versions"])
            if count > 0:
                prompt_perf[key]["avg_engagement"] /= count
        return prompt_perf

    def _analyze_visuals(self, experiences: List) -> Dict[str, Any]:
        """Analyze which visual patterns worked."""
        return {
            "systems_used": list(set([e.visual_system for e in experiences])),
            "color_systems": list(set([e.color_system for e in experiences])),
            "gene_patterns": self._extract_gene_patterns(experiences),
        }

    def _extract_gene_patterns(self, experiences: List) -> Dict[str, int]:
        """Count gene usage across successful posts."""
        gene_counts = {}
        for e in experiences:
            for gene_type, gene_value in (e.design_genes or {}).items():
                key = f"{gene_type}:{gene_value}"
                gene_counts[key] = gene_counts.get(key, 0) + 1
        return dict(sorted(gene_counts.items(), key=lambda x: x[1], reverse=True)[:20])

    def _analyze_topics(self, experiences: List) -> Dict[str, float]:
        """Analyze topic performance."""
        topic_perf = {}
        for e in experiences:
            topic = e.topic
            if topic not in topic_perf:
                topic_perf[topic] = {"count": 0, "total_engagement": 0}
            topic_perf[topic]["count"] += 1
            topic_perf[topic]["total_engagement"] += e.metrics.get("engagement_rate", 0) if e.metrics else 0
        return {t: v["total_engagement"] / v["count"] for t, v in topic_perf.items() if v["count"] > 0}

    def _generate_improvements(self, analysis: dict) -> List[Dict[str, Any]]:
        """Generate actionable improvement recommendations."""
        improvements = []

        # Check metric trends
        avgs = analysis.get("metric_averages", {})
        if avgs.get("save_rate", 0) < 0.035:
            improvements.append({
                "area": "hook",
                "issue": "Save rate below 3.5%",
                "recommendation": "Try more data-driven hooks. Focus on specific numbers, not vague claims.",
                "action": "increase_statistical_specificity"
            })

        if avgs.get("share_rate", 0) < 0.015:
            improvements.append({
                "area": "narrative",
                "issue": "Share rate below 1.5%",
                "recommendation": "Add contrarian angles that challenge conventional wisdom.",
                "action": "increase_contrarian_content"
            })

        if avgs.get("completion_rate", 0) < 0.70:
            improvements.append({
                "area": "design",
                "issue": "Completion rate below 70%",
                "recommendation": "Reduce slide count. Increase visual variety. Stronger slide 2-3 hooks.",
                "action": "optimize_slide_flow"
            })

        # Check visual patterns
        gene_patterns = analysis.get("visual_patterns", {}).get("gene_patterns", {})
        if gene_patterns:
            top_genes = list(gene_patterns.keys())[:3]
            improvements.append({
                "area": "design_genome",
                "issue": "Top performing gene combinations identified",
                "recommendation": f"Prioritize these visual genes: {top_genes}",
                "action": "weight_top_genes"
            })

        return improvements

    def record_post(self, experience: Any):
        """Record a new post for future learning."""
        self.db.save(experience)
