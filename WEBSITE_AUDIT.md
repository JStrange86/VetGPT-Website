# VetGPT Website Audit — Pre-Facelift Baseline

**Date:** 2026-07-01 · **Repo:** `/Users/joshuastrange/Desktop/vetgpt-website` · **Deploy:** Vercel (`prj_61eAI6NDp5WM0jCns0CX2zCuZpLE`, vetgpt.app)
**Total repo size:** 51MB (of which ~16MB is unreferenced dead weight — see §1/§3)
**Read-only audit. No files changed except this report.**

---

## 1. FILE INVENTORY

### HTML pages (root: 15, blog: 31 incl. index) — see §2 for page map

### Config / infra (DO NOT BREAK)
| File | Size | Purpose |
|---|---|---|
| `vercel.json` | 187B | `cleanUrls: true`, `trailingSlash: true`, rewrite `/.well-known/apple-app-site-association` → `/.well-known/aasa.json` |
| `.well-known/aasa.json` | 359B | Universal Links: appID `ATXWC7JPLB.com.joshuastrange.vetgpt`, paths `/download`, `/download/*`, `/open`, `/open/*` (deployed Jul 1) |
| `.well-known/assetlinks.json` | 314B | Android App Links: `com.vetgpt.app` + Play signing SHA256 (deployed Jul 1) |
| `robots.txt` | 85B | Allow all, `Disallow: /reviewers`, sitemap pointer |
| `sitemap.xml` | 5.7KB | 32 URLs (incomplete — see §6) |
| `.vercel/project.json` | — | Vercel project link |
| `.gitignore` | 8B | |

### Build tooling / cruft (never referenced by the live site)
| File | Size | Verdict |
|---|---|---|
| `apply_faq.py` | 18KB | One-shot script; hardcoded to a **different machine's path** (`/Users/farah/.openclaw/workspace/...`) — cruft, won't run here |
| `generate_blog.py` | 112KB | Blog post generator (contains full post content inline). One-shot; posts already generated. Historical value only |
| `generate_claude_posts.py` | 79KB | Same — one-shot batch generator for 12 posts |
| `seo_fixes.py` | 19KB | One-shot SEO patcher; also hardcoded to `/Users/farah/...` — cruft |
| `build-blog-posts.md` | 2.7KB | Task brief for a past contractor/agent run — cruft |
| `.DS_Store` | 6KB | macOS cruft (currently modified in git) |

**Note:** All of these are deployed to Vercel as publicly downloadable files (e.g. `vetgpt.app/generate_blog.py`). Harmless but sloppy; remove or exclude.

### Duplicated files (byte-identical, verified by md5)
- `favicon.png` == `logo-black.png` (97KB each, 256×256)
- `images/logo.png` == `images/app-icon.png` (1.67MB each, 1024×1024!) — `images/logo.png` is only referenced inside JSON-LD schema (never rendered), `images/app-icon.png` renders on press/creators/download/share

### Orphaned assets (zero references in any HTML)
`app-demo.mp4` (7.6MB), `hero-phone.mp4` (1.2MB), `ss-health-score.png` (260KB, superseded by ss-health-score2), `images/logoold.png` (5.3MB), all six `images/feature-*.jpg` (~1.6MB total), and `hero-phone.png` (354KB — worse than orphaned: it is *preloaded* on the homepage but never rendered, see §8).

---

## 2. PAGE MAP

