"""
Dynamic SVG Architecture & Flowchart Generator for 100x Engine.
Synthesizes real-time architectural block diagrams, isometric wireframe grids,
curved vertical flow lines, and checkmark feature matrices exact to 2026 design studio benchmarks.
"""
from typing import List, Dict, Any, Tuple


class SVGFlowEngine:
    """
    Generates inline and standalone SVG architectural primitives (Isometric grids,
    curved flowcharts, glowing outline typography, and pill badge layouts).
    """

    @staticmethod
    def generate_isometric_wireframe(primary_color: str = "#00E5CC", accent_color: str = "#FF5F2E") -> str:
        """Create the 3D/isometric wireframe geometry grid with glowing cyan nodes seen on Slide 1 Hero."""
        return f"""
  <g transform="translate(540, 480)" opacity="0.85">
    <!-- Outer dashed hexagon / isometric cube -->
    <polygon points="0,-240 208,-120 208,120 0,240 -208,120 -208,-120" fill="none" stroke="#2A2F3D" stroke-width="2" stroke-dasharray="6,6"/>
    <!-- Inner diagonals -->
    <line x1="0" y1="-240" x2="0" y2="240" stroke="#2A2F3D" stroke-width="2"/>
    <line x1="-208" y1="-120" x2="208" y2="120" stroke="#2A2F3D" stroke-width="2"/>
    <line x1="-208" y1="120" x2="208" y2="-120" stroke="#2A2F3D" stroke-width="2"/>
    <!-- Inner glowing diamond -->
    <polygon points="0,-140 140,0 0,140 -140,0" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.4"/>
    <!-- Glowing cyan vertex circles -->
    <circle cx="0" cy="-240" r="16" fill="none" stroke="{primary_color}" stroke-width="4"/>
    <circle cx="0" cy="-240" r="6" fill="{primary_color}" opacity="0.6"/>
    <circle cx="208" cy="-120" r="14" fill="none" stroke="{primary_color}" stroke-width="3"/>
    <circle cx="208" cy="120" r="14" fill="none" stroke="{primary_color}" stroke-width="3"/>
    <circle cx="0" cy="240" r="16" fill="none" stroke="{primary_color}" stroke-width="4"/>
    <circle cx="-208" cy="120" r="14" fill="none" stroke="{primary_color}" stroke-width="3"/>
    <circle cx="-208" cy="-120" r="14" fill="none" stroke="{primary_color}" stroke-width="3"/>
  </g>"""

    @staticmethod
    def generate_curved_flowchart(primary_color: str = "#00E5CC", accent_color: str = "#FF5F2E") -> str:
        """Create the vertical curved path diagram (`WebSocket API -> gRPC API`) seen on Slide 4."""
        return f"""
  <g transform="translate(0, 240)">
    <!-- Central Server Node -->
    <circle cx="540" cy="80" r="42" fill="#0E1118" stroke="#FFFFFF" stroke-width="3"/>
    <text x="540" y="86" font-family="Inter, sans-serif" font-size="16" font-weight="900" fill="#FFFFFF" text-anchor="middle">SERVER</text>
    
    <!-- Curved dashed path to WebSocket box -->
    <path d="M 540 122 C 540 190, 360 170, 360 220" fill="none" stroke="{primary_color}" stroke-width="3" stroke-dasharray="8,6"/>
    
    <!-- WebSocket Box -->
    <rect x="100" y="220" width="600" height="230" rx="20" fill="#0E131C" stroke="{primary_color}" stroke-width="2" opacity="0.95"/>
    <circle cx="145" cy="270" r="16" fill="{primary_color}" opacity="0.2"/>
    <text x="145" y="276" font-family="Inter, sans-serif" font-size="20" fill="#FFFFFF" text-anchor="middle">💬</text>
    <text x="180" y="276" font-family="Inter, sans-serif" font-size="34" font-weight="800" fill="{primary_color}">WebSocket API</text>
    <text x="135" y="330" font-family="Inter, sans-serif" font-size="23" fill="#C4C4CC">Two-way communication enabling low latency and instant</text>
    <text x="135" y="365" font-family="Inter, sans-serif" font-size="23" fill="#C4C4CC">real-time updates. The connection stays open.</text>
    <text x="135" y="415" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="2">USE CASES: CHAT APPS, LIVE GAMING</text>

    <!-- Curved solid path from WebSocket down to gRPC box -->
    <path d="M 450 450 C 450 560, 680 500, 680 570" fill="none" stroke="{accent_color}" stroke-width="3"/>
    
    <!-- gRPC Box -->
    <rect x="380" y="570" width="600" height="230" rx="20" fill="#141118" stroke="{accent_color}" stroke-width="2" opacity="0.95"/>
    <circle cx="425" cy="620" r="16" fill="{accent_color}" opacity="0.2"/>
    <text x="425" y="626" font-family="Inter, sans-serif" font-size="20" fill="#FFFFFF" text-anchor="middle">⚡</text>
    <text x="460" y="626" font-family="Inter, sans-serif" font-size="34" font-weight="800" fill="{accent_color}">gRPC API</text>
    <text x="415" y="680" font-family="Inter, sans-serif" font-size="23" fill="#C4C4CC">High-performance framework by Google. Very fast, uses</text>
    <text x="415" y="715" font-family="Inter, sans-serif" font-size="23" font-weight="700" fill="#FFFFFF">Protocol Buffers instead of JSON.</text>
    <text x="415" y="765" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="2">USE CASES: MICROSERVICES, CLOUD</text>
  </g>"""

    @staticmethod
    def generate_pipeline_svg(nodes: List[str], primary_color: str = "#00E5CC", accent_color: str = "#FF4B4B") -> str:
        if not nodes:
            nodes = ["Client App", "API Gateway", "Kafka Stream", "Worker Node"]
        nodes = nodes[:4]
        box_width = 200
        box_height = 86
        gap = 50
        start_x = 30
        start_y = 40

        svg_elements = []
        for idx, node_text in enumerate(nodes):
            x = start_x + idx * (box_width + gap)
            color = primary_color if idx % 2 == 0 else accent_color
            svg_elements.append(f"""
    <g transform="translate({x}, {start_y})">
      <rect width="{box_width}" height="{box_height}" rx="14" fill="rgba(255,255,255,0.05)" stroke="{color}" stroke-width="3"/>
      <text x="{box_width/2}" y="{box_height/2 + 7}" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" text-anchor="middle">{node_text[:22]}</text>
    </g>""")
            if idx < len(nodes) - 1:
                arrow_x = x + box_width
                arrow_y = start_y + box_height / 2
                svg_elements.append(f"""
    <path d="M {arrow_x} {arrow_y} L {arrow_x + gap - 12} {arrow_y}" stroke="#A1A1AA" stroke-width="3" marker-end="url(#arrow)"/>""")

        return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="980" height="170" viewBox="0 0 980 170" style="margin: 20px 0;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#A1A1AA"/>
    </marker>
  </defs>
  {"".join(svg_elements)}
</svg>"""

    @staticmethod
    def generate_comparison_svg(left_title: str, right_title: str, primary_color: str = "#00E5CC", accent_color: str = "#FF4B4B") -> str:
        return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="940" height="140" viewBox="0 0 940 140" style="margin: 15px 0;">
  <rect x="20" y="20" width="430" height="100" rx="14" fill="rgba(255, 75, 75, 0.08)" stroke="{accent_color}" stroke-width="3"/>
  <text x="235" y="76" font-family="Inter, sans-serif" font-size="22" font-weight="800" fill="{accent_color}" text-anchor="middle">❌ {left_title[:35]}</text>
  <path d="M 458 70 L 482 70" stroke="#71717A" stroke-width="3"/>
  <rect x="490" y="20" width="430" height="100" rx="14" fill="rgba(0, 229, 204, 0.08)" stroke="{primary_color}" stroke-width="3"/>
  <text x="705" y="76" font-family="Inter, sans-serif" font-size="22" font-weight="800" fill="{primary_color}" text-anchor="middle">⚡ {right_title[:35]}</text>
</svg>"""
