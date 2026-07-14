"""
Narrative Arcs — 8 story structures for educational Instagram carousels.
Each arc defines: topic keywords, slide-by-slide information flow, layout mapping,
density rhythm, and CTA strategy.

This REPLACES the fixed template-first approach with narrative-first generation.
"""
from typing import Dict, List, Optional
import re


# ═══════════════════════════════════════════════
# NARRATIVE ARC DEFINITIONS
# ═══════════════════════════════════════════════

NARRATIVE_ARCS = {
    "comparison": {
        "id": "comparison",
        "name": "Comparison / Versus",
        "description": "Compare two or more options side by side with verdict",
        "best_for": [
            "vs", "versus", "compared to", "better than", "difference between",
            "alternative to", "instead of", "which one", "choose between",
            "react vs vue", "rust vs go", "mysql vs postgres", "aws vs gcp",
            "python vs javascript", "sql vs nosql", "docker vs kubernetes"
        ],
        "slide_count": {"min": 6, "max": 7, "optimal": 6},
        "slides": [
            {
                "position": "hook",
                "density": "low",
                "purpose": "State the dilemma — both options face off",
                "content_instruction": "Hook headline naming BOTH contenders. Subtitle frames the stakes.",
                "example_headline": "RUST vs GO.",
                "example_subtitle": "The 2025 systems programming battleground. One delivers cloud velocity. The other gives absolute control."
            },
            {
                "position": "contenders",
                "density": "medium",
                "purpose": "Quick identity card for each contender — who/what/one-line value",
                "content_instruction": "Top half: Contender A identity. Bottom half: Deep conceptual explanation of its core philosophy.",
                "content_fields": ["contender_a_name", "contender_a_identity", "contender_a_strength_stat", "contender_a_strength_context"]
            },
            {
                "position": "criteria_1",
                "density": "high",
                "purpose": "First comparison dimension with data",
                "content_instruction": "Compare both options in detail using text blocks. Insight = why this difference matters structurally.",
                "content_fields": ["criteria_name", "winner_stat", "winner_metric", "loser_metric", "insight"]
            },
            {
                "position": "criteria_2",
                "density": "medium",
                "purpose": "Second comparison — different angle",
                "content_instruction": "Top: Context for the second comparison. Bottom: Detailed explanation of how this impacts the developer or business.",
                "content_fields": ["criteria_name", "context", "stat_value", "stat_label", "strategic_insight"]
            },
            {
                "position": "verdict",
                "density": "medium",
                "purpose": "4 key takeaways from the comparison",
                "content_instruction": "4 panels: when to choose A, when to choose B, common mistake, pro tip.",
                "content_fields": ["panel_1_title", "panel_1_body", "panel_2_title", "panel_2_body", "panel_3_title", "panel_3_body", "panel_4_title", "panel_4_body"]
            },
            {
                "position": "cta",
                "density": "low",
                "purpose": "Decision framework + save prompt",
                "content_instruction": "3 decision rules. CTA asks audience which they'd choose.",
                "cta_type": "engagement_question"
            }
        ],
        "density_rhythm": ["low", "medium", "high", "medium", "medium", "low"]
    },

    "explainer": {
        "id": "explainer",
        "name": "Concept Explainer / Deep Dive",
        "description": "Break down a complex concept with progressive disclosure",
        "best_for": [
            "what is", "how does", "explained", "understanding", "deep dive",
            "guide to", "introduction to", "101", "basics of", "mental model",
            "architecture", "how it works", "behind the scenes", "inside",
            "mechanism", "concept", "theory", "principle"
        ],
        "slide_count": {"min": 6, "max": 7, "optimal": 6},
        "slides": [
            {
                "position": "hook",
                "density": "low",
                "purpose": "Why this concept matters — pain or opportunity",
                "content_instruction": "Massive 2-word headline naming the concept. Subtitle sets stakes.",
                "content_fields": ["headline_top", "headline_accent", "subtitle"]
            },
            {
                "position": "tl_dr",
                "density": "high",
                "purpose": "30-second summary — the core concept + 2 supporting facts",
                "content_instruction": "Explain the concept deeply using 3 text boxes. Focus on the core idea, performance, and constraints.",
                "content_fields": ["main_stat", "main_label", "stat2_value", "stat2_label", "stat3_value", "stat3_label", "insight"]
            },
            {
                "position": "deep_dive_1",
                "density": "medium",
                "purpose": "Core mechanism — how it works step by step",
                "content_instruction": "3-5 nodes showing the process/flow. Active node = the key insight step.",
                "content_fields": ["nodes", "badge_value", "badge_label"]
            },
            {
                "position": "deep_dive_2",
                "density": "medium",
                "purpose": "Key insight or counterintuitive truth",
                "content_instruction": "Top: the context. Bottom: A deep explanation of the counter-intuitive truth.",
                "content_fields": ["context", "stat_value", "stat_label", "insight"]
            },
            {
                "position": "application",
                "density": "medium",
                "purpose": "4 practical applications or use cases",
                "content_instruction": "4 panels: use case 1-4 with icon, title, one-line value.",
                "content_fields": ["panels"]
            },
            {
                "position": "cta",
                "density": "low",
                "purpose": "3 key takeaways + save prompt",
                "content_instruction": "3 numbered takeaways. CTA offers value (save for reference).",
                "cta_type": "save_reference"
            }
        ],
        "density_rhythm": ["low", "high", "medium", "medium", "medium", "low"]
    },

    "tutorial": {
        "id": "tutorial",
        "name": "Step-by-Step Tutorial",
        "description": "Guide through a process from start to finish",
        "best_for": [
            "how to", "step by step", "tutorial", "setup", "build",
            "create", "install", "configure", "deploy", "implement",
            "walkthrough", "getting started", "quickstart", "guide"
        ],
        "slide_count": {"min": 6, "max": 7, "optimal": 6},
        "slides": [
            {
                "position": "hook",
                "density": "low",
                "purpose": "End result preview + time estimate",
                "content_instruction": "Headline: what they'll build. Subtitle: how fast.",
                "content_fields": ["headline_top", "headline_accent", "subtitle"]
            },
            {
                "position": "prerequisites",
                "density": "medium",
                "purpose": "What you need before starting",
                "content_instruction": "Main stat = difficulty level. Secondary = time. Insight = what you'll have at the end.",
                "content_fields": ["difficulty", "time_estimate", "prerequisites_list", "end_result"]
            },
            {
                "position": "steps_1_2",
                "density": "high",
                "purpose": "Steps 1-2 with key details",
                "content_instruction": "3-4 nodes. Node 1 = setup/foundation. Active node = the critical step. Badge = success metric.",
                "content_fields": ["nodes", "badge_value", "badge_label"]
            },
            {
                "position": "step_3_detail",
                "density": "medium",
                "purpose": "Most important step in detail",
                "content_instruction": "Top: the context (why this step matters). Bottom: the result metric.",
                "content_fields": ["context", "stat_value", "stat_label", "insight"]
            },
            {
                "position": "tips",
                "density": "medium",
                "purpose": "Pro tips + common mistakes",
                "content_instruction": "4 panels: 2 pro tips, 1 common mistake, 1 optimization.",
                "content_fields": ["panels"]
            },
            {
                "position": "cta",
                "density": "low",
                "purpose": "Summary + try it prompt",
                "content_instruction": "3 step summary. CTA: try it and share results.",
                "cta_type": "try_and_share"
            }
        ],
        "density_rhythm": ["low", "medium", "high", "medium", "medium", "low"]
    },

    "analysis": {
        "id": "analysis",
        "name": "Analysis / Case Study / Teardown",
        "description": "Deconstruct a real example with strategy and results",
        "best_for": [
            "analysis", "teardown", "case study", "breakdown", "deep dive into",
            "dissecting", "anatomy of", "inside", "postmortem", "retrospective",
            "growth strategy", "marketing strategy", "why x succeeded"
        ],
        "slide_count": {"min": 6, "max": 7, "optimal": 6},
        "slides": [
            {
                "position": "hook",
                "density": "low",
                "purpose": "The result that was achieved — number first",
                "content_instruction": "Headline: the achievement. Subtitle: who did it and why it matters.",
                "content_fields": ["headline_top", "headline_accent", "subtitle"]
            },
            {
                "position": "context",
                "density": "high",
                "purpose": "Context — before state, key metrics, scale",
                "content_instruction": "Explain the context deeply using 3 text boxes. Focus on the before state, the scale of the problem, and the timeline.",
                "content_fields": ["main_stat", "main_label", "stat2_value", "stat2_label", "stat3_value", "stat3_label", "insight"]
            },
            {
                "position": "strategy",
                "density": "medium",
                "purpose": "The strategy — key moves in sequence",
                "content_instruction": "3-5 nodes showing the strategic moves. Active node = the breakthrough moment.",
                "content_fields": ["nodes", "badge_value", "badge_label"]
            },
            {
                "position": "results",
                "density": "medium",
                "purpose": "The results — after state with detailed concept",
                "content_instruction": "Top: what they did (brief). Bottom: the massive result number.",
                "content_fields": ["context", "stat_value", "stat_label", "insight"]
            },
            {
                "position": "takeaways",
                "density": "medium",
                "purpose": "4 lessons you can steal",
                "content_instruction": "4 panels: lesson 1-4 with actionable insight.",
                "content_fields": ["panels"]
            },
            {
                "position": "cta",
                "density": "low",
                "purpose": "Framework to apply + save prompt",
                "content_instruction": "3-step framework. CTA: apply this to your [context].",
                "cta_type": "apply_framework"
            }
        ],
        "density_rhythm": ["low", "high", "medium", "medium", "medium", "low"]
    },

    "listicle": {
        "id": "listicle",
        "name": "Listicle / Cheat Sheet / Top N",
        "description": "Curated collection — high saveability",
        "best_for": [
            "top", "best", "list", "tools", "tips", "mistakes",
            "things to", "ways to", "reasons to", "examples of",
            "cheat sheet", "reference", "collection", "roundup"
        ],
        "slide_count": {"min": 6, "max": 7, "optimal": 6},
        "slides": [
            {
                "position": "hook",
                "density": "low",
                "purpose": "Numbered promise — '7 tools that...'",
                "content_instruction": "Headline: the number + category. Subtitle: the value proposition.",
                "content_fields": ["headline_top", "headline_accent", "subtitle"]
            },
            {
                "position": "items_1_2",
                "density": "high",
                "purpose": "First 2 items with key stats",
                "content_instruction": "Explain items 1 and 2 deeply using text boxes.",
                "content_fields": ["main_stat", "main_label", "stat2_value", "stat2_label", "insight"]
            },
            {
                "position": "items_3_4",
                "density": "medium",
                "purpose": "Items 3-4 with comparison angle",
                "content_instruction": "Top: item 3 context. Bottom: Detailed explanation of item 4.",
                "content_fields": ["context", "stat_value", "stat_label", "insight"]
            },
            {
                "position": "items_5_6",
                "density": "medium",
                "purpose": "Items 5-6 as quick cards",
                "content_instruction": "4 panels: items 5-6 as cards, plus bonus tip and common mistake.",
                "content_fields": ["panels"]
            },
            {
                "position": "verdict",
                "density": "medium",
                "purpose": "Decision flow — which one to pick when",
                "content_instruction": "Nodes showing decision path. Badge = top recommendation.",
                "content_fields": ["nodes", "badge_value", "badge_label"]
            },
            {
                "position": "cta",
                "density": "low",
                "purpose": "Summary + save prompt",
                "content_instruction": "3 key takeaways. CTA: save this list for later.",
                "cta_type": "save_list"
            }
        ],
        "density_rhythm": ["low", "high", "medium", "medium", "medium", "low"]
    },

    "myth_busting": {
        "id": "myth_busting",
        "name": "Myth Busting / Misconception",
        "description": "Correct common false beliefs with evidence",
        "best_for": [
            "myth", "misconception", "wrong", "false", "actually",
            "truth about", "reality of", "debunking", "fact vs fiction",
            "you're wrong about", "nobody tells you", "secret about",
            "is dead", "is wrong", "deprecated", "obsolete", "overrated",
            "stop doing", "don't", "never", "waste of time"
        ],
        "slide_count": {"min": 6, "max": 7, "optimal": 6},
        "slides": [
            {
                "position": "hook",
                "density": "low",
                "purpose": "Provocative myth statement as question",
                "content_instruction": "Headline: the myth. Subtitle: the truth preview.",
                "content_fields": ["headline_top", "headline_accent", "subtitle"]
            },
            {
                "position": "myth_1",
                "density": "medium",
                "purpose": "Myth 1: belief → reality with evidence",
                "content_instruction": "Top: the myth/belief. Bottom: A deep conceptual explanation of the reality.",
                "content_fields": ["context", "stat_value", "stat_label", "insight"]
            },
            {
                "position": "myth_2",
                "density": "high",
                "purpose": "Myth 2 with data evidence",
                "content_instruction": "Explain the reality using 3 deep text boxes. Focus on the core truth, the nuance, and why the myth persists.",
                "content_fields": ["main_stat", "main_label", "stat2_value", "stat2_label", "insight"]
            },
            {
                "position": "myth_3",
                "density": "medium",
                "purpose": "Truth reconstruction — step by step",
                "content_instruction": "4 steps showing the correct mental model replacing the myth.",
                "content_fields": ["nodes"]
            },
            {
                "position": "truth",
                "density": "medium",
                "purpose": "4 things to do instead",
                "content_instruction": "4 panels: 4 actionable alternatives to the myths.",
                "content_fields": ["panels"]
            },
            {
                "position": "cta",
                "density": "low",
                "purpose": "Reality check summary + engagement",
                "content_instruction": "3 truths. CTA: which myth did you believe?",
                "cta_type": "engagement_question"
            }
        ],
        "density_rhythm": ["low", "medium", "high", "medium", "medium", "low"]
    },

    "transformation": {
        "id": "transformation",
        "name": "Before-After / Journey / Transformation",
        "description": "Show change over time — problem to solution",
        "best_for": [
            "journey", "transformation", "before and after", "evolution",
            "from x to y", "how i", "case study", "growth", "scaling",
            "migration", "refactor", "upgrade", "rewrite"
        ],
        "slide_count": {"min": 6, "max": 7, "optimal": 6},
        "slides": [
            {
                "position": "hook",
                "density": "low",
                "purpose": "The AFTER result — lead with the destination",
                "content_instruction": "Headline: the transformation result. Subtitle: from what to what.",
                "content_fields": ["headline_top", "headline_accent", "subtitle"]
            },
            {
                "position": "before",
                "density": "high",
                "purpose": "The BEFORE state — pain, metrics, scale of problem",
                "content_instruction": "Explain the before state deeply. Focus on the pain, scope, and cost of inaction.",
                "content_fields": ["main_stat", "main_label", "stat2_value", "stat2_label", "stat3_value", "stat3_label", "insight"]
            },
            {
                "position": "turning_point",
                "density": "medium",
                "purpose": "The decision/discovery moment",
                "content_instruction": "Top: the catalyst. Bottom: deep explanation of the turning point.",
                "content_fields": ["context", "stat_value", "stat_label", "insight"]
            },
            {
                "position": "phases",
                "density": "medium",
                "purpose": "The journey phases",
                "content_instruction": "3-4 nodes showing transformation phases. Active = breakthrough.",
                "content_fields": ["nodes", "badge_value", "badge_label"]
            },
            {
                "position": "after",
                "density": "medium",
                "purpose": "4 outcomes/metrics from the transformation",
                "content_instruction": "4 panels: outcome 1-4 with specific metrics.",
                "content_fields": ["panels"]
            },
            {
                "position": "cta",
                "density": "low",
                "purpose": "3-step roadmap for reader + save",
                "content_instruction": "3 steps to start their own transformation. CTA: ready to start?",
                "cta_type": "start_journey"
            }
        ],
        "density_rhythm": ["low", "high", "medium", "medium", "medium", "low"]
    },

    "framework": {
        "id": "framework",
        "name": "Framework / Mental Model / Decision Matrix",
        "description": "Present a reusable thinking tool",
        "best_for": [
            "framework", "mental model", "decision", "matrix", "template",
            "approach", "methodology", "strategy", "system", "process",
            "architecture pattern", "design pattern", "best practice"
        ],
        "slide_count": {"min": 6, "max": 7, "optimal": 6},
        "slides": [
            {
                "position": "hook",
                "density": "low",
                "purpose": "The problem this framework solves",
                "content_instruction": "Headline: framework name/concept. Subtitle: the problem it addresses.",
                "content_fields": ["headline_top", "headline_accent", "subtitle"]
            },
            {
                "position": "overview",
                "density": "high",
                "purpose": "Framework overview — the big picture with key metric",
                "content_instruction": "Explain the framework deeply. Focus on the core mechanism, the adoption, and why it works.",
                "content_fields": ["main_stat", "main_label", "stat2_value", "stat2_label", "insight"]
            },
            {
                "position": "component_1",
                "density": "medium",
                "purpose": "Framework components in sequence",
                "content_instruction": "3-5 nodes = framework components. Active = most critical component.",
                "content_fields": ["nodes", "badge_value", "badge_label"]
            },
            {
                "position": "application",
                "density": "medium",
                "purpose": "How to apply it — with real result",
                "content_instruction": "Top: application context. Bottom: detailed explanation of the application result.",
                "content_fields": ["context", "stat_value", "stat_label", "insight"]
            },
            {
                "position": "components_detail",
                "density": "medium",
                "purpose": "4 framework components deep dive",
                "content_instruction": "4 panels: component 1-4 with icon, name, one-line value.",
                "content_fields": ["panels"]
            },
            {
                "position": "cta",
                "density": "low",
                "purpose": "3 rules of the framework + save",
                "content_instruction": "3 core rules. CTA: save this framework.",
                "cta_type": "save_framework"
            }
        ],
        "density_rhythm": ["low", "high", "medium", "medium", "medium", "low"]
    }
}


