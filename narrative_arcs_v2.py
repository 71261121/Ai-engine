"""
Enhanced Narrative Arcs V2 — Concept-Driven, Not Stat-Driven.

KEY CHANGE from V1: Removes forced "big number slide 2" pattern.
Each arc now defines:
- PURPOSE: What story this arc tells
- SLIDE_BEATS: What each position SHOULD DO (not what fields to fill)
- CONCEPT_SLOTS: What visual concepts each slide needs
- LAYOUT_FLEXIBILITY: Which layouts are allowed/forbidden
- TENSION_CURVE: Energy level across slides (1-10)
- NARRATIVE_RULES: What makes this arc unique

The LLM writes to the BEATS, not to template slots.
The Concept Enricher then translates beats into visual briefs.
The Concept Renderer generates HTML from visual briefs.

Flow: Topic → Arc Selection → Beat Writing → Concept Enrichment → Rendering
"""
from typing import Dict, List, Optional
import hashlib
import random


# ═══════════════════════════════════════════════════════════
# ENHANCED ARC DEFINITIONS
# ═══════════════════════════════════════════════════════════

ENHANCED_ARCS = {
    "explainer": {
        "name": "The Explainer",
        "purpose": "Break down a complex concept into visual intuition",
        "slides_count": 6,
        "tension_curve": [8, 6, 7, 9, 8, 5],  # hook→reorient→mechanism→aha→depth→resolution
        "allowed_layouts": ["hero", "split", "concept_deepdive", "process_detail", "bento", "outro"],
        "forbidden_layouts": ["grid"],
        "narrative_rules": [
            "Slide 1: Challenge the viewer's existing mental model (not just 'here's a topic')",
            "Slide 2: Reorient — show the CONTRAST between what they think and reality",
            "Slide 3: Mechanism — how it ACTUALLY works (visual, not text-heavy)",
            "Slide 4: Aha moment — the ONE insight that changes everything",
            "Slide 5: Depth — practical application or counterintuitive truth",
            "Slide 6: Resolution — specific takeaways, earned CTA"
        ],
        "concept_slots": {
            1: "mental_model_challenge",
            2: "reorientation_contrast",
            3: "mechanism_visual",
            4: "aha_moment",
            5: "practical_depth",
            6: "resolution_takeaway"
        },
        "slide_beats": {
            "hook": "What everyone gets WRONG about [topic] — challenge the mental model",
            "reorient": "The contrast: what they think vs what actually happens",
            "mechanism": "Visual walkthrough of how [topic] actually works",
            "aha_moment": "The ONE insight that changes everything",
            "practical_depth": "When to use this, when NOT to — decision framework",
            "cta": "Takeaway: the mental model they should leave with"
        }
    },

    "comparison": {
        "name": "The Head-to-Head",
        "purpose": "Compare two options with clear decision framework",
        "slides_count": 6,
        "tension_curve": [7, 8, 9, 8, 7, 5],
        "allowed_layouts": ["hero", "split", "comparative_text", "process_detail", "bento", "outro"],
        "forbidden_layouts": ["grid"],
        "narrative_rules": [
            "Slide 1: Frame the debate (not 'X vs Y' — WHY does this comparison matter?)",
            "Slide 2: Option A — deep dive with visual metaphor",
            "Slide 3: Option B — deep dive with visual metaphor",
            "Slide 4: Head-to-head comparison (visual, not just text)",
            "Slide 5: Decision framework — which to choose when",
            "Slide 6: Verdict with specific recommendation"
        ],
        "concept_slots": {
            1: "debate_framing",
            2: "option_a_deepdive",
            3: "option_b_deepdive",
            4: "head_to_head",
            5: "decision_framework",
            6: "verdict_recommendation"
        },
        "slide_beats": {
            "hook": "Why this comparison MATTERS — what's at stake",
            "contender_a": "Deep dive into Option A — its philosophy, strengths, visual identity",
            "contender_b": "Deep dive into Option B — its philosophy, strengths, visual identity",
            "comparison": "Head-to-head: where each wins, where each loses",
            "decision": "Decision matrix — project type → right choice",
            "cta": "Verdict: my recommendation, with reasoning"
        }
    },

    "analysis": {
        "name": "The Deep Analysis",
        "purpose": "Analyze a trend, technology, or phenomenon with evidence",
        "slides_count": 6,
        "tension_curve": [7, 8, 9, 8, 7, 6],
        "allowed_layouts": ["hero", "bento", "split", "concept_deepdive", "process_detail", "outro"],
        "forbidden_layouts": [],
        "narrative_rules": [
            "Slide 1: State the phenomenon — what's happening and why it matters",
            "Slide 2: The evidence — data that proves this is real (with context)",
            "Slide 3: The mechanism — WHY this is happening (not just THAT it is)",
            "Slide 4: The implications — what this means for the viewer",
            "Slide 5: The prediction — where this goes next (with reasoning)",
            "Slide 6: Action items — what to do about it NOW"
        ],
        "concept_slots": {
            1: "phenomenon_statement",
            2: "evidence_data",
            3: "mechanism_explanation",
            4: "implications_analysis",
            5: "prediction_forward",
            6: "action_items"
        },
        "slide_beats": {
            "hook": "The phenomenon: what's happening right now",
            "context": "Evidence: data that proves this is real and significant",
            "deep_dive": "Mechanism: WHY this is happening — the forces driving it",
            "implications": "What this means for you — implications you haven't considered",
            "prediction": "Where this goes — informed prediction with reasoning",
            "cta": "What to do: specific, actionable steps"
        }
    },

    "transformation": {
        "name": "The Transformation",
        "purpose": "Show a before→after journey with specific steps",
        "slides_count": 6,
        "tension_curve": [7, 6, 8, 9, 8, 5],
        "allowed_layouts": ["hero", "split", "comparative_text", "process_detail", "bento", "outro"],
        "forbidden_layouts": ["grid"],
        "narrative_rules": [
            "Slide 1: The pain point — make the viewer FEEL the problem",
            "Slide 2: The wrong approach — what most people do (and why it fails)",
            "Slide 3: The right approach — the paradigm shift",
            "Slide 4: The mechanism — step-by-step transformation",
            "Slide 5: The result — concrete outcome with proof",
            "Slide 6: The blueprint — how to start today"
        ],
        "concept_slots": {
            1: "pain_point",
            2: "wrong_approach",
            3: "paradigm_shift",
            4: "transformation_steps",
            5: "result_proof",
            6: "starting_blueprint"
        },
        "slide_beats": {
            "hook": "The pain: what's broken and why it hurts",
            "before": "The wrong way: what most people do and why it fails",
            "shift": "The insight: what actually works (the paradigm shift)",
            "transformation": "The journey: step-by-step from broken to working",
            "after": "The result: concrete outcome, real numbers, proof",
            "cta": "The blueprint: how to start your transformation today"
        }
    },

    "tutorial": {
        "name": "The Tutorial",
        "purpose": "Teach a specific skill or technique step-by-step",
        "slides_count": 6,
        "tension_curve": [6, 7, 8, 9, 8, 6],
        "allowed_layouts": ["hero", "process_detail", "concept_deepdive", "split", "bento", "outro"],
        "forbidden_layouts": ["grid"],
        "narrative_rules": [
            "Slide 1: What you'll learn and why it matters (specific skill, not vague topic)",
            "Slide 2: Prerequisites — what you need before starting",
            "Slide 3: Step 1 with visual example",
            "Slide 4: Step 2 with visual example",
            "Slide 5: Common pitfalls and how to avoid them",
            "Slide 6: What you've built — the result, next steps"
        ],
        "concept_slots": {
            1: "learning_objective",
            2: "prerequisites",
            3: "step_1_visual",
            4: "step_2_visual",
            5: "pitfalls_avoidance",
            6: "result_nextsteps"
        },
        "slide_beats": {
            "hook": "What you'll master: specific skill with specific outcome",
            "prerequisites": "What you need before starting — be honest about requirements",
            "step_1": "First step: detailed with visual example (not just text instructions)",
            "step_2": "Second step: building on the first, adding complexity",
            "pitfalls": "Common mistakes and how to avoid them — battle-tested advice",
            "cta": "What you've built: the result, and where to go next"
        }
    },

    "listicle": {
        "name": "The Curated List",
        "purpose": "Present a ranked or categorized list with depth",
        "slides_count": 6,
        "tension_curve": [7, 8, 9, 8, 7, 6],
        "allowed_layouts": ["hero", "bento", "grid", "process_detail", "concept_deepdive", "outro"],
        "forbidden_layouts": [],
        "narrative_rules": [
            "Slide 1: The list topic — why these items matter (not just 'Top 5 X')",
            "Slide 2: Items 1-2 with context (not just names)",
            "Slide 3: Items 3-4 with context",
            "Slide 4: Item 5 (the surprising one) — deep dive",
            "Slide 5: The meta-insight — what these items reveal together",
            "Slide 6: How to use this list — decision framework"
        ],
        "concept_slots": {
            1: "list_framing",
            2: "items_group_1",
            3: "items_group_2",
            4: "surprising_item",
            5: "meta_insight",
            6: "usage_framework"
        },
        "slide_beats": {
            "hook": "Why these items matter: the unifying principle",
            "items_early": "First items with context — why each matters, not just what it is",
            "items_mid": "Middle items — maintain depth, don't just list",
            "surprising": "The surprising item — the one that challenges assumptions",
            "meta": "The meta-insight: what these items reveal together",
            "cta": "How to use this: decision framework, not just a list"
        }
    },

    "myth_busting": {
        "name": "The Myth Buster",
        "purpose": "Challenge common misconceptions with evidence",
        "slides_count": 6,
        "tension_curve": [9, 7, 8, 9, 7, 5],
        "allowed_layouts": ["hero", "split", "comparative_text", "process_detail", "bento", "outro"],
        "forbidden_layouts": ["grid"],
        "narrative_rules": [
            "Slide 1: State the myth boldly — make it sound convincing",
            "Slide 2: The reality — contrast with evidence",
            "Slide 3: Myth #2 — another common misconception",
            "Slide 4: Reality #2 — with specific counter-evidence",
            "Slide 5: The real truth — what actually matters",
            "Slide 6: The corrected mental model — what to believe instead"
        ],
        "concept_slots": {
            1: "myth_statement",
            2: "reality_contrast",
            3: "myth_2",
            4: "reality_2",
            5: "real_truth",
            6: "corrected_model"
        },
        "slide_beats": {
            "hook": "The myth: state it boldly — make it sound convincing",
            "reality": "The reality: contrast with specific evidence",
            "myth_2": "Myth #2: another one people believe",
            "reality_2": "Reality #2: with specific counter-evidence",
            "truth": "The real truth: what actually matters",
            "cta": "The corrected model: what to believe instead"
        }
    },

    "framework": {
        "name": "The Framework",
        "purpose": "Present a decision-making framework or mental model",
        "slides_count": 6,
        "tension_curve": [7, 8, 9, 8, 7, 6],
        "allowed_layouts": ["hero", "bento", "process_detail", "split", "concept_deepdive", "outro"],
        "forbidden_layouts": ["grid"],
        "narrative_rules": [
            "Slide 1: The problem this framework solves (make it feel urgent)",
            "Slide 2: The framework overview — 3-4 key dimensions",
            "Slide 3: Dimension 1 deep dive with visual",
            "Slide 4: Dimension 2 deep dive with visual",
            "Slide 5: How to apply — real example with the framework",
            "Slide 6: Quick reference card — the framework in one view"
        ],
        "concept_slots": {
            1: "problem_statement",
            2: "framework_overview",
            3: "dimension_1",
            4: "dimension_2",
            5: "application_example",
            6: "reference_card"
        },
        "slide_beats": {
            "hook": "The problem: why you need this framework",
            "overview": "The framework: 3-4 key dimensions at a glance",
            "dimension_1": "Deep dive: first dimension with visual metaphor",
            "dimension_2": "Deep dive: second dimension with visual metaphor",
            "application": "Real example: applying the framework to a real decision",
            "cta": "Quick reference: the framework in one view — save this"
        }
    }
}


