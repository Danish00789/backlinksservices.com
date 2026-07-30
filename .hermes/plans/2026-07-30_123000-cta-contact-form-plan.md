# CTA & Contact Form Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Audit all CTAs across the website, decide which need real destinations vs. which stay as scroll anchors, and implement a working contact form submission system.

**Architecture:** Two-phase approach — (1) CTA audit and consolidation, (2) Contact form backend integration.

**Tech Stack:** Vanilla HTML/CSS/JS (no frameworks). Contact form via Formspree (free tier) or Cloudflare Workers (if user has Workers available).

---

## Phase 1: CTA Audit

### Current CTA Inventory

**Total CTAs found: 42** across 7 pages. Grouped by type:

#### A. Hero CTAs (7 total — 1 per page)
| Page | Primary CTA | Secondary CTA | Current Target |
|------|------------|---------------|----------------|
| index.html | "Get Your Free Link Plan" | "See Sample Links" | `#final-cta` / `#services` |
| guest-post-services.html | "Order Guest Posts" | "Get a Custom Quote" | `#pricing` / `#final-cta` |
| niche-edits.html | "Order Niche Edits" | "Get a Custom Quote" | `#pricing` / `#final-cta` |
| brand-mentions.html | "Order Brand Mentions" | "Get a Custom Quote" | `#pricing` / `#final-cta` |
| white-label-link-building.html | "Get Agency Pricing" | "Book a Partnership Call" | `#pricing` / `#final-cta` |
| about.html | (none in hero) | — | — |
| contact.html | (none in hero) | — | — |

#### B. Pricing Card CTAs (15 total)
- **guest-post-services.html:** 3 "Order Starter/Growth/Authority" → `#final-cta`
- **niche-edits.html:** 3 "Order Foundation/Growth/Premium" → `#final-cta`
- **brand-mentions.html:** 3 "Order Starter/Growth/Authority" → `#final-cta`
- **white-label-link-building.html:** 9 "Get Started" (3 tabs × 3 tiers) → `#final-cta`

#### C. Final CTA Section CTAs (7 total — 1 per page)
| Page | Button Text | Current Target |
|------|------------|---------------|
| index.html | "Get Your Free Link Plan" | `#` (dead) |
| guest-post-services.html | "Order Guest Posts Now" | `#` (dead) |
| niche-edits.html | "Order Niche Edits Now" | `#` (dead) |
| brand-mentions.html | "Order Brand Mentions" | `#` (dead) |
| white-label-link-building.html | "Get Agency Pricing" | `#` (dead) |
| about.html | "Get in Touch" | `contact.html` ✅ |
| contact.html | (none — form submit instead) | — |

#### D. Cross-Sell / White-Label CTAs (4 total)
- **guest-post-services.html:** "Learn About Our Agency Program →" → `white-label-link-building.html` ✅
- **niche-edits.html:** "Get Agency Pricing →" → `white-label-link-building.html` ✅
- **brand-mentions.html:** (removed — was agency offer card)
- **index.html:** "Learn About Our Agency Program →" → `/white-label-link-building/` ✅

#### E. Nav CTAs (7 total — 1 per page)
- All pages: "Get Started" in nav → `#final-cta` (scrolls to final CTA section)

#### F. Mobile Sticky CTAs (7 total — 1 per page)
| Page | Text | Current Target |
|------|------|---------------|
| index.html | "Get Started — From $70/Link" | `#final-cta` |
| guest-post-services.html | "Order Guest Posts — From $70/Link" | `#final-cta` |
| niche-edits.html | "Order Niche Edits — From $60/Link" | `#final-cta` |
| brand-mentions.html | "Order Brand Mentions — From $60/Mention" | `#final-cta` |
| white-label-link-building.html | "Get Agency Pricing — From $50/Link" | `#final-cta` |
| about.html | "Get in Touch" | `contact.html` ✅ |
| contact.html | "Email Us" | `mailto:hello@backlinksservices.com` ✅ |

#### G. Service Card "Learn More" Links (6 total)
- **index.html:** 3 cards (GP/NE/BM) → respective service pages ✅
- **guest-post-services.html:** 2 cross-sell links → respective service pages ✅
- **niche-edits.html:** 2 cross-sell links → respective service pages ✅
- **brand-mentions.html:** 2 cross-sell links → respective service pages ✅

### CTA Decision Matrix

| CTA Group | Count | Current State | Recommended Action |
|-----------|-------|--------------|-------------------|
| **Hero primary** | 5 | Scrolls to pricing or final-cta | **Keep as scroll anchors** — user sees pricing then scrolls to CTA |
| **Hero secondary** | 5 | Scrolls to final-cta | **Keep as scroll anchors** |
| **Pricing card "Order"** | 15 | All → `#final-cta` | **Keep as scroll anchors** — user picks tier, scrolls to CTA |
| **Final CTA buttons** | 5 | `#` (dead) | **Fix** — point to `contact.html` or implement checkout |
| **Cross-sell to WL** | 3 | Point to WL page ✅ | **Keep** |
| **Nav "Get Started"** | 7 | → `#final-cta` | **Keep as scroll anchor** |
| **Mobile sticky** | 7 | Mixed (5 → `#final-cta`, 2 → correct pages) | **Fix** — point to `contact.html` for service pages |
| **Service card links** | 6 | Point to correct pages ✅ | **Keep** |

### Key Decisions Needed

1. **Final CTA buttons** — currently all `#` (dead). Options:
   - **Option A:** Point to `contact.html` (simple, works now)
   - **Option B:** Build a checkout/order flow (complex, future)
   - **Option C:** Point to `mailto:hello@backlinksservices.com` (works but no tracking)

