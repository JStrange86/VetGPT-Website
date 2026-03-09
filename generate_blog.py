#!/usr/bin/env python3
"""
VetGPT Blog Post Generator
Generates static HTML blog posts from content definitions.
Run: python3 generate_blog.py
"""

import os, json

BLOG_DIR = os.path.join(os.path.dirname(__file__), "blog")
os.makedirs(BLOG_DIR, exist_ok=True)

CSS = """
        :root {
            --bg: #0a0a0a; --bg-elevated: #111111; --bg-card: rgba(255,255,255,0.04);
            --bg-card-hover: rgba(255,255,255,0.07); --border: rgba(255,255,255,0.08);
            --border-hover: rgba(255,255,255,0.15); --text: #ffffff;
            --text-secondary: #9ca3af; --text-muted: #8b95a5;
            --green: #10b981; --green-glow: rgba(16,185,129,0.3);
            --purple: #8b5cf6; --pink: #ec4899;
            --font-display: 'Outfit', sans-serif; --font-body: 'DM Sans', sans-serif;
            --font-mono: 'JetBrains Mono', monospace; --max-w: 1200px;
        }
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }
        body { font-family: var(--font-body); background: var(--bg); color: var(--text); line-height: 1.6; overflow-x: hidden; }
        a { color: inherit; text-decoration: none; }
        img { max-width: 100%; height: auto; display: block; }
        .container { max-width: var(--max-w); margin: 0 auto; padding: 0 24px; }
        .nav { position: fixed; top: 0; left: 0; right: 0; z-index: 1000; padding: 16px 0; transition: background 0.3s, padding 0.3s; }
        .nav.scrolled { background: rgba(10,10,10,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border); padding: 10px 0; }
        .nav-inner { max-width: var(--max-w); margin: 0 auto; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-family: var(--font-display); font-weight: 800; font-size: 1.6rem; display: flex; align-items: center; gap: 12px; }
        .nav-logo-img { width: 42px; height: 42px; object-fit: contain; border-radius: 8px; }
        .nav-links { display: flex; align-items: center; gap: 32px; list-style: none; }
        .nav-links a { font-family: var(--font-body); font-size: 0.9rem; color: var(--text-secondary); transition: color 0.2s; }
        .nav-links a:hover { color: var(--text); }
        .nav-cta { padding: 12px 24px; background: #10b981; color: #000 !important; font-family: var(--font-display); font-weight: 800; font-size: 0.95rem; border-radius: 10px; transition: box-shadow 0.3s, transform 0.2s; }
        .nav-cta:hover { box-shadow: 0 0 30px var(--green-glow); transform: translateY(-1px); }
        .nav-hamburger { display: none; flex-direction: column; gap: 5px; cursor: pointer; background: none; border: none; padding: 4px; }
        .nav-hamburger span { display: block; width: 24px; height: 2px; background: var(--text); border-radius: 2px; }
        .mobile-menu { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(10,10,10,0.97); z-index: 999; flex-direction: column; align-items: center; justify-content: center; gap: 32px; }
        .mobile-menu.open { display: flex; }
        .mobile-menu a { font-family: var(--font-display); font-size: 1.5rem; font-weight: 600; color: var(--text-secondary); }
        .mobile-menu-close { position: absolute; top: 20px; right: 24px; font-size: 2rem; color: var(--text); background: none; border: none; cursor: pointer; }
        @media (max-width: 768px) { .nav-links { display: none; } .nav-hamburger { display: flex; } }
        .article-wrap { padding: 120px 0 80px; }
        .article-container { max-width: 720px; margin: 0 auto; padding: 0 24px; }
        .breadcrumb { font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted); margin-bottom: 32px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
        .breadcrumb a { color: var(--text-muted); transition: color 0.2s; }
        .breadcrumb a:hover { color: var(--green); }
        .breadcrumb sep { color: var(--text-secondary); }
        .article-header { margin-bottom: 48px; }
        .article-tag { font-family: var(--font-mono); font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--green); background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); padding: 4px 12px; border-radius: 20px; display: inline-block; margin-bottom: 20px; }
        .article-header h1 { font-family: var(--font-display); font-size: clamp(1.8rem, 4vw, 2.6rem); font-weight: 800; line-height: 1.15; margin-bottom: 20px; letter-spacing: -0.02em; }
        .article-meta { font-family: var(--font-mono); font-size: 0.78rem; color: var(--text-muted); display: flex; gap: 16px; flex-wrap: wrap; }
        .article-body { font-size: 1.05rem; line-height: 1.85; color: var(--text-secondary); }
        .article-body p { margin-bottom: 24px; }
        .article-body h2 { font-family: var(--font-display); font-size: 1.5rem; font-weight: 700; color: var(--text); margin: 48px 0 16px; letter-spacing: -0.01em; }
        .article-body h3 { font-family: var(--font-display); font-size: 1.15rem; font-weight: 600; color: var(--text); margin: 32px 0 12px; }
        .article-body ul, .article-body ol { padding-left: 24px; margin-bottom: 24px; }
        .article-body li { margin-bottom: 8px; }
        .article-body strong { color: var(--text); font-weight: 600; }
        .article-body a { color: var(--green); text-decoration: underline; text-underline-offset: 3px; }
        .checklist-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 28px; margin-bottom: 24px; }
        .checklist-card h3 { font-family: var(--font-display); font-size: 1.1rem; font-weight: 700; color: var(--text); margin-bottom: 16px; }
        .checklist-card ul { list-style: none; padding: 0; margin: 0; }
        .checklist-card li { padding: 8px 0; border-bottom: 1px solid var(--border); color: var(--text-secondary); font-size: 0.95rem; display: flex; align-items: flex-start; gap: 10px; }
        .checklist-card li:last-child { border-bottom: none; }
        .checklist-card li::before { content: '✓'; color: var(--green); font-weight: 700; flex-shrink: 0; margin-top: 1px; }
        .warn-box { background: rgba(236,72,153,0.06); border: 1px solid rgba(236,72,153,0.2); border-radius: 12px; padding: 20px 24px; margin-bottom: 24px; }
        .warn-box p { margin: 0; color: var(--text-secondary); font-size: 0.95rem; }
        .warn-box strong { color: #ec4899; }
        .info-box { background: rgba(139,92,246,0.06); border: 1px solid rgba(139,92,246,0.2); border-radius: 12px; padding: 20px 24px; margin-bottom: 24px; }
        .info-box p { margin: 0; color: var(--text-secondary); font-size: 0.95rem; }
        .info-box strong { color: var(--purple); }
        .cta-box { background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(139,92,246,0.08)); border: 1px solid rgba(16,185,129,0.2); border-radius: 16px; padding: 36px; text-align: center; margin: 48px 0; }
        .cta-box h3 { font-family: var(--font-display); font-size: 1.4rem; font-weight: 700; color: var(--text); margin-bottom: 12px; }
        .cta-box p { color: var(--text-secondary); margin-bottom: 24px; font-size: 0.95rem; }
        .cta-btn { display: inline-block; padding: 14px 32px; background: var(--green); color: #000; font-family: var(--font-display); font-weight: 700; font-size: 1rem; border-radius: 10px; transition: box-shadow 0.3s, transform 0.2s; }
        .cta-btn:hover { box-shadow: 0 0 30px var(--green-glow); transform: translateY(-1px); }
        .related { margin-top: 64px; padding-top: 48px; border-top: 1px solid var(--border); }
        .related h3 { font-family: var(--font-display); font-size: 1.2rem; font-weight: 700; margin-bottom: 24px; }
        .related-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
        .related-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; transition: background 0.3s, border-color 0.3s; }
        .related-card:hover { background: var(--bg-card-hover); border-color: var(--border-hover); }
        .related-tag { font-family: var(--font-mono); font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--green); margin-bottom: 8px; }
        .related-card h4 { font-family: var(--font-display); font-size: 0.95rem; font-weight: 600; line-height: 1.35; color: var(--text); }
        @media (max-width: 600px) { .related-grid { grid-template-columns: 1fr; } }
        .footer { padding: 40px 0; border-top: 1px solid var(--border); }
        .footer-inner { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }
        .footer-links { display: flex; gap: 24px; list-style: none; flex-wrap: wrap; }
        .footer-links a { font-size: 0.85rem; color: var(--text-muted); transition: color 0.2s; }
        .footer-links a:hover { color: var(--text-secondary); }
        .footer-copy { font-size: 0.8rem; color: var(--text-muted); display: flex; align-items: center; gap: 8px; }
        .footer-logo { width: 22px; height: 22px; object-fit: contain; border-radius: 4px; opacity: 0.6; }
        @media (max-width: 600px) { .footer-inner { flex-direction: column; text-align: center; } }
"""

NAV = """    <header class="nav" id="nav">
        <div class="nav-inner">
            <a href="/" class="nav-logo"><img src="/logo-black.png" alt="VetGPT" class="nav-logo-img" width="34" height="34"> VetGPT</a>
            <nav>
                <ul class="nav-links">
                    <li><a href="/#features">Features</a></li>
                    <li><a href="/#how-it-works">How It Works</a></li>
                    <li><a href="/blog/">Blog</a></li>
                    <li><a href="/#founder">Story</a></li>
                    <li><a href="/#download" class="nav-cta">Get Early Access</a></li>
                </ul>
            </nav>
            <button class="nav-hamburger" id="menuBtn" aria-label="Open menu"><span></span><span></span><span></span></button>
        </div>
    </header>
    <div class="mobile-menu" id="mobileMenu">
        <button class="mobile-menu-close" id="menuClose">&times;</button>
        <a href="/#features">Features</a>
        <a href="/#how-it-works">How It Works</a>
        <a href="/blog/">Blog</a>
        <a href="/#founder">Story</a>
        <a href="/#download" style="color:var(--green)">Get Early Access</a>
    </div>"""

FOOTER = """    <footer class="footer">
        <div class="container">
            <div class="footer-inner">
                <ul class="footer-links">
                    <li><a href="/blog/">Blog</a></li>
                    <li><a href="/exotic-pet-care.html">Exotic Pets</a></li>
                    <li><a href="/reptile-health-tracker.html">Reptiles</a></li>
                    <li><a href="/aquarium-fish-health.html">Aquarium</a></li>
                    <li><a href="/privacy.html">Privacy Policy</a></li>
                    <li><a href="/terms.html">Terms of Service</a></li>
                    <li><a href="/support.html">Support</a></li>
                </ul>
                <p class="footer-copy"><img src="/logo-black.png" alt="" class="footer-logo" width="22" height="22"> &copy; 2026 VetGPT &middot; Made with &hearts; for pet parents everywhere</p>
            </div>
        </div>
    </footer>"""

JS = """    <script>
        const nav = document.getElementById('nav');
        window.addEventListener('scroll', () => { nav.classList.toggle('scrolled', window.scrollY > 50); });
        document.getElementById('menuBtn').addEventListener('click', () => document.getElementById('mobileMenu').classList.add('open'));
        document.getElementById('menuClose').addEventListener('click', () => document.getElementById('mobileMenu').classList.remove('open'));
        document.querySelectorAll('#mobileMenu a').forEach(a => a.addEventListener('click', () => document.getElementById('mobileMenu').classList.remove('open')));
    </script>"""

def build_faq_schema(faq_items):
    entities = []
    for q, a in faq_items:
        entities.append(f'            {{ "@type": "Question", "name": "{q}", "acceptedAnswer": {{ "@type": "Answer", "text": "{a}" }} }}')
    return '{\n        "@context": "https://schema.org",\n        "@type": "FAQPage",\n        "mainEntity": [\n' + ',\n'.join(entities) + '\n        ]\n    }'

def build_related(related_posts):
    cards = ""
    for slug, tag, title in related_posts:
        cards += f'''                        <a href="/blog/{slug}" class="related-card">
                            <p class="related-tag">{tag}</p>
                            <h4>{title}</h4>
                        </a>\n'''
    return cards