# ═══════════════════════════════════════════════════════════
# ARC SELECTION LOGIC
# ═══════════════════════════════════════════════════════════

TOPIC_ARC_AFFINITY = {
    "kafka": ["explainer", "framework"],
    "sql_commands": ["tutorial", "myth_busting"],
    "database_fundamentals": ["explainer", "framework"],
    "rust_vs_go": ["comparison", "analysis"],
    "python_vs_javascript": ["comparison", "analysis"],
    "ai_agents": ["explainer", "framework", "transformation"],
    "rag_vs_finetuning": ["comparison", "myth_busting"],
    "llm_fundamentals": ["explainer", "analysis"],
    "mcp_protocol": ["explainer", "tutorial"],
    "multi_agent_systems": ["framework", "analysis"],
    "microservices": ["framework", "myth_busting"],
    "api_design": ["comparison", "tutorial"],
    "docker_kubernetes": ["tutorial", "explainer"],
    "redis_caching": ["tutorial", "explainer"],
    "react_vs_vue": ["comparison", "analysis"],
    "nextjs_app_router": ["tutorial", "explainer"],
    "ci_cd_pipeline": ["tutorial", "framework"],
    "web_security": ["myth_busting", "framework"],
}


def select_arc(topic: str, prefer_variety: bool = True) -> str:
    """
    Select the best narrative arc for a topic.
    If prefer_variety=True, avoids recently used arcs.
    """
    topic_lower = topic.lower()

    # Find matching topic
    matched_topic = None
    for key in TOPIC_ARC_AFFINITY:
        if key in topic_lower or topic_lower in key:
            matched_topic = key
            break

    if matched_topic:
        candidates = TOPIC_ARC_AFFINITY[matched_topic]
        # Use topic hash for deterministic but varied selection
        h = int(hashlib.md5(topic.encode()).hexdigest()[:4], 16)
        return candidates[h % len(candidates)]

    # Fallback: use topic hash to pick from all arcs
    all_arcs = list(ENHANCED_ARCS.keys())
    h = int(hashlib.md5(topic.encode()).hexdigest()[:4], 16)
    return all_arcs[h % len(all_arcs)]


def get_arc(arc_id: str) -> Dict:
    """Get enhanced arc definition."""
    return ENHANCED_ARCS.get(arc_id, ENHANCED_ARCS["explainer"])


def get_all_arc_ids() -> List[str]:
    """Get all available arc IDs."""
    return list(ENHANCED_ARCS.keys())


def get_slide_beats(arc_id: str, topic: str) -> Dict[str, str]:
    """
    Get the slide beats for an arc, personalized for the topic.
    Returns: {position: beat_description}
    """
    arc = get_arc(arc_id)
    beats = dict(arc.get("slide_beats", {}))

    # Personalize beats with topic
    for key in beats:
        beats[key] = beats[key].replace("[topic]", topic)

    return beats


def get_tension_curve(arc_id: str) -> List[int]:
    """Get the energy/tension curve for an arc."""
    arc = get_arc(arc_id)
    return arc.get("tension_curve", [5] * 6)


def get_allowed_layouts(arc_id: str) -> List[str]:
    """Get allowed layouts for an arc."""
    arc = get_arc(arc_id)
    return arc.get("allowed_layouts", ["hero", "bento", "split", "outro"])


def classify_topic_to_arc(topic: str) -> str:
    """Classify a topic to its best arc (public API)."""
    return select_arc(topic)
