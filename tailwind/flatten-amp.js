const fs = require("fs");
const path = require("path");

const file = path.join(__dirname, "../static/css/home_amp.css");
const css = fs.readFileSync(file, "utf8");

function strip(input) {
  let out = "";
  let i = 0;
  while (i < input.length) {
    if (input[i] !== "@") {
      out += input[i];
      i += 1;
      continue;
    }
    const slice = input.slice(i);
    const layerStmt = slice.match(/^@layer\s+[^{;]*;/);
    if (layerStmt) {
      i += layerStmt[0].length;
      continue;
    }
    const layerBlock = slice.match(/^@layer\s+[^{]+\{/);
    if (layerBlock) {
      const open = i + layerBlock[0].length - 1;
      const close = matchingBrace(input, open);
      out += strip(input.slice(open + 1, close));
      i = close + 1;
      continue;
    }
    const droppedBlock = slice.match(/^@(?:property|supports)\b[^{]*\{/);
    if (droppedBlock) {
      const open = i + droppedBlock[0].length - 1;
      const close = matchingBrace(input, open);
      i = close + 1;
      continue;
    }
    out += input[i];
    i += 1;
  }
  return out;
}

function matchingBrace(text, open) {
  let depth = 0;
  for (let j = open; j < text.length; j += 1) {
    if (text[j] === "{") depth += 1;
    else if (text[j] === "}") {
      depth -= 1;
      if (depth === 0) return j;
    }
  }
  throw new Error("Unbalanced braces in AMP CSS");
}

let flat = strip(css).replace(/^\/\*!.*?\*\/\s*/, "");
// Django's {% static %} tag is picked up as a Tailwind class name.
flat = flat.replace(/\.static\{position:static\}/, "");
if (flat.includes("!important")) {
  throw new Error("AMP CSS still contains !important");
}
fs.writeFileSync(file, flat);
console.log(`AMP CSS ${flat.length} bytes`);
