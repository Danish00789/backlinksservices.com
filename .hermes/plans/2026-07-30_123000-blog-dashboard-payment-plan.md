# Blog & Dashboard + Payment Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a blog section and a client dashboard with payment integration for BacklinksServices.com, using a payment gateway available in Pakistan.

**Architecture:** Two-phase approach — (1) Blog as static HTML pages, (2) Dashboard as a separate app with payment integration.

**Tech Stack:** Blog = static HTML (same as site). Dashboard = Cloudflare Workers + KV (for data) + a payment gateway API.

---

## Phase 1: Blog

### Current State
- Footer has "Blog" link pointing to `#` (dead)
- No blog pages exist

### Approach
Keep it simple — static HTML pages, same design system as the rest of the site. No CMS, no database.

### Blog Structure
```
backlinksservices.com/blog/
├── index.html              ← Blog listing page
├── post-1-slug.html        ← Individual posts
├── post-2-slug.html
└── ...
```

### Blog Listing Page
- Same nav/footer as main site
- Grid of blog post cards (title, excerpt, date, read time)
- Pagination (simple "Older Posts" / "Newer Posts" links)
- Each card links to individual post page

### Individual Post Page
- Same nav/footer
- Article content with formatting
- Author byline, date, estimated read time
- Related services CTA at bottom (e.g. "Need backlinks? Check our Guest Post services")
- Internal links to service pages

### Initial Posts (Suggested)
1. "Guest Posting vs Niche Edits: Which Link Building Strategy Is Right for You?"
2. "How to Choose a White-Label Link Building Partner for Your Agency"
3. "Brand Mentions vs Backlinks: Why You Need Both for SEO in 2026"
4. "The Cost of Guest Post Services: What You're Really Paying For"

---

## Phase 2: Dashboard + Payment

### Payment Gateway Research for Pakistan

| Gateway | Available in Pakistan | API Integration | Notes |
|---------|---------------------|-----------------|-------|
| **Stripe** | ❌ No | — | Not available for Pakistan accounts |
| **Payoneer Checkout** | ✅ Yes | REST API | You have Payoneer account. Payoneer Checkout API allows payment collection via credit card. However, it's primarily a mass payout platform — their checkout product is limited. |
| **2Checkout (Verifone)** | ✅ Yes | REST API + SDK | Full payment gateway. Accepts credit cards, PayPal. 2.5% + $0.30 per transaction. Payouts to Pakistan via wire transfer. |
| **PayPro** | ✅ Yes (Pakistan-based) | REST API | Local Pakistani payment gateway. Supports credit/debit cards, JazzCash, EasyPaisa. Lower fees (~2%). Payouts to local bank account. |
| **JazzCash API** | ✅ Yes | REST API | Mobile wallet payments. Good for local clients. Lower ticket sizes. |
| **Coinbase Commerce** | ✅ Yes (anywhere) | REST API | Crypto payments (USDC, BTC, ETH). No country restrictions. Volatile but no chargebacks. |
| **Paddle** | ❌ No | — | Not available for Pakistan |
| **LemonSqueezy** | ❌ No | — | Not available for Pakistan |

### Recommended: PayPro (Primary) + Coinbase Commerce (Backup)

**PayPro** is the best option because:
- Pakistan-based — no cross-border issues
- Supports credit/debit cards + local wallets (JazzCash, EasyPaisa)
- Lower fees (~2%)
- Payouts to local bank account
- REST API for integration
- No monthly fees

**Coinbase Commerce** as backup for international clients who prefer crypto.

### Dashboard Architecture

```
┌─────────────────────────────────────────────────┐
│                  Cloudflare Pages                 │
│  ┌─────────────────────────────────────────────┐ │
│  │           Dashboard SPA (Vanilla JS)         │ │
│  │  - Login (email + magic link or password)    │ │
│  │  - Order history                             │ │
│  │  - Active orders / status tracking           │ │
│  │  - Place new order (service selection)       │ │
│  │  - Payment (redirect to PayPro checkout)     │ │
│  │  - Download reports                          │ │
│  └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│              Cloudflare Workers (API)            │
│  - Auth (JWT tokens)                            │
│  - Order CRUD                                   │
│  - Payment webhook handler                       │
│  - Report generation                             │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│              Cloudflare KV / D1                  │
│  - Users table                                  │
│  - Orders table                                 │
│  - Payments table                               │
└─────────────────────────────────────────────────┘
```