def render_post(p):
    faq_schema = build_faq_schema(p["faq"])
    related_cards = build_related(p["related"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p['page_title']}</title>
    <meta name="description" content="{p['meta_description']}">
    <meta property="og:title" content="{p['title']}">
    <meta property="og:description" content="{p['meta_description']}">
    <meta property="og:image" content="https://vetgpt.app/og-image.png">
    <meta property="og:url" content="https://vetgpt.app/blog/{p['slug']}.html">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="canonical" href="https://vetgpt.app/blog/{p['slug']}.html">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{p['title']}",
        "description": "{p['meta_description']}",
        "datePublished": "{p['date']}",
        "dateModified": "{p['date']}",
        "author": {{ "@type": "Organization", "name": "VetGPT" }},
        "publisher": {{ "@type": "Organization", "name": "VetGPT", "url": "https://vetgpt.app" }}
    }}
    </script>
    <script type="application/ld+json">
    {faq_schema}
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
{CSS}
    </style>
</head>
<body>
{NAV}
    <main>
        <div class="article-wrap">
            <div class="article-container">
                <nav class="breadcrumb" aria-label="Breadcrumb">
                    <a href="/">Home</a> <sep>&rsaquo;</sep>
                    <a href="/blog/">Blog</a> <sep>&rsaquo;</sep>
                    <span>{p['breadcrumb']}</span>
                </nav>
                <header class="article-header">
                    <span class="article-tag">{p['tag']}</span>
                    <h1>{p['title']}</h1>
                    <div class="article-meta">
                        <span>{p['date_display']}</span>
                        <span>{p['readtime']}</span>
                        <span>By VetGPT</span>
                    </div>
                </header>
                <div class="article-body">
{p['body']}
                    <div class="cta-box">
                        <h3>{p['cta_headline']}</h3>
                        <p>{p['cta_body']}</p>
                        <a href="/#download" class="cta-btn">Get Early Access &mdash; Free</a>
                    </div>
                    <h2>Frequently Asked Questions</h2>
{p['faq_html']}
                </div>
                <div class="related">
                    <h3>More from the VetGPT Blog</h3>
                    <div class="related-grid">
{related_cards}                    </div>
                </div>
            </div>
        </div>
    </main>
{FOOTER}
{JS}
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# POST DEFINITIONS
# Each post: slug, page_title, title, breadcrumb, tag, date, date_display,
#            readtime, meta_description, body (raw HTML), faq (list of [q,a]),
#            faq_html (rendered), related (list of [slug, tag, title]),
#            cta_headline, cta_body
# ─────────────────────────────────────────────────────────────────────────────

posts = []

# ── POST 4: Guinea pig health ─────────────────────────────────────────────────
posts.append({
  "slug": "guinea-pig-health-checklist",
  "page_title": "Guinea Pig Health Checklist: Daily & Weekly Care Guide | VetGPT",
  "title": "Guinea Pig Health Checklist: What to Check Every Day (And What Most Owners Miss)",
  "breadcrumb": "Guinea Pig Health Checklist",
  "tag": "🐹 Small Mammals",
  "date": "2026-03-02",
  "date_display": "March 2, 2026",
  "readtime": "5 min read",
  "meta_description": "Guinea pigs hide illness until it's serious. Here's what to check daily, weekly, and monthly — plus the warning signs every cavy owner needs to know.",
  "cta_headline": "Track your guinea pig's health with AI",
  "cta_body": "Weight trends, feeding logs, vet visit records, and AI chat that knows your cavy's full history. Free during early release.",
  "faq": [
    ("How often should I weigh my guinea pig?", "Weekly. Guinea pigs hide illness well, and weight loss is often the first sign something is wrong. A 50–100g loss over one to two weeks warrants a vet call."),
    ("What are signs of illness in guinea pigs?", "Lethargy, not eating (especially if they stop eating hay), weight loss, discharge from eyes or nose, labored breathing, tooth grinding, hunched posture, or loose stools. Guinea pigs are prey animals — they hide illness until it's advanced."),
    ("Can I track my guinea pig's health in an app?", "Yes. VetGPT supports guinea pigs with feeding logs, weight tracking, vet visit records, and AI chat that knows your cavy's history. Ask questions specific to your pet's situation — not just generic guinea pig information."),
    ("How long do guinea pigs live, and what health issues are common?", "Guinea pigs typically live 4–7 years. Common health issues include dental disease (malocclusion), respiratory infections, urinary stones, skin mites, and vitamin C deficiency. Regular vet checkups and a hay-based diet prevent most issues.")
  ],
  "related": [
    ("bearded-dragon-health-checklist.html", "🦎 Reptiles", "The Complete Bearded Dragon Health Checklist"),
    ("how-to-track-dog-medications.html", "🐕 Dogs", "How to Track Your Dog's Medications (And Never Miss a Dose Again)")
  ],
  "body": """                    <p>Guinea pigs are social, vocal, and surprisingly fragile for an animal that looks sturdy. They hide illness instinctively — a survival mechanism from being prey animals in the wild. By the time a guinea pig looks visibly sick, the problem has usually been developing for days or weeks. The solution is regular, systematic observation.</p>
                    <p>This checklist covers what to watch for daily and weekly, the most commonly missed warning signs, and how to build habits that catch problems early when they're still treatable.</p>
                    <h2>Why Guinea Pigs Are High-Risk for Missed Illness</h2>
                    <p>Unlike dogs and cats, guinea pigs have almost no outward signs of early illness. They continue eating (sometimes), moving around, and appearing social until they're in significant distress. The first clear sign is often dramatic weight loss or a sudden crash in condition — both of which are preventable with a weekly weigh-in and consistent observation.</p>
                    <p>Vets who specialize in small mammals will tell you the same thing: the owners who catch problems early are the ones who weigh their guinea pigs every week and know what "normal" looks like for their individual animal.</p>
                    <h2>Daily Checks</h2>
                    <div class="checklist-card">
                        <h3>🌅 Every Day</h3>
                        <ul>
                            <li>Is your guinea pig moving around normally and responding when you approach?</li>
                            <li>Did they eat — specifically hay (should be 80% of their diet) and fresh vegetables?</li>
                            <li>Are they making normal sounds? Silence from a usually vocal guinea pig is a flag.</li>
                            <li>Eyes clear, no discharge or crustiness?</li>
                            <li>Nose dry and clean — no discharge?</li>
                            <li>Breathing normally — no wheezing or labored breathing?</li>
                            <li>Normal stool output — if stool suddenly decreases or changes in consistency, take note.</li>
                        </ul>
                    </div>
                    <h2>Weekly Checks</h2>
                    <div class="checklist-card">
                        <h3>📅 Every Week</h3>
                        <ul>
                            <li><strong>Weigh them</strong> — this is non-negotiable. Use a kitchen scale accurate to 1g. Log every weigh-in. A 50–100g loss over one to two weeks means a vet call.</li>
                            <li>Check teeth — guinea pig teeth should be straight, meet properly, and be a pale yellow (not white). White teeth can indicate a vitamin C issue.</li>
                            <li>Check the bottom of their feet — guinea pigs are prone to bumblefoot (pododermatitis). Red, swollen, or crusty foot pads need vet attention.</li>
                            <li>Feel along their body — any lumps, bumps, or asymmetry? Guinea pigs get abscesses and cysts that are treatable if caught early.</li>
                            <li>Check ears — no wax buildup, no head tilting.</li>
                            <li>Skin and coat — any bald patches, excessive scratching, or flaky skin? Mites are common and very treatable.</li>
                            <li>Vitamin C check — are they getting 25–50mg daily? Scurvy is common and preventable.</li>
                        </ul>
                    </div>
                    <h2>The Vitamin C Problem</h2>
                    <p>Guinea pigs cannot synthesize vitamin C. They require it from diet every single day. Early signs of deficiency (scurvy) include rough coat, reluctance to move, swollen joints, and tooth problems. It progresses quickly and becomes serious.</p>
                    <p>Bell pepper (especially red) is the most efficient dietary source — a tablespoon a day covers most of their requirement. Leafy greens like romaine, parsley, and kale help. Don't rely on water additives — vitamin C degrades rapidly in water and the dosing is unreliable.</p>
                    <div class="warn-box">
                        <p><strong>Call a vet if you see:</strong> Weight loss of 50g+ in one week &middot; Not eating hay for more than 12 hours &middot; Labored breathing or wheezing &middot; Head tilting &middot; Grinding teeth (indicates pain) &middot; Blood in urine &middot; Swollen, red foot pads &middot; Complete lethargy</p>
                    </div>
                    <h2>Dental Disease: The Silent Killer</h2>
                    <p>Dental disease (malocclusion) is one of the leading causes of death in guinea pigs and one of the hardest to spot at home. Their back molars can overgrow without any visible external sign until your guinea pig stops eating or loses significant weight.</p>
                    <p>Signs: dropping food while eating, drooling, weight loss despite appearing to try to eat, pawing at the mouth. This requires an exotic vet with proper equipment — regular dental checks are recommended annually.</p>
                    <h2>How VetGPT Helps</h2>
                    <p>Tracking weekly weights, vitamin C supplementation, and vet visit history for a guinea pig in a notes app or spreadsheet works — but it's friction. VetGPT tracks all of it in one place. Log weights and see the trend over time. Record feeding details. Scan vet discharge paperwork and have the instructions captured automatically. Ask the AI chat "has her weight been stable?" and get an answer based on your actual logs.</p>""",
  "faq_html": """                    <h3>How often should I weigh my guinea pig?</h3>
                    <p>Weekly. Guinea pigs hide illness well, and weight loss is often the first sign something is wrong. A 50–100g loss over one to two weeks warrants a vet call. Use a kitchen scale accurate to 1 gram and log it every time.</p>
                    <h3>What are signs of illness in guinea pigs?</h3>
                    <p>Lethargy, not eating (especially refusing hay), weight loss, discharge from eyes or nose, labored breathing, tooth grinding, hunched posture, or loose stools. Because guinea pigs are prey animals, they hide illness until it's advanced — routine checks are how you catch it early.</p>
                    <h3>Can I track my guinea pig's health in an app?</h3>
                    <p>Yes. VetGPT supports guinea pigs with feeding logs, weight tracking, vet visit records, and AI chat that knows your cavy's history — not just generic information.</p>
                    <h3>What health issues are most common in guinea pigs?</h3>
                    <p>Dental disease (malocclusion), respiratory infections, urinary stones, skin mites, and vitamin C deficiency. Most are preventable or very treatable if caught early. Annual exotic vet checkups are strongly recommended.</p>"""
})

