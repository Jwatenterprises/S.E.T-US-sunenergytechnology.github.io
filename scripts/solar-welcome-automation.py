"""
S.E.T. Solar — Welcome Email Automation
Agent: Solana | Business: S.E.T. Solar US (sunenergytechnology.com)

Runs daily. Checks all contacts on Brevo list 4 (S.E.T. Solar US Nurture).
For each contact, determines which email they should receive based on days
since signup, sends it, and updates their SOLAR_SEQUENCE_STEP attribute.

Usage:
    python solar-welcome-automation.py              # Dry run (shows what would send)
    python solar-welcome-automation.py --send        # Live send
    python solar-welcome-automation.py --init        # Initialize existing subscribers (sets step/date)

Schedule: Run daily via Windows Task Scheduler or manually.
"""

import requests
import json
import time
import sys
from datetime import datetime, timedelta

API_KEY = None
SENDER = {"name": "Solana | Sun Energy Technology", "email": "biz@sunenergytechnology.net"}
REPLY_TO = {"email": "biz@sunenergytechnology.net", "name": "S.E.T. Solar"}
LIST_ID = 5  # S.E.T. Solar Welcome Sequence (consumer opt-ins only; list 4 = B2B leads)
SITE = "https://sunenergytechnology.com"

# Awin affiliate links
LINKS = {
    "bluetti_ac300": "https://www.awin1.com/cread.php?s=4701100&v=59271&q=568164&r=2881111",
    "bluetti_generic": "https://www.awin1.com/cread.php?s=4701099&v=59271&q=568164&r=2881111",
    "ecoflow": "https://www.awin1.com/cread.php?awinmid=59181&awinaffid=2881111&ued=https%3A%2F%2Fus.ecoflow.com",
    "allpowers": "https://www.awin1.com/cread.php?awinmid=40342&awinaffid=2881111&ued=https%3A%2F%2Fallpowers.com",
    "natures_gen": "https://www.awin1.com/cread.php?awinmid=98409&awinaffid=2881111&ued=https%3A%2F%2Fnaturesgenerator.com",
    "upfirst": "https://upfirst.ai?plid=135267",
}

FOOTER = f"""<p style="margin-top:32px; font-size:13px; color:#888;">
Sun Energy Technology &mdash; Independent Solar Generator Comparisons<br>
<a href="{SITE}" style="color:#1a73e8;">{SITE}</a><br>
<a href="{SITE}/disclosure" style="color:#888;">Affiliate Disclosure</a> |
<a href="{{{{unsubscribe}}}}" style="color:#888;">Unsubscribe</a>
</p>"""

def wrap_html(body_html):
    return f"""<div style="font-family: Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #333; max-width: 600px;">
{body_html}
{FOOTER}
</div>"""

def cta_button(text, url):
    return f'<p style="margin:24px 0;"><a href="{url}" style="background-color:#1a73e8; color:#fff; padding:12px 28px; text-decoration:none; border-radius:6px; font-weight:bold; display:inline-block;">{text}</a></p>'


# === EMAIL SEQUENCE (12 emails, every 2 days) ===

