/**
 * Fast Rust-based SVG-to-PNG renderer using @resvg/resvg-js.
 * Takes input_svg_path and output_png_path from command line arguments.
 */
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error('Usage: node svg_to_png.js <input.svg> <output.png>');
  process.exit(1);
}

const inputSvgPath = args[0];
const outputPngPath = args[1];

try {
  const { Resvg } = require('@resvg/resvg-js');
  const svgContent = fs.readFileSync(inputSvgPath, 'utf-8');
  
  const resvg = new Resvg(svgContent, {
    fitTo: { mode: 'width', value: 1080 },
    font: {
      loadSystemFonts: true,
      defaultFontFamily: 'DejaVu Sans, sans-serif'
    }
  });
  
  const pngData = resvg.render();
  const pngBuffer = pngData.asPng();
  
  fs.mkdirSync(path.dirname(outputPngPath), { recursive: true });
  fs.writeFileSync(outputPngPath, pngBuffer);
  process.exit(0);
} catch (err) {
  console.error('Error rendering SVG to PNG via resvg-js:', err.message);
  process.exit(1);
}