### Root pages
| File | URL | Linked from home? | Title | Purpose |
|---|---|---|---|---|
| `index.html` | `/` | — | VetGPT™ - AI Pet Health Tracker for Dogs, Cats & 60+ Species | Conversion + SEO. 92.7KB single file |
| `download.html` | `/download/` | nav CTA "Download Free" | Download VetGPT™ - Free on iOS & Android | **Conversion-critical** (see §7) |
| `exotic-pet-care.html` | `/exotic-pet-care/` | nav + footer | Exotic Pet Health Tracker… | SEO species landing |
| `reptile-health-tracker.html` | `/reptile-health-tracker/` | nav + footer | Reptile Health Tracker… | SEO species landing |
| `aquarium-fish-health.html` | `/aquarium-fish-health/` | nav + footer | Aquarium & Fish Health Tracker… | SEO species landing |
| `blog/index.html` | `/blog/` | nav + footer | VetGPT™ Blog… | SEO hub |
| `press.html` | `/press/` | **NOT linked** (intentional; linked from outreach) | VetGPT™ Press Kit | PR utility. ⚠ contains **wrong App Store ID** `id6738029301` (everywhere else: `id6757766151`) |
| `support.html` | `/support/` | footer | Support & FAQ | Support / App Store requirement |
| `privacy.html` | `/privacy/` | footer | Privacy Policy | Legal (store requirement) |
| `terms.html` | `/terms/` | footer | Terms of Service | Legal (store requirement) |
| `delete-account.html` | `/delete-account/` | **orphan** (linked from app/Play listing) | Delete Account | **Google Play requirement** — must stay |
| `delete-data.html` | `/delete-data/` | **orphan** (linked from app) | Delete Your Data | Play data-deletion requirement |
| `share.html` | `/share/` | **orphan** (opened via app share links) | Health Report | **Utility: renders shared vet reports** — fetches `https://qaqfslivculjeqmmgjdo.supabase.co/functions/v1/share/{token}?format=json`. Do not break |
| `confirmation.html` | `/confirmation/` | **orphan** (email confirm redirect target) | Email Confirmed | Auth utility — attempts to open the app |
| `creators.html` | `/creators/` | **orphan** (sent to creators) | VetGPT™ Creator Program | Growth utility. No meta description, no OG tags |
| `reviewers.html` | `/reviewers/` | **orphan** (given to App Review) | App Review Information | Utility; blocked in robots.txt (intentional) |

### Blog (30 posts + index)
Posts: 2am-pet-health-panic, ai-pet-health-care, ball-python, bearded-dragon, betta-fish, budgie-parakeet, canine-cognitive-dysfunction, cat-health-tracking, chinchilla, cockatiel, emergency-vet-guide, exotic-pet-health-tracker, ferret, goldfish, guinea-pig, hamster, how-to-track-dog-medications, kitten-first-year, leopard-gecko, parrot, pet-health-history, pet-health-records, pet-medication-tracking, preparing-for-vet-visit, puppy-first-year, rabbit, senior-cat, senior-dog-pain-signs, sugar-glider, turtle-tortoise.

⚠ **6 blog posts are fully orphaned** — not in `blog/index.html`, not in sitemap.xml, not linked anywhere: `budgie-parakeet-health-guide`, `chinchilla-health-guide`, `guinea-pig-health-guide`, `kitten-first-year-health-guide`, `sugar-glider-health-guide`, `turtle-tortoise-health-guide`. They're written, styled, schema'd — just never wired in. Free SEO win.

---

## 3. ASSET REPORT

### Videos
| File | Size | Dimensions / duration | Used | Flags |
|---|---|---|---|---|
| `hero-loop.mp4` | **1.33MB** | 750×1626, 14s | Homepage hero phone (`<video autoplay muted loop playsinline>`) | **Above the fold, autoplay, no `preload` attr, no poster** → full 1.3MB downloads on every homepage view |
| `app-demo.mp4` | **7.6MB** | 1080×1920, 31s | **UNREFERENCED** | 7.6MB deployed for nothing (verify no external outreach links point at `vetgpt.app/app-demo.mp4` before deleting) |
| `hero-phone.mp4` | **1.2MB** | 512×1110, 32s | **UNREFERENCED** | Old hero video |

