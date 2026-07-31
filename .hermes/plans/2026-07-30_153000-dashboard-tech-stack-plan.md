# Dashboard — Complete Tech Stack & Architecture Plan

> **For Hermes:** This is a decision document + implementation plan. Read fully before starting.

**Goal:** Define the complete tech stack, architecture, and structure for the client dashboard with payment integration.

---

## 1. Authentication & User Management

### Options Comparison

| Solution | Free Tier | Features | Ease | Best For |
|----------|-----------|----------|------|----------|
| **Supabase Auth** | ✅ Unlimited users | Email/password, Google OAuth, Magic link, Row Level Security, Session management | ⭐⭐⭐ | All-in-one (DB + Auth + Storage) |
| **Clerk** | ✅ Up to 10K users | Email/password, Google, GitHub, prebuilt components, webhooks | ⭐⭐⭐⭐ | Best DX, prebuilt UI |
| **Custom JWT** | ✅ Free | Full control, no dependencies | ⭐⭐ | Simple, few users |
| **Cloudflare Access** | ✅ Free (up to 50 users) | Zero Trust, SSO, integrates with CF | ⭐⭐⭐ | If you use CF Zero Trust |

### ✅ Recommendation: **Supabase Auth**

**Why:**
- Free tier: **unlimited users** (Clerk caps at 10K)
- Built-in **Row Level Security** — users can only see their own orders
- Same service handles **database + auth + storage** (for report files)
- Email/password + Google OAuth out of the box
- Magic link login (no password needed — email only)
- Works perfectly with Cloudflare Workers via REST API
- No extra cost, no extra service to manage

---

## 2. Database

### Options Comparison

| Solution | Type | Free Tier | Query | Real-time |
|----------|------|-----------|-------|-----------|
| **Supabase (Postgres)** | SQL | 500MB, 5GB bandwidth | Full SQL, JS SDK | ✅ Built-in |
| **Cloudflare D1** | SQLite (beta) | 5GB storage, 5M reads/mo | SQL via Workers | ❌ Polling needed |
| **Cloudflare KV** | Key-value | 1GB storage | Key lookups only | ❌ |
| **MongoDB Atlas** | NoSQL | 512MB | MongoDB queries | ❌ |

### ✅ Recommendation: **Supabase (Postgres)**

**Why:**
- **Relational data** — orders, users, statuses, link plans all relate to each other. SQL is the right tool.
- **Row Level Security** — `user_id = auth.uid()` means users can ONLY see their own data. No backend code needed for basic queries.
- **Real-time subscriptions** — when admin updates order status, client sees it instantly without refreshing
- **500MB free** — more than enough for years of orders
- **Built-in auth** — same service, no integration needed
- **Storage** — can store report PDFs/CSVs too

---

## 3. Frontend Framework

### Options Comparison

| Framework | Bundle Size | Learning Curve | Build Step | Best For |
|-----------|------------|---------------|------------|----------|
| **Svelte** | ~3KB (compiled) | ⭐⭐⭐⭐ | ✅ Yes (Vite) | Lightest compiled framework |
| **Alpine.js** | ~10KB | ⭐⭐⭐⭐⭐ | ❌ No | Add interactivity to HTML |
| **HTMX** | ~14KB | ⭐⭐⭐⭐ | ❌ No | Server-rendered HTML |
| **React** | ~40KB + React | ⭐⭐ | ✅ Yes | Most popular, heavy |
| **Vue** | ~30KB | ⭐⭐⭐ | ✅ Yes | Middle ground |
| **Vanilla JS** | 0KB | ⭐⭐ | ❌ No | Full control, more code |

### ✅ Recommendation: **Svelte + Vite**

**Why:**
- **Lightest compiled framework** — Svelte compiles to vanilla JS at build time. No virtual DOM, no runtime overhead. Final bundle is tiny (~3-5KB for a dashboard).
- **Best DX** — reactive declarations, stores, transitions built in. Less code than React for the same thing.
- **Vite** — instant HMR, fast builds, easy to set up.
- **Cloudflare Pages** supports Svelte + Vite natively (adapter-static).
- **Dashboard is an SPA** — Svelte's component model is perfect for this.

**Alternative if you want NO build step:** Alpine.js + HTMX. But Svelte gives a much better UX for a dashboard with complex state (order status, real-time updates, multi-step forms).

---

## 4. Backend / API

### Options Comparison

| Solution | Runtime | Free Tier | Best For |
|----------|---------|-----------|----------|
| **Cloudflare Workers** | JavaScript/TS | 100k req/day | Edge, same ecosystem as main site |
| **Supabase Edge Functions** | Deno/JS | 500k invocations/mo | Integrated with Supabase |
| **Node.js (VPS)** | JavaScript | VPS cost | Full control, overkill |
| **Python (FastAPI)** | Python | VPS cost | If you prefer Python |

