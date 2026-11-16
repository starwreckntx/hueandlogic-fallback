# Hue & Logic · GitHub Pages

This repository serves the public static site at www.hueandlogic.com. The custom domain is configured by CNAME. The website source and the FrontDesk service have their own repositories.

## ARC release candidate

The native ARC panel and studio entrance use the public, text-only FrontDesk gateway. The published site contains the browser client and public email contact. The generated static pages use a single Next.js build with the production homepage and assessment prices, both November articles, their media and the Medium vs. Method explainer. The homepage preserves the existing first-arrival behavior and the `/?home` override.

The public article index, library, sitemap and two static feeds include 14 approved articles. The feed URLs are `/api/articles` and `/api/rss`; each is an ordinary static file. The site has no server API routes. Future releases must preserve the approved content from this mirror and validate the complete output. The historical notes below describe earlier builds.

## 2026-11-10 rebuild: prices filled in

- The homepage offer cards and the tiers on `/logic/assessment` now show "from" prices.
  They are floors, not quotes: the written scope sets the final number.
- Built from the site branch `claude/set-from-prices` (one commit on top of 60e7683).
  Every other page has the same visible text, and every non-build asset is byte-identical.

## 2026-11-10 rebuild: the studio entrance is back

- `/enter` (the 3D studio entrance: shed, gallery, doors) is in the mirror again. The
  first build left it out.
- Arrivals from outside the site land on `/enter`, as they did on the live site. The live
  site does this in `middleware.ts`. A static host can't run that, so the homepage carries
  a small inline script that makes the same test before the page paints. `/?home`, links
  inside the site, reloads and crawlers still get the homepage.
- Same source commit as the first build. Every other page has the same visible text, and
  every non-build asset is byte-identical.
- The first build's `_next` files are kept, so pages already cached by browsers keep loading.

The contact page offers email in place of the form, because the form has no server to
send to on this copy. That change lives only in the mirror build; the site source still
has the form. ARC chat also needs a server and will not answer here. That includes the
"ARC keeps the door" box at the doors; both doors work without it.

## 2026-11-11: new article "swarm-response-sop"

