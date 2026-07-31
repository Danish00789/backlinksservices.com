# Blog & Client Dashboard Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a blog section and a client dashboard with order management and payment integration using 2Checkout (Verifone).

**Architecture:** Blog = static HTML. Dashboard = Cloudflare Workers API + D1 database + vanilla JS SPA frontend. Payment = 2Checkout inline checkout + webhook.

**Tech Stack:** Cloudflare Workers (API), Cloudflare D1 (SQL database), Cloudflare Pages (frontend hosting), 2Checkout/Verifone (payment gateway), Vanilla JS (no framework).

---

## Payment Gateway: 2Checkout (Verifone)

### Availability in Pakistan
- ✅ 2Checkout accepts merchants from Pakistan
- ✅ Payouts via wire transfer to Pakistani bank accounts
- ✅ Supports: Visa, Mastercard, American Express, Discover, PayPal, Diners Club
- ✅ Pricing: 2.5% + $0.30 per transaction (typical for their 2PayJS plan)
- ✅ No monthly fees on the 2PayJS plan
- ✅ 3D Secure included
- ✅ API: REST + inline checkout (no redirect to external page)

### Payouts to Pakistani Banks
2Checkout pays out via wire transfer. The supported payout methods for Pakistan:
- **Wire transfer** to any Pakistani bank account (HBL, UBL, MCB, Allied, Alfalah, etc.)
- Minimum payout: $50
- Payout frequency: Weekly, bi-weekly, or monthly (you choose)
- Currency: USD (converted to PKR by your bank at their rate)

### Bank List (Pakistan — all major banks supported via wire transfer)
- Habib Bank Limited (HBL)
- United Bank Limited (UBL)
- Muslim Commercial Bank (MCB)
- Allied Bank Limited (ABL)
- Bank Alfalah
- National Bank of Pakistan (NBP)
- Standard Chartered Pakistan
- Meezan Bank
- Bank Al Habib
- Faysal Bank
- JS Bank
- Askari Bank
- Soneri Bank
- Silkbank
- Summit Bank

### 2Checkout Integration Flow
```
1. Client fills order on dashboard
2. Frontend calls Worker API to create order
3. Worker creates 2Checkout checkout session via API
4. 2Checkout returns a checkout URL/token
5. Frontend opens 2Checkout inline checkout (lightbox, no redirect)
6. Client pays
7. 2Checkout sends webhook to Worker (payment confirmed)
8. Worker updates order status to "paid"
9. Worker sends confirmation
```

---

## Dashboard Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Cloudflare Pages                        │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              Dashboard SPA (Vanilla JS)                │ │
│  │                                                        │ │
│  │  /dashboard/          → Login page                     │ │
│  │  /dashboard/orders    → Order list + status            │ │
│  │  /dashboard/order-new → Place new order                │ │
│  │  /dashboard/order/:id → Order detail + timeline        │ │
│  │  /dashboard/admin     → Admin panel (manage orders)    │ │
│  └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────┐
│              Cloudflare Workers (API Layer)               │
│                                                        │
│  POST   /api/auth/register      → Create account        │
│  POST   /api/auth/login         → Login → JWT           │
│  GET    /api/orders             → List user's orders     │
│  POST   /api/orders             → Create new order       │
│  GET    /api/orders/:id         → Order detail           │
│  PATCH  /api/orders/:id/status  → Update status (admin)  │
│  POST   /api/orders/:id/note   → Add note (admin)       │
│  POST   /api/checkout           → Create 2CO session     │
│  POST   /api/webhook/2checkout  → Payment confirmation   │
│  GET    /api/link-plans         → Get available plans    │
│  POST   /api/link-plans         → Assign plan to user    │
└──────────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────┐
│              Cloudflare D1 (SQL Database)                 │
│                                                        │
│  users:    id, email, name, company, password_hash,      │
│            created_at, is_admin                          │
│                                                        │
│  orders:   id, user_id, service, tier, quantity,         │
│            total, currency, status, target_url,          │
│            anchor_text, created_at, completed_at          │
│                                                        │
│  order_statuses: id, order_id, status, note,             │
│                  created_at (timeline entries)           │
│                                                        │
│  link_plans: id, user_id, title, description,           │
│              created_at, assigned_by                     │
│                                                        │
│  plan_links: id, plan_id, target_url, anchor_text,       │
│              status (pending/outreach/writing/submitted/  │
│              delivered), notes, created_at               │
└──────────────────────────────────────────────────────────┘
```

---

## Order Status Flow

```
PENDING_PAYMENT → PAID → IN_PROGRESS → COMPLETED
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
              OUTREACH    WRITING   SUBMISSION
                                         │
                                         ▼
                                     DELIVERED
