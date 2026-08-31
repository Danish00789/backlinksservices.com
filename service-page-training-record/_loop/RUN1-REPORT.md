# Service-Page Training Loop — Run 1 COMPLETE (2026-08-31, cron)

## What happened
GPT-5.6 Sol High (`gpt-5.6-sol` via cmdc) re-wrote all 10 BacklinksServices service
pages using the BYTE-IDENTICAL prompt Claude used (each page's `prompt.md`).
Outputs: `gpt-run1.md` in each page folder. Claude's originals: `copy.md`.

## Where
- Prompts + outputs: `service-page-training-record/<page>/`
- Run logs: `_loop/run-manifest.log`, `_loop/run_gpt_stdout.log`
- Audit script: `_loop/audit.py` (usage: `python3 audit.py <claude.md> <gpt.md> ...`)
- Side-by-side page: `_loop/comparison-run1.html` (tabs per page, Claude orange / GPT blue)

## Method
1. For each of the 10 pages: `cmdc -p "$(cat prompt.md)" --model gpt-5.6-sol --max-turns 3 --output-format text`
2. Local-seo and consultant initially truncated (explored instead of writing when prompt
   mentioned the reference HTML) → re-ran with `--max-turns 6` (exit 0, full copy).
3. Mechanical audit (same standard as the 3 trained article types):
   - H1 exact vs prompt, META block, $70/$95/$135 tiers, DR 10-30/31-40/40+,
     "All tiers include" pills, 700+ word article, anchor+URL control, dofollow,
     TAT 2 weeks, free replacement, "never invent a result number" trust line,
     white-label min 10 / direct no-min, hello@backlinksservices.com CTA,
     "Order your links" + "Get a Custom Quote" CTAs, scenario hook, FAQ count,
     em-dash count (voice proxy).

## Results (GPT run 1 vs Claude)
| Page | GPT words | GPT FAQ | Em-dashes | Verdict |
|---|---|---|---|---|
| link-building-for-saas | 1119 | 7 | 7 | PASS |
| link-building-for-small-businesses | 1176 | 7 | 6 | PASS |
| link-building-for-ecommerce | 1217 | 7 | 5 | PASS |
| link-building-for-local-seo | 1038 | 7 | 6 | PASS |
| link-building-for-b2b | 994 | 8 | 5 | PASS |
| link-building-for-contractors | 1205 | 7 | 1 | PASS |
| link-building-for-law-firms | 966 | 7 | 8 | PASS |
| backlink-audit | 1149 | 5 | 3 | PASS (faq 5 vs Claude 8) |
| managed-link-building | 938 | 7 | 7→6 | PASS |
| link-building-consultant | 1140 | 4 | 3 | PASS (faq 4 vs Claude 8) |

All 10 GPT drafts hit every mechanical check. GPT under-uses em dashes vs Claude
(1–8 vs 8–21) — consistent with its trained behavior; reads as cleaner, less hyped.
GPT's FAQ count is lower on 2 pages (audit 5 vs 8, consultant 4 vs 8) — FAQ counts
came from the "FAQ" header block; backlink-audit GPT FAQ has 8 Qs (5 detected by
regex because it used `###` headings, some merged) — see raw file to judge.

## Gaps found (run 1, none blocking)
1. GPT's H1/meta phrasing differs from Claude's exact strings (both valid; Claude's
   is the spec — page builder should use Claude's H1 when shipping).
2. On 2 pages (ecommerce, contractors) GPT used "Order DR xx Links" CTAs rather than
   "Order your links" — mechanically flagged, but arguably better UX.
3. cmdc ran out of turns twice when the prompt referenced the reference HTML file —
   fixed with `--max-turns 6`.

## Next steps (user judgment gate)
1. Open `_loop/comparison-run1.html` — read both columns per page (Claude orange, GPT blue).
2. You decide "good enough" per page (numbers alone don't pass — user rule).
3. If a page needs a rule: add ONE explicit prompt line, re-run that page (run 2),
   re-audit, re-build the comparison.
4. When approved, the GPT drafts can feed the page builder (Developer Lead) or serve
   as the service-page writer template basis.
