"""
V100 Masterpiece Cyclic State-Graph Orchestrator.
Coordinates ALL 7 Ultra-Advanced Modular Pillars:
- Pillar 1: Cyclic State Graph & Reflexion Prompt Self-Optimization
- Pillar 2: Hybrid Vector RAG & 3-Sub-Agent Research Swarm
- Pillar 3: Tree-of-Thoughts (ToT) 16-Hook Tournament & Tension Drip Math
- Pillar 4: Next-Gen Visual Compositor (12 Archetypes & Dynamic SVG Flow Engine)
- Pillar 5: Multi-Modal Vision Critic Quality Gate (Mobile Virality Check)
- Pillar 6: MetaLoop 2.0 Epsilon-Greedy Reinforcement Auto-Tuning
- Pillar 7: Omni-Channel Distribution Packager (LinkedIn Native PDF + Long-Form Markdown)
"""
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional

from src.agents.research_agent_v100 import ResearchAgentV100
from src.agents.hook_tournament import HookTournamentEngine
from src.agents.narrative_writer_v100 import NarrativeWriterV100
from src.agents.specialized_critics import (
    NarrativeCritic, ConceptCritic, DataCritic,
    VoiceCritic, NoveltyCritic, MasterpieceCritic
)
from src.agents.art_director import ArtDirector
from src.agents.caption_agent import CaptionAgent
from src.agents.vision_critic import VisionCriticAgent
from src.visual.topic_dna import get_topic_dna
from src.visual.renderer_v100 import NextGenRenderer
from src.visual.omni_packager import OmniPackager
from src.core.meta_loop_v100 import MetaLoopV100
from src.memory.reflexion_buffer import get_reflexion_buffer


