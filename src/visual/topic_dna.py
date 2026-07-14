"""
TopicDNA Engine — Visual Language Generator per Topic.
Generates unique visual metaphors, color palettes, and tone rules for each carousel topic.
"""
import hashlib
from typing import Dict, Any


def get_topic_dna(topic: str) -> Dict[str, Any]:
    """
    Generate the visual and tone DNA for a given topic.
    Uses deterministic hashing combined with keyword heuristics to produce a rich,
    consistent visual brief for rendering and critique.
    """
    t_lower = topic.lower()

    # Determine Color Language & Metaphor Palette by topic category
    if any(k in t_lower for k in ["kubernetes", "docker", "cloud", "aws", "infrastructure", "devops"]):
        category = "infrastructure"
        color_language = {
            "background": "#0D1117",
            "primary": "#38BDF8",     # Sky Blue
            "accent": "#F59E0B",      # Amber
            "text": "#F9FAFB",
            "subtext": "#9CA3AF"
        }
        metaphor = {
            "core": "containerized grid blocks and interconnected node network diagrams",
            "elements": ["node clusters", "flow vectors", "boundary boxes", "packet streams"]
        }
        tone = "structural, precise, and systems-oriented"
        insight = "System reliability depends on isolation boundaries and automated orchestration."

    elif any(k in t_lower for k in ["ai", "agent", "llm", "machine learning", "neural", "python"]):
        category = "ai_engineering"
        color_language = {
            "background": "#0F0F13",
            "primary": "#00E5CC",     # Cyber Cyan
            "accent": "#FF4B4B",      # Neon Red
            "text": "#FFFFFF",
            "subtext": "#B0B0B0"
        }
        metaphor = {
            "core": "neural decision trees, autonomous loop circuits, and dynamic data matrices",
            "elements": ["synapse nodes", "feedback loops", "vector arrays", "agent pipelines"]
        }
        tone = "forward-looking, technical, and analytical"
        insight = "Autonomous systems require robust control loops, not just raw model intelligence."

    elif any(k in t_lower for k in ["sql", "database", "data engineering", "kafka", "pipeline", "etl"]):
        category = "data_systems"
        color_language = {
            "background": "#111827",
            "primary": "#10B981",     # Emerald Green
            "accent": "#6366F1",      # Indigo
            "text": "#FFFFFF",
            "subtext": "#D1D5DB"
        }
        metaphor = {
            "core": "high-throughput relational tables, stream channels, and storage silos",
            "elements": ["table indices", "stream pipes", "aggregation blocks", "partition keys"]
        }
        tone = "rigorous, data-centric, and performance-focused"
        insight = "Data architecture scales cleanly only when schemas and partition strategies align."

    elif any(k in t_lower for k in ["rust", "go", "c++", "code", "clean code", "microservices", "api"]):
        category = "software_engineering"
        color_language = {
            "background": "#121214",
            "primary": "#A855F7",     # Purple
            "accent": "#EC4899",      # Pink
            "text": "#FAFAFA",
            "subtext": "#A1A1AA"
        }
        metaphor = {
            "core": "modular code building blocks, memory pointers, and low-latency execution threads",
            "elements": ["call stacks", "memory safe boxes", "concurrent threads", "interface contracts"]
        }
        tone = "pragmatic, engineering-driven, and architectural"
        insight = "Language selection and architectural decoupling dictate long-term maintainability."

    else:
        # Fallback / General Technical
        category = "general_tech"
        hash_val = int(hashlib.md5(topic.encode("utf-8")).hexdigest(), 16)
        palettes = [
            {"background": "#0F0F13", "primary": "#00E5CC", "accent": "#FF4B4B", "text": "#FFFFFF", "subtext": "#B0B0B0"},
            {"background": "#0D1117", "primary": "#58A6FF", "accent": "#D29922", "text": "#F0F6FC", "subtext": "#8B949E"},
            {"background": "#131316", "primary": "#F43F5E", "accent": "#3B82F6", "text": "#FFFFFF", "subtext": "#94A3B8"},
            {"background": "#101014", "primary": "#EAB308", "accent": "#14B8A6", "text": "#FAFAFA", "subtext": "#A1A1AA"}
        ]
        color_language = palettes[hash_val % len(palettes)]
        metaphor = {
            "core": "structural architecture blueprints and clear comparative concept layouts",
            "elements": ["concept cards", "hierarchy steps", "metric badges", "comparison splits"]
        }
        tone = "professional, authoritative, and deeply educational"
        insight = "Clear mental models transform complex technical concepts into actionable workflows."

    return {
        "topic": topic,
        "category": category,
        "tone": tone,
        "visual_metaphor": metaphor,
        "color_language": color_language,
        "key_insight": insight
    }