# ── POST 5: Cat health tracker ────────────────────────────────────────────────
posts.append({
  "slug": "cat-health-tracker-guide",
  "page_title": "How to Track Your Cat's Health: The Complete Owner's Guide | VetGPT",
  "title": "How to Track Your Cat's Health (Because Cats Won't Tell You When Something's Wrong)",
  "breadcrumb": "Cat Health Tracking Guide",
  "tag": "🐱 Cats",
  "date": "2026-03-02",
  "date_display": "March 2, 2026",
  "readtime": "6 min read",
  "meta_description": "Cats are masters at hiding illness. Here's what to track, how often to check, and what signs should send you to the vet — before it becomes serious.",
  "cta_headline": "Track your cat's health with AI",
  "cta_body": "Weight trends, medication tracking, vet visit records, and AI chat that knows your cat's full history. Free during early release.",
  "faq": [
    ("How often should cats see the vet?", "Adult cats (1–7 years) should have annual wellness exams. Senior cats (7+) benefit from twice-yearly visits. Kittens need more frequent visits in their first year for vaccines and development checks."),
    ("What are early signs of illness in cats?", "Subtle changes in eating or drinking, weight loss, increased hiding, changes in litter box behavior (frequency, consistency, missing the box), coat changes, and altered grooming habits. Cats mask pain and illness — changes in normal behavior are the main signal."),
    ("Should I track my cat's weight at home?", "Yes, especially for cats over 7. Monthly home weigh-ins catch weight loss early. Weigh yourself holding the cat, then weigh yourself alone. The difference is your cat's weight. A kitchen scale works for smaller cats."),
    ("What's the most important thing to track for a cat's health?", "Litter box behavior. Changes in frequency, consistency, straining, or blood in urine or stool are often the first signs of kidney disease, urinary issues, diabetes, and other serious conditions. Track it — even informally.")
  ],
  "related": [
    ("preparing-for-vet-visit.html", "🏥 Vet Visits", "How to Prepare for a Vet Visit (So You Never Blank at the Worst Moment)"),
    ("senior-dog-care-guide.html", "🐕 Dogs", "The Senior Dog Care Guide: Health Changes to Watch After Age 7")
  ],
  "body": """                    <p>Cats are extraordinary at hiding illness. It's not stubbornness — it's biology. As obligate predators who are also prey for larger animals, showing weakness is dangerous. So they compensate, compensate, compensate until they can't. By the time a cat looks visibly sick, things are often quite serious.</p>
                    <p>The good news: cats have patterns. They're creatures of habit, and changes in those patterns — eating, drinking, elimination, grooming, activity — are almost always the first signal. The owners who catch things early are the ones paying attention to patterns, not just obvious symptoms.</p>
                    <h2>What to Watch: The Core Metrics</h2>
                    <h3>Eating and Drinking</h3>
                    <p>Know your cat's normal. Do they finish every meal? Do they graze? Do they drink a lot or a little? Changes matter more than absolute amounts. A cat who suddenly drinks much more water (polydipsia) is showing a classic sign of kidney disease or diabetes. A cat who stops eating for more than 24 hours needs vet attention — unlike dogs, cats can develop hepatic lipidosis (fatty liver disease) from even brief food refusal.</p>
                    <h3>Litter Box Behavior</h3>
                    <p>This is the most information-dense signal you have. Track it — even informally. Changes to watch for:</p>
                    <ul>
                        <li>Straining to urinate or defecate</li>
                        <li>Urinating outside the box (often a sign of pain associated with the box, not defiance)</li>
                        <li>Blood in urine or stool</li>
                        <li>Sudden changes in stool consistency</li>
                        <li>Increased or decreased urination frequency</li>
                        <li>Crying while in the litter box</li>
                    </ul>
                    <p>Male cats who are straining to urinate are a medical emergency — urinary blockages can be fatal within 24–48 hours.</p>
                    <h3>Weight</h3>
                    <p>Weigh your cat monthly — especially after age 7. A 10% weight loss in a cat who is already lean is significant. You can do this at home: weigh yourself holding the cat, then weigh yourself alone. The difference is your cat's weight. Log it every month.</p>
                    <div class="checklist-card">
                        <h3>📋 Monthly Check-In</h3>
                        <ul>
                            <li>Weight (log it, look at the trend)</li>
                            <li>Coat condition — dull, greasy, or patchy coat often means something systemic</li>
                            <li>Teeth and gums — red or swollen gumline is dental disease; bad breath can indicate kidney disease</li>
                            <li>Eyes — clear, bright, no third eyelid showing prominently</li>
                            <li>Ears — clean, no dark debris (ear mites), no scratching</li>
                            <li>Behavior — any increase in hiding, vocalization, or aggression can indicate pain</li>
                            <li>Activity level — is your cat as playful, or as interested, as usual?</li>
                        </ul>
                    </div>
                    <h2>Senior Cats: Age 7 and Up</h2>
                    <p>After age 7, cats need more attention. Hyperthyroidism, kidney disease, diabetes, hypertension, and dental disease all become significantly more common. The American Association of Feline Practitioners recommends twice-yearly vet visits for senior cats — not because they're sicker, but because six months is a long time in a senior cat's life and early detection makes a real difference.</p>
                    <p>Signs to watch more closely in senior cats:</p>
                    <ul>
                        <li>Increased vocalization, especially at night</li>
                        <li>Changes in sleep patterns or spatial awareness (cognitive dysfunction)</li>
                        <li>Weight loss despite normal or increased appetite (hyperthyroidism)</li>
                        <li>Increased water intake and urination</li>
                        <li>Muscle wasting — particularly noticeable along the spine</li>
                    </ul>
                    <h2>Tracking Vaccinations and Preventatives</h2>
                    <p>Adult indoor cats need rabies and FVRCP vaccines — your vet will advise on schedule. Flea and parasite prevention is important even for indoor cats. Keep a record of what was given, when, and when it's next due. This information matters especially when you see a new vet or an emergency clinic.</p>
                    <div class="warn-box">
                        <p><strong>Seek emergency care for:</strong> Male cats straining to urinate &middot; Complete food refusal for 24+ hours &middot; Labored or open-mouth breathing &middot; Collapse or inability to stand &middot; Seizures &middot; Pale or white gums &middot; Suspected poisoning</p>
                    </div>
                    <h2>How VetGPT Helps</h2>
                    <p>The challenge with cat health tracking is that the signals are subtle and spread across months. A weight log from six months ago is genuinely useful at a vet appointment. VetGPT keeps weight trends, litter box observations, feeding notes, medication records, and vet visit history in one place — so when you walk in and the vet asks "any changes?", you have a real answer.</p>""",
  "faq_html": """                    <h3>How often should cats see the vet?</h3>
                    <p>Adult cats (1–7 years) should have annual wellness exams. Senior cats (7+) benefit from twice-yearly visits. Kittens need more frequent visits in their first year for vaccines and development monitoring.</p>
                    <h3>What are early signs of illness in cats?</h3>
                    <p>Subtle changes in eating or drinking, weight loss, increased hiding, changes in litter box behavior, coat changes, and altered grooming habits. Cats mask illness — changes in normal behavior are the main signal to watch for.</p>
                    <h3>Should I track my cat's weight at home?</h3>
                    <p>Yes, especially after age 7. Monthly weigh-ins catch weight loss early. Weigh yourself holding the cat, then alone. The difference is your cat's weight. Log it every month and look for trends.</p>
                    <h3>What's the most important thing to track?</h3>
                    <p>Litter box behavior. Changes in frequency, consistency, straining, or blood in urine or stool are often the first signs of serious conditions including kidney disease, urinary issues, and diabetes.</p>"""
})

# ── POST 6: Senior dog care ───────────────────────────────────────────────────
posts.append({
  "slug": "senior-dog-care-guide",
  "page_title": "Senior Dog Care Guide: Health Changes to Watch After Age 7 | VetGPT",
  "title": "The Senior Dog Care Guide: Health Changes to Watch After Age 7",
  "breadcrumb": "Senior Dog Care Guide",
  "tag": "🐕 Dogs",
  "date": "2026-03-02",
  "date_display": "March 2, 2026",
  "readtime": "6 min read",
  "meta_description": "Dogs age faster than we do. After age 7, health checks and vet visits matter more. Here's what changes, what to watch, and how to give your senior dog the best years.",
  "cta_headline": "Track your senior dog's health over time",
  "cta_body": "Weight trends, medication logs, vet visit history, and AI that knows your dog's full history. Catch changes before they become problems.",
  "faq": [
    ("When is a dog considered senior?", "It depends on size. Large and giant breeds age faster — a Great Dane is considered senior around 5–6. Medium breeds around 7–8. Small breeds around 9–10. Your vet can give you a breed-specific guideline."),
    ("How often should senior dogs see the vet?", "Twice a year. Every six months is a long time in a senior dog's life. Conditions like kidney disease, heart disease, hypothyroidism, and cancer are all more common in senior dogs and respond much better to early treatment."),
    ("What supplements are good for senior dogs?", "Speak to your vet before adding supplements. Commonly recommended options include omega-3 fatty acids (fish oil) for joints and inflammation, glucosamine/chondroitin for joint support, and probiotics for digestive health. Not all supplements are beneficial for every dog."),
    ("What are signs of pain in older dogs?", "Changes in movement (stiffness, reluctance to use stairs or jump), behavioral changes (irritability, increased hiding), changes in sleep, reduced interest in activities they used to love, altered posture, or excessive licking of a specific area. Dogs often don't vocalize pain — behavioral changes are the signal.")
  ],
  "related": [
    ("how-to-track-dog-medications.html", "🐕 Dogs", "How to Track Your Dog's Medications (And Never Miss a Dose Again)"),
    ("preparing-for-vet-visit.html", "🏥 Vet Visits", "How to Prepare for a Vet Visit (So You Never Blank at the Worst Moment)")
  ],
  "body": """                    <p>A dog's seventh birthday is a milestone — and a signal. Not that anything dramatic changes overnight, but the risk profile shifts. Conditions that were unlikely become common. Changes that seemed gradual become significant. The dogs who age well are the ones whose owners notice and respond to early signals.</p>
                    <p>This guide covers what changes after age 7, what to monitor at home, and how to advocate for your senior dog at the vet.</p>
                    <h2>What Changes in a Senior Dog's Body</h2>
                    <p>The changes are real and worth understanding:</p>
                    <ul>
                        <li><strong>Metabolism slows</strong> — senior dogs need fewer calories, but their nutritional needs may actually increase. Obesity becomes a serious risk and compounds joint problems.</li>
                        <li><strong>Organ function declines</strong> — kidney and liver efficiency decrease gradually. This affects how medications are processed and why dosing sometimes changes in senior dogs.</li>
                        <li><strong>Immune function changes</strong> — cancer becomes significantly more common. Lumps and bumps that would be dismissed in a young dog deserve more attention in a senior.</li>
                        <li><strong>Joints wear</strong> — osteoarthritis is estimated to affect 80% of dogs over age 8. It's often silent until significant, and most owners underestimate how much pain their dog is managing.</li>
                        <li><strong>Senses dull</strong> — hearing and vision loss are common and usually gradual. A dog who seems to be ignoring you may be going deaf.</li>
                        <li><strong>Cognitive function</strong> — canine cognitive dysfunction (similar to dementia) affects an estimated 28% of dogs aged 11–12.</li>
                    </ul>
                    <h2>What to Monitor at Home</h2>
                    <div class="checklist-card">
                        <h3>📋 Monthly Senior Dog Check</h3>
                        <ul>
                            <li>Weight — monthly weigh-in. Unintentional weight loss or gain both matter.</li>
                            <li>Movement — any new stiffness getting up, reluctance to use stairs, or changes in gait?</li>
                            <li>Appetite and thirst — increased thirst is a classic sign of kidney disease, diabetes, and Cushing's disease.</li>
                            <li>Lumps and skin — run your hands over their whole body. New lumps get noted and checked at the next vet visit. Growing or changing lumps get checked sooner.</li>
                            <li>Teeth and gums — dental disease worsens with age and affects heart and kidney health.</li>
                            <li>Eyes — cloudiness is often normal aging (nuclear sclerosis), but glaucoma and cataracts need vet evaluation.</li>
                            <li>Behavior — any increase in confusion, nighttime restlessness, or loss of house training can indicate cognitive changes.</li>
                        </ul>
                    </div>
                    <h2>Arthritis: The Most Underestimated Condition</h2>
                    <p>Most owners think they'd know if their dog was in significant pain. They're usually wrong. Dogs are stoic — they adapt to chronic pain gradually, and owners adapt with them. The dog who "used to love fetch but isn't as interested anymore" is often a dog in pain who's learned to avoid it.</p>
                    <p>Signs of arthritis that aren't limping: reluctance to jump into the car, slower on walks, stiffness after resting, licking a joint, aggression when touched in a specific area, personality changes.</p>
                    <p>Arthritis is manageable. Pain medication, weight management, joint supplements, and modifications to the environment (ramps, orthopedic beds) make a real difference. But it requires recognition first.</p>
                    <h2>The Twice-Yearly Vet Visit</h2>
                    <p>Once a year is not enough for senior dogs. Six months is a long time. Standard senior wellness bloodwork (CBC, chemistry panel, urinalysis, thyroid) can catch kidney disease, liver issues, diabetes, and thyroid dysfunction years before they become symptomatic. Catching these on bloodwork vs. catching them when your dog is sick is the difference between management and crisis.</p>
                    <div class="info-box">
                        <p><strong>Ask your vet about:</strong> Senior bloodwork panel &middot; Blood pressure measurement (often missed, important in senior dogs) &middot; Dental cleaning (anesthesia risk vs. dental disease risk — often worth it) &middot; Pain assessment for arthritis &middot; Cognitive dysfunction screening</p>
                    </div>
                    <h2>Nutrition and Weight</h2>
                    <p>Obesity in senior dogs directly worsens arthritis, heart disease, and lifespan. A body condition score of 4–5 out of 9 is ideal. You should be able to feel but not see the ribs. Talk to your vet about a senior-appropriate food — many senior dogs do well on a higher-protein diet to maintain muscle mass, contrary to older advice about protein restriction.</p>
                    <h2>How VetGPT Helps</h2>
                    <p>Senior dog health is longitudinal — you're tracking slow changes over months and years. Monthly weight logs, medication records, lump observations, behavioral notes, and vet visit history all become more valuable over time. When your vet asks "has there been any change in drinking?" you want an answer based on actual notes, not memory. VetGPT keeps that history organized and accessible — including the ability to share a complete health summary at any vet appointment.</p>""",
  "faq_html": """                    <h3>When is a dog considered senior?</h3>
                    <p>It depends on size. Large breeds (Great Dane, Mastiff) are senior around 5–6. Medium breeds around 7–8. Small breeds around 9–10. Your vet can give you a breed-specific recommendation.</p>
                    <h3>How often should senior dogs see the vet?</h3>
                    <p>Twice a year. Six months is a long time in a senior dog's life. Standard bloodwork at these visits catches kidney disease, liver issues, diabetes, and thyroid dysfunction before they become symptomatic.</p>
                    <h3>What supplements help senior dogs?</h3>
                    <p>Consult your vet first. Commonly recommended options include omega-3 fatty acids for inflammation and joints, glucosamine/chondroitin for joint support, and probiotics. Not all supplements benefit every dog, and some interact with medications.</p>
                    <h3>What are signs of pain in older dogs?</h3>
                    <p>Changes in movement, behavioral changes (irritability, hiding), altered sleep, reduced interest in activities, or excessive licking of a specific area. Dogs often don't vocalize pain — behavioral changes are the main signal.</p>"""
})

