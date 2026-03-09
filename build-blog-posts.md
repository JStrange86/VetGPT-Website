# Blog Build Task

You are working on the VetGPT website blog. Your job is to create 12 new HTML blog post files and update the blog index.

## Context

The blog is at /Users/farah/.openclaw/workspace/VetGPT-Website/blog/
There are 4 existing posts. Look at bearded-dragon-health-checklist.html to understand the exact HTML structure, CSS, nav, footer, JS, etc.

The source content for all 15 posts is at:
/Users/farah/.openclaw/workspace/drafts/blog-posts-1-15.md

## Posts to CREATE (12 new files)

Skip posts 4, 5, 7 (they duplicate existing posts). Create these:

1. Post 1 → 2am-pet-health-panic.html
2. Post 2 → canine-cognitive-dysfunction.html
3. Post 3 → exotic-pet-health-tracker.html
4. Post 6 → pet-medication-tracking.html (all-pets version, different from existing dog-only)
5. Post 8 → senior-dog-pain-signs.html
6. Post 9 → ball-python-health-checklist.html
7. Post 10 → ai-pet-health-care.html
8. Post 11 → pet-health-records.html
9. Post 12 → parrot-health-guide.html
10. Post 13 → emergency-vet-guide.html
11. Post 14 → cat-health-tracking.html
12. Post 15 → pet-health-history.html

## Requirements for each HTML file

Match the EXACT structure of bearded-dragon-health-checklist.html:
- Same CSS variables and styles (copy entire CSS block)
- Same nav header with mobile hamburger menu
- Same article layout (.article-wrap > .article-container)
- Breadcrumb: Home > Blog > [Post Title]
- article-tag span with relevant emoji + category
- h1 with post title from the markdown
- article-meta: date = "March 6, 2026", read time from markdown, "By VetGPT"
- Full article body — convert markdown to HTML faithfully
- CTA box pointing to vetgpt.app with /#download button
- Related posts section (pick 2 relevant existing posts to link to)
- Same footer
- Same JS scroll behavior for nav
- Proper meta title, description, OG tags, canonical URL, JSON-LD Article schema
- Add a simple FAQ section at the bottom with 3-4 questions relevant to the post topic

Convert markdown faithfully: preserve all headings (## → h2, ### → h3), bullet lists → ul/li, bold → strong. Use .checklist-card divs for checklist content. Use .warn-box divs for warning/emergency sections.

Canonical URLs: https://vetgpt.app/blog/[filename]

## Update blog/index.html

Add all 12 new posts as blog-card article entries in the existing grid.
Match the existing card format exactly (blog-tag, h2, blog-meta, p description, blog-read-more link).
Add them ABOVE the existing 4 cards (they are March 6, 2026 vs existing March 1).
Choose appropriate emoji tags for each post.

## When done

Run: openclaw system event --text "Done: Created 12 new VetGPT blog post HTML files and updated blog index" --mode now
