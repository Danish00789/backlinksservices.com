#!/usr/bin/env python3
"""Sync a site's universal <header> and <footer> across every page.

WHY: static sites with a header/footer copy in every page drift apart. The homepage gets
updated, the other pages don't. This keeps ONE source of truth per site and pushes it out.

USAGE (run from the site root):
    python _shell/sync_shell.py --extract <homepage.html>   capture the current shell as the template
    python _shell/sync_shell.py --sync                      apply templates to every page
    python _shell/sync_shell.py --check                     report pages that drift from the template

Templates live in _shell/header.html and _shell/footer.html.

On the FIRST --sync, each page's existing <header>/<footer> block is replaced and wrapped in
marker comments. After that, sync only touches the marked region - so a hand edit outside the
shell is never clobbered.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL_HEADER = os.path.join(HERE, "header.html")
TPL_FOOTER = os.path.join(HERE, "footer.html")

H_START, H_END = "<!-- SHELL:HEADER START -->", "<!-- SHELL:HEADER END -->"
F_START, F_END = "<!-- SHELL:FOOTER START -->", "<!-- SHELL:FOOTER END -->"

# directories never touched
SKIP_DIRS = {"_shell", ".git", "node_modules", "dist", ".astro", "backup", "backups",
             "service-page-training-record", "LBHQ Ops. Batch Analysis", "content-drafts"}

# individual files never touched (e.g. live orphan duplicates awaiting a decision)
SKIP_FILES = {"backlinks-services-homepage.html"}

PAGE_GLOB = ".html"


def iter_pages():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f.endswith(PAGE_GLOB) and f not in SKIP_FILES:
                yield os.path.join(dp, f)


def read(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def write(p, s):
    with open(p, "w", encoding="utf-8", errors="replace", newline="") as fh:
        fh.write(s)


def extract_block(html, tag):
    m = re.search(rf"<{tag}\b.*?</{tag}>", html, re.S | re.I)
    return m.group(0) if m else None


def do_extract(homepage):
    p = homepage if os.path.isabs(homepage) else os.path.join(ROOT, homepage)
    if not os.path.isfile(p):
        sys.exit(f"homepage not found: {p}")
    h = read(p)
    for tag, tpl in (("header", TPL_HEADER), ("footer", TPL_FOOTER)):
        b = extract_block(h, tag)
        if not b:
            sys.exit(f"no <{tag}> found in {p}")
        write(tpl, b + "\n")
        print(f"  extracted <{tag}> ({len(b)} chars) -> {os.path.relpath(tpl, ROOT)}")
    print("\n  NOTE: edit the templates now, then run --sync.")


def substitute(html, tag, tpl_body, start, end):
    """Return (new_html, status)."""
    # 1. already marked -> replace marked region
    if start in html and end in html:
        pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
        new = pat.sub(lambda m: start + "\n" + tpl_body + "\n" + end, html, count=1)
        return new, ("in-sync" if new == html else "updated")
    # 2. first run -> wrap existing block
    m = re.search(rf"<{tag}\b.*?</{tag}>", html, re.S | re.I)
    if not m:
        return html, "no-region"
    block = start + "\n" + tpl_body + "\n" + end
    return html[:m.start()] + block + html[m.end():], "updated"


def do_sync(check_only=False):
    for tpl, label in ((TPL_HEADER, "header"), (TPL_FOOTER, "footer")):
        if not os.path.isfile(tpl):
            sys.exit(f"missing template {tpl} - run --extract first")
    tpl_h = read(TPL_HEADER).strip()
    tpl_f = read(TPL_FOOTER).strip()

    counts = {"updated": 0, "in-sync": 0}
    problems = []
    for p in sorted(iter_pages()):
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        h = read(p)
        orig = h
        h, s1 = substitute(h, "header", tpl_h, H_START, H_END)
        h, s2 = substitute(h, "footer", tpl_f, F_START, F_END)
        for s, what in ((s1, "header"), (s2, "footer")):
            if s == "no-region":
                problems.append(f"{rel}: no <{what}>")
        if h != orig:
            if not check_only:
                write(p, h)
            counts["updated"] += 1
            print(f"  {'WOULD UPDATE' if check_only else 'updated'}  {rel}")
        else:
            counts["in-sync"] += 1

    print(f"\n  updated : {counts['updated']}")
    print(f"  in sync : {counts['in-sync']}")
    if problems:
        print(f"  problems: {len(problems)}")
        for x in problems:
            print(f"    {x}")
    return counts


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract", metavar="HOMEPAGE")
    ap.add_argument("--sync", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.extract:
        do_extract(a.extract)
    elif a.check:
        print("CHECK (no writes):")
        do_sync(check_only=True)
    elif a.sync:
        print("SYNC:")
        do_sync()
    else:
        ap.print_help()
