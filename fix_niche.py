import re

# ===== NICHE EDITS =====
with open('/c/Users/HT/Desktop/Coding Projects/LinkBuilding Agency/niche-edits.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update pricing cards - DR ranges, traffic highlights, descriptions
old_pricing = '''          <!-- Foundation -->
          <div class="pricing-card">
            <div class="pricing-card-tier">Foundation</div>
            <div class="pricing-card-name">DR 10\u201330</div>
            <div class="pricing-card-dr">300+ organic traffic \xb7 Starter links</div>
            <div class="pricing-card-price">$50<span>/link</span></div>
            <div class="pricing-card-per">per placement</div>
            <div class="pricing-card-divider"></div>
            <ul class="pricing-card-features">
              <li class="pricing-feature-highlight"><strong>300+ organic traffic</strong></li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>700+ word article</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Anchor + URL control</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Dofollow contextual link</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>TAT: 2 weeks</li>
            </ul>
            <a href="#final-cta" class="btn-primary cta-track" data-cta="pricing-foundation">Order Foundation</a>
          </div>

          <!-- Growth (Most Popular) -->
          <div class="pricing-card popular">
            <div class="pricing-card-badge">Most Popular</div>
            <div class="pricing-card-tier">Growth</div>
            <div class="pricing-card-name">DR 31\u201340</div>
            <div class="pricing-card-dr">500+ organic traffic \xb7 Competitive niches</div>
            <div class="pricing-card-price">$75<span>/link</span></div>
            <div class="pricing-card-per">per placement</div>
            <div class="pricing-card-divider"></div>
            <ul class="pricing-card-features">
              <li class="pricing-feature-highlight"><strong>500+ organic traffic</strong></li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>700+ word article</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Anchor + URL control</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Dofollow contextual link</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>TAT: 2 weeks</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Free replacement if removed</li>
            </ul>
            <a href="#final-cta" class="btn-primary cta-track" data-cta="pricing-growth">Order Growth</a>
          </div>

          <!-- Premium -->
          <div class="pricing-card">
            <div class="pricing-card-tier">Premium</div>
            <div class="pricing-card-name">DR 40+</div>
            <div class="pricing-card-dr">1,000+ organic traffic \xb7 Premium placements</div>
            <div class="pricing-card-price">$150<span>/link</span></div>
            <div class="pricing-card-per">per placement</div>
            <div class="pricing-card-divider"></div>
            <ul class="pricing-card-features">
              <li class="pricing-feature-highlight"><strong>1,000+ organic traffic</strong></li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>700+ word article</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Anchor + URL control</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Dofollow contextual link</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>TAT: 2 weeks</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Free replacement if removed</li>
            </ul>
            <a href="#final-cta" class="btn-primary cta-track" data-cta="pricing-premium">Order Premium</a>
          </div>'''

new_pricing = '''          <!-- Foundation -->
          <div class="pricing-card">
            <div class="pricing-card-tier">Foundation</div>
            <div class="pricing-card-name">DR 10\u201330</div>
            <div class="pricing-card-dr">Starter links</div>
            <div class="pricing-card-price">$50<span>/link</span></div>
            <div class="pricing-card-per">per placement</div>
            <div class="pricing-card-divider"></div>
            <ul class="pricing-card-features">
              <li class="pricing-feature-highlight"><strong>200+ organic traffic</strong></li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>700+ word article</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Anchor + URL control</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Dofollow contextual link</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>TAT: 2 weeks</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Free replacement if removed</li>
            </ul>
            <a href="#final-cta" class="btn-primary cta-track" data-cta="pricing-foundation">Order Foundation</a>
          </div>

          <!-- Growth (Most Popular) -->
          <div class="pricing-card popular">
            <div class="pricing-card-badge">Most Popular</div>
            <div class="pricing-card-tier">Growth</div>
            <div class="pricing-card-name">DR 31\u201340</div>
            <div class="pricing-card-dr">Competitive niches</div>
            <div class="pricing-card-price">$75<span>/link</span></div>
            <div class="pricing-card-per">per placement</div>
            <div class="pricing-card-divider"></div>
            <ul class="pricing-card-features">
              <li class="pricing-feature-highlight"><strong>500+ organic traffic</strong></li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>700+ word article</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Anchor + URL control</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Dofollow contextual link</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>TAT: 2 weeks</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Free replacement if removed</li>
            </ul>
            <a href="#final-cta" class="btn-primary cta-track" data-cta="pricing-growth">Order Growth</a>
          </div>

          <!-- Premium -->
          <div class="pricing-card">
            <div class="pricing-card-tier">Premium</div>
            <div class="pricing-card-name">DR 40+</div>
            <div class="pricing-card-dr">Premium placements</div>
            <div class="pricing-card-price">$150<span>/link</span></div>
            <div class="pricing-card-per">per placement</div>
            <div class="pricing-card-divider"></div>
            <ul class="pricing-card-features">
              <li class="pricing-feature-highlight"><strong>1,000+ organic traffic</strong></li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>700+ word article</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Anchor + URL control</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Dofollow contextual link</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>TAT: 2 weeks</li>
              <li><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3 4.3L6 11.6L2.7 8.3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Free replacement if removed</li>
            </ul>
            <a href="#final-cta" class="btn-primary cta-track" data-cta="pricing-premium">Order Premium</a>
          </div>'''

content = content.replace(old_pricing, new_pricing)

# 2. Remove "What Are Niche Edits?" section
what_are_start = content.find('<!-- ========== WHAT ARE NICHE EDITS ========== -->')
what_are_end = content.find('<!-- ========== NICHE EDITS VS GUEST POSTS ========== -->')
if what_are_start > 0 and what_are_end > 0:
    content = content[:what_are_start] + content[what_are_end:]

# 3. Remove Agency Offer section
agency_start = content.find('<div class="pricing-whitelabel-wrapper">')
if agency_start > 0:
    next_section = content.find('<!-- ========== WHITE-LABEL ========== -->', agency_start)
    if next_section > 0:
        content = content[:agency_start] + content[next_section:]

# 4. Reorder: move Pricing after Hero (after comparison table)
hero_end = content.find('<!-- ========== NICHE EDITS VS GUEST POSTS ========== -->')
pricing_start = content.find('<!-- ========== PRICING ========== -->')
pricing_end = content.find('<!-- ========== WHITE-LABEL ========== -->')

if pricing_start > 0 and pricing_end > 0 and hero_end > 0:
    pricing_section = content[pricing_start:pricing_end]
    content = content[:pricing_start] + content[pricing_end:]
    new_hero_end = content.find('<!-- ========== NICHE EDITS VS GUEST POSTS ========== -->')
    content = content[:new_hero_end] + pricing_section + content[new_hero_end:]

# 5. Add FAQ items
faq_list_start = content.find('<div class="faq-list reveal">')
new_faq = '''          <div class="faq-item open">
            <button class="faq-question" aria-expanded="true">
              What Are Niche Edits?
              <span class="faq-toggle" aria-hidden="true">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 2V12M2 7H12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              </span>
            </button>
            <div class="faq-answer">
              <div class="faq-answer-inner">A niche edit (also called a curated link or link insertion) is a backlink placed inside an existing article that is already published and ranking on a relevant website. Instead of writing new content, we insert your contextual backlink into live pages that Google already trusts and indexes. Guest posts build new authority. Niche edits borrow existing authority. Both have a place in a serious SEO strategy.</div>
            </div>
          </div>
          <div class="faq-item">
            <button class="faq-question" aria-expanded="false">
              How much do niche edit services cost?
              <span class="faq-toggle" aria-hidden="true">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 2V12M2 7H12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              </span>
            </button>
            <div class="faq-answer">
              <div class="faq-answer-inner">Niche edit services typically range from $50 to $150 per placement depending on the domain authority (DR 10-40+) and organic traffic of the publishing site, with white-label bundles available from $50/link for agencies.</div>
            </div>
          </div>
'''
content = content[:faq_list_start] + new_faq + content[faq_list_start:]

with open('/c/Users/HT/Desktop/Coding Projects/LinkBuilding Agency/niche-edits.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Niche Edits done")
