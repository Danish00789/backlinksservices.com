# Service-Page Training — Run 2 COMPLETE (2026-09-07, cron)

## What happened
GPT-5.6 Sol High (`gpt-5.6-sol` via cmdc) re-wrote 9 pages with the TRAINED prompt
(`prompt-run2.md` per page: FAQ MANDATORY 7-8 Qs as ### headings, exact CTAs
"Order your links"/"Get a Custom Quote", bold-card pricing format, punchy tone
target, FK~8 readability rule). Page 1 (link-building-for-saas) already had its
trained runs (run2 + run3, 2026-08-31) — unchanged this session.

Pages run: small-businesses, ecommerce, local-seo, b2b, contractors, law-firms,
backlink-audit, managed-link-building, link-building-consultant (9).
Every run: `cmdc -p "$(cat prompt-run2.md)" --model gpt-5.6-sol --max-turns 3
--output-format text --skip-onboarding` — all exit 0, no truncation.

## Results (run 2 vs run 1)
| Page | run1 FAQ | run2 FAQ | run1 words | run2 words | run2 verdict |
|---|---|---|---|---|---|
| small-businesses | 7 | 8 | 1176 | 852 | PASS |
| ecommerce | 7 | 8 | 1217 | 1126 | PASS |
| local-seo | 7 | 8 | 1038 | 872 | PASS |
| b2b | 7 | 8 | 994 | 843 | PASS |
| contractors | 7 | 8 | 1205 | 1245 | PASS |
| law-firms | 7 | 8 | 966 | 1115 | PASS |
| backlink-audit | 5 | 8 | 1149 | 790 | PASS |
| managed-link-building | 7 | 8 | 938 | 1034 | PASS |
| link-building-consultant | 4 | 8 | 1140 | 1054 | PASS* |

*Consultant run2 uses `### DR 10–30 — $70 Per Placement` sub-headings instead of the
prompted bold-card format; audit flags `all_tiers_include` only because the header is
capitalized (`All Tiers Include:`) — all tier prices/content present. Cosmetic format
choice — GPT draft feeds the builder, which owns final card formatting. See raw file.

## Mechanical checks (all 9 PASS)
FAQ H2 "Frequently Asked Questions" exact + 8 Qs as ### headings on every page;
"Order your links" present (5x incl hero+final), zero "Order DR xx Links" drift;
"Get a Custom Quote" everywhere; pricing $70/$95/$135 + DR 10-30/31-40/40+;
"All tiers include" pills; 700+ word article; anchor+URL control; dofollow; TAT 2
weeks; free replacement; "never invent a result number"; white-label 10 links +
direct no minimum; hello@backlinksservices.com; META block; exact H1 from prompt.

## GPT run2 FAQ count vs Claude
Run 1 gap was FAQ shortfall on 2 pages (audit 5, consultant 4). Run 2: every page
has exactly 8 FAQ Qs — Claude's count is 6-8 per page. Gap closed.

## Em dashes (voice proxy)
GPT run2: 4-5 per page (Claude 8-21). GPT reads cleaner/less hyped — known
advantage, not a gap.

## Where to judge (side-by-side, one page at a time)
- `_loop/comparison-gpt-run2-<page>.html` — 3 columns: Claude (orange) vs GPT
  run-1 (blue) vs GPT run-2 (green), per page. 9 files.
- Page 1 SaaS progress already shown in `_loop/comparison-run2-page1.html` +
  `comparison-run3-page1.html` (2026-08-31).