SEQUENCE = [
    # Email 1 — Day 0 (immediate)
    {
        "day": 0,
        "subject": "Welcome to S.E.T. Solar (+ Your Blackout Cheat Sheet)",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>Welcome to the S.E.T. Solar community. We're glad you're here.</p>
<p>Most people start looking into solar generators after a storm, a blackout, or a high electric bill. But here's the problem: most "emergency" buys are the wrong ones.</p>
<p>Before you spend a dime, you need to know your <strong>Blackout Math</strong>.</p>
<p>If your fridge uses 150W and you want to run it for 10 hours, you don't need a "big" generator &mdash; you need at least 1,500Wh of capacity.</p>
<p>We've put together a simple use-case guide to help you calculate exactly what you need for your home.</p>
{cta_button("Calculate Your Needs", f"{SITE}/use-cases")}
<p>Talk soon,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 2 — Day 2
    {
        "day": 2,
        "subject": "Why 'All-in-One' is usually a mistake",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>When most people buy a solar generator, they buy a single, heavy box.</p>
<p>The problem? If you need more power later, you have to buy a whole new box. Or worse, if the battery fails in 5 years, the entire unit is a paperweight.</p>
<p>At S.E.T. Solar, we advocate for <strong>Modularity</strong>.</p>
<p>Systems like the <strong>BLUETTI AC300</strong> separate the "brain" (the inverter) from the "muscle" (the batteries). This lets you:</p>
<ol>
<li>Start small (1 battery).</li>
<li>Expand later (up to 4 batteries).</li>
<li>Easily replace a single module instead of the whole system.</li>
</ol>
<p>It's the smartest way to future-proof your home's energy.</p>
{cta_button("See How Modularity Works", LINKS['bluetti_ac300'])}
<p>Best,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 3 — Day 4
    {
        "day": 4,
        "subject": "Will your generator last 2 years or 10?",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>Not all batteries are created equal.</p>
<p>If you buy a cheap generator from a big-box store, it likely uses standard Lithium-ion (NCM). These are great for phones, but they only last about 500-800 charges before they start dying.</p>
<p>For home backup, you want <strong>LiFePO4 (Lithium Iron Phosphate)</strong>.</p>
<p>LiFePO4 batteries are:</p>
<ul>
<li><strong>Safer:</strong> They don't catch fire even if punctured.</li>
<li><strong>Durable:</strong> They last 3,500+ cycles. That's <strong>10 years of daily use.</strong></li>
</ul>
<p>Every "Top Pick" on our site uses LiFePO4 chemistry. We don't recommend anything less.</p>
{cta_button("Compare LiFePO4 Models", f"{SITE}/compare")}
<p>Best,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 4 — Day 6
    {
        "day": 6,
        "subject": "The hidden bottleneck in your solar setup",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>You have the generator. You have the sun. But why is it taking 14 hours to charge?</p>
<p>It's usually the <strong>MPPT Controller</strong>.</p>
<p>Think of it as the "traffic cop" between your solar panels and your battery. A cheap controller wastes up to 30% of the energy your panels collect.</p>
<p>Our value pick, the <strong>ALLPOWERS R3500</strong>, features a high-efficiency controller that can take in up to 1,500W of solar. In peak sun, you can go from 0% to 100% in a single afternoon.</p>
{cta_button("Check Out the ALLPOWERS R3500", LINKS['allpowers'])}
<p>Best,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 5 — Day 8
    {
        "day": 8,
        "subject": "Portable or Permanent? Choosing your panels",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>Once you've picked your solar generator, the next question is always: "Which panels should I get?"</p>
<p>Most beginners gravitate toward <strong>Portable Foldable Panels</strong>. They're great because:</p>
<ul>
<li>They're "plug and play."</li>
<li>You can take them camping or to a job site.</li>
<li>You can move them to follow the sun.</li>
</ul>
<p>But if you're looking for a permanent home backup, <strong>Rigid (Glass) Panels</strong> are often better. They're more durable, have a higher efficiency rating over 20 years, and usually cost 30-50% less per Watt.</p>
{cta_button("Read the Panel Comparison Guide", f"{SITE}/spec-guide")}
<p>Best,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 6 — Day 10
    {
        "day": 10,
        "subject": "How to get 30% more power from the same sun",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>If you're setting up panels in your yard or on a flat roof, you need to know about <strong>Bifacial Technology</strong>.</p>
<p>Standard panels only collect light from the front. Bifacial panels have glass on both sides, allowing them to capture "albedo" light &mdash; the sunlight that reflects off the ground, snow, or a white roof.</p>
<p>In the right conditions, a bifacial panel can produce up to <strong>30% more energy</strong> than a standard panel of the same size.</p>
<p>If you're limited on space but need maximum charging speed, this is the technology you want.</p>
{cta_button("See Bifacial Panel Options", LINKS['bluetti_generic'])}
<p>Best,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 7 — Day 12
    {
        "day": 12,
        "subject": "Tired of moving panels? Let's look at the roof",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>Portable solar generators are amazing for emergencies, but if you find yourself constantly dragging panels out to keep your batteries full, it might be time to think bigger.</p>
<p>A permanent rooftop solar installation doesn't just charge your portable station &mdash; it offsets your entire monthly electric bill.</p>
<p>The best part? You can now get a professional rooftop solar quote in minutes without a high-pressure salesperson sitting in your living room.</p>
<p>We've partnered with the top installers in the U.S. to provide independent, side-by-side quotes.</p>
{cta_button("Get Your Free Rooftop Solar Quote", f"{SITE}/index#quote-bridge")}
<p>Talk soon,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 8 — Day 14
    {
        "day": 14,
        "subject": "Is a dirty panel killing your ROI?",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>You've invested in high-quality solar. Now, how do you make sure it keeps performing?</p>
<p>A layer of dust, pollen, or bird droppings can drop your panel's efficiency by <strong>15% or more</strong>. That's the difference between a full charge and a dead battery by sunset.</p>
<p>Here are the top 3 maintenance tips:</p>
<ol>
<li><strong>The Hose is Your Friend:</strong> A simple spray-down once a month does wonders.</li>
<li><strong>Check Your Angle:</strong> As the seasons change, the sun's path shifts. A 10-degree adjustment can boost your output significantly.</li>
<li><strong>Inspect the MC4s:</strong> Ensure your connections are tight and corrosion-free.</li>
</ol>
{cta_button("Full Solar Maintenance Guide", f"{SITE}/spec-guide")}
<p>Best,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 9 — Day 16
    {
        "day": 16,
        "subject": "Your generator can protect your home 24/7",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>Most people think solar generators are only for camping or storm blackouts. But the best systems have a feature that changes everything: <strong>UPS Mode.</strong></p>
<p>UPS (Uninterruptible Power Supply) mode keeps your generator plugged into the wall, fully charged, and standing by. The moment your power goes out &mdash; even for a split second &mdash; it switches over in under 20 milliseconds.</p>
<p>That's fast enough that your Wi-Fi router never drops, your CPAP machine never stops, and your security cameras never go dark.</p>
<p>Systems with UPS mode worth considering:</p>
<ul>
<li><strong>BLUETTI AC300</strong> &mdash; 20ms switchover, pairs with up to 4 battery modules<br>
<a href="{LINKS['bluetti_ac300']}" style="color:#1a73e8;">View on BLUETTI</a></li>
<li><strong>EcoFlow DELTA Pro</strong> &mdash; 30ms switchover, whole-home panel integration<br>
<a href="{LINKS['ecoflow']}" style="color:#1a73e8;">View on EcoFlow</a></li>
</ul>
{cta_button("Compare UPS-Capable Systems", f"{SITE}/use-cases")}
<p>Best,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 10 — Day 18
    {
        "day": 18,
        "subject": "Can a solar generator actually run your fridge?",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>The #1 question we get: "Can this thing actually run my refrigerator?"</p>
<p>Short answer: <strong>Yes &mdash; if you size it right.</strong></p>
<p>Here's the real-world math:</p>
<ul>
<li>A standard fridge draws about <strong>150W</strong> running, but surges to <strong>400-600W</strong> when the compressor kicks on.</li>
<li>To run it for 10 hours, you need at least <strong>1,500Wh</strong> of battery capacity.</li>
<li>To handle that compressor surge, you need at least <strong>1,200W</strong> of inverter power (ideally 2,000W+).</li>
</ul>
<p>Beyond the fridge, here's what our readers are actually powering:</p>
<ul>
<li><strong>Chest freezers</strong> (great for storm prep)</li>
<li><strong>Window AC units</strong> (the difference between comfort and misery in July)</li>
<li><strong>Medical devices</strong> &mdash; CPAP, oxygen concentrators, nebulizers</li>
<li><strong>Well pumps</strong> (requires 240V &mdash; only the BLUETTI AC300 Fusion handles this)</li>
</ul>
{cta_button("Size Your System", f"{SITE}/use-cases")}
<p>Best,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 11 — Day 20
    {
        "day": 20,
        "subject": "Taking solar off the grid (literally)",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>Solar generators aren't just for the house. Some of our most passionate readers are using them on the road.</p>
<p><strong>RV / Camper life:</strong><br>
Most RVs come with a basic lead-acid battery that dies after a couple of years. Swapping in a LiFePO4 portable station means you can run your AC, microwave, and coffee maker at a campsite without plugging in &mdash; or running a loud gas generator at 5 AM.</p>
<p><strong>Van life:</strong><br>
Space is everything. The <strong>ALLPOWERS R3500</strong> packs 3,168Wh into a compact footprint with 30A RV plug output built in.</p>
<p><a href="{LINKS['allpowers']}" style="color:#1a73e8;">Check out the ALLPOWERS R3500</a></p>
<p><strong>Tailgating &amp; job sites:</strong><br>
Need to run a blender, speakers, and a TV in a parking lot? A 1,000Wh+ unit handles it all day without fumes or noise complaints.</p>
{cta_button("Compare Portable Options", f"{SITE}/compare")}
<p>Best,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
    # Email 12 — Day 22
    {
        "day": 22,
        "subject": "Hurricane season is here. Is your backup plan ready?",
        "html": wrap_html(f"""
<p>Hi {{{{params.name}}}},</p>
<p>Every year, millions of Americans lose power for 24-72+ hours during storm season. FEMA recommends 72 hours of supplies. Here's how to make sure your solar backup covers that window:</p>
<p><strong>The 72-Hour Solar Checklist:</strong></p>
<ol>
<li><strong>Know your critical loads.</strong> Fridge, phone chargers, medical devices, one light per room, Wi-Fi router. Total: usually 300-500W continuous.</li>
<li><strong>Do the math.</strong> 400W x 72 hours = 28,800Wh. That's a lot &mdash; but you don't run everything 24/7. Realistically, you need <strong>3,000-6,000Wh</strong> of stored capacity.</li>
<li><strong>Have panels ready.</strong> 400W of solar panels during 4 sunny hours = 1,600Wh back into your batteries.</li>
<li><strong>Test it before you need it.</strong> Plug in your fridge and critical devices on a Saturday. Time how long the battery lasts.</li>
<li><strong>Charge everything tonight.</strong> Keep your solar generator at 80%+ at all times during storm season.</li>
</ol>
<p><strong>Our top picks for storm backup:</strong></p>
<ul>
<li><a href="{LINKS['bluetti_ac300']}" style="color:#1a73e8;">BLUETTI AC300 + B300</a> &mdash; expandable, UPS mode</li>
<li><a href="{LINKS['ecoflow']}" style="color:#1a73e8;">EcoFlow DELTA Pro</a> &mdash; whole-home integration</li>
<li><a href="{LINKS['allpowers']}" style="color:#1a73e8;">ALLPOWERS R3500</a> &mdash; best value for capacity</li>
</ul>
{cta_button("Find the Right System for Your Home", f"{SITE}/use-cases")}
<p>Stay safe,<br>Solana<br>Sun Energy Technology</p>
"""),
    },
]


def load_api_key():
    global API_KEY
    import os
    env_path = os.path.expanduser("~/.kiyomimax/.env")
    with open(env_path) as f:
        for line in f:
            if line.startswith("BREVO_API_KEY="):
                API_KEY = line.strip().split("=", 1)[1]
                return
    raise RuntimeError("BREVO_API_KEY not found")


def brevo_get(endpoint):
    resp = requests.get(
        f"https://api.brevo.com/v3{endpoint}",
        headers={"api-key": API_KEY, "accept": "application/json"},
        timeout=30,
    )
    return resp.json()


def brevo_post(endpoint, data):
    resp = requests.post(
        f"https://api.brevo.com/v3{endpoint}",
        headers={"api-key": API_KEY, "Content-Type": "application/json", "accept": "application/json"},
        json=data,
        timeout=30,
    )
    return resp.status_code, resp.json()


def brevo_put(endpoint, data):
    resp = requests.put(
        f"https://api.brevo.com/v3{endpoint}",
        headers={"api-key": API_KEY, "Content-Type": "application/json", "accept": "application/json"},
        json=data,
        timeout=30,
    )
    return resp.status_code


def get_list_contacts():
    contacts = []
    offset = 0
    while True:
        data = brevo_get(f"/contacts/lists/{LIST_ID}/contacts?limit=50&offset={offset}")
        batch = data.get("contacts", [])
        if not batch:
            break
        contacts.extend(batch)
        offset += len(batch)
        if offset >= data.get("count", 0):
            break
    return contacts


def send_email(to_email, to_name, subject, html_content):
    name = to_name if to_name else "there"
    html_personalized = html_content.replace("{{params.name}}", name)

    payload = {
        "sender": SENDER,
        "to": [{"email": to_email, "name": to_name or to_email}],
        "replyTo": REPLY_TO,
        "subject": subject,
        "htmlContent": html_personalized,
    }
    status_code, resp = brevo_post("/smtp/email", payload)
    return status_code in (200, 201), resp


def update_contact_step(email, step, subscribe_date=None):
    attrs = {"SOLAR_SEQUENCE_STEP": step}
    if subscribe_date:
        attrs["SOLAR_SUBSCRIBE_DATE"] = subscribe_date
    brevo_put(f"/contacts/{requests.utils.quote(email)}", {"attributes": attrs})


def run_init():
    """Initialize existing subscribers: set step=0 and subscribe_date=today for anyone without them."""
    print("=== INIT MODE: Setting up existing subscribers ===\n")
    contacts = get_list_contacts()
    today = datetime.now().strftime("%Y-%m-%d")
    initialized = 0

    for c in contacts:
        attrs = c.get("attributes", {})
        step = attrs.get("SOLAR_SEQUENCE_STEP")
        sub_date = attrs.get("SOLAR_SUBSCRIBE_DATE")

        if step is None or step == 0:
            if not sub_date:
                update_contact_step(c["email"], 0, today)
                print(f"  [INIT] {c['email']} — set step=0, date={today}")
                initialized += 1
            else:
                print(f"  [SKIP] {c['email']} — already has date={sub_date}")
        else:
            print(f"  [SKIP] {c['email']} — already on step {int(step)}")

    print(f"\nInitialized {initialized} contacts. Run again with --send to start sending.")


def run_automation(dry_run=True):
    """Main automation loop: check each contact and send the next email if due."""
    mode = "DRY RUN" if dry_run else "LIVE SEND"
    print(f"=== S.E.T. Solar Welcome Automation ({mode}) ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    contacts = get_list_contacts()
    today = datetime.now().date()
    sent_count = 0
    skip_count = 0
    error_count = 0

    for c in contacts:
        email = c["email"]
        attrs = c.get("attributes", {})
        name = attrs.get("FIRSTNAME", "")
        step = int(attrs.get("SOLAR_SEQUENCE_STEP") or 0)
        sub_date_str = attrs.get("SOLAR_SUBSCRIBE_DATE", "")

        if not sub_date_str:
            print(f"  [SKIP] {email} — no subscribe date (run --init first)")
            skip_count += 1
            continue

        try:
            sub_date = datetime.strptime(sub_date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"  [SKIP] {email} — invalid date: {sub_date_str}")
            skip_count += 1
            continue

        days_since_signup = (today - sub_date).days

        if step >= len(SEQUENCE):
            print(f"  [DONE] {email} — completed all {len(SEQUENCE)} emails")
            skip_count += 1
            continue

        next_email = SEQUENCE[step]
        target_day = next_email["day"]

        if days_since_signup < target_day:
            print(f"  [WAIT] {email} — step {step}, day {days_since_signup}/{target_day}")
            skip_count += 1
            continue

        print(f"  [SEND] {email} — Email {step+1}: \"{next_email['subject']}\" (day {days_since_signup}, target day {target_day})")

        if not dry_run:
            success, resp = send_email(email, name, next_email["subject"], next_email["html"])
            if success:
                update_contact_step(email, step + 1)
                print(f"         Sent OK — step updated to {step + 1}")
                sent_count += 1
            else:
                print(f"         ERROR: {resp}")
                error_count += 1
            time.sleep(1)
        else:
            sent_count += 1

    print(f"\n=== Summary ===")
    print(f"Contacts checked: {len(contacts)}")
    print(f"{'Would send' if dry_run else 'Sent'}: {sent_count}")
    print(f"Skipped/waiting: {skip_count}")
    if error_count:
        print(f"Errors: {error_count}")
    if dry_run and sent_count > 0:
        print(f"\nRun with --send to send these emails for real.")


if __name__ == "__main__":
    load_api_key()

    if "--init" in sys.argv:
        run_init()
    elif "--send" in sys.argv:
        run_automation(dry_run=False)
    else:
        run_automation(dry_run=True)