# ── POST 7: Puppy first year ──────────────────────────────────────────────────
posts.append({
  "slug": "puppy-first-year-vet-guide",
  "page_title": "Puppy's First Year: Vet Schedule, Vaccines & Health Milestones | VetGPT",
  "title": "Your Puppy's First Year: The Complete Vet Schedule and Health Milestone Guide",
  "breadcrumb": "Puppy First Year Vet Guide",
  "tag": "🐶 Puppies",
  "date": "2026-03-03",
  "date_display": "March 3, 2026",
  "readtime": "6 min read",
  "meta_description": "The first year of a puppy's life is the most medically dense. Here's the full vet schedule, vaccine timeline, and what to track month by month for a healthy start.",
  "cta_headline": "Track your puppy's health milestones",
  "cta_body": "Vaccine records, vet visits, weight growth curve, and medication logs — all in one place from day one.",
  "faq": [
    ("When should puppies get their first vet visit?", "Within the first week of bringing them home, ideally. Sooner if you notice any health concerns. The first visit establishes a baseline, confirms vaccination history from the breeder or shelter, and starts your relationship with your vet."),
    ("What vaccines do puppies need and when?", "Core vaccines: DHPP (distemper, hepatitis, parvovirus, parainfluenza) starting at 6–8 weeks, boosted every 3–4 weeks until 16 weeks. Rabies at 12–16 weeks. Bordetella (kennel cough) if they'll be around other dogs. Your vet will tailor the schedule to your puppy's risk factors."),
    ("When should I spay or neuter my puppy?", "This varies by breed and size. Traditionally 6 months, but current research suggests waiting until physical maturity for large and giant breeds (12–24 months). Discuss with your vet — the answer is breed and sex specific."),
    ("What should I track during my puppy's first year?", "Weight monthly (or more often for small breeds), vaccine dates and reactions, deworming history, parasite prevention medications, food and any dietary changes, any behavioral or health concerns between visits, and the results of each vet visit.")
  ],
  "related": [
    ("how-to-track-dog-medications.html", "🐕 Dogs", "How to Track Your Dog's Medications (And Never Miss a Dose Again)"),
    ("preparing-for-vet-visit.html", "🏥 Vet Visits", "How to Prepare for a Vet Visit (So You Never Blank at the Worst Moment)")
  ],
  "body": """                    <p>The first year of a puppy's life is the most medically intensive period they'll ever have — more vet visits, more vaccines, more decisions than any subsequent year. Getting it right sets the foundation for their entire life. Getting it wrong means playing catch-up.</p>
                    <p>This guide gives you the full timeline: what happens when, what you need to track, and what questions to ask at each stage.</p>
                    <h2>The Core Vaccine Schedule</h2>
                    <p>Vaccine schedules vary by vet, region, and your puppy's specific risk factors — but here's the standard framework:</p>
                    <div class="checklist-card">
                        <h3>💉 Core Vaccine Timeline</h3>
                        <ul>
                            <li><strong>6–8 weeks:</strong> First DHPP (distemper, hepatitis, parvo, parainfluenza). Often given by breeder — get documentation.</li>
                            <li><strong>10–12 weeks:</strong> Second DHPP booster. Bordetella if they'll be around other dogs. Leptospirosis in high-risk areas.</li>
                            <li><strong>14–16 weeks:</strong> Third DHPP booster. Rabies vaccine (legally required in most states). Second Bordetella if needed.</li>
                            <li><strong>12–16 months:</strong> Boosters for DHPP and rabies. Then adult schedule (every 1–3 years depending on vaccine type).</li>
                        </ul>
                    </div>
                    <p>Keep every vaccine record. If you lose the paperwork from the breeder or shelter, reconstructing it is difficult. Photograph everything and log it.</p>
                    <h2>Month-by-Month Health Milestones</h2>
                    <h3>Months 1–3: Foundation</h3>
                    <p>First vet visit within the first week home. Physical exam confirms what the breeder or shelter told you. Fecal exam for parasites — many puppies have worms regardless of source. Begin heartworm and flea prevention. Establish baseline weight. Start a feeding schedule and track growth.</p>
                    <h3>Months 3–6: Socialization and Development</h3>
                    <p>Socialization window is closing — prioritize positive exposure to people, other dogs, environments, and sounds. Vet visits for boosters continue. Watch for limping in large breeds — rapid growth can cause joint issues (panosteitis, HOD). Monthly weigh-ins help track growth curve. Puppy classes are worth the investment — they're medical history, not just training.</p>
                    <h3>Months 6–12: Maturation</h3>
                    <p>The spay/neuter decision window (discuss with your vet based on breed and size). Transition to adult food — timing varies by breed size. Small breeds may switch at 9 months; giant breeds may stay on puppy food until 18 months. Adult teeth fully in by 7 months — first dental check. Establish exercise routines appropriate to their breed and joint development.</p>
                    <h2>Parasite Prevention: The Ongoing Commitment</h2>
                    <p>Heartworm prevention is monthly and lifelong — in most of the US, year-round. Missing doses has real consequences. Flea and tick prevention depends on your region and lifestyle. Get your vet's specific recommendation, then track it. The most common mistake is assuming a dose was given when it wasn't.</p>
                    <div class="checklist-card">
                        <h3>🗓️ Track Every Month</h3>
                        <ul>
                            <li>Heartworm prevention — date given, product name</li>
                            <li>Flea/tick prevention — date applied or given</li>
                            <li>Weight — puppies should grow steadily; sudden weight loss in a puppy needs vet attention</li>
                            <li>Any behavioral or physical changes since last visit</li>
                            <li>Food — what they're eating, how much, any changes</li>
                        </ul>
                    </div>
                    <h2>When to Call the Vet Between Visits</h2>
                    <div class="warn-box">
                        <p><strong>Call your vet for:</strong> Vomiting or diarrhea more than once &middot; Not eating for more than 12 hours &middot; Lethargy or unusual weakness &middot; Limping that doesn't resolve in 24 hours &middot; Coughing or sneezing persistently &middot; Any suspected ingestion of something toxic &middot; Vaccine reaction (swelling, hives, vomiting within hours of vaccination)</p>
                    </div>
                    <h2>How VetGPT Helps</h2>
                    <p>The first year generates a lot of records: multiple vet visits, multiple vaccine certificates, deworming records, parasite prevention logs, growth tracking. VetGPT keeps all of it organized — including the ability to photograph and scan documents from the breeder or shelter so nothing gets lost. When your puppy becomes an adult dog, their complete history from day one is right there.</p>""",
  "faq_html": """                    <h3>When should puppies get their first vet visit?</h3>
                    <p>Within the first week of bringing them home. The first visit establishes a baseline, confirms vaccination history, and starts your relationship with your vet. Go sooner if you notice any health concerns.</p>
                    <h3>What vaccines do puppies need and when?</h3>
                    <p>Core vaccines: DHPP starting at 6–8 weeks, boosted every 3–4 weeks until 16 weeks. Rabies at 12–16 weeks. Bordetella if they'll be around other dogs. Your vet will tailor the schedule to your puppy's specific risk factors and location.</p>
                    <h3>When should I spay or neuter my puppy?</h3>
                    <p>This varies by breed and size. Traditionally 6 months, but current research suggests waiting until physical maturity for large and giant breeds (12–24 months). Discuss with your vet — the answer is breed and sex specific.</p>
                    <h3>What should I track during my puppy's first year?</h3>
                    <p>Weight monthly, vaccine dates and any reactions, deworming history, parasite prevention medications, food and dietary changes, and the results of each vet visit.</p>"""
})

