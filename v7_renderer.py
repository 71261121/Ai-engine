"""
V7 Renderer — Produces 2160x2700 PNG (deviceScaleFactor: 2) from HTML slides.
Uses Puppeteer with proper font loading wait.
"""
import os
import subprocess
from pathlib import Path


def render_carousel(slides_dir: str, output_dir: str = None, scale: int = 2):
    """
    Render all HTML slides in a directory to PNG.
    
    Args:
        slides_dir: Directory containing HTML slides
        output_dir: Output directory (default: slides_dir/output_v7)
        scale: deviceScaleFactor (2 = 2160x2700 final output)
    """
    slides_path = Path(slides_dir)
    if output_dir is None:
        output_path = slides_path / "output_v7"
    else:
        output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all slide HTML files
    html_files = sorted(slides_path.glob("slide_*.html"))
    if not html_files:
        html_files = sorted(slides_path.glob("*.html"))

    if not html_files:
        raise ValueError(f"No HTML files found in {slides_dir}")

    print(f"🎨 Rendering {len(html_files)} slides at {scale}x scale (1080x1350 -> {1080*scale}x{1350*scale})...")

    # Build render script
    render_script = output_path / "render_temp.js"
    script_content = f'''
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const SLIDES_DIR = "{slides_path.as_posix()}";
const OUTPUT_DIR = "{output_path.as_posix()}";
const SCALE = {scale};

const slides = {[
    {{"file": f.name, "output": f"V7_{f.stem}.png", "name": f.stem}}
    for f in html_files
]};

(async () => {{
  const browser = await puppeteer.launch({{
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
  }});

  const page = await browser.newPage();
  await page.setViewport({{ width: 1080, height: 1350, deviceScaleFactor: SCALE }});

  console.log(`🎨 Rendering ${{slides.length}} slides at ${{SCALE}}x scale...\\n`);

  for (const slide of slides) {{
    const filePath = path.join(SLIDES_DIR, slide.file);
    const outputPath = path.join(OUTPUT_DIR, slide.output);

    if (!fs.existsSync(filePath)) {{
      console.error(`❌ Missing: ${{slide.file}}`);
      continue;
    }}

    const fileUrl = 'file:///' + filePath.replace(/\\\\/g, '/');
    await page.goto(fileUrl, {{ waitUntil: 'networkidle0', timeout: 30000 }});

    // Wait for fonts to load
    await page.evaluate(() => document.fonts.ready);
    // Extra delay for SVGs and heavy glassmorphism blur effects
    await new Promise(r => setTimeout(r, 2000));

    await page.screenshot({{ path: outputPath, type: 'png' }});

    const stats = fs.statSync(outputPath);
    const sizeKB = (stats.size / 1024).toFixed(0);
    console.log(`  ✅ ${{slide.name}} -> ${{slide.output}} (${{sizeKB}} KB)`);
  }}

  await browser.close();
  console.log(`\\n🎉 All slides rendered to ${{OUTPUT_DIR}}`);
}})();
'''

    render_script.write_text(script_content)
    
    # Run puppeteer
    result = subprocess.run(
        ["node", str(render_script)],
        capture_output=True,
        text=True,
        cwd=str(output_path.parent),
        timeout=180
    )
    
    if result.returncode != 0:
        print(f"❌ Render failed: {result.stderr}")
        raise RuntimeError(f"Puppeteer render failed: {result.stderr}")
    
    print(result.stdout)
    
    # Clean up temp script
    render_script.unlink(missing_ok=True)
    
    return str(output_path)


def render_single(html_path: str, output_path: str = None, scale: int = 2) -> str:
    """Render a single HTML file to PNG."""
    html_file = Path(html_path)
    if output_path is None:
        output_file = html_file.parent / f"V7_{html_file.stem}.png"
    else:
        output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    script = f'''
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {{
  const browser = await puppeteer.launch({{
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
  }});
  const page = await browser.newPage();
  await page.setViewport({{ width: 1080, height: 1350, deviceScaleFactor: {scale} }});
  
  const fileUrl = 'file:///' + "{html_file.as_posix()}".replace(/\\\\/g, '/');
  await page.goto(fileUrl, {{ waitUntil: 'networkidle0', timeout: 30000 }});
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));
  
  await page.screenshot({{ path: "{output_file.as_posix()}", type: 'png' }});
  await browser.close();
  console.log('✅ Rendered: {output_file.name}');
}})();
'''

    temp_script = output_file.parent / "render_one.js"
    temp_script.write_text(script)
    
    result = subprocess.run(
        ["node", str(temp_script)],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    temp_script.unlink(missing_ok=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Render failed: {result.stderr}")
    
    return str(output_file)


if __name__ == "__main__":
    # Test render
    import sys
    if len(sys.argv) > 1:
        render_carousel(sys.argv[1])
    else:
        print("Usage: python -m src.visual.v7_renderer <slides_dir>")