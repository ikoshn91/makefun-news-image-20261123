// News-image entry for make.fun's "Sum up 23 November's world news
// in one image". The front page (entry.png) was drawn by gen_image.py
// in this repository; this program only copies it to the grader's
// output directory. Node 22, standard library only. No network, no
// randomness: every run writes exactly the same bytes.
import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'entry.png');
// The gate allows at most 1 MiB: refuse to write an oversize file.
if (statSync(src).size > 1048576) {
  throw new Error(`entry.png is ${statSync(src).size} bytes, over the 1 MiB limit`);
}
copyFileSync(src, join(outDir, 'entry.png'));
