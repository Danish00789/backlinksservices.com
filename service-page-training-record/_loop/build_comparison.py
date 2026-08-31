#!/usr/bin/env python3
"""Build the side-by-side Claude vs GPT comparison HTML (user's judgment deliverable)."""
import re, html, os

REC = r"C:/Users/HT/Desktop/Coding Projects/LinkBuilding Agency/service-page-training-record"
PAGES = ["link-building-for-saas","link-building-for-small-businesses","link-building-for-ecommerce",
         "link-building-for-local-seo","link-building-for-b2b","link-building-for-contractors",
         "link-building-for-law-firms","backlink-audit","managed-link-building","link-building-consultant"]
NAMES = ["SaaS","Small Businesses","Ecommerce","Local SEO","B2B","Contractors","Law Firms",
         "Backlink Audit","Managed","Consultant"]

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

def section_marker(line):
    s = line.strip().upper()
    for key in ['META','HERO','WHAT YOU GET','HOW IT WORKS','HOW OUR','PRICING','TRUST','FAQ','FINAL CTA','WHY WORK','WHY CHOOSE','ABOUT','HONEST','REAL REPORT','WHITE-LABEL','NO MINIMUM','ALL TIERS','DR 10','DR 31','DR 40']:
        if s.startswith(key):
            return key
    return None

def render_page(name, c_raw, g_raw):
    c_raw = strip_ansi(c_raw); g_raw = strip_ansi(g_raw)
    c_html = md_to_html(c_raw); g_html = md_to_html(g_raw)
    return f'''
<div class="tabpane" id="tab-{name}">
  <div class="cols">
    <div class="col">
      <div class="colhead claude">CLAUDE — copy.md (reference)</div>
      <div class="doc">{c_html}</div>
    </div>
    <div class="col">
      <div class="colhead gpt">GPT-5.6 Sol High — gpt-run1.md</div>
      <div class="doc">{g_html}</div>
    </div>
  </div>
</div>'''

tabs = []
panes = []
for i, p in enumerate(PAGES):
    c = open(os.path.join(REC, p, 'copy.md'), encoding='utf-8').read()
    g = open(os.path.join(REC, p, 'gpt-run1.md'), encoding='utf-8').read()
    tabs.append(f'<button class="tablink" onclick="showTab({i})">{NAMES[i]}</button>')
    panes.append(render_page(p, c, g))

html_doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Service-Page Training — Claude vs GPT-5.6 Sol High (run 1)</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f5f6f8;color:#1a1d21}}
h1{{font-size:20px;padding:16px 20px;margin:0;background:#14161a;color:#fff}}
.sub{{font-size:12px;color:#9aa3ad;padding:0 20px 10px;background:#14161a}}
.tabs{{padding:10px 20px;background:#fff;border-bottom:1px solid #ddd;position:sticky;top:0;z-index:5}}
.tablink{{padding:7px 12px;margin:2px 4px 2px 0;border:1px solid #ccc;background:#fff;border-radius:6px;cursor:pointer;font-size:12px}}
.tablink.active{{background:#1f6feb;color:#fff;border-color:#1f6feb}}
.tabpane{{display:none;padding:16px 20px}}
.tabpane.active{{display:block}}
.cols{{display:flex;gap:16px;align-items:flex-start}}
.col{{flex:1;min-width:0;background:#fff;border:1px solid #e2e5e9;border-radius:8px;overflow:hidden}}
.colhead{{padding:8px 12px;font-size:12px;font-weight:700;letter-spacing:.5px;color:#fff}}
.colhead.claude{{background:#b4551d}}
.colhead.gpt{{background:#1f6feb}}
.doc{{padding:14px 18px;font-size:13px;line-height:1.55}}
.doc h1{{font-size:17px;color:#111;background:none;padding:0;margin:6px 0 10px}}
.doc h2{{font-size:14px;margin:16px 0 6px;color:#0f355e}}
.doc h3{{font-size:13px;margin:12px 0 4px;color:#333}}
.doc h4{{font-size:12.5px;margin:10px 0 3px}}
.doc p{{margin:5px 0}}
.doc ul{{margin:4px 0 8px;padding-left:20px}}
.doc .cta{{color:#1f6feb;font-weight:700}}
.doc .bold{{font-weight:700}}
.doc hr{{border:none;border-top:1px solid #eee;margin:10px 0}}
</style></head><body>
<h1>Service-Page Training — Claude vs GPT-5.6 Sol High · Run 1 (all 10 pages, byte-identical prompts)</h1>
<div class="sub">Mechanical audit: GPT PASSED all 10 (pricing tiers, H1, trust line, FAQ count, CTAs, META). Your read decides. Claude = orange left, GPT = blue right.</div>
<div class="tabs">{"".join(tabs)}</div>
{"".join(panes)}
<script>
let cur=0;
function showTab(i){{document.querySelectorAll('.tabpane').forEach(p=>p.classList.remove('active'));
document.querySelectorAll('.tablink').forEach(b=>b.classList.remove('active'));
document.getElementById('tab-'+['{"','".join(PAGES)}'][i]).classList.add('active');
document.querySelectorAll('.tablink')[i].classList.add('active');}}
showTab(0);
</script>
</body></html>'''

out = os.path.join(REC, '_loop', 'comparison-run1.html')
open(out, 'w', encoding='utf-8').write(html_doc)
print('wrote', out, os.path.getsize(out), 'bytes')