### Images (>50KB or notable)
| File | Size | Dim | Format | Used | Flags |
|---|---|---|---|---|---|
| `images/logo.png` | 1.67MB | 1024×1024 | PNG | JSON-LD schema only (index + 30 blog posts) — never rendered | Not on page-load path, but Google fetches it as the Organization logo; 1.67MB is absurd. Duplicate of app-icon.png |
| `images/logoold.png` | 5.3MB | 2048×2048 | PNG | UNREFERENCED | Delete |
| `images/app-icon.png` | 1.67MB | 1024×1024 | PNG | press, creators, download (96px!), share | >200KB, not WebP; **loads 1.67MB on the conversion-critical download page** for a 96×96 icon |
| `ss-ai-chat.png` | 776KB | 989×1908 | PNG | index (lazy) | >200KB, not WebP |
| `ss-goldfish.png` | 546KB | 616×1220 | PNG | index (lazy) | >200KB, not WebP |
| `hero-phone.png` | 354KB | 616×1020 | PNG | **preloaded on index (`fetchpriority=high`) but never rendered** | 354KB of pure wasted above-fold bandwidth |
| `ss-health-score2.png` | 267KB | 610×1303 | PNG | index (lazy) | >200KB, not WebP |
| `ss-health-score.png` | 260KB | 616×1020 | PNG | UNREFERENCED (v1) | Delete |
| `images/feature-*.jpg` ×6 | 197–342KB | 1800×960 | JPG | ALL UNREFERENCED | ~1.6MB total, delete |
| `og-image.png` | 162KB | 1200×630 | PNG | og:image on all 44 pages | Keep (social crawlers only) |
| `favicon.png` | 97KB | 256×256 | PNG | all pages | Heavy for a favicon; duplicate of logo-black.png |
| `logo-black.png` | 97KB | 256×256 | PNG | nav+footer logo on index/species/blog (rendered ~22–28px) | **Above the fold on every page**; 97KB for a 22px logo |
| `apple-touch-icon.png` | 49KB | 180×180 | PNG | all pages | OK |
| `jessica-avatar.png` | 76KB | 200×200 | PNG | index testimonials (lazy) | Convert to WebP |
| `brody/pumpkin/wola-avatar.jpg` | 9–12KB | 160×160 | JPG | index testimonials (lazy) | OK |

**Zero WebP/AVIF anywhere. No local fonts (Google Fonts CDN).**

---

## 4. CSS / JS REPORT

- **Architecture:** 100% inline. Every page carries its own full `<style>` block (index: 2 blocks incl. noscript; ~1,500 lines of CSS in index alone). No external stylesheets, no shared CSS file — a facelift must touch every page or introduce a shared sheet.
- **JS:** No frameworks, no libraries, no CDN JS **except** Google tag (`gtag.js?id=AW-18007593933`, async, on all 44 pages; configures both AW-18007593933 Google Ads + G-LQK6G7TGL3 GA4). All other JS is small inline vanilla.
- **Render-blocking:** effectively none by design — fonts use the `preload as=style onload` async pattern + noscript fallback; gtag is `async`; all CSS inline. The real above-fold cost is media (see §8).
- **Homepage JS behaviors (index.html ~line 2115+):**
  - `IntersectionObserver` scroll-reveal (`.reveal` → `.visible`, threshold 0.1)
  - 1 `scroll` listener: nav `.scrolled` state + hero aurora parallax (`translateY(scrollY*0.08)` under 900px)
  - Mobile menu with focus trapping + Escape close
- **Animations (homepage):** 6 `@keyframes` — `aurora`, `urgencyPulse`, `borderSpin`, `phoneFloat`, `marquee` (species ticker), `btnSpin`; 21 `transition:` rules. Other pages with keyframes: exotic-pet-care, aquarium-fish-health, reptile-health-tracker, confirmation, share.
- **Noscript resilience:** `.reveal` forced visible via noscript style — keep this pattern in the redesign.

---

## 5. CURRENT DESIGN SYSTEM (as implemented on index.html) vs APP

Fonts: **Outfit** (display, 300–800), **DM Sans** (body), **JetBrains Mono** (labels/eyebrows) — 13 weights loaded from Google Fonts.
Layout: `--max-w: 1200px`, `--section-pad: clamp(60px,10vw,120px)`, container pad 24px, cards = `rgba(255,255,255,0.04)` bg + `rgba(255,255,255,0.08)` border (elevation via white-alpha, not solid surfaces).
Type scale: h1 `clamp(2.2rem,5vw,3.5rem)`, section titles `clamp(1.75rem,4vw,2.75rem)`, body 1rem / 0.9rem / 0.85rem clusters.