```

Each status change creates a timeline entry visible to the client on the order detail page.

---

## Step-by-Step Plan

### Task 1: Create Blog (4 pages)

**Objective:** Static blog with listing page and 4 initial posts.

**Files:**
- Create: `blog/index.html`
- Create: `blog/guest-posting-vs-niche-edits.html`
- Create: `blog/choose-white-label-link-building-partner.html`
- Create: `blog/brand-mentions-vs-backlinks.html`
- Create: `blog/cost-of-guest-post-services.html`

**Details:**
- Same nav/footer as main site
- Blog listing: grid of post cards with title, excerpt, date, read time
- Each post: article content, author, date, related services CTA at bottom
- Internal links to service pages

### Task 2: Set Up Cloudflare D1 Database

**Objective:** Create the database schema for users, orders, statuses, link plans.

**Files:**
- Create: `workers/dashboard-api/schema.sql`
- Create: `workers/dashboard-api/wrangler.toml`

**SQL Schema:**
```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  company TEXT,
  password_hash TEXT NOT NULL,
  is_admin INTEGER DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE orders (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  service TEXT NOT NULL,
  tier TEXT NOT NULL,
  quantity INTEGER DEFAULT 1,
  total REAL NOT NULL,
  currency TEXT DEFAULT 'USD',
  status TEXT DEFAULT 'pending_payment',
  target_url TEXT,
  anchor_text TEXT,
  notes TEXT,
  report_url TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  completed_at TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_statuses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id TEXT NOT NULL,
  status TEXT NOT NULL,
  note TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE link_plans (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  assigned_by TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE plan_links (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plan_id TEXT NOT NULL,
  target_url TEXT,
  anchor_text TEXT,
  status TEXT DEFAULT 'pending',
  notes TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (plan_id) REFERENCES link_plans(id)
);
```

### Task 3: Create Worker API

**Objective:** Build the backend API with all endpoints.

**Files:**
- Create: `workers/dashboard-api/index.js`
- Create: `workers/dashboard-api/package.json`

**Endpoints:**
- Auth: register, login (JWT-based)
- Orders: CRUD + status updates
- Checkout: create 2Checkout session
- Webhook: handle 2Checkout payment confirmation
- Link plans: CRUD for admin-assigned plans

### Task 4: Create Dashboard Frontend

**Objective:** Build the client dashboard SPA.

**Files:**
- Create: `dashboard/index.html` — Login page
- Create: `dashboard/orders.html` — Order list with status cards
- Create: `dashboard/order-new.html` — Place order form
- Create: `dashboard/order-detail.html` — Order detail with timeline
- Create: `dashboard/admin.html` — Admin panel
- Create: `dashboard/css/style.css` — Shared styles
- Create: `dashboard/js/app.js` — Shared JS (auth, API calls, router)

**Dashboard Pages:**

**Login Page (`/dashboard/`):**
- Email + password form
- "Register" link for new clients
- Clean, minimal design matching main site

**Order List (`/dashboard/orders`):**
- Cards showing each order with status badge
- Color-coded statuses (amber=pending, blue=paid, green=delivered)
- Click to view detail
- "Place New Order" button

**New Order (`/dashboard/order-new`):**
- Step 1: Select service (Guest Posts / Niche Edits / Brand Mentions)
- Step 2: Select tier (Starter / Growth / Authority)
- Step 3: Enter target URL + anchor text (or check "I need a link plan")
- Step 4: Review + Pay (opens 2Checkout inline checkout)
- OR: "Request a custom link plan" → admin gets notified, creates plan

**Order Detail (`/dashboard/order/:id`):**
- Order info (service, tier, quantity, total)
- Status timeline (vertical timeline with dots + dates)
- Each link in the plan shown with its own status
- Download report button (when delivered)

**Admin Panel (`/dashboard/admin`):**
- List all orders (all users)
- Update order status with notes
- Create link plans for users
- Assign links to plans with target URL + anchor text
- Update individual link status

### Task 5: Integrate 2Checkout Payment

**Objective:** Connect the dashboard to 2Checkout for payment processing.

**Files:**
- Modify: `workers/dashboard-api/index.js` — add 2Checkout API calls
- Modify: `dashboard/order-new.html` — add 2Checkout inline checkout

**2Checkout Integration Details:**
```javascript
// Worker: Create 2Checkout checkout session
const 2checkout = require('2checkout-node')({
  sellerId: process.env.TWOCHECKOUT_SELLER_ID,
  secretKey: process.env.TWOCHECKOUT_SECRET_KEY,
  sandbox: true // false in production
});

// Frontend: Open inline checkout
// 2Checkout provides a JS library that opens a lightbox
// Client enters card details, pays
// On success, 2Checkout calls webhook
```

### Task 6: Update Main Site Navigation

**Objective:** Link blog and dashboard from main site.

**Files:**
- Modify: `index.html` — footer "Blog" → `/blog/`
- Modify: All 6 other HTML files — footer "Blog" → `/blog/`
- Modify: `index.html` — add "Dashboard" link in nav (for logged-in users, future)

---

## Files That Will Change

| File | Change |
|------|--------|
| `index.html` | Footer "Blog" → `/blog/` |
| `guest-post-services.html` | Footer "Blog" → `/blog/` |
| `niche-edits.html` | Footer "Blog" → `/blog/` |
| `brand-mentions.html` | Footer "Blog" → `/blog/` |
| `white-label-link-building.html` | Footer "Blog" → `/blog/` |
| `about.html` | Footer "Blog" → `/blog/` |
| `contact.html` | Footer "Blog" → `/blog/` |

## Files That Will Be Created

| File | Purpose |
|------|---------|
| `blog/index.html` | Blog listing |
| `blog/post-1.html` through `blog/post-4.html` | Individual posts |
| `workers/dashboard-api/schema.sql` | Database schema |
| `workers/dashboard-api/wrangler.toml` | Worker config |
| `workers/dashboard-api/index.js` | Backend API |
| `workers/dashboard-api/package.json` | Dependencies |
| `dashboard/index.html` | Login page |
| `dashboard/orders.html` | Order list |
| `dashboard/order-new.html` | New order form |
| `dashboard/order-detail.html` | Order detail + timeline |
| `dashboard/admin.html` | Admin panel |
| `dashboard/css/style.css` | Dashboard styles |
| `dashboard/js/app.js` | Dashboard JS |

## Risks & Open Questions

1. **2Checkout merchant approval:** You need to apply and get approved. This can take 3-7 business days. They'll ask for business documents.
2. **2Checkout API keys:** Need seller ID + secret key from the 2Checkout dashboard after approval.
3. **D1 vs KV:** D1 is recommended for relational data. It's in beta but stable enough for this use case.
4. **Auth security:** Simple bcrypt + JWT. Not enterprise-grade but fine for a B2B dashboard with few users.
5. **Blog content:** The 4 posts need to be written. Can use Claude/MiniMax for content generation.
6. **2Checkout inline checkout:** Requires loading their JS library. Works as a lightbox overlay — client never leaves your site.

## What You Need to Do (Manual Steps)

1. **Sign up for 2Checkout** at verifone.com/en/signup — select "2Checkout" plan
2. **Complete KYC** — provide business documents
3. **Get API credentials** — seller ID + secret key from dashboard
4. **Set payout method** — add your Pakistani bank account for wire transfers
5. **Share the API keys** with me once approved

## Implementation Order

1. Blog (static, can start immediately)
2. D1 database setup
3. Worker API (auth + orders)
4. Dashboard frontend (login + order list + new order)
5. 2Checkout integration
6. Admin panel
7. Link plan system
8. Navigation updates