### ✅ Recommendation: **Cloudflare Workers**

**Why:**
- **Same ecosystem** as the main site (already on Cloudflare Pages)
- **Free tier** — 100k requests/day, more than enough
- **Edge deployment** — fast globally
- **JavaScript** — same language as frontend, share types/validation
- **Workers + D1 binding** — direct database access from edge
- **Cron triggers** — can schedule status check emails

---

## 5. Complete Stack Decision

| Layer | Choice | Why |
|-------|--------|-----|
| **Auth** | Supabase Auth | Free, unlimited users, RLS, magic link |
| **Database** | Supabase Postgres | Free 500MB, RLS, real-time, same service as auth |
| **Frontend** | Svelte + Vite | Lightest compiled framework, best DX for SPA |
| **Backend API** | Cloudflare Workers | Free, edge, same ecosystem, JS |
| **Payment** | 2Checkout (Verifone) | Available in Pakistan, wire transfer to PK banks |
| **Hosting** | Cloudflare Pages | Free, same as main site, Svelte adapter |
| **File Storage** | Supabase Storage | Free 1GB, store report PDFs |

---

## 6. Project Structure

```
backlinksservices.com/
│
├── index.html                          ← Main site (existing)
├── guest-post-services.html            ← Existing
├── niche-edits.html                    ← Existing
├── brand-mentions.html                 ← Existing
├── white-label-link-building.html      ← Existing
├── about.html                          ← Existing
├── contact.html                        ← Existing
├── robots.txt                          ← Existing
├── sitemap.xml                         ← Existing
│
├── blog/                               ← Static blog
│   ├── index.html
│   ├── guest-posting-vs-niche-edits.html
│   ├── choose-white-label-partner.html
│   ├── brand-mentions-vs-backlinks.html
│   └── cost-of-guest-post-services.html
│
├── dashboard/                          ← Svelte SPA (built output)
│   ├── index.html                      ← Login page
│   ├── orders.html                     ← Order list
│   ├── order-new.html                  ← New order form
│   ├── order-detail.html               ← Order + timeline
│   └── admin.html                      ← Admin panel
│
├── workers/                            ← Cloudflare Workers
│   └── dashboard-api/
│       ├── src/
│       │   ├── index.js                ← Main worker (router)
│       │   ├── auth.js                 ← JWT + Supabase auth helpers
│       │   ├── orders.js               ← Order CRUD
│       │   ├── checkout.js             ← 2Checkout integration
│       │   ├── webhook.js              ← 2Checkout webhook handler
│       │   ├── link-plans.js           ← Link plan management
│       │   └── admin.js                ← Admin endpoints
│       ├── schema.sql                  ← Database schema
│       ├── wrangler.toml               ← Worker config
│       └── package.json
│
├── dashboard-svelte/                   ← Svelte source (builds to /dashboard/)
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api.js                  ← API client (fetch to Worker)
│   │   │   ├── auth.js                 ← Auth store
│   │   │   ├── stores.js              ← Order stores
│   │   │   └── utils.js               ← Helpers
│   │   ├── routes/
│   │   │   ├── Login.svelte
│   │   │   ├── Orders.svelte
│   │   │   ├── OrderNew.svelte
│   │   │   ├── OrderDetail.svelte
│   │   │   └── Admin.svelte
│   │   ├── components/
│   │   │   ├── Nav.svelte
│   │   │   ├── StatusBadge.svelte
│   │   │   ├── Timeline.svelte
│   │   │   ├── OrderCard.svelte
│   │   │   ├── PricingSelector.svelte
│   │   │   └── PaymentModal.svelte
│   │   ├── App.svelte
│   │   └── main.js
│   ├── static/
│   │   └── favicon.png
│   ├── svelte.config.js
│   ├── vite.config.js
│   └── package.json
│
└── .hermes/plans/                      ← Plans (existing)
```

---

## 7. Data Flow Diagrams

### Client Places Order
```
Client → Dashboard Svelte App
  → Fills form (service, tier, URL, anchor)
  → Clicks "Place Order"
  → Svelte calls Worker API: POST /api/orders
  → Worker creates order in Supabase (status: pending_payment)
  → Worker calls 2Checkout API → gets checkout URL
  → Svelte opens 2Checkout inline checkout lightbox
  → Client pays with card/PayPal
  → 2Checkout sends webhook to Worker: POST /api/webhook/2checkout
  → Worker updates order status to: paid
  → Worker sends confirmation email
  → Svelte shows "In Progress" with timeline
```

### Client Requests Link Plan
```
Client → Dashboard Svelte App
  → Checks "I need a link plan" on new order form
  → Submits (no payment needed yet)
  → Worker creates order (status: awaiting_plan)
  → Admin sees order in admin panel
  → Admin creates link plan with specific URLs + anchors
  → Admin assigns plan to client
  → Worker updates order status to: pending_payment
  → Client sees plan details + "Pay Now" button
  → Same payment flow as above
```