### Dashboard Features (MVP)

| Feature | Description |
|---------|-------------|
| **Client Login** | Email + password or magic link. Simple auth via Cloudflare Workers |
| **Place Order** | Select service (GP/NE/BM), tier (Starter/Growth/Authority), quantity |
| **Checkout** | Redirect to PayPro payment page. Webhook confirms payment |
| **Order Status** | Show: Pending → In Progress → Completed. Manual status updates by admin |
| **Order History** | List of all past orders with status, date, amount |
| **Report Download** | After completion, client can download placement report (CSV/PDF) |
| **Admin Panel** | Simple admin view to update order status, add notes, upload reports |

### Payment Flow

```
1. Client selects service + tier on dashboard
2. Client clicks "Place Order"
3. Backend creates order (status: pending_payment)
4. Backend creates PayPro checkout session
5. Client redirected to PayPro hosted payment page
6. Client pays via card/JazzCash/EasyPaisa
7. PayPro sends webhook to Cloudflare Worker
8. Worker updates order status to: paid
9. Worker sends confirmation email to client
10. Client sees "In Progress" on dashboard
```

### Data Model (KV or D1)

**Users:**
```json
{
  "id": "uuid",
  "email": "client@example.com",
  "name": "Client Name",
  "company": "Agency Name",
  "created_at": "2026-07-30T00:00:00Z"
}
```

**Orders:**
```json
{
  "id": "ORD-20260730-001",
  "user_id": "uuid",
  "service": "guest-posts",
  "tier": "growth",
  "quantity": 5,
  "total": 475,
  "currency": "USD",
  "status": "paid",
  "target_url": "https://client-site.com/page",
  "anchor_text": "best seo tool",
  "created_at": "2026-07-30T00:00:00Z",
  "completed_at": null,
  "report_url": null
}
```

---

## Step-by-Step Plan

### Task 1: Create Blog Listing Page

**Objective:** Create `/blog/index.html` with same nav/footer as main site, listing 4 initial blog posts as cards.

**Files:**
- Create: `blog/index.html`

**Details:**
- Same design system (colors, fonts, nav, footer)
- Grid of blog post cards with title, excerpt, date, read time
- Each card links to `/blog/post-1-slug.html` etc.
- Footer "Blog" link on main site now points to `/blog/`

### Task 2: Create 4 Blog Post Pages

**Objective:** Create individual blog post pages with full article content.

**Files:**
- Create: `blog/guest-posting-vs-niche-edits.html`
- Create: `blog/choose-white-label-link-building-partner.html`
- Create: `blog/brand-mentions-vs-backlinks.html`
- Create: `blog/cost-of-guest-post-services.html`

**Details:**
- Same nav/footer
- Article content with headings, paragraphs
- Author byline, date, read time
- Related services CTA at bottom
- Internal links to service pages

### Task 3: Set Up PayPro Account

**Objective:** Sign up for PayPro and get API credentials.

**Steps:**
1. Go to paypro.com.pk → sign up
2. Complete KYC/verification
3. Get API key and secret
4. Set up webhook endpoint URL
5. Note: This requires manual action by user

### Task 4: Create Cloudflare Worker API

**Objective:** Build the backend API for the dashboard.

**Files:**
- Create: `workers/dashboard-api/index.js`
- Create: `workers/dashboard-api/wrangler.toml`

**Endpoints:**
- `POST /api/auth/login` — email + password → JWT
- `POST /api/auth/register` — create client account
- `GET /api/orders` — list user's orders
- `POST /api/orders` — create new order
- `GET /api/orders/:id` — get order details
- `POST /api/payments/create-checkout` — create PayPro checkout session
- `POST /api/payments/webhook` — PayPro payment confirmation webhook