# ── POST 8: Hamster health ────────────────────────────────────────────────────
posts.append({
  "slug": "hamster-health-signs",
  "page_title": "Hamster Health Signs: What's Normal and What Needs a Vet | VetGPT",
  "title": "Hamster Health Signs: What's Normal, What's Not, and When to See a Vet",
  "breadcrumb": "Hamster Health Signs",
  "tag": "🐹 Small Mammals",
  "date": "2026-03-03",
  "date_display": "March 3, 2026",
  "readtime": "5 min read",
  "meta_description": "Hamsters have short lifespans and hide illness fast. Here's how to read normal vs. concerning signs, daily checks, and when to find an exotic vet.",
  "cta_headline": "Track your hamster's health with VetGPT",
  "cta_body": "Daily logs, weight tracking, vet visit records, and AI chat for small mammal questions. Free during early release.",
  "faq": [
    ("How do I know if my hamster is sick?", "Key signs: wet or matted fur around the tail (wet tail — serious), weight loss, not eating or drinking, lethargy beyond their normal sleep schedule, discharge from eyes or nose, labored breathing, or a tilted head. Hamsters hide illness well; changes from their normal behavior are the main signal."),
    ("What is wet tail in hamsters?", "Wet tail (proliferative ileitis) is a serious bacterial infection that causes severe diarrhea and can be fatal within 24–48 hours. Signs: wet, matted fur around the tail and bottom, strong odor, lethargy, hunched posture. Requires emergency vet treatment immediately."),
    ("How long do hamsters live?", "Syrian hamsters typically live 2–3 years. Dwarf hamsters (Campbell's, Winter White, Roborovski) often live 1.5–2.5 years. After age 1.5, health monitoring becomes more important as age-related conditions become more common."),
    ("Do hamsters need vet visits?", "Yes. Annual wellness checks are recommended, and any time you notice health changes. Finding an exotic vet who sees small mammals before you need one urgently is important — not all vets see hamsters.")
  ],
  "related": [
    ("guinea-pig-health-checklist.html", "🐹 Small Mammals", "Guinea Pig Health Checklist: What to Check Every Day"),
    ("rabbit-health-checklist.html", "🐰 Rabbits", "Rabbit Health Checklist: Daily and Weekly Care for a Long Life")
  ],
  "body": """                    <p>Hamsters pack a lot of life into a short time — typically 2–3 years for Syrians, slightly less for most dwarfs. That compressed lifespan means health changes move fast. A hamster who was fine yesterday can be seriously ill today, and the signs are easy to miss if you don't know what normal looks like.</p>
                    <p>This guide covers normal hamster behavior, daily health checks, the most urgent warning signs, and what to do when something seems off.</p>
                    <h2>Know Your Hamster's Normal</h2>
                    <p>Before you can spot what's wrong, you need to know what's right for your individual hamster. Spend a few minutes each evening when they're naturally active observing: how much they eat, how much they drink, how active they are, where they sleep, what their coat looks like, what their stool looks like. This is your baseline.</p>
                    <p>Syrian hamsters are solitary and nocturnal — they'll sleep most of the day and become active at dusk. Dwarf hamsters may be active at multiple points throughout the day. Waking a sleeping hamster to check if they're alive is normal owner behavior; a hamster who doesn't wake when gently disturbed (and who isn't in torpor) needs attention.</p>
                    <h2>Daily Checks (Takes 2 Minutes)</h2>
                    <div class="checklist-card">
                        <h3>🌅 Every Day</h3>
                        <ul>
                            <li>Is there fresh food in the bowl? Did they eat and cache overnight?</li>
                            <li>Is the water bottle working and depleted slightly? (Check the ball bearing — these clog)</li>
                            <li>Are they responsive when gently disturbed during their sleeping period?</li>
                            <li>Any unusual smell from the enclosure? (Wet tail has a distinctive foul odor)</li>
                            <li>Check the tail area — should be dry and clean</li>
                            <li>Normal stool in the enclosure — small, firm, dry pellets</li>
                        </ul>
                    </div>
                    <h2>The Most Urgent Warning Sign: Wet Tail</h2>
                    <div class="warn-box">
                        <p><strong>Wet tail is an emergency.</strong> Signs: wet, matted fur around the tail and anus, strong unpleasant odor, lethargy, hunched posture, possibly diarrhea. This is most common in Syrian hamsters under 12 weeks, often triggered by stress (new home, transport). If you see it, call an exotic vet immediately — wet tail can be fatal within 24–48 hours without treatment.</p>
                    </div>
                    <h2>Other Signs That Need Vet Attention</h2>
                    <ul>
                        <li><strong>Weight loss</strong> — weigh monthly. A hamster losing weight may have dental issues preventing proper eating, or an internal problem.</li>
                        <li><strong>Head tilt</strong> — can indicate an ear infection or neurological issue. Seek vet care promptly.</li>
                        <li><strong>Discharge from eyes or nose</strong> — often a respiratory infection, which spreads fast.</li>
                        <li><strong>Labored breathing or wheezing</strong> — respiratory infections in hamsters progress quickly.</li>
                        <li><strong>Lumps or bumps</strong> — tumors are common in hamsters, especially Syrians over 1.5 years. Many are treatable if caught early.</li>
                        <li><strong>Paralysis or loss of coordination</strong> — can be neurological or a sign of severe illness.</li>
                        <li><strong>Not coming out at all during their normal active period</strong> — a hamster who isn't active for multiple nights running isn't just tired.</li>
                    </ul>
                    <h2>Hibernation vs. Torpor vs. Death</h2>
                    <p>Hamsters can enter torpor (a short-term state of reduced body temperature and activity) when they get cold. A hamster in torpor feels cold to the touch, has slowed breathing, and may appear dead. Warm them gradually in your hands — they should revive within 30–60 minutes. If the temperature in their space is dropping below 60°F regularly, address the heating.</p>
                    <p>True hibernation is rare in domestic hamsters but can occur. A hamster that doesn't revive with warming, or that is limp with no response at all, needs emergency vet care.</p>
                    <h2>Find an Exotic Vet Before You Need One</h2>
                    <p>Not all veterinary practices see hamsters. Finding one now — before you have an emergency — is essential. Search for "exotic vet" or "small mammal vet" in your area. Call ahead to confirm they see hamsters and have experience with them.</p>
                    <h2>How VetGPT Helps</h2>
                    <p>For a small animal with a short lifespan, consistent logging matters. VetGPT tracks weight, behavioral notes, vet visits, and medications for hamsters. The AI chat can help you assess whether what you're seeing is concerning or normal — based on your hamster's specific history and logs.</p>""",
  "faq_html": """                    <h3>How do I know if my hamster is sick?</h3>
                    <p>Key signs: wet or matted fur around the tail (wet tail — very serious), weight loss, not eating or drinking, lethargy beyond normal sleep, discharge from eyes or nose, labored breathing, or head tilting. Changes from their normal behavior are the main signal.</p>
                    <h3>What is wet tail in hamsters?</h3>
                    <p>A serious bacterial infection causing severe diarrhea, most common in young Syrian hamsters. Signs: wet matted fur around the tail, strong odor, lethargy, hunched posture. Can be fatal within 24–48 hours — requires emergency vet treatment immediately.</p>
                    <h3>How long do hamsters live?</h3>
                    <p>Syrian hamsters typically 2–3 years. Dwarf hamsters 1.5–2.5 years. Health monitoring becomes more important after age 1.5 as age-related conditions increase.</p>
                    <h3>Do hamsters need vet visits?</h3>
                    <p>Yes. Annual wellness checks are recommended, plus any time you notice changes. Find an exotic vet who sees small mammals before you need one urgently — not all vets see hamsters.</p>"""
})

# ── POST 9: Rabbit health ─────────────────────────────────────────────────────
posts.append({
  "slug": "rabbit-health-checklist",
  "page_title": "Rabbit Health Checklist: Daily and Weekly Care for a Long Life | VetGPT",
  "title": "Rabbit Health Checklist: Daily and Weekly Care for a Long, Healthy Life",
  "breadcrumb": "Rabbit Health Checklist",
  "tag": "🐰 Rabbits",
  "date": "2026-03-03",
  "date_display": "March 3, 2026",
  "readtime": "6 min read",
  "meta_description": "Rabbits hide illness and can crash fast. Here's the complete health checklist for daily and weekly rabbit care — including the signs that need same-day vet attention.",
  "cta_headline": "Track your rabbit's health with VetGPT",
  "cta_body": "Feeding logs, weight tracking, vet visits, and AI chat built for exotic pets. Free during early release.",
  "faq": [
    ("What is GI stasis in rabbits?", "GI stasis is a life-threatening slowdown or stoppage of the digestive system. Signs: not eating (especially refusing hay), no droppings or very small droppings, a hunched posture, loud gurgling or silence from the gut, and lethargy. It can become fatal within 24 hours and requires same-day emergency vet care."),
    ("How often should rabbits see the vet?", "Annually for wellness exams, twice yearly for rabbits over 5 years. Find a rabbit-savvy vet (often listed as 'exotic' or 'small mammal') before you need one — not all general practice vets are experienced with rabbits."),
    ("What should rabbits eat?", "Unlimited timothy hay (80% of their diet), fresh leafy greens daily (romaine, cilantro, parsley — avoid iceberg lettuce and high-sugar vegetables), and a limited amount of plain pellets. No fruit or treats except as very occasional small amounts. Hay is non-negotiable — it maintains gut motility and dental health."),
    ("What are signs of dental disease in rabbits?", "Drooling or wet chin, dropping food while eating, weight loss despite appearing to try to eat, watery eyes, and facial swelling. Rabbit teeth grow continuously — misalignment (malocclusion) causes overgrowth that needs regular veterinary management.")
  ],
  "related": [
    ("guinea-pig-health-checklist.html", "🐹 Small Mammals", "Guinea Pig Health Checklist: What to Check Every Day"),
    ("hamster-health-signs.html", "🐹 Small Mammals", "Hamster Health Signs: What's Normal and What Needs a Vet")
  ],
  "body": """                    <p>Rabbits are often underestimated as pets — seen as low-maintenance starter animals when they're actually complex, sensitive creatures with specific needs and a surprising ability to hide serious illness. A rabbit who stops eating is a medical emergency. A rabbit with a dental problem may lose significant weight before showing obvious signs. The difference between good and poor outcomes in rabbit health is almost always early detection.</p>
                    <p>This checklist covers what you should check every single day, what to look at weekly, and the warning signs that mean "get to a vet now."</p>
                    <h2>The Most Important Number: Is Your Rabbit Eating Hay?</h2>
                    <p>Before anything else, every day: is your rabbit eating hay? Hay should make up 80% of their diet and it's not optional — it maintains gut motility (preventing GI stasis) and wears down their continuously growing teeth. A rabbit who stops eating hay for more than a few hours needs assessment. A rabbit who hasn't eaten in 12 hours needs a vet call.</p>
                    <h2>Daily Checks</h2>
                    <div class="checklist-card">
                        <h3>🌅 Every Day</h3>
                        <ul>
                            <li>Eating hay — this is the most critical daily check</li>
                            <li>Droppings — check for normal round, firm cecotropes and regular fecal pellets. Absence of droppings, very small droppings, or strung-together droppings (like a pearl necklace) indicate a problem.</li>
                            <li>Alert and responsive — a rabbit that doesn't greet you or ignores stimulation may be unwell</li>
                            <li>Breathing — normal resting respiratory rate is 30–60 breaths per minute. Labored or open-mouth breathing is an emergency.</li>
                            <li>Eyes and nose — clear, no discharge. Eyes should be bright and alert.</li>
                            <li>Posture — a hunched, tense posture (especially with teeth grinding) often indicates abdominal pain</li>
                            <li>Water consumption — know their baseline. Significant changes warrant attention.</li>
                        </ul>
                    </div>
                    <h2>GI Stasis: Know It, Fear It</h2>
                    <div class="warn-box">
                        <p><strong>GI stasis is an emergency.</strong> If your rabbit hasn't eaten in 12+ hours, has produced few or no droppings, is sitting hunched with teeth grinding, or has a hard and distended abdomen — this is same-day emergency care. GI stasis can become fatal within 24 hours. Do not wait to see if it improves on its own.</p>
                    </div>
                    <h2>Weekly Checks</h2>
                    <div class="checklist-card">
                        <h3>📅 Every Week</h3>
                        <ul>
                            <li>Weight — use a kitchen scale. Log it. Weight loss is often the first sign of dental disease, kidney disease, or other illness.</li>
                            <li>Teeth — the front incisors should be aligned and not overgrown. You can't check the back molars at home, which is why regular exotic vet visits matter.</li>
                            <li>Fur and skin — check for bald patches, mats (especially in the dewlap of females), or signs of mites. Fly strike (flystrike) risk in outdoor rabbits in warm weather — check under the tail.</li>
                            <li>Nails — overgrown nails curl and cause pain. Clip or have them trimmed every 4–6 weeks.</li>
                            <li>Ears — clean, no dark debris, no head shaking. Ear mites cause intense discomfort.</li>
                            <li>Scent glands — two small pouches near the genitals can become packed with a dark waxy material. Clean gently if needed; buildup can become painful.</li>
                        </ul>
                    </div>
                    <h2>Dental Disease</h2>
                    <p>Rabbit teeth grow continuously throughout their life. Without proper hay consumption to wear them down naturally, and without the genetic foundation for well-aligned teeth (a lottery), malocclusion develops. The molars are affected first — you can't see them at home, but your rabbit will show signs: drooling, dropping food, weight loss, watery eyes.</p>
                    <p>Some rabbits need dental procedures every few months. Find a rabbit-savvy vet who can examine the molars properly and have teeth checked at least annually.</p>
                    <h2>How VetGPT Helps</h2>
                    <p>Rabbit health requires tracking patterns — daily hay intake, droppings, weight over time. These patterns tell the story. VetGPT logs all of it in one place, tracks weight trends so you can see changes before they become obvious, and stores vet visit records so you have a complete history when you need it. The AI chat understands rabbit-specific health — not just generic small animal information.</p>""",
  "faq_html": """                    <h3>What is GI stasis in rabbits?</h3>
                    <p>A life-threatening slowdown or stoppage of the digestive system. Signs: not eating (especially refusing hay), no droppings or very small droppings, hunched posture, lethargy. Can be fatal within 24 hours — requires same-day emergency vet care.</p>
                    <h3>How often should rabbits see the vet?</h3>
                    <p>Annually for wellness exams, twice yearly for rabbits over 5. Find a rabbit-savvy vet (often listed as exotic or small mammal) before you need one — not all general practice vets are experienced with rabbits.</p>
                    <h3>What should rabbits eat?</h3>
                    <p>Unlimited timothy hay (80% of diet), fresh leafy greens daily, limited plain pellets. Hay is non-negotiable — it maintains gut motility and dental health. No fruit except as very occasional small amounts.</p>
                    <h3>What are signs of dental disease in rabbits?</h3>
                    <p>Drooling or wet chin, dropping food while eating, weight loss despite trying to eat, watery eyes, facial swelling. Rabbit teeth grow continuously — misalignment causes overgrowth that needs regular veterinary management.</p>"""
})