2. **Mobile sticky CTAs** — currently scroll to `#final-cta`. Should they go to `contact.html` instead?

3. **Pricing card "Order" buttons** — currently scroll to `#final-cta`. Should they go to `contact.html` with a pre-filled subject?

---

## Phase 2: Contact Form Backend

### Current State
- Contact form at `contact.html` uses `action="mailto:hello@backlinksservices.com"` with `enctype="text/plain"`
- **Problem:** `mailto:` forms don't work reliably in most browsers. They open the user's email client with pre-filled fields but the user must send manually. No server-side capture.

### Options for Form Submission

| Option | Cost | Setup Time | Pros | Cons |
|--------|------|-----------|------|------|
| **Formspree** | Free (50 submissions/mo) | 10 min | Zero backend, just a form action URL | 50/mo limit on free tier |
| **Cloudflare Workers** | Free (100k req/day) | 30 min | Full control, same stack, can forward to email | Need to write + deploy a Worker |
| **Web3Forms** | Free (250/mo) | 10 min | Simple API, email forwarding | Third-party dependency |
| **Getform** | Free (50/mo) | 10 min | Similar to Formspree | Same limits |

### Recommended: Formspree (Phase 2a) → Cloudflare Worker (Phase 2b)

**Phase 2a — Quick win (10 min):**
1. Sign up at formspree.io
2. Create a form → get endpoint URL
3. Update `contact.html` form action
4. Form submissions arrive via email

**Phase 2b — Proper solution (30 min):**
1. Write a Cloudflare Worker that:
   - Accepts POST from contact form
   - Validates fields
   - Sends email via SendGrid/Mailgun or Cloudflare Email Routing
   - Returns success/error response
2. Deploy Worker
3. Update form action to Worker URL

---

## Step-by-Step Plan

### Task 1: Fix Final CTA Buttons (5 pages)

**Objective:** Point all dead `#` final CTA buttons to `contact.html`

**Files to modify:**
- `index.html` — "Get Your Free Link Plan" → `contact.html`
- `guest-post-services.html` — "Order Guest Posts Now" → `contact.html`
- `niche-edits.html` — "Order Niche Edits Now" → `contact.html`
- `brand-mentions.html` — "Order Brand Mentions" → `contact.html`
- `white-label-link-building.html` — "Get Agency Pricing" → `contact.html`

**Verification:** Open each page, scroll to final CTA, click button → navigates to contact.html

### Task 2: Fix Mobile Sticky CTAs (3 pages)

**Objective:** Point service page mobile sticky CTAs to `contact.html` instead of `#final-cta`

**Files to modify:**
- `guest-post-services.html` — "Order Guest Posts — From $70/Link" → `contact.html`
- `niche-edits.html` — "Order Niche Edits — From $60/Link" → `contact.html`
- `brand-mentions.html` — "Order Brand Mentions — From $60/Mention" → `contact.html`

**Verification:** Open each page on mobile width, scroll down, tap sticky CTA → navigates to contact.html

### Task 3: Set Up Formspree (or alternative)

**Objective:** Get a working form endpoint that captures submissions

**Steps:**
1. Go to formspree.io → sign up (or use existing account)
2. Create new form → get endpoint URL (e.g., `https://formspree.io/f/xyz123`)
3. Update `contact.html` form action to the Formspree URL
4. Add `method="POST"` to form tag
5. Test by submitting the form

**Verification:** Submit test entry → receive email notification

### Task 4: Add Form Success/Error Handling

**Objective:** Show user feedback after form submission

**Files to modify:**
- `contact.html` — add JS to handle form submit event, show success message or error

**Steps:**
1. Add `onsubmit` handler that prevents default, submits via fetch to Formspree
2. On success: show "Thanks! We'll get back to you within 24 hours." message
3. On error: show "Something went wrong. Please email us directly at hello@backlinksservices.com"
4. Hide form on success

**Verification:** Submit form → see success message. Disconnect network → see error message.

### Task 5 (Optional): Cloudflare Worker for Form Backend

**Objective:** Replace Formspree with self-hosted solution

**Files to create:**
- `workers/contact-form/index.js` — Worker script
- `wrangler.toml` — Worker config

**Steps:**
1. Write Worker that accepts POST, validates, sends email
2. Deploy with `npx wrangler deploy`
3. Update form action in `contact.html`

---

## Files That Will Change

| File | Change |
|------|--------|
| `index.html` | Final CTA href → `contact.html` |
| `guest-post-services.html` | Final CTA href → `contact.html`; Mobile sticky href → `contact.html` |
| `niche-edits.html` | Final CTA href → `contact.html`; Mobile sticky href → `contact.html` |
| `brand-mentions.html` | Final CTA href → `contact.html`; Mobile sticky href → `contact.html` |
| `white-label-link-building.html` | Final CTA href → `contact.html` |
| `contact.html` | Form action → Formspree URL; Add JS for success/error handling |

## Risks & Open Questions

1. **Formspree free tier:** 50 submissions/month. If traffic is low, this is fine. If not, need to upgrade ($10/mo) or build Worker.
2. **Spam protection:** Formspree includes CAPTCHA. If using Worker, need to add Turnstile (Cloudflare's free CAPTCHA alternative).
3. **Pricing card "Order" buttons:** Currently all scroll to `#final-cta`. Should they instead go to `contact.html` with a query param like `?service=guest-posts&tier=starter` so the contact form pre-fills? This would require JS on contact.html to read URL params.
4. **Checkout flow:** If you eventually want a real checkout (not just contact form), that's a separate project. The current plan assumes contact form is sufficient for now.
