"""
Narrative Content Writer (V100).
Integrates ToT Tournament Winner Hooks, Progressive Disclosure drip math,
and Reflexion Buffer optimization rules to construct high-retention slide blueprints.
"""
import json
from typing import Dict, Any, List, Optional
from src.llm_client import get_client
from src.memory.reflexion_buffer import get_reflexion_buffer


class NarrativeWriterV100:
    """
    V100 Writer constructing 6-slide progressive disclosure carousels
    using ToT Winner Hooks and self-optimizing Reflexion rules.
    """

    def __init__(self):
        self.client = get_client()
        self.reflexion = get_reflexion_buffer()

    def write(self, research: Dict[str, Any], topic: str, winner_hook: Dict[str, Any], arc_id: str = "explainer") -> Dict[str, Any]:
        print(f"  ✍️ [Narrative Writer V100] Constructing 6-slide progressive disclosure blueprint...")

        # Load dynamic self-optimization rules from Reflexion Buffer
        rules = self.reflexion.load_rules(topic, limit=3)
        rules_text = "\n".join([f"- REFLEXION RULE: {r}" for r in rules]) if rules else "- REFLEXION RULE: Ensure every stat has clear comparison context."

        hook_headline = winner_hook.get("hook", f"{topic} is Broken.")
        hook_sub = winner_hook.get("subtitle", "The exact architectural breakdown and blueprint to fix it.")
        eyebrow = f"{topic[:25].upper()} BLUEPRINT"

        prompt = f"""Write a 6-slide progressive disclosure carousel blueprint for: "{topic}"
WINNER HOOK (Slide 1 Headline): "{hook_headline}"
WINNER SUBTITLE: "{hook_sub}"
RESEARCH DATA: {json.dumps(research.get('key_statistics', [])[:3])}

{rules_text}

Return ONLY valid JSON:
{{
  "slides": [
    {{"layout": "hero", "eyebrow": "{eyebrow}", "headline": "{hook_headline}", "subtitle": "{hook_sub}"}},
    {{"layout": "concept_deepdive", "eyebrow": "{eyebrow}", "headline": "The Core Architecture", "box1_title": "The Problem", "box1_body": "...", "box2_title": "The Mechanism", "box2_body": "...", "box3_title": "The Payoff", "box3_body": "..."}},
    {{"layout": "process_detail", "eyebrow": "{eyebrow}", "headline": "Execution Flow", "box1_title": "Step 1: Isolate", "box1_body": "...", "box2_title": "Step 2: Decouple", "box2_body": "...", "box3_title": "Step 3: Automate", "box3_body": "..."}},
    {{"layout": "stat_highlight", "headline": "The Reality Check", "main_stat": "73%", "stat_label": "of modern engineering organizations see massive bottlenecks without this decoupling."}},
    {{"layout": "comparative_text", "headline": "Amateur vs Pro Approach", "left_col": "Tight coupling, manual retry logic, synchronous blocking requests.", "right_col": "Idempotent event triggers, exponential backoff, autonomous state recovery."}},
    {{"layout": "outro", "eyebrow": "THE BOTTOM LINE", "headline": "Key Architectural Insight", "items": [{{"text": "Bookmark this blueprint for your next review."}}], "cta_text": "SAVE THIS POST.", "cta_highlight": "Follow @AIWITHSUFIYAN for daily systems engineering deep dives."}}
  ]
}}"""

        res = self.client.call_json(prompt, system="You are a world-class narrative architect. Return ONLY valid JSON.", model_tier="fast")
        if isinstance(res, dict) and "slides" in res and isinstance(res["slides"], list) and len(res["slides"]) >= 4:
            return res

        return self._fallback_blueprint(topic, hook_headline, hook_sub, eyebrow)

    def _fallback_blueprint(self, topic: str, hook_headline: str, hook_sub: str, eyebrow: str) -> Dict[str, Any]:
        return {
            "slides": [
                {"layout": "hero", "eyebrow": eyebrow, "headline": hook_headline, "subtitle": hook_sub},
                {"layout": "concept_deepdive", "eyebrow": eyebrow, "headline": "The Core Architecture", "box1_title": "The Bottleneck", "box1_body": "Traditional architectures force synchronous state blocking across every microservice boundary.", "box2_title": "The Mechanism", "box2_body": "By introducing autonomous event-driven loops, systems self-heal without manual intervention.", "box3_title": "The Payoff", "box3_body": "Engineers ship 4x faster with 99.99% operational reliability and zero silent state drift."},
                {"layout": "process_detail", "eyebrow": eyebrow, "headline": "The 3-Step Execution Flow", "box1_title": "Step 1: Isolate State", "box1_body": "Separate transactional boundaries from long-running analytical pipelines.", "box2_title": "Step 2: Dead-Letter Queues", "box2_body": "Implement automated backoff circuits for failed network requests.", "box3_title": "Step 3: Continuous Telemetry", "box3_body": "Track p99 latency anomalies across distributed agent boundaries in real time."},
                {"layout": "stat_highlight", "headline": "The 73% Reality Check", "main_stat": "73%", "stat_label": "of enterprise architectures experience silent bottlenecks within 6 months of deployment without this structure."},
                {"layout": "comparative_text", "headline": "Amateur vs Pro Approach", "left_col": "Tight coupling, manual retry logic, synchronous blocking requests across all services.", "right_col": "Idempotent event triggers, exponential backoff, autonomous state recovery circuits."},
                {"layout": "outro", "eyebrow": "THE BOTTOM LINE", "headline": "Key Architectural Insight", "items": [{"text": "Bookmark this blueprint — you will reference it across your projects."}], "cta_text": "SAVE THIS POST.", "cta_highlight": "You'll need these architectural insights for your next production deployment."}
            ]
        }
