"""
Dynamic SVG Architecture & Flowchart Generator for 100x Engine.
Synthesizes real-time architectural block diagrams and comparison flow vectors
embeddable directly into HTML slides and renderable as clean vector cards.
"""
from typing import List, Dict, Any


class SVGFlowEngine:
    """
    Generates inline SVG diagrams (1000x340px) representing architectural pipelines,
    feedback loops, and comparative splits.
    """

    @staticmethod
    def generate_pipeline_svg(nodes: List[str], primary_color: str = "#00E5CC", accent_color: str = "#FF4B4B") -> str:
        """Create an interconnected node flowchart SVG."""
        if not nodes:
            nodes = ["Client App", "API Gateway", "Kafka Stream", "Worker Node"]
        nodes = nodes[:4]
        box_width = 190
        box_height = 80
        gap = 50
        start_x = 30
        start_y = 40

        svg_elements = []
        for idx, node_text in enumerate(nodes):
            x = start_x + idx * (box_width + gap)
            color = primary_color if idx % 2 == 0 else accent_color
            svg_elements.append(f"""
    <g transform="translate({x}, {start_y})">
      <rect width="{box_width}" height="{box_height}" rx="10" fill="rgba(255,255,255,0.05)" stroke="{color}" stroke-width="3"/>
      <text x="{box_width/2}" y="{box_height/2 + 6}" font-family="Inter, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">{node_text[:22]}</text>
    </g>""")
            if idx < len(nodes) - 1:
                arrow_x = x + box_width
                arrow_y = start_y + box_height / 2
                svg_elements.append(f"""
    <path d="M {arrow_x} {arrow_y} L {arrow_x + gap - 10} {arrow_y}" stroke="#A1A1AA" stroke-width="3" marker-end="url(#arrow)"/>""")

        return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="980" height="160" viewBox="0 0 980 160" style="margin: 20px 0;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#A1A1AA"/>
    </marker>
  </defs>
  {"".join(svg_elements)}
</svg>"""

    @staticmethod
    def generate_comparison_svg(left_title: str, right_title: str, primary_color: str = "#00E5CC", accent_color: str = "#FF4B4B") -> str:
        """Create a visual split vs flowchart SVG."""
        return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="940" height="140" viewBox="0 0 940 140" style="margin: 15px 0;">
  <rect x="20" y="20" width="430" height="100" rx="12" fill="rgba(255, 75, 75, 0.08)" stroke="{accent_color}" stroke-width="3"/>
  <text x="235" y="76" font-family="Inter, sans-serif" font-size="20" font-weight="800" fill="{accent_color}" text-anchor="middle">❌ {left_title[:35]}</text>
  <path d="M 458 70 L 482 70" stroke="#71717A" stroke-width="3"/>
  <rect x="490" y="20" width="430" height="100" rx="12" fill="rgba(0, 229, 204, 0.08)" stroke="{primary_color}" stroke-width="3"/>
  <text x="705" y="76" font-family="Inter, sans-serif" font-size="20" font-weight="800" fill="{primary_color}" text-anchor="middle">⚡ {right_title[:35]}</text>
</svg>"""