- Added `/articles/swarm-response-sop/` ("When Your Server Overloads at 2 AM: A
  Blast-Radius Containment SOP for Small Shops Without an IT Department"), its
  `/logic/library/text/swarm-response-sop` payload, the LOGIC Library listing entry, and
  its `sitemap.xml` entry. Nothing else on the site changed.
- Built from the site source at 60e7683 with the mirror steps below, plus
  `content/articles/swarm-response-sop.md` (id 14). That article file is not in the site
  repo yet; add it there before the next full rebuild or the page will drop out.
- Only new `_next` files were added; no existing `_next` file was changed or removed.
  Pages from this build and the 2026-11-10 build use different chunk sets, so moving
  between them is a normal full page load.
- `/articles` (the listing page) loads its list from `/api/articles`, which this static copy
  doesn't have, so that listing was already empty before this change and still is. The
  LOGIC Library (`/logic/library`) lists the article.

## 2026-11-15: new article "survives-a-change-of-hands" + 3D explainer

- Added `/articles/survives-a-change-of-hands/` ("Build Your Own Multi-Agent Architecture
  That Survives a Change of Hands", id 15) and `/explainers/medium-vs-method/` (static
  three.js explainer of the Nov 13, 2026 ground stop; three.js 0.160.0 vendored, no CDN),
  plus both `sitemap.xml` entries. Nothing else on the site changed.
- Built from the site repo at 9f45692 (PR #53) with the mirror steps below. The site repo
  gave the article id 14, which collides with `swarm-response-sop` here; this build uses
  id 15, and the site repo gets the same fix.
- Only new `_next` files were added (28); no existing `_next` file was changed or removed.
- Not updated: the LOGIC Library listing. A rebuild of that page from the site repo would
  drop `swarm-response-sop`, whose source is still not in the site repo.
- Why this copy carries it: Vercel paused deployments for the account on Nov 8, 2026
  (Hobby fair-use limit, Fluid Provisioned Memory) until Dec 8, 2026.

## 2026-11-15: explainer works without 3D graphics

- `/explainers/medium-vs-method/` needed WebGL. In a browser without it the page was a blank
  box with a dead Play button. It now checks first and, with no WebGL, shows the same six-step
  timeline and sources over a still picture of each step (`still/*.jpg`, canvas captures of the
  same scene). With WebGL nothing changes.
- The seal-check line wraps on phones instead of running off both edges.
- Source: site repo PR #55. `explainers/medium-vs-method/MANIFEST.sha256` lists the folder's 11 files;
  from the mirror root, `sha256sum -c explainers/medium-vs-method/MANIFEST.sha256`.

## 2026-11-15: three newer pages rebuilt from one build; Articles listing and RSS work

- **One build for the newer pages.** `/articles/swarm-response-sop/`,
  `/articles/survives-a-change-of-hands/` and `/logic/library/` now come from a single build:
  site repo `d2daa5f` plus `content/articles/swarm-response-sop.md` (site repo PR #55), with
  the mirror steps below. The tree holds two builds: 44 pages and these 3.
- **The 2026-11-13 crash, corrected cause.** It was not the mixed builds. The original
  2026-11-11 page runs clean beside the other build. On 2026-11-12 the teaser video was
  pasted into the built page by hand. The same text also sits in the page's inline data, in a
  length-prefixed block, and the paste changed the text without the length. The data stream
  never finished, React threw "Connection closed" and Next showed its error screen. Dropping
  the page's scripts hid that, and left the mobile menu dead on that article.
- **Fix.** The teaser is part of the article source now, with absolute asset paths. The page
  hydrates normally again: scripts are back and the mobile menu works. Its visible text is
  identical to the page it replaces. The two teaser files did not change.
- **Rule.** Never edit text inside a built page by hand. Change the source and rebuild the page.
- **LOGIC Library** lists 26 pieces; the new article is No. 01.
  `logic/library/text/survives-a-change-of-hands` is new and the swarm payload carries the teaser.
- **`/api/articles` and `/api/rss`** are static files now, written by
  `scripts/mirror-static-api.ts` in the site repo with the same code as the site routes
  (15 articles). The Articles listing page shows them. The files have no extension, so Pages
  serves them as `application/octet-stream`: the listing and feed readers parse them, and a
  browser offers the feed as a download. Regenerate both whenever an article is added.
- Only two `_next` files were added (the new build's manifests). No existing `_next` file
  was changed or removed. The guard was re-run; `--check` exits 0.

## 2026-11-15: cross-build navigation guard

- **What was wrong.** This mirror holds pages from three builds. A link from a page of one
  build to a page of another did not do "a normal full page load", as the 2026-11-11 note
  below says. The Next router fetched the other page's `index.txt`, could not parse it
  against its own chunks, and its error path sent the browser to the raw `.../index.txt`.
  Seen on LOGIC → "Enter the Library" and on every header link of the new article.
- **Fix.** `_mirror/xbuild_guard.py` puts one constant inline script first in `<head>` of
  every Next page (47 files, `404.html` included). It wraps `fetch` for same-origin
  `*/index.txt` requests only, compares the payload's build id with the page's own, and for a
  different build hands the router a non-payload response so Next does an ordinary full page
  load of the clean URL. Links inside one build still navigate client-side. Other-build
  payloads are no longer parsed at all, so their chunks are never loaded into the wrong runtime.
- **Rule for partial updates.** After copying pages from a new build into this tree, run
  `python3 _mirror/xbuild_guard.py .` and then `python3 _mirror/xbuild_guard.py --check .`
  (exit 0 = every Next page carries the current guard). The script is identical on every page;
  its sha256 is `5abb4a6ab6d788442defd1d2d0a9b2382da87b014a813d4b4ef546205042aa15`.
- No page text, asset or `_next` file changed. One full single-build rebuild remains the
  durable fix and would make the guard unnecessary.

## How this build was made

From the site repo at the commit above:

1. Remove `app/api`, `app/admin`, `app/console`, `app/screening` and `middleware.ts`.
2. `next.config.js`: add `trailingSlash: true`.
3. `app/robots.ts` and `app/sitemap.ts`: add `export const dynamic = 'force-static'`, and
   drop `/screening` from the sitemap.
4. `app/page.tsx`: add the inline arrival script described above.
5. `app/contact/page.tsx`: replace the form with an email button (mirror only).
6. `NEXT_OUTPUT_MODE=export next build`, then copy `out/` here and keep `CNAME`,
   `.nojekyll` and this file.

GitHub Pages project URL (subpath) is obsolete after this cutover; use the custom domain.
