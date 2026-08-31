#!/usr/bin/env python3
"""Service-page training-loop audit: compare Claude copy.md vs GPT gpt-run1.md per page.

Usage: python3 audit.py <claude-copy.md> <gpt-run1.md> [more pairs...]
Checks mirror the BacklinksServices service-page standard (pricing block, trust,
FAQ, CTA, META) + mechanical (em dashes) + content flags.
"""
import re, os, sys

def words(t):
    return len(re.sub(r'[#*_>\[\]|]', ' ', t).split())

def audit(text):
    r = {}
    r['words'] = words(text)
    m_h1 = re.search(r'^(?:H1:\s*|#\s*)(.+)$', text, re.M)
    r['h1_text'] = m_h1.group(1).strip() if m_h1 else ''
    r['meta_block'] = bool(re.search(r'meta_title', text, re.I))
    r['price_70_95_135'] = all(x in text for x in ["$70", "$95", "$135"])
    r['dr_tiers'] = all(x in text for x in ["DR 10–30", "DR 31–40", "DR 40+"]) or all(x in text for x in ["DR 10-30", "DR 31-40", "DR 40+"])
    r['all_tiers_include'] = "All tiers include" in text or "ALL TIERS INCLUDE" in text
    r['700+_article'] = bool(re.search(r'700\s*\+\s*word', text)) or "700+ word" in text
    r['anchor_url_ctrl'] = ("Anchor + URL control" in text or "anchor and URL control" in text.lower() or "anchor and url control" in text.lower())
    r['dofollow'] = "dofollow" in text.lower()
    r['tat_2wk'] = any(x in text for x in ["2 weeks", "two-week", "two weeks", "TAT: 2 weeks"])
    r['free_replacement'] = "replacement" in text.lower()
    r['trust_no_invent'] = "never invent a result number" in text.lower()
    r['whitelabel_min10'] = ("10 links" in text) and ("white" in text.lower())
    r['no_min_direct'] = ("no minimum" in text.lower() or "without a minimum" in text.lower() or "no minimum order" in text.lower())
    r['email_cta'] = "hello@backlinksservices.com" in text
    r['cta_order'] = ("Order your links" in text or "Order DR" in text or "order individual placements" in text.lower())
    r['cta_quote'] = ("Custom Quote" in text or "custom quote" in text)
    r['scenario_hook'] = bool(re.search(r'stall|flatline|climb|competitor|ranking', text[:1200], re.I))
    r['em_dash_count'] = text.count("—")
    qs = re.findall(r'\*\*([^*\n]+\?)\*\*', text) or re.findall(r'^###\s+([^\n]+\?)$', text, re.M)
    # GPT sometimes writes FAQ questions as bare lines after a "FAQ" header (no bold, no ###)
    if not qs:
        lines = text.split('\n')
        for i, ln in enumerate(lines):
            if ln.strip().lower() == 'faq':
                for l2 in lines[i+1:i+30]:
                    s = l2.strip()
                    if s.endswith('?') and not s.startswith(('#', '*', '-', 'CTA')):
                        qs.append(s)
    r['faq_count'] = len(qs)
    r['faq_questions'] = qs
    r['forbidden_whatis'] = "what is saas seo" in text.lower()
    r['guest_sites_primary_count'] = len(re.findall(r'guest posting sites for saas', text.lower()))
    return r

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return 1
    results = []
    for i in range(0, len(args), 2):
        cpath, gpath = args[i], args[i+1]
        c = audit(re.sub(r'\x1b\[[0-9;]*m', '', open(cpath, encoding='utf-8').read()))
        g = audit(re.sub(r'\x1b\[[0-9;]*m', '', open(gpath, encoding='utf-8').read()))
        results.append((os.path.basename(os.path.dirname(cpath)), c, g))
    # summary table
    hdr = f"{'PAGE':<30}{'WRDS':>6}{'EM':>4}{'FAQ':>4}  MISSING vs standard (claude|gpt)"
    print(hdr); print('-' * len(hdr))
    for name, c, g in results:
        keys = ['H1_exact','meta_block','price_70_95_135','dr_tiers','all_tiers_include','700+_article','anchor_url_ctrl','dofollow','tat_2wk','free_replacement','trust_no_invent','whitelabel_min10','no_min_direct','email_cta','cta_order','cta_quote','scenario_hook']
        # H1: compare to expected via claude's own h1_text (exact match required)
        expected = c['h1_text']
        g['H1_exact'] = (g['h1_text'] == expected)
        cm = [k for k in keys if not c.get(k)]
        gm = [k for k in keys if not g.get(k)]
        mark = 'PASS' if not gm else 'GAP'
        print(f"{name:<30}{g['words']:>6}{g['em_dash_count']:>4}{g['faq_count']:>4}  {mark:>4}  {','.join(gm) or 'all checks OK'}")
        if cm:
            print(f"{'':<30}{'':>6}{'':>4}{'':>4}  claude-missing (informational): {','.join(cm)}")
    print()
    for name, c, g in results:
        print(f"\n=== {name} ===")
        print(f"Claude FAQ ({c['faq_count']}):")
        for q in c['faq_questions']: print("  -", q)
        print(f"GPT FAQ ({g['faq_count']}):")
        for q in g['faq_questions']: print("  -", q)
    return 0

if __name__ == '__main__':
    sys.exit(main())
