#!/usr/bin/env python3
"""Build a 3-column comparison page: Claude (reference) vs GPT run-N (before) vs GPT run-M (after).
Usage: build_progress.py <page-slug> <before-file> <after-file>
Output: _loop/comparison-<after-stem>-<slug>.html
"""
import re, html, os, sys

REC = r"C:/Users/HT/Desktop/Coding Projects/LinkBuilding Agency/service-page-training-record"
C_BG = "#fff3e6"; C_TX = "#9a3412"; C_BD = "#fed7aa"
B_BG = "#e0f2fe"; B_TX = "#075985"; B_BD = "#bae6fd"
A_BG = "#dcfce7"; A_TX = "#166534"; A_BD = "#bbf7d0"

def strip_ansi(t):
    return re.sub(r'\x1b\[[0-9;]*m', '', t)

def md_to_html(t):
    t = html.escape(t)
    lines = t.split('\n')
    out, in_list = [], False
    for ln in lines:
        s = ln.rstrip()
        if not s.strip():
            if in_list: out.append('</ul>'); in_list = False
            continue
        if re.match(r'^#{1,3}\s', s):
            if in_list: out.append('</ul>'); in_list = False
            lvl = len(re.match(r'^(#+)', s).group(1))
            out.append(f'<h{lvl+1}>{s.lstrip("# ")}</h{lvl+1}>')
        elif re.match(r'^[-*]\s', s):
            if not in_list: out.append('<ul>'); in_list = True
            out.append(f'<li>{s[2:]}</li>')
        elif re.match(r'^\*\*', s) and s.endswith('**') and not s.endswith('?**'):
            out.append(f'<p class="bold">{s}</p>')
        elif s.startswith('CTA'):
            out.append(f'<p class="cta">{s}</p>')
        elif s.strip().startswith('H1:'):
            out.append(f'<h1>{s.strip()[3:]}</h1>')
        else:
            out.append(f'<p>{s}</p>')
    if in_list: out.append('</ul>')
    return '\n'.join(out)

def col(block, head, bg, tx, bd, label):
    return f'''<div class="col" style="--bg:{bg};--tx:{tx};--bd:{bd}">
  <div class="colhead">{label}</div>
  <div class="doc">{md_to_html(strip_ansi(block))}</div>
</div>'''

def main():
    slug, before, after = sys.argv[1], sys.argv[2], sys.argv[3]
    page_dir = os.path.join(REC, slug)
    c = open(os.path.join(page_dir, 'copy.md'), encoding='utf-8').read()
    b = open(os.path.join(page_dir, before), encoding='utf-8').read()
    a = open(os.path.join(page_dir, after), encoding='utf-8').read()
    before_label = f"GPT run before — {before}"
    after_label = f"GPT after — {after}"
    title = f"Page Training: {slug} — Claude vs {before} vs {after}"
    doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f5f6f8;color:#1a1d21}}
h1{{font-size:19px;padding:16px 24px;margin:0;background:#14161a;color:#fff}}
.sub{{font-size:12px;color:#9aa3ad;padding:0 24px 10px;background:#14161a}}
.columns{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;padding:20px 24px;align-items:start}}
@media(max-width:1100px){{.columns{{grid-template-columns:1fr}}}}
.col{{background:#fff;border:1px solid var(--bd);border-radius:8px;overflow:hidden}}
.colhead{{padding:8px 12px;font-size:12px;font-weight:700;letter-spacing:.5px;color:#fff;
  background:var(--bg);border-bottom:3px solid var(--tx)}}
.doc{{padding:14px 18px;font-size:13px;line-height:1.55}}
.doc h1{{font-size:16px;color:#111;background:none;padding:0;margin:6px 0 10px}}
.doc h2{{font-size:14px;margin:16px 0 6px;color:#0f355e}}
.doc h3{{font-size:13px;margin:12px 0 4px;color:#333}}
.doc p{{margin:5px 0}}
.doc ul{{margin:4px 0 8px;padding-left:20px}}
.doc .cta{{font-weight:700}}
.doc .bold{{font-weight:700}}
</style></head><body>
<h1>Page: {html.escape(slug)} — Training Progress</h1>
<div class="sub">Claude (live baseline, orange) · GPT before (blue) · GPT after (green). Numbers alone don't pass — your read decides.</div>
<div class="columns">
{col(c, 'x', C_BG, C_TX, C_BD, 'CLAUDE — copy.md (reference spec)')}
{col(b, 'x', B_BG, B_TX, B_BD, html.escape(before_label))}
{col(a, 'x', A_BG, A_TX, A_BD, html.escape(after_label))}
</div>
</body></html>'''
    out = os.path.join(REC, '_loop', f'comparison-{after.replace(".md","")}-{slug}.html')
    open(out, 'w', encoding='utf-8').write(doc)
    print('wrote', out, os.path.getsize(out), 'bytes')

if __name__ == '__main__':
    main()
