"""
V10 Orchestrator Pipeline.
Coordinates Research -> Content Generation -> Unified Critique -> Revision -> Caption -> Visual Rendering.
"""
import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.agents.research_agent import ResearchAgent
from src.agents.narrative_writer import NarrativeWriter
from src.agents.critic_agent import UnifiedCritic
from src.agents.art_director import ArtDirector
from src.agents.caption_agent import CaptionAgent
from src.visual.renderer import ConceptRenderer
from src.memory.experience_db import get_experience_db


class V10Orchestrator:
    """
    Production V10 Orchestrator managing end-to-end carousel generation.
    """

    def __init__(self, max_iterations: int = 2):
        self.researcher = ResearchAgent()
        self.writer = NarrativeWriter()
        self.critic = UnifiedCritic()
        self.art_director = ArtDirector(max_iterations=max_iterations)
        self.captioner = CaptionAgent()
        self.renderer = ConceptRenderer()
        self.db = get_experience_db()
        self.project_root = Path(__file__).resolve().parent.parent.parent

    def run(self, topic: str, run_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute a full pipeline run for the specified topic."""
        start_time = time.time()
        if not run_id:
            run_id = f"run_v10_{int(start_time)}"

        output_dir = self.project_root / "outputs" / "runs" / run_id
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n🚀 [V10] Starting pipeline run for: '{topic}' (ID: {run_id})")

        # Step 1: Research
        print("  [1/6] Running topic research...")
        research = self.researcher.research(topic)

        # Step 2: Write Narrative Blueprint
        print("  [2/6] Writing initial slide narrative...")
        content_pkg = self.writer.write(research, topic)
        slides = content_pkg.get("slides", [])

        # Step 3: Critique & Revision Loop
        print("  [3/6] Running Art Director revision loop...")
        def _evaluate_wrapper(s_list):
            res = self.critic.evaluate({"topic": topic, "slides": s_list})
            return {"unified_critic": res}

        final_slides, revision_report = self.art_director.run_revision_loop(
            slides=slides,
            topic=topic,
            arc_id="explainer",
            critics_fn=_evaluate_wrapper
        )

        # Step 4: Caption Generation
        print("  [4/6] Generating viral caption...")
        caption_data = self.captioner.generate_caption(topic, final_slides, narrative_arc="explainer")

        # Step 5: Visual Rendering
        print(f"  [5/6] Rendering HTML slides to {output_dir.relative_to(self.project_root)}...")
        rendered_paths = self.renderer.render(final_slides, topic, output_dir)

        # Step 6: Package & Record
        total_time = time.time() - start_time
        final_score = revision_report.get("final_score", 7.5)
        verdict = revision_report.get("verdict", "STRONG")

        result = {
            "run_id": run_id,
            "topic": topic,
            "version": "v10",
            "output_dir": str(output_dir),
            "slides": final_slides,
            "slide_count": len(final_slides),
            "slide_files": [p.name for p in rendered_paths],
            "caption": caption_data.get("caption", ""),
            "hashtags": caption_data.get("hashtags", []),
            "revision_report": revision_report,
            "score": final_score,
            "verdict": verdict,
            "total_time_s": round(total_time, 2)
        }

        # Save run manifest
        manifest_path = output_dir / "report.json"
        manifest_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

        # Record to database
        self.db.save(result)

        print(f"  [6/6] ✅ Run complete in {total_time:.1f}s! Score: {final_score:.2f}/10 ({verdict})")
        return result

    def run_continuous(self, count: int = 1, topics: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Run multiple topics in sequence."""
        if not topics:
            topics = ["Understanding Microservice Boundaries", "Why SQL Beats NoSQL in 2026"]
        
        results = []
        for i in range(min(count, len(topics))):
            topic = topics[i]
            try:
                res = self.run(topic=topic, run_id=f"run_v10_prod_{int(time.time())}_{i+1}")
                results.append(res)
            except Exception as e:
                results.append({"error": str(e), "topic": topic})
        return results