# ═══════════════════════════════════════════════
# TOPIC CLASSIFIER
# ═══════════════════════════════════════════════

def classify_topic(topic: str) -> str:
    """
    Classify a topic into one of 8 narrative arc types.
    Uses keyword matching with priority scoring.
    Returns: arc_id string
    """
    topic_lower = topic.lower().strip()

    scores = {}
    for arc_id, arc in NARRATIVE_ARCS.items():
        score = 0
        for keyword in arc["best_for"]:
            if keyword in topic_lower:
                # Longer keywords = more specific = higher weight
                score += len(keyword.split())
        scores[arc_id] = score

    # Return highest scoring arc, default to explainer
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    return "explainer"


def get_arc(arc_id: str) -> Dict:
    """Get narrative arc definition by ID."""
    return NARRATIVE_ARCS.get(arc_id, NARRATIVE_ARCS["explainer"])


def get_slide_blueprint(arc_id: str, position: int) -> Dict:
    """Get the blueprint for a specific slide position in an arc."""
    arc = get_arc(arc_id)
    slides = arc["slides"]
    if 0 <= position < len(slides):
        return slides[position]
    return slides[-1]  # Fallback to last slide


def get_density_for_position(arc_id: str, position: int) -> str:
    """Get the density tier for a specific position."""
    arc = get_arc(arc_id)
    rhythm = arc.get("density_rhythm", ["low", "medium", "high", "medium", "medium", "low"])
    if position < len(rhythm):
        return rhythm[position]
    return "medium"


