# Hue & Logic — static fallback mirror

Static fallback copy of the public pages of hueandlogic.com, built from the site's
main branch (commit 60e7683) plus the price change described below. Build output only.
No source, no server routes, no forms backend.

This tree is the **root-path** build (assets at `/…`) for serving on the custom domain
`www.hueandlogic.com` via GitHub Pages. Excluded from this mirror: `/screening`,
`/api`, `/admin`, `/console`, and any Maxtena / pLEO / Hydra / Starshield content.

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