| Token | Website (`:root`) | App | Match? |
|---|---|---|---|
| Background | `--bg: #0a0a0a` (elevated `#111111`) | `#121212` | ❌ website darker |
| Surface | `rgba(255,255,255,0.04)` translucent cards | `#1E1E1E` solid | ❌ different system |
| Surface light | `rgba(255,255,255,0.07)` hover | `#2a2a2a` | ❌ |
| Primary green | **`#10b981`** (emerald, Tailwind) | **`#1DB954`** (Spotify) | ❌ **brand primary mismatch** |
| Text | `#ffffff` | `#FFFFFF` | ✅ |
| Text secondary | `#9ca3af` | `#B3B3B3` | ❌ cooler gray |
| Text muted | `#8b95a5` | `#727272` | ❌ |
| Purple | `#8b5cf6` | `#8b5cf6` | ✅ |
| Pink | `#ec4899` | `#ec4899` | ✅ |
| Teal | **absent** | `#14b8a6` | ❌ never used on site |
| Info blue | `#3b82f6` (1 use) | `#3b82f6` | ✅ |
| Error | `#ef4444` (1 use) | `#ef4444` | ✅ |

Sub-brand drift: `download.html` uses its own bg `#0a0f1a` (navy) — not the homepage `#0a0a0a`, not the app `#121212`. `exotic-pet-care.html` uses off-palette grays (`#eeeef2`, `#9898b0`, `#b9b9c8`) + amber `#f59e0b`. The single biggest brand decision for the facelift: **`#10b981` (site) vs `#1DB954` (app) green.**

---

## 6. SEO INVENTORY (do-not-break list)

