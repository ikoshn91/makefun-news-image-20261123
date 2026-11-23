import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry program for make.fun news-image-20261123.
// Copies the pre-rendered entry.png (drawn by gen_image.py) into the
// output directory. Standard library only, no network, deterministic:
// the same input bytes are copied on every run.
const MAX_BYTES = 1048576; // 1 MiB, the competition's image size cap

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const out = join(outDir, "entry.png");

let size: number;
try {
  size = statSync(src).size;
} catch {
  console.error(`entry.png not found next to main.ts: ${src}`);
  process.exit(1);
}

if (size > MAX_BYTES) {
  console.error(`entry.png is ${size} bytes, over the ${MAX_BYTES} byte cap`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, out);
console.log(`copied entry.png (${size} bytes) to ${out}`);