# ═══════════════════════════════════════════════
# CTA TYPES
# ═══════════════════════════════════════════════

CTA_VARIANTS = {
    "engagement_question": {
        "items": [
            {"text": "Which would you choose? <strong>Drop your answer below.</strong>"},
            {"text": "Agree or disagree? <strong>Let me know in the comments.</strong>"},
            {"text": "What's your experience? <strong>Share below.</strong>"},
        ],
        "cta_text": "Drop your take.",
        "cta_highlight": "The best answers get featured.",
        "cta_icon": "💬"
    },
    "save_reference": {
        "items": [
            {"text": "Bookmark this — <strong>you'll reference it.</strong>"},
            {"text": "This is your <strong>cheat sheet</strong> for the next 6 months."},
            {"text": "Send this to your team — <strong>they need this.</strong>"},
        ],
        "cta_text": "Save this post.",
        "cta_highlight": "You'll need these insights for your next project.",
        "cta_icon": "📌"
    },
    "try_and_share": {
        "items": [
            {"text": "Try this today — <strong>it takes 10 minutes.</strong>"},
            {"text": "Tag someone who <strong>needs to see this.</strong>"},
            {"text": "Screenshot this and <strong>save it for later.</strong>"},
        ],
        "cta_text": "Try it now.",
        "cta_highlight": "Share your results — I'd love to see them.",
        "cta_icon": "🚀"
    },
    "apply_framework": {
        "items": [
            {"text": "Apply this framework to <strong>your next project.</strong>"},
            {"text": "Start with step 1 — <strong>the rest follows.</strong>"},
            {"text": "This pattern works across <strong>every domain.</strong>"},
        ],
        "cta_text": "Apply this framework.",
        "cta_highlight": "The results speak for themselves.",
        "cta_icon": "🎯"
    },
    "save_list": {
        "items": [
            {"text": "This list grows — <strong>save before it's updated.</strong>"},
            {"text": "Send this to your <strong>team Slack channel.</strong>"},
            {"text": "Bookmark — <strong>you'll need this quarterly.</strong>"},
        ],
        "cta_text": "Save this list.",
        "cta_highlight": "Updated quarterly with new data.",
        "cta_icon": "📋"
    },
    "start_journey": {
        "items": [
            {"text": "Step 1 starts <strong>today</strong>, not Monday."},
            {"text": "The best time to start was yesterday. <strong>Second best: now.</strong>"},
            {"text": "Your transformation <strong>begins with one decision.</strong>"},
        ],
        "cta_text": "Start your transformation.",
        "cta_highlight": "Follow for the step-by-step playbook.",
        "cta_icon": "⚡"
    },
    "save_framework": {
        "items": [
            {"text": "This framework replaces <strong>100 hours of trial and error.</strong>"},
            {"text": "Save this — <strong>it's your decision shortcut.</strong>"},
            {"text": "Print it. Pin it. <strong>Use it daily.</strong>"},
        ],
        "cta_text": "Save this framework.",
        "cta_highlight": "Your future self will thank you.",
        "cta_icon": "🧠"
    }
}


def get_cta_variant(arc_id: str, variant_index: int = 0) -> Dict:
    """Get a CTA variant for the given arc type."""
    arc = get_arc(arc_id)
    cta_type = arc["slides"][-1].get("cta_type", "save_reference")
    variants = CTA_VARIANTS.get(cta_type, CTA_VARIANTS["save_reference"])
    items = variants["items"]
    idx = variant_index % len(items)
    return {
        "items": [{"text": items[idx]["text"]}],
        "cta_text": variants["cta_text"],
        "cta_highlight": variants["cta_highlight"],
        "cta_icon": variants["cta_icon"],
    }