### Task 5: Create Dashboard Frontend

**Objective:** Build the client dashboard SPA.

**Files:**
- Create: `dashboard/index.html` — login page
- Create: `dashboard/orders.html` — order list
- Create: `dashboard/order-new.html` — place new order
- Create: `dashboard/order-detail.html` — order detail + status

**Details:**
- Same design system as main site
- Vanilla JS SPA (no framework)
- JWT stored in localStorage
- Fetch API calls to Worker endpoints
- Responsive

### Task 6: Integrate PayPro Checkout

**Objective:** Connect the dashboard to PayPro for payment processing.

**Files:**
- Modify: `workers/dashboard-api/index.js` — add PayPro API calls
- Modify: `dashboard/order-new.html` — redirect to PayPro checkout

**Details:**
- When client clicks "Pay", backend creates PayPro checkout session
- Client redirected to PayPro hosted payment page
- On success, PayPro redirects back to dashboard
- Webhook confirms payment and updates order status

### Task 7: Add Admin Panel

**Objective:** Simple admin view to manage orders.

**Files:**
- Create: `dashboard/admin.html`

**Features:**
- List all orders (not just user's)
- Update order status (Pending → In Progress → Completed)
- Add notes
- Upload report files
- Simple password protection (or same auth with admin flag)

### Task 8: Update Footer + Navigation

**Objective:** Link blog and dashboard from main site.

**Files:**
- Modify: `index.html` — footer "Blog" → `/blog/`
- Modify: All service pages — add "Blog" to footer
- Modify: `index.html` — add "Dashboard" link for logged-in users (future)

---

## Files That Will Change

| File | Change |
|------|--------|
| `index.html` | Footer "Blog" link → `/blog/` |
| `guest-post-services.html` | Footer "Blog" link → `/blog/` |
| `niche-edits.html` | Footer "Blog" link → `/blog/` |
| `brand-mentions.html` | Footer "Blog" link → `/blog/` |
| `white-label-link-building.html` | Footer "Blog" link → `/blog/` |
| `about.html` | Footer "Blog" link → `/blog/` |
| `contact.html` | Footer "Blog" link → `/blog/` |

## Files That Will Be Created

| File | Purpose |
|------|---------|
| `blog/index.html` | Blog listing |
| `blog/post-1.html` through `blog/post-4.html` | Individual posts |
| `workers/dashboard-api/index.js` | Backend API |
| `workers/dashboard-api/wrangler.toml` | Worker config |
| `dashboard/index.html` | Login page |
| `dashboard/orders.html` | Order list |
| `dashboard/order-new.html` | New order form |
| `dashboard/order-detail.html` | Order detail |
| `dashboard/admin.html` | Admin panel |

## Risks & Open Questions

1. **PayPro availability:** Need to confirm PayPro is still active and accepting new merchants. If not, fallback to 2Checkout (Verifone).
2. **Payoneer Checkout:** Payoneer does have a checkout API but it's designed for marketplace scenarios, not direct e-commerce. It may require a Payoneer account on the buyer side too. Need to investigate further.
3. **Cloudflare D1 vs KV:** D1 (SQL database) is better for relational data (orders, users). KV is simpler but harder to query. Recommend D1 for the dashboard.
4. **Auth complexity:** Simple email+password auth is fine for MVP but not production-grade. For now, it's acceptable since this is a B2B service with few clients.
5. **Blog content:** The 4 initial posts need to be written. Can use Claude/MiniMax for content generation.
6. **Dashboard URL:** Should it be `dashboard.backlinksservices.com` (subdomain) or `backlinksservices.com/dashboard/` (subdirectory)? Subdirectory is simpler with Cloudflare Pages.

## Decision Needed

**Which payment gateway should I research further first?**
- **PayPro** (Pakistan-based, cards + local wallets, ~2% fees)
- **2Checkout/Verifone** (International, cards + PayPal, 2.5% + $0.30)
- **Payoneer Checkout** (You already have an account, but may be limited)
