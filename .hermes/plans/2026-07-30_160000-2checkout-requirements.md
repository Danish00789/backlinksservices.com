# 2Checkout (Verifone) — Requirements & Integration Guide

> **For Hermes:** Reference document for setting up 2Checkout as the payment gateway.

---

## 1. Is 2Checkout Good for International Clients?

**Yes, absolutely.** In fact, 2Checkout is **better for international clients** than local Pakistani gateways because:

| Feature | 2Checkout | PayPro (local) |
|---------|-----------|----------------|
| **Client sees** | USD pricing, familiar checkout | PKR pricing, local payment methods |
| **Payment methods** | Visa, MC, Amex, Discover, PayPal, Diners | Cards + JazzCash/EasyPaisa |
| **Currency** | USD (what you price in) | PKR |
| **Client location** | Any country | Mostly Pakistan |
| **Merchant of Record** | ✅ 2Checkout handles tax/VAT compliance | ❌ You handle it |
| **Chargeback protection** | ✅ Built-in | Basic |

**Key advantage:** 2Checkout is a **Merchant of Record (MoR)**. This means:
- They handle **sales tax / VAT compliance** for every country
- They handle **chargebacks** and disputes
- They handle **global regulations** (GDPR, PSD2, 3D Secure)
- You just get paid — they take the regulatory risk

---

## 2. Requirements for Account Creation

### What 2Checkout Needs From You

| Requirement | Details |
|-------------|---------|
| **Business type** | Registered company (sole proprietor OK in some cases) |
| **Business documents** | Company registration certificate, tax ID / NTN |
| **Owner/partner ID** | CNIC or passport copy |
| **Bank account** | Any Pakistani bank account for wire transfer payouts |
| **Website URL** | `https://backlinksservices.com` (must be live) |
| **Product description** | What you sell (link building services, guest posts) |
| **Pricing** | Your price list ($70-$135 per link) |
| **Processing volume** | Estimated monthly transaction volume |
| **Refund policy** | You need a published refund policy on your site |

### Documents You'll Need

1. **Company registration certificate** (SECP registration or similar)
2. **NTN certificate** (National Tax Number)
3. **CNIC or Passport** (owner/partner)
4. **Bank account statement** (for payout verification)
5. **Proof of address** (utility bill or bank statement)

### Timeline
- Application: 10-15 minutes online
- Approval: **3-7 business days** (sometimes faster)
- Integration: 1-2 hours after approval

---

## 3. Pricing & Fees

| Fee | Amount |
|-----|--------|
| **Transaction fee** | 2.5% + $0.30 per transaction (typical for 2PayJS) |
| **Chargeback fee** | $25 (refunded if you win) |
| **Monthly fee** | $0 (no monthly fee on 2PayJS plan) |
| **Payout fee** | Free (wire transfer to Pakistan) |
| **Currency conversion** | 1% if client pays in non-USD currency |
| **Refund fee** | Transaction fee is NOT refunded on refunds |

### Example: Client orders $500 worth of guest posts
- Transaction: $500
- 2Checkout fee: $500 × 2.5% + $0.30 = **$12.80**
- You receive: **$487.20**
- Wire transfer to your Pakistani bank account

---

## 4. Integration Options

2Checkout offers two integration methods:

### Option A: 2PayJS (Recommended — Inline Checkout)
- Client stays on your dashboard
- A lightbox/overlay opens for payment
- Client enters card details
- No redirect to 2Checkout site
- **Best UX** — professional, seamless

### Option B: Standard Checkout (Redirect)
- Client is redirected to 2Checkout's hosted payment page
- After payment, redirected back to your site
- Simpler to implement
- **Less professional** — client leaves your site

### ✅ Recommendation: **2PayJS (Inline Checkout)**

---

## 5. What I Need From You

Once your 2Checkout account is approved, share these:

```
TWOCHECKOUT_SELLER_ID = "your-seller-id"     # From 2Checkout dashboard
TWOCHECKOUT_SECRET_KEY = "your-secret-key"    # From 2Checkout dashboard
```

These will be stored as Cloudflare Worker secrets (encrypted, never exposed).

---

## 6. Payout to Your Pakistani Bank Account

### How It Works
1. 2Checkout collects payments from your international clients
2. They hold funds for a settlement period (typically 7 days)
3. They send wire transfer to your Pakistani bank account
4. Funds arrive in PKR (converted at your bank's rate)

### Payout Settings You Can Configure
- **Frequency:** Weekly, bi-weekly, or monthly
- **Minimum payout:** $50 (default, can be changed)
- **Currency:** USD (your bank converts to PKR)

### Supported Pakistani Banks for Payout
- HBL, UBL, MCB, Allied Bank, Bank Alfalah, Meezan Bank
- National Bank, Standard Chartered, Faysal Bank, JS Bank
- Askari Bank, Bank Al Habib, Soneri Bank, Silkbank, Summit Bank

---

## 7. Integration Flow (Technical)

```
1. Client fills order on Svelte dashboard
2. Svelte calls Cloudflare Worker: POST /api/checkout
3. Worker creates 2Checkout charge via their API
4. 2Checkout returns a checkout token
5. Svelte loads 2Checkout JS library
6. 2Checkout opens inline checkout lightbox
7. Client enters card details and pays
8. 2Checkout processes payment (3D Secure if needed)
9. On success, 2Checkout calls webhook: POST /api/webhook/2checkout
10. Worker verifies webhook signature
11. Worker updates order status to "paid" in Supabase
12. Client sees "In Progress" on dashboard
```

---

## 8. What You Need to Do Now

1. **Go to:** https://www.verifone.com/en/signup
2. **Select:** "2Checkout" plan (not Verifone Pure)
3. **Fill in:** Company details, website, product info
4. **Upload:** Business documents (registration, NTN, ID)
5. **Add:** Your Pakistani bank account for payouts
6. **Wait:** 3-7 days for approval
7. **Share:** Seller ID + Secret Key with me once approved

While you wait, I can start building the **blog** and the **Svelte dashboard frontend** — those don't need 2Checkout keys.
