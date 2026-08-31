#!/usr/bin/env bash
# GPT-5.6 Sol High service-page training loop — run GPT on each Claude page with the SAME prompt.
# Sequential, one page at a time. Saves gpt-run1.md per page + appends to run-manifest.log.
set -u
REC="/c/Users/HT/Desktop/Coding Projects/LinkBuilding Agency/service-page-training-record"
CMD="/c/Users/HT/AppData/Local/hermes/node/cmdc"
LOG="$REC/_loop/run-manifest.log"
PAGES=(link-building-for-saas link-building-for-small-businesses link-building-for-ecommerce link-building-for-local-seo link-building-for-b2b link-building-for-contractors link-building-for-law-firms backlink-audit managed-link-building link-building-consultant)

for page in "${PAGES[@]}"; do
  OUT="$REC/$page/gpt-run1.md"
  if [ -f "$OUT" ]; then
    echo "[$(date +%H:%M:%S)] SKIP $page (gpt-run1.md exists)" | tee -a "$LOG"
    continue
  fi
  start=$(date +%s)
  echo "[$(date +%H:%M:%S)] START $page" | tee -a "$LOG"
  ( cd "$REC/$page" && "$CMD" -p "$(cat prompt.md)" --model gpt-5.6-sol --max-turns 3 --output-format text --skip-onboarding > gpt-run1.md 2> gpt-run1.err )
  ec=$?
  end=$(date +%s)
  sz=$(wc -c < "$OUT" 2>/dev/null || echo 0)
  echo "[$(date +%H:%M:%S)] DONE $page exit=$ec elapsed=$((end-start))s bytes=$sz" | tee -a "$LOG"
  sleep 2
done
echo "[$(date +%H:%M:%S)] ALL DONE" | tee -a "$LOG"
