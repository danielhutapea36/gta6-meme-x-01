// A working gta6-meme-x-01 entry (Node 22, standard library only): it validates
// POST.json, then copies POST.json and meme.png from the repository root to
// /output/POST.json and /output/meme.png, where the gate reads POST.json. That is
// all the program has to do. The entry is the post itself: this agent made a GTA 6
// meme (meme.png), it is posted on X from a public account with make.fun (a link or
// written out) and/or a tag of @makefunai and the entrant's play code in its text,
// POST.json names the post, and the house reads the post from X (its first picture
// and its text) and hands that to the judge. Nothing this program writes about the
// post is judged.
//
// POST.json must name the posted meme's address
// (https://x.com/<handle>/status/<id>); a placeholder address is refused here
// with a clear error instead of being copied on to the gate.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand
// in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// The post's address: https://x.com/<handle>/status/<digits> (or twitter.com).
// A placeholder (<handle> / <id> still in it) or anything else is refused here,
// so a bad POST.json fails loudly instead of reaching the gate.
const POST_URL = /^(?:https?:\/\/)?(?:www\.)?(?:x\.com|twitter\.com)\/[A-Za-z0-9_]+\/status\/[0-9]+$/;
let post: unknown;
try {
  post = JSON.parse(readFileSync(join(BOT_DIR, 'POST.json'), 'utf8'));
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
const url = (post as { url?: unknown } | null)?.url;
if (typeof url !== 'string' || !POST_URL.test(url)) {
  console.error(
    `POST.json does not name a posted X status (expected https://x.com/<handle>/status/<id>, got ${JSON.stringify(url)}); post the meme first, then put its address in POST.json.`,
  );
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
for (const file of ['POST.json', 'meme.png']) {
  try {
    copyFileSync(join(BOT_DIR, file), join(OUTPUT_DIR, file));
  } catch (err) {
    console.error(`${file} could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
    process.exit(1);
  }
}
console.log(`copied POST.json (${url}) and meme.png to ${OUTPUT_DIR}`);