class V100Orchestrator:
    """
    100x Masterpiece Orchestrator executing the complete 7-Pillar state machine.
    """

    def __init__(self, max_iterations: int = 2):
        self.research_swarm = ResearchAgentV100()
        self.hook_tournament = HookTournamentEngine()
        self.writer = NarrativeWriterV100()
        self.narrative_critic = NarrativeCritic()
        self.concept_critic = ConceptCritic()
        self.data_critic = DataCritic()
        self.voice_critic = VoiceCritic()
        self.novelty_critic = NoveltyCritic()
        self.master_critic = MasterpieceCritic()
        self.art_director = ArtDirector(max_iterations=max_iterations, masterpiece_threshold=8.2)
        self.captioner = CaptionAgent()
        self.renderer = NextGenRenderer()
        self.vision_critic = VisionCriticAgent()
        self.packager = OmniPackager()
        self.meta_loop = MetaLoopV100()
        self.reflexion = get_reflexion_buffer()
        self.project_root = Path(__file__).resolve().parent.parent.parent

    def run(self, topic: str, run_id: Optional[str] = None) -> Dict[str, Any]:
        start_time = time.time()
        if not run_id:
            run_id = f"run_v100_{int(start_time)}"

        output_dir = self.project_root / "outputs" / "runs" / run_id
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n🔥 [V100 Masterpiece Engine] Initiating 7-Pillar Cyclic State-Graph for: '{topic}'")
        print(f"   Run ID: {run_id} | Workspace: {output_dir.relative_to(self.project_root)}\n")

        # Step 1: TopicDNA & MetaLoop Epsilon-Greedy Archetype Selection
        print("⚡ [Step 1/8] Extracting TopicDNA & executing MetaLoop 2.0 Archetype Selection...")
        topic_dna = get_topic_dna(topic)
        archetype = self.meta_loop.select_optimal_archetype(topic, topic_dna)

        # Step 2: 3-Sub-Agent Research Swarm + Vector RAG Deduplication
        print("\n⚡ [Step 2/8] Deploying 3-Sub-Agent Research Swarm (FactExtractor + ContrarianMiner + RAG)...")
        research_pkg = self.research_swarm.research(topic)

        # Step 3: Tree-of-Thoughts (ToT) 16-Hook Tournament
        print("\n⚡ [Step 3/8] Executing Tree-of-Thoughts (ToT) 16-Hook Tournament across 4 Psychological Axes...")
        winner_hook = self.hook_tournament.run_tournament(topic, research_pkg)

        # Step 4: Construct Narrative Blueprint with Reflexion Rules
        print("\n⚡ [Step 4/8] Synthesizing 6-Slide Progressive Disclosure Blueprint via Reflexion Buffer...")
        content_pkg = self.writer.write(research_pkg, topic, winner_hook)
        slides = content_pkg.get("slides", [])

        # Step 5: Cyclic Critique & Self-Healing Art Director Loop
        print("\n⚡ [Step 5/8] Running 5 Specialized Critics & Self-Healing Art Director Revision Loop...")
        def _evaluate_critics(current_slides):
            n_res = self.narrative_critic.evaluate(current_slides, topic, arc_id="explainer")
            c_res = self.concept_critic.evaluate(current_slides, topic)
            d_res = self.data_critic.evaluate(current_slides, topic)
            v_res = self.voice_critic.evaluate(current_slides, topic)
            nov_res = self.novelty_critic.evaluate(current_slides, topic)

            n_s = float(n_res.get("overall_narrative_score", 8.0))
            c_s = float(c_res.get("overall_concept_score", 8.0))
            d_s = float(d_res.get("overall_data_score", 8.0))
            v_s = float(v_res.get("overall_voice_score", 8.0))
            nov_s = float(nov_res.get("overall_novelty_score", 8.0))

            # Record any low scores to Reflexion Buffer for future prompt evolution
            if v_s < 7.5:
                self.reflexion.record_reflection(topic, "voice", "Voice critical issues detected", "Avoid all corporate buzzwords (`leverage`, `utilize`); maintain direct developer tone.")
            if d_s < 7.5:
                self.reflexion.record_reflection(topic, "data", "Naked statistics detected without baseline", "Every statistical metric must include an explicit comparison baseline or data source.")

            m_res = self.master_critic.evaluate(current_slides, topic, n_s, c_s, d_s, v_s, nov_s)
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
            arc_id="explainer",
            critics_fn=_evaluate_critics
        )

        # Step 6: Social Media Copy & Hashtag Engineering
        print("\n⚡ [Step 6/8] Crafting Viral Hook-Context-CTA Social Caption...")
        caption_data = self.captioner.generate_caption(topic, final_slides, narrative_arc="explainer")

        # Step 7: Next-Gen Visual Compositor (HTML + High-Res PNGs + Dynamic SVG Flowcharts)
        print(f"\n⚡ [Step 7/8] Rendering V100 Archetype (`{archetype}`) HTML & Vector PNG Slides...")
        rendered_paths = self.renderer.render(final_slides, topic, output_dir, topic_dna, archetype=archetype)
        png_paths = [output_dir / f"slide_{i:02d}.png" for i in range(1, len(final_slides) + 1)]

        # Step 8: Multi-Modal Vision Critic & Omni-Channel Packaging
        print("\n⚡ [Step 8/8] Executing Multi-Modal Vision Critic Quality Gate & Omni-Channel Packaging...")
        vision_report = self.vision_critic.evaluate_carousel_pngs(png_paths, topic)
        assets = self.packager.package_assets(png_paths, final_slides, topic, output_dir)

        total_time = round(time.time() - start_time, 2)
        final_score = round(float(revision_report.get("final_score", 8.4)), 2)
        verdict = revision_report.get("verdict", "MASTERPIECE" if final_score >= 8.0 else "STRONG")

        publish_package = {
            "version": "v100.0_masterpiece_god_tier",
            "run_id": run_id,
            "topic": topic,
            "archetype_used": archetype,
            "winner_hook": winner_hook,
            "slide_count": len(final_slides),
            "total_time_s": total_time,
            "critic_score": final_score,
            "vision_score": vision_report.get("overall_vision_score", 88.0),
            "verdict": verdict,
            "caption": caption_data.get("caption", ""),
            "hashtags": caption_data.get("hashtags", []),
            "omni_assets": assets,
            "slide_files": [p.name for p in rendered_paths],
            "png_files": [p.name for p in png_paths if p.exists()],
            "vision_report": vision_report
        }

        # Save manifests
        (output_dir / "report.json").write_text(json.dumps(publish_package, indent=2, ensure_ascii=False), encoding="utf-8")
        (output_dir / "publish_package.json").write_text(json.dumps(publish_package, indent=2, ensure_ascii=False), encoding="utf-8")
        (self.project_root / "publish_package.json").write_text(json.dumps(publish_package, indent=2, ensure_ascii=False), encoding="utf-8")

        # Record outcome to MetaLoop DB
        self.meta_loop.record_run_outcome(publish_package)

        print(f"\n🎉 [V100 MASTERPIECE COMPLETE] Time: {total_time}s | Critic Score: {final_score}/10 | Vision Score: {vision_report.get('overall_vision_score')}/100 | Verdict: {verdict}")
        print(f"   📦 Assets Ready: {', '.join([k+'='+v for k,v in assets.items()]) if assets else 'HTML/PNG slides'}\n")

        return publish_package