### Admin Updates Status
```
Admin → Admin Panel
  → Clicks order → "Update Status"
  → Selects new status (outreach → writing → submitted → delivered)
  → Adds note: "Found DR 35 site in your niche, pitching now"
  → Worker creates order_statuses entry
  → Client sees new timeline entry in real-time (Supabase real-time subscription)
```

---

## 8. Database Schema (Supabase)

```sql
-- Users (managed by Supabase Auth, but we add profile data)
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  email TEXT,
  name TEXT,
  company TEXT,
  is_admin BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Users can read their own profile
CREATE POLICY "Users can read own profile"
  ON public.profiles FOR SELECT
  USING (auth.uid() = id);

-- Orders
CREATE TABLE public.orders (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  service TEXT NOT NULL CHECK (service IN ('guest-posts', 'niche-edits', 'brand-mentions')),
  tier TEXT NOT NULL CHECK (tier IN ('starter', 'growth', 'authority')),
  quantity INTEGER DEFAULT 1,
  total DECIMAL(10,2) NOT NULL,
  currency TEXT DEFAULT 'USD',
  status TEXT DEFAULT 'pending_payment'
    CHECK (status IN ('pending_payment', 'awaiting_plan', 'paid', 'outreach', 'writing', 'submission', 'delivered', 'cancelled')),
  target_url TEXT,
  anchor_text TEXT,
  notes TEXT,
  report_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

-- Users can read their own orders, admins can read all
CREATE POLICY "Users can read own orders"
  ON public.orders FOR SELECT
  USING (auth.uid() = user_id OR EXISTS (
    SELECT 1 FROM profiles WHERE id = auth.uid() AND is_admin = TRUE
  ));

-- Users can create orders (their own)
CREATE POLICY "Users can create orders"
  ON public.orders FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Order status timeline
CREATE TABLE public.order_statuses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  order_id UUID REFERENCES public.orders NOT NULL,
  status TEXT NOT NULL,
  note TEXT,
  created_by UUID REFERENCES auth.users,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.order_statuses ENABLE ROW LEVEL SECURITY;

-- Users can read statuses for their orders
CREATE POLICY "Users can read own order statuses"
  ON public.order_statuses FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM orders WHERE id = order_id AND user_id = auth.uid()
  ) OR EXISTS (
    SELECT 1 FROM profiles WHERE id = auth.uid() AND is_admin = TRUE
  ));

-- Link plans (admin creates for clients who request one)
CREATE TABLE public.link_plans (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  assigned_by UUID REFERENCES auth.users
);

ALTER TABLE public.link_plans ENABLE ROW LEVEL SECURITY;

-- Individual links within a plan
CREATE TABLE public.plan_links (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  plan_id UUID REFERENCES public.link_plans NOT NULL,
  target_url TEXT,
  anchor_text TEXT,
  status TEXT DEFAULT 'pending'
    CHECK (status IN ('pending', 'outreach', 'writing', 'submitted', 'delivered')),
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.plan_links ENABLE ROW LEVEL SECURITY;
```

---

## 9. Implementation Order

| Phase | Tasks | Dependencies | Time |
|-------|-------|-------------|------|
| **Phase 1** | Blog (static pages) | None | 1-2 hours |
| **Phase 2** | Set up Supabase project + schema | Supabase account | 30 min |
| **Phase 3** | Worker API (auth + orders + checkout) | Supabase + 2Checkout keys | 3-4 hours |
| **Phase 4** | Svelte dashboard (login + orders + new order) | Worker API | 4-5 hours |
| **Phase 5** | 2Checkout integration | 2Checkout approval + keys | 2 hours |
| **Phase 6** | Admin panel + link plan system | Worker API | 2-3 hours |
| **Phase 7** | Navigation updates + deploy | All above | 30 min |

---

## 10. What You Need to Do (Manual Steps)

1. **Sign up for Supabase** (supabase.com) — free, no credit card
2. **Sign up for 2Checkout** (verifone.com/en/signup) — complete KYC (3-7 days)
3. **Share Supabase project URL + anon key** with me
4. **Share 2Checkout seller ID + secret key** once approved

---

## 11. Key Decisions Summary

| Decision | Choice | Alternative |
|----------|--------|-------------|
| Auth | **Supabase Auth** | Clerk (10K cap) |
| Database | **Supabase Postgres** | Cloudflare D1 (beta) |
| Frontend | **Svelte + Vite** | Alpine.js (no build) |
| Backend | **Cloudflare Workers** | Supabase Edge Functions |
| Payment | **2Checkout (Verifone)** | PayPro (local) |
| Hosting | **Cloudflare Pages** | Vercel |
| File Storage | **Supabase Storage** | Cloudflare R2 |
