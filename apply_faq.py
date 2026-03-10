#!/usr/bin/env python3
"""Apply FAQ schema + sections and fix Google Fonts on 8 blog posts."""

import re
import os

BLOG_DIR = "/Users/farah/.openclaw/workspace/VetGPT-Website/blog"

# ─── FONT FIX ──────────────────────────────────────────────────────────────
FONT_OLD = '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
FONT_NEW = '<link rel="preload" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n    <noscript><link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"></noscript>'

# ─── FAQ DATA ───────────────────────────────────────────────────────────────
FAQS = {
    "senior-dog-pain-signs.html": {
        "questions": [
            {
                "q": "How do I know if my senior dog is in pain?",
                "a": "Senior dogs rarely vocalize pain. Instead, watch for subtle changes: reduced appetite, withdrawal from family interaction, reluctance to use stairs or jump, changes in sleep patterns, stiffness when rising, and reduced activity. Tracking these behaviors over time reveals patterns that are often invisible day-to-day."
            },
            {
                "q": "What age is considered 'senior' for a dog?",
                "a": "It depends on size. Small dogs (under 20 lbs) are considered senior around age 10–12. Medium dogs (20–50 lbs) around 8–10. Large dogs (50–90 lbs) around 7–8. Giant breeds (90+ lbs) as early as 5–6. Larger breeds age faster and tend to have shorter lifespans."
            },
            {
                "q": "What are the most common causes of pain in senior dogs?",
                "a": "Osteoarthritis is the most common cause, affecting an estimated 20% of dogs over age 1 and the majority of senior dogs. Other causes include dental disease, cancer, intervertebral disc disease, hip dysplasia, and post-surgical or injury pain."
            },
            {
                "q": "How often should I log my senior dog's pain indicators?",
                "a": "Daily is ideal. A 2-minute daily check covering appetite, energy, mobility, social behavior, and sleep takes almost no time and builds the pattern data that makes vet visits more productive. Weekly notes on weight and changes in activity round out the picture."
            },
            {
                "q": "Can pain in senior dogs be treated effectively?",
                "a": "Yes. Most chronic pain in senior dogs is manageable with the right approach. NSAIDs like carprofen, meloxicam, and grapiprant are effective for many arthritic dogs. Joint supplements, physical rehabilitation, acupuncture, and laser therapy are also effective options. The key is catching it — which requires consistent observation and logging."
            }
        ]
    },
    "emergency-vet-guide.html": {
        "questions": [
            {
                "q": "When should I take my pet to the emergency vet immediately?",
                "a": "Go immediately — no waiting — for: difficulty breathing, suspected poisoning, seizures (especially if first-time or lasting more than 3 minutes), suspected broken bones, eye injuries, collapse or inability to stand, severe vomiting or diarrhea with blood, or if your pet is unresponsive."
            },
            {
                "q": "How do I find a 24-hour emergency vet near me?",
                "a": "Search 'emergency vet near me' or '24-hour animal hospital [your city]'. Do this BEFORE you need it — save the number in your phone now. Many areas have dedicated emergency animal hospitals that operate outside of normal vet hours."
            },
            {
                "q": "What information should I bring to the emergency vet?",
                "a": "Bring or have ready: your pet's current medications (name, dose, frequency), any known conditions or allergies, recent symptom history with dates, vaccination records if relevant, and the name and contact of your regular vet. A digital health record (like VetGPT) lets you pull this up in one tap."
            },
            {
                "q": "Is my exotic pet covered at emergency vet clinics?",
                "a": "Not always. Many emergency vet clinics primarily see dogs and cats. For reptiles, birds, fish, and other exotic species, you may need an exotics-specialist emergency vet. Research exotic animal emergency clinics in your area before you need one — availability varies widely by location."
            },
            {
                "q": "How can I tell if a pet emergency can wait until morning?",
                "a": "If your pet is in distress, unable to breathe normally, vomiting blood, collapsed, or experiencing a seizure — don't wait. If symptoms are concerning but stable (mild limping without trauma, reduced appetite without other symptoms), call an emergency line for guidance. When in doubt, call and describe what you're seeing."
            }
        ]
    },
    "pet-medication-tracking.html": {
        "questions": [
            {
                "q": "What's the best way to track pet medications?",
                "a": "A dedicated pet health app beats notes apps and spreadsheets. Look for features like medication schedules with reminders, one-tap dose logging, medication history, refill tracking, and the ability to photo-capture prescription labels. The goal is reducing the cognitive load so doses don't get missed or doubled."
            },
            {
                "q": "What happens if I miss a dose of my pet's medication?",
                "a": "It depends on the medication and how much time has passed. For most medications, if you realize within a few hours, give the dose then. If it's almost time for the next dose, skip it and resume the regular schedule. Never double up without your vet's guidance. For critical medications like insulin or seizure drugs, contact your vet immediately."
            },
            {
                "q": "How do I remember to give my pet medication every day?",
                "a": "Tie it to an existing habit — feeding time, morning coffee, or bedtime. Set a phone alarm. Use a medication tracking app with push reminders. For households with multiple people managing pet care, a shared digital log prevents the 'did you give it?' confusion."
            },
            {
                "q": "How do I track medications for multiple pets?",
                "a": "Each pet should have their own medication profile with their own schedule. A notes app with mixed data across pets is a recipe for confusion and errors. Dedicated pet health apps like VetGPT support separate profiles per pet with individual medication logs, so there's no mixing up who got what."
            },
            {
                "q": "Can I photograph my pet's prescription labels to log them?",
                "a": "VetGPT lets you photograph prescription bottles and vet documents — AI automatically extracts the medication name, dose, frequency, and refill date. This eliminates manual entry errors and gives you a searchable record of every prescription your pet has ever had."
            }
        ]
    },
    "cat-health-tracking.html": {
        "questions": [
            {
                "q": "Why do cats hide when they're sick?",
                "a": "It's an evolutionary survival instinct. In the wild, showing weakness makes an animal vulnerable to predators. Even domesticated cats retain this behavior — they instinctively conceal illness and pain. By the time a cat shows obvious symptoms, they've often been sick for a while."
            },
            {
                "q": "What are the early signs that a cat is sick?",
                "a": "Early signs are subtle: slight reduction in appetite, drinking more or less water than usual, litter box changes (frequency, consistency, missing it), less grooming or over-grooming, reduced activity, hiding more than usual, or changes in social behavior. Any change from your cat's personal baseline is worth noting."
            },
            {
                "q": "How often should I weigh my cat?",
                "a": "Monthly is a good baseline for healthy adult cats. For senior cats (10+) or cats with health conditions, every 2 weeks is better. Weight loss is one of the most important early indicators of illness in cats — but you can only detect it if you have a baseline to compare against."
            },
            {
                "q": "What should I track for my cat's health?",
                "a": "Core tracking items: weight (monthly), water intake, appetite and food consumption, litter box output (frequency and consistency), sleep and activity levels, coat and skin condition, and any behavioral changes. These form the baseline that makes changes visible."
            },
            {
                "q": "How is tracking a cat's health different from tracking a dog's?",
                "a": "Cats are harder. Dogs show symptoms more overtly. Cats suppress them. This means cat health tracking requires more proactive logging of subtle changes and a lower threshold for 'this seems different.' Baseline data is especially critical for cats — without it, you're flying blind when something is wrong."
            }
        ]
    },
    "2am-pet-health-panic.html": {
        "questions": [
            {
                "q": "What should I do if my pet seems sick at 2am?",
                "a": "First, assess urgency. If your pet is in distress, unable to breathe, having a seizure, or collapsed — go to an emergency vet immediately. For concerning but non-critical symptoms, call your local emergency vet's phone line — most will triage over the phone and tell you whether to come in or monitor at home."
            },
            {
                "q": "How do I find a 24-hour vet for a middle-of-the-night emergency?",
                "a": "Search 'emergency vet near me' or '24-hour animal hospital [your city]'. The best time to find this information is right now — before you need it. Save the number in your phone. Many areas have dedicated emergency animal hospitals separate from regular clinics."
            },
            {
                "q": "How can I tell if my pet's symptoms are an emergency vs. something that can wait?",
                "a": "True emergencies that require immediate care: difficulty breathing, suspected poisoning, seizures, collapse, severe trauma, uncontrolled bleeding, inability to urinate (especially in cats). Symptoms that are concerning but can usually wait for a morning vet call: mild vomiting without blood, slight lethargy, reduced appetite for one day. When unsure, call an emergency line and describe the symptoms."
            },
            {
                "q": "Why does pet health anxiety feel so overwhelming at night?",
                "a": "At night, you're tired, you can't reach your regular vet, and everything feels more serious. Without clear information about your pet's baseline health, it's impossible to know if a symptom is new or expected. Having an organized health record changes this completely — you can check their history, see what's normal for them, and make a calmer, more informed decision."
            },
            {
                "q": "How can I be better prepared for a pet health crisis?",
                "a": "Set up your pet's health record now, not during the crisis. Log their medications, conditions, weight history, and vet contacts in one place. Know where your nearest emergency vet is and have their number saved. The goal is to make the information available when your brain is stressed and decision-making is hard."
            }
        ]
    },
    "ai-pet-health-care.html": {
        "questions": [
            {
                "q": "How is AI being used in pet health care right now?",
                "a": "AI is currently being used in veterinary medicine for diagnostic imaging analysis (detecting tumors, joint abnormalities, and organ changes in X-rays and ultrasounds), pathology slide analysis, and clinical documentation. For pet owners at home, AI tools now help analyze symptoms, extract information from vet documents, track health trends, and answer questions based on a pet's personal health history."
            },
            {
                "q": "Can AI replace a veterinarian?",
                "a": "No — and it shouldn't. AI is a tool that enhances what vets and pet owners can do, not a replacement for professional medical care. AI can help identify patterns, answer questions, and organize information, but physical examination, diagnostic testing, and treatment decisions require a licensed veterinarian. Think of AI as a smarter way to prepare for and follow up on vet visits."
            },
            {
                "q": "Is it safe to use AI to assess my pet's symptoms?",
                "a": "AI symptom tools are useful for preliminary triage and education, but shouldn't be used as a substitute for veterinary care. They can help you understand whether a symptom is potentially serious, what questions to ask your vet, and whether something warrants an emergency visit or can wait. The key is using AI as a starting point, not a final answer."
            },
            {
                "q": "What makes AI pet health apps different from searching symptoms online?",
                "a": "Generic symptom searches give generic answers. AI pet health apps that know your pet's individual history — their breed, age, conditions, medications, weight, and past symptoms — can give contextual answers specific to your pet. This is fundamentally different from a one-size-fits-all web search result."
            },
            {
                "q": "What does the future of AI in pet health look like?",
                "a": "The trajectory points toward predictive health monitoring (catching disease earlier from subtle pattern changes), personalized treatment recommendations based on aggregated anonymized data, better integration with veterinary practice management systems, and eventually AI-assisted diagnosis that supports vets with more complete information. The pet health data being collected now will power the breakthroughs of the next decade."
            }
        ]
    }
}

