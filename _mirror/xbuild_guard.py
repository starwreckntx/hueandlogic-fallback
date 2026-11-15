#!/usr/bin/env python3
"""Cross-build navigation guard for the static mirror.

Usage (from the mirror root):
    python3 _mirror/xbuild_guard.py .           # inject / refresh the guard in every Next page
    python3 _mirror/xbuild_guard.py --check .   # verify every Next page carries the current guard

Why: this mirror holds pages from more than one `next build`. When a page from build A
client-navigates (or prefetches) to a page from build B, the Next router fetches B's
`<path>/index.txt` payload, fails to parse it against A's chunks, and its error path sends the
browser to the payload URL itself, so the visitor lands on raw text at `.../index.txt`.

The guard is one constant inline script, first thing in <head>. It wraps window.fetch for
same-origin `*/index.txt` requests only: it reads the payload's build id (`0:{..."b":"<id>"`)
and compares it with this page's own build id (the `<!--id-->` comment Next writes after the
doctype). Same build: the response is passed through untouched. Different build: the router is
handed a non-payload response whose URL is the clean page URL, which makes Next do an ordinary
full page load of that page. Nothing else is intercepted.

The script is identical on every page, so adding pages from a new build only needs this tool
re-run; pages already guarded do not change.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys

MARK_START, MARK_END = "<!--xbuild-guard-->", "<!--/xbuild-guard-->"
GUARD_JS = (
    '(function(){var F=window.fetch,c=document.documentElement.previousSibling,'
    'B=c&&c.nodeType===8?c.data:"";if(!F||!B)return;'
    'window.fetch=function(i){var a=arguments,s=this,u;'
    'try{u=new URL(typeof Request!=="undefined"&&i instanceof Request?i.url:String(i),location.href);'
    'if(u.origin!==location.origin||!/\\/index\\.txt$/.test(u.pathname))u=0}catch(e){u=0}'
    'var p=F.apply(s,a);if(!u)return p;'
    'return p.then(function(r){if(!r.ok)return r;'
    'return r.clone().text().then(function(t){'
    'var m=/(?:^|\\n)0:\\{[^\\n]{0,200}?"b":"([^"]+)"/.exec(t);'
    'if(!m||m[1]===B)return r;'
    'u.pathname=u.pathname.slice(0,-9);u.searchParams.delete("_rsc");'
    'var x=new Response("",{status:200,headers:{"content-type":"text/html"}});'
    'Object.defineProperty(x,"url",{value:u.href});return x},function(){return r})})}})();'
)
TAG = MARK_START + "<script>" + GUARD_JS + "</script>" + MARK_END
NEXT_PAGE = re.compile(r"^<!DOCTYPE html><!--([^>]+)-->")
STRIP = re.compile(re.escape(MARK_START) + ".*?" + re.escape(MARK_END), re.S)


def next_pages(root: str):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in (".git", "_next", "_mirror")]
        for f in files:
            if not f.endswith(".html"):
                continue
            path = os.path.join(d, f)
            with open(path, encoding="utf-8") as fh:
                head = fh.read(200)
            m = NEXT_PAGE.match(head)
            if m:
                yield path, m.group(1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root")
    ap.add_argument("--check", action="store_true", help="verify only; exit 1 if any Next page lacks the current guard")
    args = ap.parse_args()
    builds: dict[str, int] = {}
    changed, missing, total = 0, [], 0
    for path, build in sorted(next_pages(args.root)):
        total += 1
        builds[build] = builds.get(build, 0) + 1
        with open(path, encoding="utf-8") as fh:
            s = fh.read()
        if s.count(TAG) == 1 and len(STRIP.findall(s)) == 1:
            continue
        if args.check:
            missing.append(os.path.relpath(path, args.root))
            continue
        s = STRIP.sub("", s)
        i = s.find("<head>")
        if i < 0:
            missing.append(os.path.relpath(path, args.root))
            continue
        s = s[: i + 6] + TAG + s[i + 6 :]
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(s)
        changed += 1
    print(f"next pages={total} builds={len(builds)} changed={changed} missing={len(missing)}")
    for b, n in sorted(builds.items(), key=lambda kv: -kv[1]):
        print(f"  build {b}: {n} pages")
    print("  guard sha256:", hashlib.sha256(GUARD_JS.encode()).hexdigest())
    for m in missing:
        print("  MISSING:", m)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