- **sitemap.xml:** 32 URLs — home, 3 species pages, privacy, terms, support, blog index, 24 blog posts. **Missing:** the 6 orphan blog posts, `/download/`, `/press/`. (delete-*/share/confirmation/reviewers/creators intentionally out.)
- **robots.txt:** allow all, `Disallow: /reviewers`, sitemap pointer. Keep.
- **Canonicals:** present on every page, trailing-slash style matching `vercel.json` — **EXCEPT all 30 blog posts, which have a malformed canonical**: `https://vetgpt.app/blog/{slug}.html/` (`.html` + trailing slash — matches neither the served clean URL nor the sitemap's `/blog/{slug}/`). `og:url` on posts uses a third variant (`…{slug}.html`, no slash). Pre-existing bug; fix during facelift.
- **Structured data (JSON-LD):**
  - `index.html`: `@graph` of **Organization** (founder, sameAs socials, contactPoint) + **SoftwareApplication** (offers $0/$2.99, featureList) + **WebSite** (SearchAction) — the crown jewels, preserve exactly.
  - Every blog post: WebPage + Article + Blog + Organization + ImageObject, most also **FAQPage** (Question/Answer) → rich-result eligible. Preserve.
  - Species pages/press/legal: none.
- **OG/Twitter:** index has full OG + Twitter card; species pages og×5 + twitter:card; press og×4; support/privacy/terms og×3; download og×4; blog posts full OG. `creators.html` and `share.html` have **zero** OG tags (gap, not breakage).
- **Verification/analytics tags on index:** Google site verification `cS_PEnntd5jCrhO8IQeaqdVgAfihW4sY8IhcbLePvEU`, Impact affiliate verification meta, GA4 `G-LQK6G7TGL3` + Google Ads `AW-18007593933` (gtag on **all 44 pages**).

---

## 7. CONVERSION MACHINERY (critical do-not-break)

### download.html (`/download/`) — updated Jun 27, the attribution backbone
1. **UTM propagation:** reads `utm_source/medium/campaign/content/term`.
   - **Android:** appends URL-encoded UTM string as `&referrer=` on the Play link (Play install-referrer attribution). Guarded against double-append.
   - **iOS:** derives `ct` (utm_campaign, fallback utm_source) + `pt` (utm_source) tokens; `ppid` map `{tiktok: 'd68f323f-9297-47b0-80ae-5940cc43673b'}` (kobe CPP) → App Store Connect Campaigns attribution. Extend the ppid map as CPPs go live.
2. **GA4 `store_click` event** (`store: ios|android` + utm dims) fired with `transport_type: 'beacon'` **before** redirect so it survives Safari unload.
3. **Device-aware auto-redirect:** iOS UA (incl. iPadOS-as-Mac touch check) → App Store after 100ms; Android → Play. Matching button stays as manual fallback; other platform collapses to a quiet text link. Desktop: both buttons, no redirect.
4. **QA bypass:** `?noredirect=1`.
5. Also a Universal-Link path (`/download`, `/download/*` in aasa.json) — installed users deep-link into the app instead of hitting this page.
- App icon here loads the 1.67MB `images/app-icon.png` with an emoji `onerror` fallback.

### .well-known (deployed Jul 1 — MUST survive any redeploy)
- `aasa.json` served via the `vercel.json` rewrite from `/.well-known/apple-app-site-association` (Apple requires no extension, correct content-type — the rewrite is the whole trick).
- `assetlinks.json` served natively at `/.well-known/assetlinks.json`.
- **A facelift that touches `vercel.json` (or a framework migration that takes over routing) can silently kill Universal/App Links.** `cleanUrls` + `trailingSlash` also underpin every canonical/sitemap URL.

### Store badges (inline SVG, custom-styled — no external badge images)
index (hero + download section + nav area: 3× each store), all 3 species pages (2× each), download (1+1), press (1 each — **with the wrong iOS app id `id6738029301`**). Correct link everywhere else: `https://apps.apple.com/app/vetgpt/id6757766151` and `https://play.google.com/store/apps/details?id=com.vetgpt.app`.

### Other machinery
- `share.html`: tokenized health-report viewer calling the Supabase `share` edge function — app feature, keep intact.
- `confirmation.html`: Supabase email-confirm landing, auto-opens app.
- `delete-account.html` / `delete-data.html`: Google Play policy requirements.
- `press.html`: linked from media outreach (live at vetgpt.app/press since Jun 4).

---

## 8. PERFORMANCE BASELINE (homepage, first view, approximate)

| Resource | Size | Notes |
|---|---|---|
| index.html | 93KB | all CSS/JS inline |
| `hero-loop.mp4` | **1,328KB** | above-fold autoplay, no `preload="metadata"`, no poster |
| `hero-phone.png` | **354KB** | `<link rel=preload fetchpriority=high>` but **never rendered** — 100% waste |
| `logo-black.png` (nav) | 97KB | 256px asset shown at ~22px |
| gtag.js + config | ~130KB | async |
| Google Fonts (3 families / 13 weights) | ~120–180KB | async pattern, but heavy weight count |
| favicon.png | 97KB | oversized |
| **Above-fold total** | **≈ 2.1–2.2MB** | ~80% is the video + the phantom preload |
| Lazy below-fold (3 screenshots + 4 avatars) | ~1.7MB | `loading="lazy"` correctly applied (8 imgs) |
| **Full homepage** | **≈ 3.8MB** | |

Quick wins without redesign: delete the `hero-phone.png` preload (–354KB), add `poster` + compress hero-loop to ~400–600KB, WebP the screenshots (~–60%), 32px favicon (–90KB), resized nav logo (–90KB). That alone is roughly –2MB.

---

## KEEP / FIX / REMOVE

| Item | Verdict | Why |
|---|---|---|
| `index.html` | **KEEP/FIX** | Facelift target; preserve JSON-LD graph, GA4/AdWords, verification metas, store links, noscript fallbacks. FIX: remove phantom `hero-phone.png` preload |
| `download.html` | **KEEP (do not redesign logic)** | Entire paid/creator attribution chain lives here. Reskin visuals only; keep script byte-for-byte in behavior. FIX: 1.67MB app-icon |
| `.well-known/*` + `vercel.json` | **KEEP — sacred** | Universal/App Links deployed Jul 1 + cleanUrls/trailingSlash URL scheme |
| 3 species pages | **KEEP/FIX** | In sitemap, ranking pages. FIX: align palette during facelift |
| `blog/` (30 posts) | **KEEP/FIX** | FIX: broken `.html/` canonicals on all 30; wire in the 6 orphan posts (index + sitemap) |
| `press.html` | **KEEP/FIX** | FIX wrong App Store id `id6738029301` → `id6757766151` |
| privacy/terms/support/delete-account/delete-data | **KEEP** | Store/legal requirements |
| `share.html`, `confirmation.html`, `reviewers.html`, `creators.html` | **KEEP** | App/auth/review/growth utilities. Optional: OG tags for creators |
| `sitemap.xml`, `robots.txt` | **KEEP/FIX** | Add 6 orphan posts + `/download/` (+ `/press/` if desired) |
| `hero-loop.mp4` | **KEEP/FIX** | Compress + poster + `preload="metadata"` |
| `og-image.png`, `apple-touch-icon.png`, avatars (jpg), `ss-*.png` (3 used) | **KEEP/FIX** | WebP the 3 screenshots |
| `favicon.png` / `logo-black.png` | **FIX** | Deduplicate + resize |
| `images/app-icon.png` / `images/logo.png` | **FIX** | Deduplicate; serve a ~50KB version; keep a big one only for schema logo if wanted |
| `hero-phone.png` | **REMOVE** (after deleting its preload tag) | Preloaded, never rendered |
| `app-demo.mp4` (7.6MB) | **REMOVE*** | Unreferenced. *Verify no outreach/email links hit the URL first |
| `hero-phone.mp4`, `ss-health-score.png`, `images/logoold.png`, `images/feature-*.jpg` ×6 | **REMOVE** | Unreferenced, ~8.6MB combined |
| `apply_faq.py`, `generate_blog.py`, `generate_claude_posts.py`, `seo_fixes.py`, `build-blog-posts.md` | **REMOVE** (or move to a non-deployed `/tools` + archive in git history) | One-shot generators, two hardcoded to another machine; currently publicly downloadable |
| `.DS_Store` | **REMOVE** + gitignore | |

---

## TOP-10 FACELIFT WATCH-OUTS (things a redesign could silently break)

1. **`vercel.json` rewrite for `apple-app-site-association`** — touch/replace vercel.json (or migrate to a framework that owns routing) and Universal Links die silently. Same for `/.well-known/assetlinks.json` being served as-is.
2. **`download.html` inline script** — device detection, sendBeacon `store_click`, UTM→Play `referrer`, UTM→Apple `ppid/ct/pt`, `?noredirect=1`. A redesign that rebuilds the buttons (new selectors: script targets `a[href*="apps.apple.com"]` / `a[href*="play.google.com"]`) or defers the script breaks all paid attribution with zero visible error.
3. **`cleanUrls` + `trailingSlash: true`** — every canonical, sitemap entry, and GSC-indexed URL assumes `/page/`. Also the known gotcha: trailingSlash breaks relative asset paths — all current asset refs are root-absolute (`/foo.png`); keep them absolute.
4. **Homepage JSON-LD `@graph`** (Organization + SoftwareApplication + WebSite/SearchAction) and per-post Article+FAQPage schema — easy to drop when rewriting `<head>`s; these drive rich results.
5. **gtag on all 44 pages** (`G-LQK6G7TGL3` + `AW-18007593933`) + Google site-verification + Impact verification metas on index — new templates must carry all three.
6. **Store links**: iOS `id6757766151` everywhere (fix press.html's stale `id6738029301` while at it); Play `com.vetgpt.app`. Badges are hand-built inline SVG — no external assets to preserve, but don't change hrefs.
7. **`share.html` + `confirmation.html`** are app infrastructure (Supabase share edge fn viewer; email-confirm → app open). A "delete the weird orphan pages" cleanup instinct would break in-app features.
8. **Blog canonical fix must go to the sitemap URL** (`https://vetgpt.app/blog/{slug}/`) — "fixing" them to `.html` (no slash) would just create a different mismatch; align canonical, og:url, and sitemap to one form.
9. **CSS is 100% per-page inline** — a shared stylesheet is the right move, but every one of the 46 HTML files must be migrated or you get a two-design site; also preserve the noscript `.reveal` fallback and focus-visible/focus-trap a11y work.
10. **Robots `Disallow: /reviewers`** and the *intentional* absence of press/creators/share/delete pages from nav+sitemap — don't "helpfully" add them to nav or sitemap wholesale; and don't lose `?noredirect=1` QA docs when touching download.

---

*Generated 2026-07-01 as the pre-facelift baseline. Everything measured from the working tree at commit `7e71495`.*