# ─── HTML FAQ SECTION TEMPLATE ──────────────────────────────────────────────
def build_faq_html(questions):
    items = []
    for faq in questions:
        items.append(f"""                    <div class="faq-item">
                        <h3 class="faq-q">{faq['q']}</h3>
                        <p class="faq-a">{faq['a']}</p>
                    </div>""")
    return "\n\n                    <h2>Frequently Asked Questions</h2>\n\n" + "\n\n".join(items) + "\n\n"

# ─── JSON-LD FAQ SCHEMA ──────────────────────────────────────────────────────
def build_faq_schema(questions):
    entities = []
    for faq in questions:
        q = faq['q'].replace('"', '\\"')
        a = faq['a'].replace('"', '\\"')
        entities.append(f'            {{ "@type": "Question", "name": "{q}", "acceptedAnswer": {{ "@type": "Answer", "text": "{a}" }} }}')
    entity_str = ",\n".join(entities)
    return f"""    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
{entity_str}
        ]
    }}
    </script>"""

# ─── PROCESS EACH FILE ───────────────────────────────────────────────────────
results = []

# Posts that already have FAQ — just fix fonts
already_done = ["bearded-dragon-health-checklist.html", "preparing-for-vet-visit.html"]

for filename, data in FAQS.items():
    filepath = os.path.join(BLOG_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content

    # 1. Fix Google Fonts render-blocking
    if FONT_OLD in content:
        content = content.replace(FONT_OLD, FONT_NEW)
        results.append(f"✅ {filename}: Fixed Google Fonts render-blocking")
    
    # 2. Add FAQ JSON-LD schema (after the closing </script> of the Article schema)
    schema_html = build_faq_schema(data['questions'])
    # Insert after the first </script> block in head (the Article schema)
    content = content.replace(
        '    </script>\n    <link rel="preconnect"',
        f'    </script>\n{schema_html}\n    <link rel="preconnect"',
        1  # only replace first occurrence
    )
    
    # 3. Add visible FAQ section before <div class="cta-box">
    faq_html = build_faq_html(data['questions'])
    content = content.replace(
        '\n                    <div class="cta-box">',
        faq_html + '                    <div class="cta-box">',
        1
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results.append(f"✅ {filename}: FAQ schema + section added")
    else:
        results.append(f"⚠️  {filename}: No changes made (check markers)")

# Fix fonts on already-done posts
for filename in already_done:
    filepath = os.path.join(BLOG_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    if FONT_OLD in content:
        content = content.replace(FONT_OLD, FONT_NEW)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results.append(f"✅ {filename}: Fixed Google Fonts render-blocking")
    else:
        results.append(f"ℹ️  {filename}: Fonts already optimized or different pattern")

for r in results:
    print(r)
