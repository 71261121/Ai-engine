# 🚀 AI Carousel Masterpiece Engine (V12 & V10)

An autonomous, multi-agent artificial intelligence pipeline designed to research, write, critique, art-direct, and render production-grade **1080x1350 Instagram/LinkedIn carousels**.

---

## 🏗️ Micro-Level Architectural Directory Structure

The repository has been engineered and organized on a **granular, micro-modular level** to separate core agent logic, orchestration workflows, memory management, visual concept rendering, configurations, scripts, and output artifacts:

```
Ai-engine/
├── README.md                      # Comprehensive architecture & usage documentation
├── pyproject.toml                 # Modern packaging & module configurations
├── requirements.txt               # Direct dependency manifest
├── main.yaml                      # Root configuration (synced with config/)
├── publish_package.json           # Latest published carousel manifest
├── .run_info                      # Run session tracking metadata
├── novelty_log.jsonl              # Historical novelty tracking log
│
├── config/                        # ⚙️ Configuration Assets
│   └── main.yaml                  # System configuration parameters
│
├── scripts/                       # 🛠️ Execution & Utility Scripts
│   ├── run_v12.py                 # V12 Masterpiece Engine runner
│   ├── run_v10_prod.py            # V10 Production Engine runner
│   ├── run_batch.py               # Batch topic generator & runner
│   ├── run_5_posts.py             # 5 posts batch runner
│   ├── test_orch.py               # Orchestrator test harness
│   ├── backfill_captions.py       # Utility: Caption backfiller
│   └── fix_manual_posts.py        # Utility: Fix and upgrade legacy manual posts
│
├── outputs/                       # 📦 Generated Artifacts & Reports
│   ├── runs/                      # Individual pipeline run directories (V10 & V12 outputs)
│   ├── samples/                   # Sample & template HTML slide designs (slide_01 - slide_08)
│   ├── reports/                   # Comprehensive quality reports & analytics
│   │   ├── COMPREHENSIVE_ANALYSIS_REPORT.json
│   │   ├── MASTER_ANALYSIS_REPORT.json
│   │   └── carousel_comprehensive_analysis.json
│   └── db/                        # SQLite & JSONL Experience Memory Database
│
└── src/                           # 🧠 Core Source Package
    ├── __init__.py
    ├── llm_client.py              # Universal LLM Client (LiteLLM/OpenAI + Offline Simulation Engine)
    ├── agents/                    # 🤖 AI Agents & Narrative Engines
    │   ├── __init__.py
    │   ├── art_director.py        # ArtDirector & VoiceEngine (Multi-iteration revision loops)
    │   ├── caption_agent.py       # CaptionAgent (Viral social media copy & hashtag generator)
    │   ├── critic_agent.py        # UnifiedCritic (One-pass 6-perspective quality reviewer)
    │   ├── specialized_critics.py # Narrative, Concept, Data, Voice, Novelty, & Masterpiece Critics
    │   ├── idea_market.py         # IdeaMarket (Topic idea generation & tournament evaluation)
    │   ├── research_agent.py      # ResearchAgent (Data-backed fact & statistics gathering)
    │   ├── writer_agent.py        # WriterAgent (v1 baseline writer)
    │   ├── writer_agent_v7.py     # WriterAgentV7 (v7 layout archetype content engineer)
    │   ├── narrative_writer.py    # NarrativeWriter (v9 narrative-first content writer)
    │   ├── narrative_writer_v11.py# NarrativeWriter (v11 advanced narrative content strategist)
    │   ├── narrative_arcs.py      # Narrative Arc Frameworks (v1)
    │   ├── narrative_arcs_v2.py   # Narrative Arc Frameworks (v2)
    │   └── narrative_arcs_v11.py  # Narrative Arc Frameworks (v11 - 8 distinct storytelling arcs)
    ├── visual/                    # 🎨 Visual Language & Concept Rendering
    │   ├── __init__.py
    │   ├── topic_dna.py           # TopicDNA Generator (Visual metaphors, color palettes, tone rules)
    │   └── renderer.py            # ConceptRenderer (Dynamic 1080x1350 HTML slide generation)
    ├── memory/                    # 💾 Memory & Experience Tracking
    │   ├── __init__.py
    │   └── experience_db.py       # ExperienceDB (Dual SQLite/JSONL storage for MetaLoop feedback)
    ├── core/                      # 🔄 Self-Improvement & Learning Loops
    │   ├── __init__.py
    │   └── meta_loop.py           # MetaLoop (Autonomous learning from actual Instagram metrics)
    └── graph/                     # 🕸️ Execution Orchestrators
        ├── __init__.py
        ├── orchestrator_v10.py    # V10Orchestrator (Standard production pipeline)
        └── orchestrator_v12.py    # V12Orchestrator (Masterpiece pipeline with TopicDNA & 5 Critics)
```

