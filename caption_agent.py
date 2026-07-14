"""
Caption Agent V10 — Post-Generation Viral Caption Writer
Generates aggressive, engaging captions using the Hook-Context-CTA framework.
Works by reading the finalized slides so the caption perfectly matches the data.
"""
import json
from typing import Dict, Any, List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.llm_client import get_client

CAPTION_SYSTEM_PROMPT = """You are a world-class social media copywriter (LinkedIn/Instagram).
Your goal is to write a highly engaging, aggressive caption for a carousel post.

## YOUR TASK
You will be provided with the FINALIZED slides of a carousel, the topic, and the narrative arc.
You must write a caption using the H-C-C framework (Hook, Context, CTA).

## THE "H-C-C" FRAMEWORK (STRICT)

1. **HOOK (The Scroll-Stopper):** 
   - Write 1-2 punchy lines that stop the scroll.
   - Use a psychological trigger: A contrarian myth-buster, a shocking stat from the slides, or a massive curiosity gap.
   - NO generic openings like "In today's fast-paced digital world..." or "Are you struggling with..."
   - Start immediately with the punch.

2. **CONTEXT (The Value Expansion):**
   - Write 2-3 short, readable lines explaining why this matters.
   - DO NOT just repeat what is in the slides. Add meta-commentary or context.
   - Treat this as the "second hook" to get them to swipe through the carousel.

3. **CTA (Call-to-Action):**
   - End with a single, high-friction CTA. 
   - Examples: "Save this post for your next project 📌", "Swipe to see the exact breakdown 👉", "Which step are you stuck on? Let me know below!"
   - Do NOT use "Follow for more" or "Like and share".

## RULES
- Use emojis very sparingly (max 1-2 per caption). We want a clean, professional aesthetic.
- Format with clear line breaks.
- Generate 5-7 highly targeted, niche hashtags (do NOT just use generic ones like #tech #ai).

## OUTPUT FORMAT
Return ONLY a valid JSON object with EXACTLY this structure:
{
  "caption": "The full text of the caption, with \\n for line breaks.",
  "hashtags": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"]
}
"""

class CaptionAgent:
    """Agent that writes viral captions based on finalized slide data."""
    
    def __init__(self):
        self.client = get_client()

    def generate_caption(self, topic: str, slides: List[Dict], narrative_arc: str) -> Dict[str, Any]:
        """Generate a caption for the given slides."""
        
        print(f"\n✍️ Step 9.5: Caption Generation...")
        import time
        t = time.time()
        
        # We don't need to pass massive HTML, just the core data text to save tokens
        slide_summary = []
        for i, s in enumerate(slides):
            text_bits = []
            for k, v in s.items():
                if isinstance(v, str) and len(v) > 5 and k not in ["layout", "narrative_role"]:
                    text_bits.append(v)
            slide_summary.append(f"Slide {i+1}: {' | '.join(text_bits)}")
            
        slides_text = "\n".join(slide_summary)
        
        prompt = f"""Write a viral caption for this carousel post.

TOPIC: "{topic}"
NARRATIVE ARC: {narrative_arc}

ACTUAL CAROUSEL CONTENT:
{slides_text}

Generate the JSON response following the Hook-Context-CTA framework. Return ONLY JSON."""

        result = self.client.call_json(prompt, system=CAPTION_SYSTEM_PROMPT, model_tier="strong")
        
        if "error" in result:
            print(f"  ⚠️ Caption generation failed: {result['error'][:100]}")
            return {
                "caption": f"Deep dive into {topic}. Swipe to see the exact breakdown 👉",
                "hashtags": ["strategy", "insights", "growth"]
            }
            
        print(f"   ✅ Caption generated in {time.time()-t:.1f}s")
        return {
            "caption": result.get("caption", "").strip(),
            "hashtags": result.get("hashtags", [])
        }