# ── POST 10: Backyard chicken health ──────────────────────────────────────────
posts.append({
  "slug": "backyard-chicken-health-guide",
  "page_title": "Backyard Chicken Health Guide: Flock Monitoring & Common Illnesses | VetGPT",
  "title": "Backyard Chicken Health Guide: How to Monitor Your Flock and Spot Problems Early",
  "breadcrumb": "Backyard Chicken Health Guide",
  "tag": "🐔 Poultry",
  "date": "2026-03-04",
  "date_display": "March 4, 2026",
  "readtime": "6 min read",
  "meta_description": "Keeping backyard chickens healthy means knowing what normal looks like and catching problems early. Here's the complete flock monitoring guide for small flock owners.",
  "cta_headline": "Track your flock's health with VetGPT",
  "cta_body": "VetGPT supports chickens and poultry with flock logs, individual bird health records, and AI chat for poultry health questions.",
  "faq": [
    ("How do I know if a chicken is sick?", "Key signs: separation from the flock, puffed feathers, lethargy, reduced or absent egg production, changes in droppings, labored breathing, discharge from eyes or nostrils, pale comb, or loss of appetite. Chickens hide illness and often separate from the flock when unwell."),
    ("What are the most common backyard chicken illnesses?", "Respiratory diseases (Mycoplasma, infectious bronchitis), Marek's disease, coccidiosis (bloody droppings in young birds), egg binding in hens, bumblefoot, mites and lice, and Fowl pox. Many are preventable with vaccination, biosecurity, and clean housing."),
    ("Do backyard chickens need vet care?", "Yes. Finding a poultry-experienced vet before you have an emergency is important. Fecal testing annually for parasite load, treatment for individual sick birds, and biosecurity advice are all legitimate vet services for backyard flocks."),
    ("How often should I clean a chicken coop?", "Full cleaning and disinfecting monthly minimum. Spot clean (remove obvious droppings and soiled bedding) daily or every few days. Deep litter method can extend full cleaning intervals but requires active management. Clean water and feeders daily.")
  ],
  "related": [
    ("bearded-dragon-health-checklist.html", "🦎 Reptiles", "The Complete Bearded Dragon Health Checklist"),
    ("rabbit-health-checklist.html", "🐰 Rabbits", "Rabbit Health Checklist: Daily and Weekly Care for a Long Life")
  ],
  "body": """                    <p>Backyard chicken keeping has exploded in popularity, and with it comes a learning curve that most new flock owners hit the hard way — discovering an ill bird too late to help. Chickens are prey animals with a strong instinct to mask illness. A hen who looks fine in the morning can be in serious distress by evening, and the lag time is reduced when you know what to look for.</p>
                    <p>This guide is for small flock owners who want to monitor their birds proactively, not reactively.</p>
                    <h2>Daily Flock Observation</h2>
                    <p>The most valuable health tool you have is consistent daily observation. Most experienced chicken keepers do a quick scan every morning when they open the coop and again in the evening. You're not running a clinical exam — you're looking for deviations from normal.</p>
                    <div class="checklist-card">
                        <h3>🌅 Every Morning</h3>
                        <ul>
                            <li>Is every bird present and out of the nest box? (A hen in the nest all morning may be egg-bound or ill)</li>
                            <li>Normal activity level — scratching, foraging, interacting with flock?</li>
                            <li>Any bird separated from the flock or being picked on? (Chickens pick on weak birds — isolation is a red flag)</li>
                            <li>Comb and wattles — should be red and plump. Pale, purple-tinged, or shrunken combs indicate illness or stress.</li>
                            <li>Droppings on the coop floor — know what normal looks like. Cecal droppings (brown and smelly, about once daily) are normal. Runny, bloody, or very off-color droppings warrant attention.</li>
                            <li>Fresh water and feed available</li>
                        </ul>
                    </div>
                    <h2>What to Look for in Individual Birds</h2>
                    <p>When you handle birds (which should happen regularly so they're accustomed to it), look at:</p>
                    <ul>
                        <li><strong>Body condition</strong> — feel the keel bone (breastbone). Should be covered with muscle, not protruding sharply. A sharp keel means a bird is underweight.</li>
                        <li><strong>Feather condition</strong> — normal, glossy feathers vs. dull, broken, or missing patches (which can indicate mites, lice, or pecking)</li>
                        <li><strong>Eyes</strong> — clear, bright. Discharge or cloudy eyes need attention.</li>
                        <li><strong>Nostrils</strong> — clean. Discharge can indicate respiratory disease.</li>
                        <li><strong>Vent area</strong> — clean and dry. Pastiness (matted droppings) in chicks is life-threatening. Damp or dirty vent in adults can attract flies.</li>
                        <li><strong>Feet and legs</strong> — check for bumblefoot (swollen, scabby footpad — an infection that needs treatment) and scaly leg mites (scales lifted and crusty).</li>
                    </ul>
                    <h2>Egg Production as a Health Indicator</h2>
                    <p>Know each hen's normal egg production. A sudden drop in production can indicate stress, poor nutrition, illness, molt onset, or shortened days — but sustained drops outside of normal molt and winter cycles warrant investigation. An individual hen who stops laying entirely and looks unwell may be egg-bound (a medical emergency).</p>
                    <div class="warn-box">
                        <p><strong>Egg binding is an emergency.</strong> Signs: straining without producing an egg, penguin-like gait, sitting fluffed and lethargic, abdomen visibly swollen. A retained egg can rupture internally. Warm baths and gentle steam may help; if no egg within a few hours, seek veterinary care.</p>
                    </div>
                    <h2>Respiratory Disease</h2>
                    <p>Respiratory disease spreads fast through a flock. Signs: sneezing, rattling breathing, nasal discharge, facial swelling, reduced activity. Quarantine any bird showing respiratory symptoms immediately — before it spreads. Many respiratory diseases in chickens are manageable with treatment but become flock-wide problems without quarantine.</p>
                    <p>Biosecurity basics: quarantine new birds for 30 days before introducing to your flock. Limit wild bird access to feed and water. Disinfect equipment between flocks.</p>
                    <h2>Mites and Lice</h2>
                    <p>Mites and lice are common in backyard flocks and worth checking for monthly — especially red mite (Dermanyssus gallinae), which lives in the coop rather than on the birds and feeds at night. Signs of mite infestation: birds reluctant to enter the coop at night, pale combs from blood loss, excessive preening. Inspect the coop seams at night with a flashlight — red mites appear as moving red or grey dots.</p>
                    <h2>How VetGPT Helps</h2>
                    <p>VetGPT supports chickens and backyard poultry — including per-bird health records for small flocks and flock-level notes. Log egg production, treatments, individual observations, and vet visits. The AI chat understands poultry health specifically, not just generic bird information.</p>""",
  "faq_html": """                    <h3>How do I know if a chicken is sick?</h3>
                    <p>Key signs: separation from the flock, puffed feathers, lethargy, reduced egg production, changes in droppings, labored breathing, discharge from eyes or nostrils, pale or purple comb, loss of appetite. Chickens hide illness and often separate from the flock when unwell.</p>
                    <h3>What are the most common backyard chicken illnesses?</h3>
                    <p>Respiratory diseases (Mycoplasma, infectious bronchitis), Marek's disease, coccidiosis, egg binding, bumblefoot, mites and lice, and Fowl pox. Many are preventable with vaccination, biosecurity, and clean housing.</p>
                    <h3>Do backyard chickens need vet care?</h3>
                    <p>Yes. Find a poultry-experienced vet before you have an emergency. Fecal testing, treatment for individual sick birds, and biosecurity advice are all legitimate vet services for backyard flocks.</p>
                    <h3>How often should I clean a chicken coop?</h3>
                    <p>Full cleaning and disinfecting monthly minimum. Spot clean daily or every few days. Fresh water and feeders should be cleaned daily.</p>"""
})