---

## 🤖 Core Pipeline Architecture

### V12 Masterpiece Engine Pipeline (`V12Orchestrator`)
The **V12 Pipeline** represents the state-of-the-art carousel generation workflow:
1. **TopicDNA Extraction (`src/visual/topic_dna.py`)**: Analyzes the topic to generate a customized category, tone, visual metaphor, and color palette (`background`, `primary`, `accent`, `text`, `subtext`).
2. **Narrative Arc Classification (`src/agents/narrative_arcs_v11.py`)**: Maps the topic into one of 8 specialized storytelling frameworks (e.g., `explainer`, `comparison`, `transformation`, `mythbuster`, etc.).
3. **Data-Backed Research (`src/agents/research_agent.py`)**: Collects key verified statistics, source citations, and unique industry insights with budget limits to prevent infinite loops.
4. **Narrative Content Writing (`src/agents/narrative_writer_v11.py`)**: Generates 6–7 high-retention slide blueprints matching the assigned narrative arc and density requirements.
5. **Multi-Perspective Critique (`src/agents/specialized_critics.py`)**: Runs 5 distinct specialized reviewers (**NarrativeCritic**, **ConceptCritic**, **DataCritic**, **VoiceCritic**, **NoveltyCritic**) + **MasterpieceCritic** calculation.
6. **Art Director Revision Loop (`src/agents/art_director.py`)**: Evaluates critic feedback and automatically executes targeted slide revisions until reaching the masterpiece threshold (`8.0+`) or maximum iteration limit.
7. **Social Caption Generation (`src/agents/caption_agent.py`)**: Crafts an engaging, aggressive Hook-Context-CTA Instagram/LinkedIn caption and optimized hashtags.
8. **Responsive Concept Rendering (`src/visual/renderer.py`)**: Synthesizes the slide blueprints and `TopicDNA` color language into standalone **1080x1350px HTML slides** (`slide_01.html`, `slide_02.html`, etc.) along with structured data packages (`report.json`, `carousel_data.json`).

---

## 🚀 Usage & Execution

For developer convenience, **root-level wrapper scripts** (`run_v12.py`, `run_v10_prod.py`, `test_orch.py`, etc.) are provided in the repository root alongside the organized `scripts/` directory. You can run any command directly from the root:

### 1. Run the V12 Masterpiece Engine
Generate carousels using the V12 architecture (`TopicDNA` + 5 Specialized Critics):
```bash
# Run a dry-run queue check
python run_v12.py --dry-run

# Run V12 for a single custom topic
python run_v12.py --topic "Rust vs Go: Which Should You Learn in 2025" --iters 2

# Run V12 for 3 default topics
python run_v12.py --count 3
```

### 2. Run the V10 Production Engine
```bash
# Run V10 continuous pipeline
python run_v10_prod.py

# Or run batch topic generation
python run_batch.py
```

### 3. Run Pipeline Orchestrator Tests
```bash
python test_orch.py
```

---

## 🛠️ Offline Simulation & Fallback Engine
If LiteLLM / API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.) are **not set**, the `LLMClient` (`src/llm_client.py`) automatically activates its internal **Simulation Engine**. This enables developers to test pipelines, run dry-runs, and generate complete HTML carousels and JSON packages offline without experiencing API connection crashes.
