#!/usr/bin/env bash
# Per-page service-page audit: structural + content checks vs the Claude standard.
# Runs from the _loop dir; uses ONLY relative paths (native python mangles MSYS /c/... args).
set -u
cd "/c/Users/HT/Desktop/Coding Projects/LinkBuilding Agency/service-page-training-record/_loop"
python3 audit.py \
  ../link-building-for-saas/copy.md            ../link-building-for-saas/gpt-run1.md \
  ../link-building-for-small-businesses/copy.md ../link-building-for-small-businesses/gpt-run1.md \
  ../link-building-for-ecommerce/copy.md        ../link-building-for-ecommerce/gpt-run1.md \
  ../link-building-for-local-seo/copy.md        ../link-building-for-local-seo/gpt-run1.md \
  ../link-building-for-b2b/copy.md              ../link-building-for-b2b/gpt-run1.md \
  ../link-building-for-contractors/copy.md      ../link-building-for-contractors/gpt-run1.md \
  ../link-building-for-law-firms/copy.md        ../link-building-for-law-firms/gpt-run1.md \
  ../backlink-audit/copy.md                     ../backlink-audit/gpt-run1.md \
  ../managed-link-building/copy.md              ../managed-link-building/gpt-run1.md \
  ../link-building-consultant/copy.md           ../link-building-consultant/gpt-run1.md \
  > audit-all.txt 2>&1
echo "wrote audit-all.txt ($(wc -l < audit-all.txt) lines)"