# ── POST 11: Ball python care ─────────────────────────────────────────────────
posts.append({
  "slug": "ball-python-care-guide",
  "page_title": "Ball Python Health & Care Guide: Feeding, Shedding & Vet Signs | VetGPT",
  "title": "Ball Python Care Guide: Feeding Schedules, Shedding, and Signs of Illness",
  "breadcrumb": "Ball Python Care Guide",
  "tag": "🐍 Reptiles",
  "date": "2026-03-04",
  "date_display": "March 4, 2026",
  "readtime": "6 min read",
  "meta_description": "Ball pythons are hardy but have specific care needs. Here's what to track for feeding, shedding, and health — plus the signs that need a reptile vet.",
  "cta_headline": "Track your ball python's health with AI",
  "cta_body": "Feeding logs, shedding cycles, weight tracking, and husbandry records for ball pythons. Free during early release.",
  "faq": [
    ("How often should I feed my ball python?", "Hatchlings (under 200g): every 5–7 days. Juveniles (200g–500g): every 7–10 days. Adults (500g+): every 10–14 days. Feed appropriately sized prey — roughly the width of the snake's widest point. Always feed pre-killed or frozen/thawed for safety."),
    ("Why won't my ball python eat?", "Ball pythons are notorious for food refusal. Common causes: shedding cycle (normal — many refuse during), breeding season (adults, especially males in fall/winter), husbandry issues (incorrect temps or humidity), stress from handling or enclosure changes, or illness. A healthy adult refusing for 2–4 weeks is usually fine. Prolonged refusal with weight loss needs vet attention."),
    ("How do I know if my ball python's shed is complete?", "Check the eye caps and tail tip — these are the most commonly retained shed areas. The shed should come off in one piece. A retained eye cap looks like a dull film over the eye after shed. Do not forcibly remove retained shed — soak the snake in shallow lukewarm water and let it come off naturally, or see a vet."),
    ("What are signs of illness in ball pythons?", "Respiratory infection signs: wheezing, mucus from mouth or nostrils, open-mouth breathing, holding the head up. Other concerns: retained shed, weight loss despite feeding, mites (small moving dots on the snake or enclosure), irregular movement, lumps or swelling, and incomplete muscle tone.")
  ],
  "related": [
    ("bearded-dragon-health-checklist.html", "🦎 Reptiles", "The Complete Bearded Dragon Health Checklist"),
    ("reptile-health-tracker-guide.html", "🦎 Reptiles", "Why Every Reptile Owner Needs a Health Tracker")
  ],
  "body": """                    <p>Ball pythons are one of the most popular pet snakes for good reason — they're generally docile, manageable in size, and can thrive for 20–30 years with proper care. But "easy" is relative. They have specific environmental requirements, a notorious reputation for food refusal that can send new owners into a panic, and a real vulnerability to respiratory infections when conditions aren't right.</p>
                    <p>This guide focuses on the tracking and observation habits that keep ball pythons healthy long-term.</p>
                    <h2>Husbandry: The Foundation of Health</h2>
                    <p>Most ball python illness is preventable with correct husbandry. The two most common problems are respiratory infections from low temperatures or high humidity issues, and stuck shed from low humidity. Get the environment right first.</p>
                    <div class="checklist-card">
                        <h3>🌡️ Daily Husbandry Checks</h3>
                        <ul>
                            <li>Warm side temperature: 88–92°F (surface), 80–85°F ambient</li>
                            <li>Cool side: 76–80°F</li>
                            <li>Humidity: 60–80% baseline; 80–90% during shed</li>
                            <li>Both hides should be present and positioned correctly (warm and cool side)</li>
                            <li>Fresh water in a dish large enough to soak in</li>
                            <li>Any soaking in the water dish? (Often indicates stuck shed or mites)</li>
                        </ul>
                    </div>
                    <h2>Feeding Logs: Why They Matter</h2>
                    <p>Ball pythons' food refusal is legendary — and without a feeding log, it's easy to lose track of how long it's actually been. "He hasn't eaten in a while" is different from "he's refused 8 consecutive meals over 16 weeks with 10% weight loss." The log tells the real story.</p>
                    <p>Track every feeding attempt: date, prey type and size, whether it was accepted, and if refused — how the prey was offered. This data is what your vet needs and what helps you identify patterns (does she always refuse during cooler months? Always eat within an hour of lights out?).</p>
                    <h2>Shedding Cycles</h2>
                    <p>Ball pythons shed every 4–6 weeks on average when young, less frequently as adults. Know your snake's normal shedding frequency — any significant change in cycle length can indicate a health change.</p>
                    <p>Signs an upcoming shed: eyes turn blue or cloudy (the "blue" phase), color dulls, behavior may change (more defensive, less active, often refuses food). This is all normal. Increased humidity to 80–90% helps the shed come off cleanly.</p>
                    <p>After a shed: always check that eye caps came off. Hold the shed up to light and confirm there are two clear circular windows where the eyes were. If not — the eye caps are retained on the snake.</p>
                    <h2>Monthly Weight Checks</h2>
                    <p>Weigh monthly. A food-refusing ball python who is maintaining weight is not a concern. A ball python losing weight over multiple months is. Adults can lose some weight during fasting seasons (especially breeding season) and recover it when they resume eating — but significant or persistent loss needs vet evaluation.</p>
                    <div class="warn-box">
                        <p><strong>See a reptile vet for:</strong> Open-mouth breathing or wheezing &middot; Mucus from mouth or nostrils &middot; Retained eye caps after shed &middot; Mites (check along the spine seam, around the eyes, in water dish) &middot; Progressive weight loss &middot; Lumps, asymmetry, or swelling &middot; Abnormal muscle tone or inability to right itself when placed on its back</p>
                    </div>
                    <h2>Mites: Catch Them Early</h2>
                    <p>Snake mites (Ophionyssus natricis) are tiny — about the size of a period — and dark red or black. They spread fast. Signs: tiny moving dots on the snake's skin (often around the eyes or in the water dish), the snake soaking constantly, or you finding mites on your hands after handling. Mites are treatable but require treating both the snake and the entire enclosure simultaneously.</p>
                    <h2>How VetGPT Helps</h2>
                    <p>Ball pythons need longitudinal tracking — feeding history over months, shedding cycles, weight trends. VetGPT tracks all of it. Feeding logs show patterns. Weight charts show trends. Shedding history reveals cycle changes. The AI chat understands ball python biology and can help you assess whether what you're seeing is normal variation or a flag to call your reptile vet.</p>""",
  "faq_html": """                    <h3>How often should I feed my ball python?</h3>
                    <p>Hatchlings (under 200g): every 5–7 days. Juveniles: every 7–10 days. Adults: every 10–14 days. Feed prey roughly the width of the snake's widest point. Always use pre-killed or frozen/thawed prey.</p>
                    <h3>Why won't my ball python eat?</h3>
                    <p>Common causes: shedding cycle (normal), breeding season, husbandry issues, stress, or illness. A healthy adult refusing for 2–4 weeks is usually fine. Prolonged refusal with weight loss needs vet attention.</p>
                    <h3>How do I know if my ball python's shed is complete?</h3>
                    <p>Check that the eye caps came off — hold the shed up to light and look for two clear circles where the eyes were. A retained eye cap looks like a dull film over the eye. Soak in shallow lukewarm water to help — don't forcibly remove.</p>
                    <h3>What are signs of illness in ball pythons?</h3>
                    <p>Respiratory infection: wheezing, mucus from mouth or nostrils, open-mouth breathing. Other concerns: retained shed, weight loss despite feeding, mites, irregular movement, lumps or swelling.</p>"""
})

# ── POST 12: Cat not eating ───────────────────────────────────────────────────
posts.append({
  "slug": "cat-not-eating-what-to-do",
  "page_title": "Cat Not Eating: Causes, What to Do, and When to See a Vet | VetGPT",
  "title": "Cat Not Eating: What Causes It, What to Do, and When It's an Emergency",
  "breadcrumb": "Cat Not Eating Guide",
  "tag": "🐱 Cats",
  "date": "2026-03-04",
  "date_display": "March 4, 2026",
  "readtime": "5 min read",
  "meta_description": "A cat who stops eating for more than 24 hours needs attention — hepatic lipidosis can develop fast. Here's what causes food refusal in cats and when to call the vet.",
  "cta_headline": "Keep a feeding log for your cat",
  "cta_body": "Track meals, appetite changes, and vet visits with VetGPT. Spot patterns before they become problems.",
  "faq": [
    ("How long can a cat go without eating?", "Not long safely. Cats who stop eating for 24–48 hours are at risk of hepatic lipidosis (fatty liver disease), especially if they are overweight. Unlike dogs, cats cannot safely fast for extended periods. If your cat hasn't eaten in 24 hours, call your vet."),
    ("What are common reasons cats stop eating?", "Illness or pain (dental disease is very common), stress or environmental change, new food or food the cat has decided they don't like, nausea from a medication, upper respiratory infection (loss of smell reduces appetite), a foreign object obstruction, or psychological factors like grief or anxiety."),
    ("How do I get my cat to eat?", "Warm the food slightly (enhances smell). Try different textures — some cats switch between wet and dry preferences. A different flavor or protein source. Hand-feeding small amounts. Reduced meal size with more frequent offerings. But if it's been 24 hours, these tips matter less than calling your vet — appetite loss this long needs medical evaluation, not food tricks."),
    ("Is it normal for cats to be picky eaters?", "Some preference is normal, but dramatic food refusal or going from eating normally to refusing food is a health signal, not just pickiness. Cats who have eaten the same food for months and suddenly refuse it often have an underlying reason — dental pain, nausea, or illness — not a preference change.")
  ],
  "related": [
    ("cat-health-tracker-guide.html", "🐱 Cats", "How to Track Your Cat's Health (Because Cats Won't Tell You When Something's Wrong)"),
    ("preparing-for-vet-visit.html", "🏥 Vet Visits", "How to Prepare for a Vet Visit (So You Never Blank at the Worst Moment)")
  ],
  "body": """                    <p>When a dog skips a meal, it's often not concerning. When a cat stops eating, it's a different situation entirely. Cats who don't eat for 24–48 hours are at real risk of hepatic lipidosis — a liver condition triggered when the body mobilizes fat reserves too quickly in a cat who isn't eating. It can develop fast and become serious. Understanding why your cat isn't eating is important, but so is acting quickly.</p>
                    <h2>The 24-Hour Rule</h2>
                    <p>A cat who hasn't eaten in 24 hours should be assessed by a vet — or at minimum, have you on the phone with one. This is especially true for overweight cats, who develop hepatic lipidosis faster, and for cats who have never skipped meals before. A known picky eater who sometimes skips meals has a different risk profile than a cat who suddenly stops eating entirely.</p>
                    <h2>Most Common Causes</h2>
                    <h3>Dental Pain</h3>
                    <p>One of the most common and most missed causes. A cat with a broken tooth, abscess, or severe gum disease may stop eating because eating hurts. Signs: chewing on one side, dropping food, drooling, or being interested in food but then backing away from the bowl. Dental disease in cats is extremely common — estimates suggest over 50% of cats over 3 have some form of dental disease.</p>
                    <h3>Upper Respiratory Infection</h3>
                    <p>Cats rely heavily on smell to identify and enjoy food. An upper respiratory infection (cat flu) congests the nasal passages and kills appetite. Signs: sneezing, nasal discharge, watery eyes, and reduced appetite. Warming food strongly helps — the increased aroma compensates somewhat for reduced smell.</p>
                    <h3>Nausea</h3>
                    <p>Nausea from any cause — kidney disease, liver disease, medication side effects, hairballs, pancreatitis, or toxin ingestion — reduces appetite. A nauseated cat may sit near the food bowl but not eat, or eat a bite and walk away.</p>
                    <h3>Stress and Environment</h3>
                    <p>New pet in the home, moving, construction noise, change in schedule, new person, or loss of a companion animal can all cause temporary appetite reduction. This is real but should be short-lived — and if your cat stops eating for more than 24 hours regardless of cause, the 24-hour rule applies.</p>
                    <h3>Food Change</h3>
                    <p>Some cats object strenuously to food changes — especially when switched abruptly. If you've changed foods recently, try transitioning back and introducing the new food gradually (10–15% new food per day over 1–2 weeks).</p>
                    <div class="warn-box">
                        <p><strong>Call your vet if your cat:</strong> Hasn't eaten for 24 hours &middot; Shows signs of lethargy, vomiting, or weight loss alongside food refusal &middot; Is drooling or showing pain near the mouth &middot; Has been straining in the litter box &middot; Has any discharge from eyes or nose &middot; Was previously a reliable eater and has suddenly stopped</p>
                    </div>
                    <h2>What to Do Right Now</h2>
                    <ol>
                        <li>Note when the food refusal started and log it</li>
                        <li>Observe for other symptoms — lethargy, vomiting, litter box changes, hiding</li>
                        <li>Check if anything in the environment changed recently</li>
                        <li>Try warming the food to enhance smell</li>
                        <li>If 24 hours have passed — call your vet, not a search engine</li>
                    </ol>
                    <h2>At the Vet</h2>
                    <p>Be prepared to tell the vet: when the cat last ate normally, what they ate, any other symptoms, any changes in the environment, any medications, and your cat's weight history. A vet who knows these details can narrow the diagnosis faster. VetGPT's feeding log and health history make this information immediately accessible rather than something you have to reconstruct under stress.</p>
                    <h2>How VetGPT Helps</h2>
                    <p>A feeding log isn't just useful during a crisis — it's how you spot the early pattern. A cat who ate slightly less on Monday, skipped Tuesday evening, and refused Wednesday morning is telling a story that's harder to read without a log. VetGPT tracks meals, appetite changes, and observations so you have data when you need it most.</p>""",
  "faq_html": """                    <h3>How long can a cat go without eating?</h3>
                    <p>Not long safely. Cats who stop eating for 24–48 hours are at risk of hepatic lipidosis, especially if overweight. If your cat hasn't eaten in 24 hours, call your vet — don't wait and see.</p>
                    <h3>What are common reasons cats stop eating?</h3>
                    <p>Dental disease (very common), upper respiratory infection (loss of smell kills appetite), nausea from illness or medication, stress or environmental change, food change, or foreign object obstruction.</p>
                    <h3>How do I get my cat to eat?</h3>
                    <p>Try warming food to enhance smell. Different texture or protein. Hand-feeding small amounts. But if it's been 24 hours, call your vet — appetite loss this long needs medical evaluation, not food tricks.</p>
                    <h3>Is it normal for cats to be picky eaters?</h3>
                    <p>Some preference is normal, but a cat who has eaten normally for months and suddenly refuses food is showing a health signal, not a preference change. Dental pain and nausea are common hidden causes.</p>"""
})

