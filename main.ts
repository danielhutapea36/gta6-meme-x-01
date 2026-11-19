// A working gta6-meme-x-01 entry (Node 22, standard library only): it copies
// POST.json and meme.png from the repository root to /output/POST.json and
// /output/meme.png, where the gate reads POST.json. That is all the program has
// to do. The entry is the post itself: this agent made a GTA 6 meme (meme.png),
// it is posted on X from a public account with make.fun (a link or written out)
// and/or a tag of @makefunai and the entrant's play code in its text, POST.json
// names the post, and the house reads the post from X (its first picture and
// its text) and hands that to the judge. Nothing this program writes about the
// post is judged.
//
// The POST.json this entry ships holds a placeholder address, so the gate
// refuses it as it stands (valid 0). It is replaced with the post's address
// (https://x.com/<handle>/status/<id>) once the meme is posted, before submit.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand
// in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
for (const file of ['POST.json', 'meme.png']) {
  try {
    copyFileSync(join(BOT_DIR, file), join(OUTPUT_DIR, file));
  } catch (err) {
    console.error(`${file} could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
    process.exit(1);
  }
}
