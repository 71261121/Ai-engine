"""
V12 Masterpiece Engine Orchestrator.
Integrates TopicDNA visual language, 8-Arc Narrative classification,
5 Specialized Critics (Narrative, Concept, Data, Voice, Novelty), and Art Director loops.
"""
import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.agents.research_agent import ResearchAgent
from src.agents.narrative_writer_v11 import NarrativeWriter as NarrativeWriterV11
from src.agents.narrative_arcs_v11 import classify_topic
from src.agents.specialized_critics import (
    NarrativeCritic, ConceptCritic, DataCritic,
    VoiceCritic, NoveltyCritic, MasterpieceCritic
)
from src.agents.art_director import ArtDirector
from src.agents.caption_agent import CaptionAgent
from src.visual.topic_dna import get_topic_dna
from src.visual.renderer import ConceptRenderer
from src.memory.experience_db import get_experience_db


class V12Orchestrator:
    """
    V12 Masterpiece Orchestrator implementing multi-perspective critique and TopicDNA aesthetics.
    """

    def __init__(self, max_iterations: int = 2):
        self.researcher = ResearchAgent()
        self.writer = NarrativeWriterV11()
        self.narrative_critic = NarrativeCritic()
        self.concept_critic = ConceptCritic()
        self.data_critic = DataCritic()
        self.voice_critic = VoiceCritic()
        self.novelty_critic = NoveltyCritic()
        self.master_critic = MasterpieceCritic()
        self.art_director = ArtDirector(max_iterations=max_iterations, masterpiece_threshold=8.0)
        self.captioner = CaptionAgent()
        self.renderer = ConceptRenderer()
        self.db = get_experience_db()
        self.project_root = Path(__file__).resolve().parent.parent.parent

    def run(self, topic: str, run_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute the full V12 Masterpiece pipeline."""
        start_time = time.time()
        if not run_id:
            run_id = f"run_v12_{int(start_time)}"

        output_dir = self.project_root / "outputs" / "runs" / run_id
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n✨ [V12 Masterpiece] Starting pipeline run for: '{topic}' (ID: {run_id})")

        # Step 1: TopicDNA Analysis
        print("  [1/8] Extracting TopicDNA & visual aesthetics...")
        topic_dna = get_topic_dna(topic)
        print(f"        ↳ Category: {topic_dna['category']} | Metaphor: {topic_dna['visual_metaphor']['core'][:60]}...")

        # Step 2: Narrative Arc Selection
        print("  [2/8] Selecting optimal narrative arc...")
        arc_id = classify_topic(topic)
        print(f"        ↳ Selected Arc: '{arc_id}'")

        # Step 3: Research
        print("  [3/8] Running deep data-backed research...")
        research = self.researcher.research(topic)

        # Step 4: Write Narrative Blueprint
        print("  [4/8] Generating V11 narrative slide sequence...")
        content_pkg = self.writer.write(research, topic, arc_id=arc_id)
        slides = content_pkg.get("slides", [])
        if not slides:
            slides = [
                {"layout": "hero", "headline": topic, "subtitle": "Deep technical analysis and architecture breakdown."},
                {"layout": "cta_classic", "headline": "Follow @AIWITHSUFIYAN", "subtitle": "Daily engineering deep dives."}
            ]

        # Step 5: Specialized Critique & Art Director Loop
        print("  [5/8] Running 5 Specialized Critics & Art Director revision loop...")
        def _critics_evaluator(current_slides):
            n_res = self.narrative_critic.evaluate(current_slides, topic, arc_id=arc_id)
            c_res = self.concept_critic.evaluate(current_slides, topic)
            d_res = self.data_critic.evaluate(current_slides, topic)
            v_res = self.voice_critic.evaluate(current_slides, topic)
            nov_res = self.novelty_critic.evaluate(current_slides, topic, recent_runs=self.db.load_recent(days=14))

            n_score = float(n_res.get("overall_narrative_score", 7.5))
            c_score = float(c_res.get("overall_concept_score", 7.5))
            d_score = float(d_res.get("overall_data_score", 7.5))
            v_score = float(v_res.get("overall_voice_score", 7.5))
            nov_score = float(nov_res.get("overall_novelty_score", 7.5))

            m_res = self.master_critic.evaluate(
                current_slides, topic, n_score, c_score, d_score, v_score, nov_score
            )

            return {
                "narrative_critic": n_res,
                "concept_critic": c_res,
                "data_critic": d_res,
                "voice_critic": v_res,
                "novelty_critic": nov_res,
                "masterpiece_critic": m_res
            }

        final_slides, revision_report = self.art_director.run_revision_loop(
            slides=slides,
            topic=topic,
            arc_id=arc_id,
            critics_fn=_critics_evaluator
        )

        # Step 6: Caption Generation
        print("  [6/8] Crafting viral social media caption...")
        caption_data = self.captioner.generate_caption(topic, final_slides, narrative_arc=arc_id)

        # Step 7: Visual Concept Rendering
        print(f"  [7/8] Rendering TopicDNA styled HTML slides to {output_dir.relative_to(self.project_root)}...")
        rendered_paths = self.renderer.render(final_slides, topic, output_dir, topic_dna=topic_dna)

        # Step 8: Package & Publish Manifest
        total_time = round(time.time() - start_time, 2)
        final_score = round(float(revision_report.get("final_score", 8.0)), 2)
        verdict = revision_report.get("verdict", "MASTERPIECE" if final_score >= 8.0 else "STRONG")

        publish_package = {
            "version": "v12.0_masterpiece",
            "run_id": run_id,
            "topic": topic,
            "arc_id": arc_id,
            "topic_dna": topic_dna,
            "slide_count": len(final_slides),
            "total_time_s": total_time,
            "final_score": final_score,
            "verdict": verdict,
            "caption": caption_data.get("caption", ""),
            "hashtags": caption_data.get("hashtags", []),
            "generated_files": [p.name for p in rendered_paths]
        }

        # Save package manifests
        (output_dir / "report.json").write_text(json.dumps(publish_package, indent=2, ensure_ascii=False), encoding="utf-8")
        (output_dir / "publish_package.json").write_text(json.dumps(publish_package, indent=2, ensure_ascii=False), encoding="utf-8")

        # Also update global latest publish package
        global_package = self.project_root / "publish_package.json"
        global_package.write_text(json.dumps(publish_package, indent=2, ensure_ascii=False), encoding="utf-8")

        # Save experience to MetaLoop DB
        self.db.save(publish_package)

        print(f"  [8/8] ✅ V12 Run complete! Score: {final_score}/10 | Verdict: {verdict} | Time: {total_time}s")

        return {
            "run_id": run_id,
            "output_dir": str(output_dir),
            "slides": final_slides,
            "revision_report": revision_report,
            "publish_package": publish_package
        }