# ── POST 13: Dog dental health ────────────────────────────────────────────────
posts.append({
  "slug": "dog-dental-health-guide",
  "page_title": "Dog Dental Health: Signs of Problems, Brushing, and When to See a Vet | VetGPT",
  "title": "Dog Dental Health: Signs of Problems, How to Help at Home, and When It's Time for the Vet",
  "breadcrumb": "Dog Dental Health Guide",
  "tag": "🐕 Dogs",
  "date": "2026-03-05",
  "date_display": "March 5, 2026",
  "readtime": "5 min read",
  "meta_description": "80% of dogs over age 3 have dental disease. Most owners don't know until it's advanced. Here's how to spot it early, what helps, and when professional cleaning is needed.",
  "cta_headline": "Track your dog's dental health over time",
  "cta_body": "Vet visits, dental cleanings, medications, and observations all in one place. Know your dog's full history at every appointment.",
  "faq": [
    ("How often should dogs get professional dental cleaning?", "Most adult dogs benefit from professional cleaning every 1–2 years. Small breeds typically need more frequent cleaning (annually). Your vet will recommend a schedule based on your dog's dental health. Home care between cleanings significantly affects how quickly tartar builds up."),
    ("Can I brush my dog's teeth at home?", "Yes, and it's the single most effective home care option. Use a dog-specific toothpaste (never human toothpaste — xylitol is toxic to dogs). Daily brushing is ideal; even three times a week makes a meaningful difference. Start slowly with a finger brush if your dog is resistant."),
    ("What are signs of dental pain in dogs?", "Dropping food while eating, chewing only on one side, reluctance to eat hard food, pawing at the mouth, bad breath that's gotten significantly worse, facial swelling, or behavioral changes like increased irritability. Many dogs hide dental pain well — lack of obvious symptoms doesn't mean absence of disease."),
    ("Is anesthesia for dog dental cleaning safe?", "Modern veterinary anesthesia is very safe, especially in healthy dogs with a pre-anesthetic bloodwork screen. The risks of untreated dental disease — systemic infection, heart and kidney disease, chronic pain — substantially outweigh anesthesia risks for most dogs. Non-anesthetic dentistry does not allow subgingival cleaning and is not a substitute.")
  ],
  "related": [
    ("senior-dog-care-guide.html", "🐕 Dogs", "The Senior Dog Care Guide: Health Changes to Watch After Age 7"),
    ("how-to-track-dog-medications.html", "🐕 Dogs", "How to Track Your Dog's Medications (And Never Miss a Dose Again)")
  ],
  "body": """                    <p>Studies estimate that 80% of dogs over age 3 have some form of dental disease. It's one of the most common health conditions in dogs and one of the most undertreated — because it develops gradually, dogs hide pain well, and owners aren't always sure what to look for.</p>
                    <p>Dental disease isn't just about teeth. Untreated periodontal disease allows bacteria to enter the bloodstream, where it's linked to heart disease, kidney disease, and liver disease. The mouth is connected to everything else.</p>
                    <h2>What Dental Disease Looks Like</h2>
                    <p>It progresses in stages:</p>
                    <ul>
                        <li><strong>Stage 1 — Gingivitis:</strong> Gum line is red and inflamed. No bone loss yet. Fully reversible with professional cleaning and good home care.</li>
                        <li><strong>Stage 2 — Early periodontitis:</strong> Some bone and attachment loss. Reversible with treatment.</li>
                        <li><strong>Stage 3 — Moderate periodontitis:</strong> More significant bone loss. Requires cleaning and may require extractions. Partially reversible.</li>
                        <li><strong>Stage 4 — Advanced periodontitis:</strong> Severe bone loss, tooth loss, potential systemic effects. Extractions required. Not reversible — management only.</li>
                    </ul>
                    <p>Most dogs showing obvious symptoms are already at Stage 3 or 4. The goal is to catch it at Stage 1 or 2.</p>
                    <h2>How to Check Your Dog's Teeth at Home</h2>
                    <div class="checklist-card">
                        <h3>📋 Monthly Home Dental Check</h3>
                        <ul>
                            <li>Lift the lips and look at the teeth — particularly the back upper premolars and molars where tartar accumulates fastest</li>
                            <li>Tartar appears as yellow-brown buildup along the gum line</li>
                            <li>Gums should be pink (or pigmented in some breeds) — not red, swollen, or bleeding</li>
                            <li>Smell the breath — some odor is normal; significant bad breath (beyond "dog breath") indicates bacterial load</li>
                            <li>Note any broken teeth — a fractured tooth often looks like a chip and may have a dark center (exposed pulp)</li>
                            <li>Watch while they eat — do they drop food, chew only on one side, or seem reluctant?</li>
                        </ul>
                    </div>
                    <h2>Home Care: What Actually Works</h2>
                    <h3>Toothbrushing (Best)</h3>
                    <p>Daily toothbrushing is the gold standard. Even every other day makes a meaningful difference. Use enzymatic dog toothpaste — the enzymes continue working after brushing. Focus on the outside surfaces of the teeth, particularly the back upper teeth. You don't need to brush the inside surfaces — the tongue handles those.</p>
                    <p>If your dog resists: start by just letting them lick the toothpaste from your finger. Then your finger on their teeth. Then a finger brush. Patience matters more than perfect technique.</p>
                    <h3>Dental Chews (Helpful, Not Sufficient Alone)</h3>
                    <p>Look for the VOHC (Veterinary Oral Health Council) seal — products with this seal have demonstrated clinical evidence of reducing plaque or tartar. They help but don't replace brushing or professional cleaning.</p>
                    <h3>Water Additives and Dental Wipes (Supplemental)</h3>
                    <p>These help but are the lowest-impact options. Use them as supplements to brushing, not replacements.</p>
                    <h2>Professional Cleaning</h2>
                    <p>Professional dental cleaning under anesthesia allows the vet to clean above and below the gum line, probe pockets, take X-rays, and extract teeth that cannot be saved. It's the only way to adequately address dental disease that's progressed past very early stages. Pre-anesthetic bloodwork (to confirm organ function before anesthesia) is standard and worth doing.</p>
                    <div class="info-box">
                        <p><strong>Ask your vet:</strong> What stage is my dog's dental disease? How often should they have professional cleaning? Are any extractions needed? What home care do you recommend for my dog specifically?</p>
                    </div>
                    <h2>How VetGPT Helps</h2>
                    <p>Track dental cleanings, home care routines, vet dental observations, and any behavioral changes that might indicate dental pain. When your vet asks when the last dental cleaning was, you'll have the exact date — not a rough estimate.</p>""",
  "faq_html": """                    <h3>How often should dogs get professional dental cleaning?</h3>
                    <p>Most adult dogs benefit from cleaning every 1–2 years. Small breeds often need annual cleaning. Your vet will recommend a schedule based on your dog's individual dental health and how quickly tartar builds up.</p>
                    <h3>Can I brush my dog's teeth at home?</h3>
                    <p>Yes — it's the most effective home care option. Use dog-specific toothpaste (never human toothpaste — xylitol is toxic). Daily is ideal; three times a week makes a meaningful difference. Start with a finger brush if your dog is resistant.</p>
                    <h3>What are signs of dental pain in dogs?</h3>
                    <p>Dropping food, chewing on one side, reluctance to eat hard food, pawing at the mouth, significantly worsened bad breath, facial swelling, or behavioral changes. Many dogs hide dental pain well — regular inspection matters.</p>
                    <h3>Is anesthesia for dental cleaning safe?</h3>
                    <p>Modern veterinary anesthesia with pre-anesthetic bloodwork is very safe for healthy dogs. The risks of untreated dental disease substantially outweigh anesthesia risks for most patients.</p>"""
})

# ── POST 14: Ferret health guide ──────────────────────────────────────────────
posts.append({
  "slug": "ferret-health-guide",
  "page_title": "Ferret Health Guide: Common Diseases, Symptoms & Vet Care | VetGPT",
  "title": "Ferret Health Guide: Common Diseases, What to Watch For, and Why Ferrets Need Exotic Vet Care",
  "breadcrumb": "Ferret Health Guide",
  "tag": "🦦 Small Mammals",
  "date": "2026-03-05",
  "date_display": "March 5, 2026",
  "readtime": "6 min read",
  "meta_description": "Ferrets are prone to specific diseases — insulinoma, adrenal disease, lymphoma — that most general vets don't routinely treat. Here's what every ferret owner needs to know.",
  "cta_headline": "Track your ferret's health with VetGPT",
  "cta_body": "Medication logs, vet visits, weight tracking, and AI chat that understands ferret-specific health. Free during early release.",
  "faq": [
    ("What diseases are most common in ferrets?", "Insulinoma (pancreatic tumor causing low blood sugar), adrenal gland disease (causing hair loss and hormonal symptoms), lymphoma (cancer of the lymph system), and Aleutian disease. These are the 'big three' that most ferret owners will encounter — awareness and early diagnosis make a real difference."),
    ("How often do ferrets need vet visits?", "Annual wellness exams are minimum. Ferrets over 3 years should ideally see an exotic vet every 6 months. Blood glucose testing and adrenal assessment become important after age 3–4, when these conditions become much more common."),
    ("What are signs of insulinoma in ferrets?", "Weakness or staggering (especially after activity), salivating excessively, glazed eyes, pawing at the mouth, collapsing, or seizure-like activity. These are signs of hypoglycemia (low blood sugar) and require immediate vet attention. A small amount of corn syrup rubbed on the gums can help briefly while you get to the vet."),
    ("Do ferrets need vaccines?", "In the US, yes. Ferrets should receive annual rabies vaccine and distemper vaccine (CDV). Distemper is nearly always fatal in ferrets — vaccination is critical. Use ferret-approved vaccines; some dog vaccines are not safe for ferrets.")
  ],
  "related": [
    ("guinea-pig-health-checklist.html", "🐹 Small Mammals", "Guinea Pig Health Checklist: What to Check Every Day"),
    ("preparing-for-vet-visit.html", "🏥 Vet Visits", "How to Prepare for a Vet Visit (So You Never Blank at the Worst Moment)")
  ],
  "body": """                    <p>Ferrets are intelligent, playful, and surprisingly medically complex. They're prone to a specific set of diseases — particularly adrenal disease, insulinoma, and lymphoma — that require an exotic or ferret-savvy vet, not a general practice. Most ferret owners encounter at least one of these conditions during their ferret's life. Knowing what they are and how they present early can mean the difference between managed and terminal.</p>
                    <h2>The Three Most Common Serious Ferret Diseases</h2>
                    <h3>Insulinoma (Pancreatic Tumor)</h3>
                    <p>Insulinoma is a tumor of the pancreas that causes it to produce too much insulin, resulting in chronically low blood sugar (hypoglycemia). It's extremely common in ferrets over 3 years — some estimates put it at affecting the majority of middle-aged to older ferrets.</p>
                    <p>Signs: weakness or wobbliness, excessive salivating or pawing at the mouth, glazed eyes, collapsing, seizure-like episodes. Symptoms are often worse after activity or when the ferret hasn't eaten recently. Episodes can look like brief "spells" that owners might dismiss initially.</p>
                    <p>Management: medical management (prednisolone, diazoxide) or surgery to remove the tumor. Early diagnosis and treatment significantly extend quality of life.</p>
                    <h3>Adrenal Gland Disease</h3>
                    <p>Adrenal gland tumors or hyperplasia cause the adrenal glands to overproduce hormones. In the US, this is one of the most common ferret diseases, with some reports suggesting it affects up to 70% of ferrets by age 5.</p>
                    <p>Signs: hair loss starting at the tail base and progressing up the back and sides, itchiness, muscle wasting, enlarged abdomen, behavioral changes, and in females, a swollen vulva (mimicking being in heat). Male ferrets may have urinary blockage from prostate enlargement.</p>
                    <p>Management: hormonal implants (Lupron or Suprelorin), surgical removal, or both. This is very manageable with treatment.</p>
                    <h3>Lymphoma</h3>
                    <p>Lymphoma (cancer of the lymph system) is the third major ferret disease. It can occur at any age but is more common in older ferrets. Signs vary depending on which form: enlarged lymph nodes, weight loss, lethargy, difficulty breathing, or GI symptoms. Diagnosis requires biopsy. Treatment with chemotherapy can extend life significantly in some cases.</p>
                    <h2>Daily Observation</h2>
                    <div class="checklist-card">
                        <h3>🌅 Every Day</h3>
                        <ul>
                            <li>Eating and drinking normally?</li>
                            <li>Normal energy level during active periods?</li>
                            <li>Normal stool — small,