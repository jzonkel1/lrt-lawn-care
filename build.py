# -*- coding: utf-8 -*-
"""
LRT Lawn Care & Landscaping — static site generator.

    python build.py

Every page on the site is emitted from this file. The generated HTML files
carry a "generated" banner comment — DON'T hand-edit them; edit the data /
templates here and re-run.

Facts sourced from the client's Fillout onboarding (Aug 2026) and
research-notes.md in the DEMOS folder. Pricing is QUOTE-ONLY by the
client's explicit choice — never print dollar amounts.
"""
import html as htmllib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent

# Optional URL prefix for the GitHub Pages preview build, which serves under
# /<repo-name>/ instead of the domain root. The master branch is always built
# WITHOUT a base (Netlify-ready); the gh-pages branch is built with:
#   LRT_BASE=/lrt-lawn-care python build.py
BASE = os.environ.get("LRT_BASE", "").rstrip("/")

# Absolute origin used for canonical URLs, og: tags, schema and sitemap.xml.
# TODO AT LAUNCH: change this default to the real domain (https://...) once
# it's registered and the Netlify site is live, then rebuild BOTH branches.
SITE_URL = os.environ.get("LRT_SITE_URL", "https://jzonkel1.github.io/lrt-lawn-care").rstrip("/")

# ============================================================
# BUSINESS DATA
# ============================================================
BIZ = "LRT Lawn Care &amp; Landscaping"
BIZ_LLC = "LRT Lawn Care &amp; Landscaping, LLC"
PHONE = "(361) 765-5258"
TEL = "tel:+13617655258"
SMS = "sms:+13617655258"
EMAIL = "lachristian.thomas@gmail.com"
FB = "https://www.facebook.com/LRTMowingAndSmallLandscapingProjects/"
TAGLINE = "Taking Pride in Every Property We Maintain."
HOURS = "Monday&ndash;Friday, 8am&ndash;5pm"

# ============================================================
# ICONS (lucide, matching the demo)
# ============================================================
IC = {
 "phone": '<path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/>',
 "phone2": '<path d="M13 2a9 9 0 0 1 9 9"/><path d="M13 6a5 5 0 0 1 5 5"/><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "chev": '<path d="m9 18 6-6-6-6"/>',
 "chevd": '<path d="m6 9 6 6 6-6"/>',
 "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
 "mail": '<path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/><rect x="2" y="4" width="20" height="16" rx="2"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
 "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="m9 16 2 2 4-4"/>',
 "card": '<rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/>',
 "building": '<path d="M10 12h4"/><path d="M10 8h4"/><path d="M14 21v-3a2 2 0 0 0-4 0v3"/><path d="M6 10H4a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2"/><path d="M6 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16"/>',
 "layers": '<path d="m12 8 6-3-6-3v10"/><path d="m8 11.99-5.5 3.14a1 1 0 0 0 0 1.74l8.5 4.86a2 2 0 0 0 2 0l8.5-4.86a1 1 0 0 0 0-1.74L16 12"/><path d="m6.49 12.85 11.02 6.3"/><path d="M17.51 12.85 6.5 19.15"/>',
 "sprout": '<path d="M12 5a3 3 0 1 1 3 3m-3-3a3 3 0 1 0-3 3m3-3v1M9 8a3 3 0 1 0 3 3M9 8h1m5 0a3 3 0 1 1-3 3m3-3h-1m-2 3v-1"/><circle cx="12" cy="8" r="2"/><path d="M12 10v12"/><path d="M12 22c4.2 0 7-1.667 7-5-4.2 0-7 1.667-7 5Z"/><path d="M12 22c-4.2 0-7-1.667-7-5 4.2 0 7 1.667 7 5Z"/>',
 "tree": '<path d="M10 10v.2A3 3 0 0 1 8.9 16H5a3 3 0 0 1-1-5.8V10a3 3 0 0 1 6 0Z"/><path d="M7 16v6"/><path d="M13 19v3"/><path d="M12 19h8.3a1 1 0 0 0 .7-1.7L18 14h.3a1 1 0 0 0 .7-1.7L16 9h.2a1 1 0 0 0 .8-1.7L13 3l-1.4 1.5"/>',
 "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
 "grass": '<path d="M14 9.536V7a4 4 0 0 1 4-4h1.5a.5.5 0 0 1 .5.5V5a4 4 0 0 1-4 4 4 4 0 0 0-4 4c0 2 1 3 1 5a5 5 0 0 1-1 3"/><path d="M4 9a5 5 0 0 1 8 4 5 5 0 0 1-8-4"/><path d="M5 21h14"/>',
 "mower": '<circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/>',
 "shovel": '<path d="M2 22v-5l5-5 5 5-5 5z"/><path d="M9.5 14.5 16 8"/><path d="m17 2 5 5-.5.5a3.53 3.53 0 0 1-5 0s0 0 0 0a3.53 3.53 0 0 1 0-5L17 2"/>',
 "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
 "pick": '<path d="M21.56 4.56a1.5 1.5 0 0 1 0 2.122l-.47.47a3 3 0 0 1-4.212-.03 3 3 0 0 1 0-4.243l.44-.44a1.5 1.5 0 0 1 2.121 0z"/><path d="M3 22a1 1 0 0 1-1-1v-3.586a1 1 0 0 1 .293-.707l3.355-3.355a1.205 1.205 0 0 1 1.704 0l3.296 3.296a1.205 1.205 0 0 1 0 1.704l-3.355 3.355a1 1 0 0 1-.707.293z"/><path d="m9 15 7.879-7.878"/>',
 "expand": '<path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/>',
 "quote": '<path d="M16 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z"/><path d="M5 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z"/>',
 "home": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 "handshake": '<path d="M11 15h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 17"/><path d="m7 21 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9"/><path d="m2 16 6 6"/><circle cx="16" cy="9" r="2.9"/><circle cx="6" cy="5" r="3"/>',
 "msg": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
}
FB_PATH = '<path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/>'

def ic(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24">{IC[name]}</svg>'

def fbic():
    return f'<svg class="ic ic-f" viewBox="0 0 24 24">{FB_PATH}</svg>'

TIKTOK = "https://www.tiktok.com/@lachristianthomas"
TT_PATH = '<path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/>'

def ttic():
    return f'<svg class="ic ic-f" viewBox="0 0 24 24">{TT_PATH}</svg>'

# ============================================================
# SERVICES
# ============================================================
SERVICES = [
 dict(
  slug="commercial-lawn-maintenance", kind="Recurring &middot; weekly or bi-weekly", name="Commercial Lawn Maintenance", icon="building",
  card_photo="g-field-mowers.webp", card_alt="Two SCAG zero-turn mowers cutting a large open commercial field",
  card_desc="The recurring one: mowing, edging and grounds upkeep on a fixed weekly or bi-weekly schedule &mdash; including the ditches, right-of-ways and fence lines most crews skip.",
  tags=["Fixed schedule","Ditch &amp; ROW","Fully insured"],
  title="Commercial Lawn Maintenance | Coastal Bend, TX",
  desc="Fully insured commercial lawn maintenance for offices, retail, rentals, HOAs and industrial sites in Portland, Corpus Christi and the Coastal Bend. Fixed schedule, one invoice. Call (361) 765-5258.",
  h1="Commercial lawn maintenance that <em>holds its schedule</em>.",
  sub="Offices, storefronts, rental properties and multi-building sites across the Coastal Bend &mdash; one crew, one schedule, one invoice.",
  hero_photo="hero-field-mowers.webp", hero_alt="Two SCAG zero-turn mowers cutting a large open commercial field",
  intro=[
   "A commercial property doesn&rsquo;t get an off week. LRT keeps offices, retail centers, rental properties, HOA common areas, municipal grounds and industrial sites on a fixed service day, so the grounds look the same sharp way every time a tenant, customer or property manager pulls in.",
   "LaChristian has spent 12 years maintaining Coastal Bend properties &mdash; ten of them running commercial routes for other companies, the last two building LRT&rsquo;s own book. The person who walks your site and quotes it is the same person who shows up to cut it.",
  ],
  prop_types=["Offices","Retail &amp; shopping centers","Rental properties","HOAs","Municipal &amp; government","Industrial"],
  includes=[
   "Mowing on a fixed, scheduled day",
   "Edging &amp; weed-eating along walks, curbs &amp; fence lines",
   "Blow down of walkways, drives &amp; lots",
   "Ditches &amp; right-of-ways included",
   "Shrub &amp; bed upkeep on request",
   "Invoicing or card on file &mdash; your call",
  ],
  photo="g-commercial-lot.webp", photo_alt="A newly picked-up commercial property with the grounds mowed to the fence line",
  photo_cap="A commercial property on the route, mowed to the fence line.",
  faqs=[
   ("Are you insured?", "Yes &mdash; $1,000,000 general liability with a $2,000,000 aggregate, on an active commercial policy. We can provide documentation for your vendor file."),
   ("Do you work off a contract?", "Whatever your property needs. Written service agreements are available for commercial accounts; some owners prefer a simple standing schedule. Both work."),
   ("How does billing work?", "Commercial accounts can be invoiced (Stripe) or keep a card on file so service just runs. No chasing paperwork every month."),
   ("How do I get a price?", "Call, text or send the form with the property address. We&rsquo;ll walk the site and quote it per property &mdash; free, no obligation."),
  ],
  related=["commercial-landscaping","pressure-washing","seasonal-cleanups-haul-off"],
 ),
 dict(
  slug="residential-lawn-care", kind="Recurring &middot; weekly or bi-weekly", name="Residential Lawn Care", icon="grass",
  card_photo="svc-residential-front.webp", card_alt="A freshly mowed front lawn with clean rock beds in front of a stone-fronted house",
  card_desc="Mow, edge, weed-eat and blow down &mdash; front, back and sides &mdash; on a weekly or bi-weekly route so your yard never gets away from you.",
  tags=["Mowing","Edging","Weed eating","Blow down"],
  title="Residential Lawn Care | Portland &amp; Corpus Christi, TX",
  desc="Weekly and bi-weekly residential lawn care in Portland, Corpus Christi and the Coastal Bend. Mow, edge, weed-eat and blow down every visit. Free quotes — call or text (361) 765-5258.",
  h1="A yard that never <em>gets away</em> from you.",
  sub="Weekly or bi-weekly service &mdash; front, back and sides &mdash; edged, weed-eaten and blown down before we leave.",
  hero_photo="hero-pool.webp", hero_alt="A backyard pool bordered by mowed lawn and a clean patio",
  intro=[
   "Every visit is the full job: mow the front, back and sides, edge along the driveway and walks, weed-eat the fence lines and beds, and blow every hard surface down before the trailer leaves. Not a quick pass with the gate left open &mdash; the whole yard, done right the first time.",
   "Recurring customers get a consistent day on the route, so the yard never reaches that embarrassing stage between cuts. Keep a card on file and the billing takes care of itself, or pay per visit &mdash; cash, check, Zelle, Venmo or Cash App all work.",
  ],
  includes=[
   "Mowing &mdash; front, back &amp; side yards",
   "Edging along drives, walks &amp; curbs",
   "Weed-eating fence lines &amp; beds",
   "Blow down of all hard surfaces",
   "A consistent day on the route",
   "Card on file optional &mdash; or pay per visit",
  ],
  photo="g-front-drive.webp", photo_alt="A crisply edged front lawn meeting a curved concrete driveway",
  photo_cap="A front lawn on the weekly route &mdash; mowed, edged and blown down.",
  faqs=[
   ("How much is a weekly cut?", "Every lawn is different, so we quote per property &mdash; free and no obligation. Call or text with your address and you&rsquo;ll usually have a number the same day."),
   ("Weekly or bi-weekly &mdash; which do I need?", "Through the Coastal Bend growing season most lawns need weekly service to stay sharp. Slower-growing or shaded lawns do fine on bi-weekly. We&rsquo;ll tell you honestly which one your yard needs."),
   ("Do I need to be home?", "No &mdash; most customers aren&rsquo;t. Just make sure the gate is unlocked on your service day."),
   ("Can I get just one cut?", "Yes. One-time cuts and as-needed service are welcome &mdash; and if the yard has gotten away from you, that&rsquo;s exactly the kind of job we post before-and-afters of."),
  ],
  related=["residential-landscaping","tree-shrub-trimming","seasonal-cleanups-haul-off"],
 ),
 dict(
  slug="commercial-landscaping", kind="Project &middot; install &amp; upkeep", name="Commercial Landscaping", icon="layers",
  card_photo="svc-commercial-rig.webp", card_alt="LRT's truck and trailer at a commercial property with fresh rock beds and ornamental grasses",
  card_desc="The project one: beds, borders, plantings, mulch and sod installed once &mdash; then handed to the maintenance route so they hold up.",
  tags=["Beds &amp; borders","Mulch &amp; sod","Property appearance"],
  title="Commercial Landscaping | Coastal Bend, TX",
  desc="Commercial landscaping for offices, retail centers, rentals and HOAs in Portland, Corpus Christi and the Coastal Bend — installed, then maintained. Call (361) 765-5258.",
  h1="Landscaping that makes a property <em>easier to lease</em>.",
  sub="Beds, borders, plantings, mulch and sod for offices, centers and multi-unit properties &mdash; installed, then maintained.",
  hero_photo="hero-commercial.webp", hero_alt="LRT's truck and enclosed trailer at a commercial property, fresh rock beds and ornamental grasses in the foreground",
  intro=[
   "Curb appeal is the first thing a prospective tenant, buyer or customer judges a property on &mdash; before they ever see the inside. LRT builds and maintains the beds, borders and plantings that make a commercial property read as well-run from the street.",
   "The difference with LRT is what happens after the install: the same crew that put the landscape in keeps it on the maintenance schedule, so beds actually fill in and hold up instead of going shaggy by the next quarter. That&rsquo;s the property appearance management side of the business &mdash; one vendor responsible for how the whole site looks, year round.",
  ],
  prop_types=["Offices","Retail &amp; shopping centers","Rental properties","HOAs","Municipal &amp; government","Industrial"],
  includes=[
   "Beds, borders &amp; plantings",
   "Mulch installation",
   "Sod installation",
   "Shrub &amp; tree trimming",
   "Property appearance management",
   "Ongoing maintenance after the install",
  ],
  photo="svc-commercial-beds.webp", photo_alt="A fresh river-rock bed cut in along the mowed lawn at a commercial property",
  photo_cap="Rock beds cut in at a commercial site &mdash; installed by LRT, then kept on the route.",
  faqs=[
   ("Do you maintain what you install?", "Yes &mdash; that&rsquo;s the point. Most commercial landscaping fails because nobody maintains it after the install. LRT quotes the install and the upkeep together so the property keeps looking the way it did on day one."),
   ("What kinds of properties do you take on?", "Offices, retail and shopping centers, rental and multi-unit properties, HOA common areas, municipal grounds and industrial sites across the Coastal Bend."),
   ("Are you insured?", "Yes &mdash; $1,000,000 general liability with a $2,000,000 aggregate, on an active commercial policy."),
   ("How do I get a price?", "Call or text with the property address, or send the form. We&rsquo;ll walk the site with you and quote the work per property &mdash; free, no obligation."),
  ],
  related=["commercial-lawn-maintenance","mulch-sod-installation","pressure-washing"],
 ),
 dict(
  slug="residential-landscaping", kind="Project &middot; install &amp; upkeep", name="Residential Landscaping", icon="sprout",
  card_photo="svc-landscaping.webp", card_alt="A curved decomposed granite walkway installed through fresh sod",
  card_desc="Beds, borders, walkways, rock beds and plantings designed for your yard &mdash; then maintained so they actually fill in and hold up.",
  tags=["Mulch install","Sod install","Beds &amp; walkways"],
  title="Residential Landscaping | Portland &amp; Corpus Christi, TX",
  desc="Residential landscaping in Portland, Corpus Christi and the Coastal Bend — beds, borders, walkways, rock beds, mulch and sod, installed and maintained. Free quotes — call or text (361) 765-5258.",
  h1="Built for your yard, <em>then maintained</em>.",
  sub="Beds, borders, walkways, rock beds and plantings &mdash; designed for the property and kept up after the install.",
  hero_photo="svc-landscaping.webp", hero_alt="A curved decomposed granite walkway installed through fresh sod",
  intro=[
   "A landscape install only looks good long-term if somebody keeps it up. LRT designs beds, borders, walkways and plantings around how your yard actually gets used &mdash; then keeps them on the maintenance route so they fill in the way the plan intended.",
   "And when the request is unusual, we don&rsquo;t talk you out of it. One client wanted a crape myrtle where there was nothing but concrete slab &mdash; so we marked the circle, broke it out, hauled it off and backfilled a clean planting hole. <a href=\"/our-work/\">See it on the Our Work page.</a>",
  ],
  includes=[
   "Beds &amp; borders",
   "Mulch installation",
   "Sod installation",
   "Rock beds &amp; ground cover",
   "Walkways &amp; paths",
   "Shrub &amp; tree plantings",
  ],
  photo="g-path-wide.webp", photo_alt="A backyard landscape install with a curving granite path through fresh sod",
  photo_cap="A backyard install &mdash; granite path curving through fresh sod.",
  faqs=[
   ("Where do I start if I just have an idea?", "Send a photo of the yard and tell us what you&rsquo;re picturing &mdash; text works great for this. We&rsquo;ll come look at the space and talk through what fits it and what it takes."),
   ("Will you maintain it afterward?", "Yes &mdash; installs can go straight onto the weekly or bi-weekly route so the new landscape gets edged, weeded and kept up instead of left to fend for itself."),
   ("How is it priced?", "Quoted per job, free and no obligation. Materials and scope vary too much for flat rates, so we look at the yard first and give you a real number."),
   ("Can you work around existing concrete or structures?", "Yes &mdash; we&rsquo;ve broken out slab concrete to open up planting space and built beds around trees, walkways and pool decks."),
  ],
  related=["mulch-sod-installation","residential-lawn-care","tree-shrub-trimming"],
 ),
 dict(
  slug="tree-shrub-trimming", kind="Recurring or one-time", name="Tree &amp; Shrub Trimming", icon="tree",
  card_photo="svc-shrub-trim.webp", card_alt="A tightly trimmed hedge line running along a walkway",
  card_desc="Shrub and tree trimming that keeps sight lines open, walkways clear and the front of the property looking sharp.",
  tags=["Shrub trimming","Tree trimming"],
  title="Tree &amp; Shrub Trimming | Coastal Bend, TX",
  desc="Shrub shaping and tree trimming in Portland, Corpus Christi and the Coastal Bend — sight lines opened, walkways cleared, debris hauled off. Free quotes — call or text (361) 765-5258.",
  h1="Trimmed, shaped, and the <em>debris hauled off</em>.",
  sub="Shrubs shaped, trees trimmed, walkways and entries cleared &mdash; and everything we cut leaves on the trailer.",
  hero_photo="hero-shrub-trim.webp", hero_alt="A tightly trimmed hedge line running along a walkway",
  intro=[
   "Overgrown shrubs and low branches sneak up on a property &mdash; they block windows and sight lines, crowd walkways, and make an otherwise-maintained yard look neglected. Regular trimming keeps the shape tight and the property looking deliberate.",
   "Trimming can ride along with your regular lawn service or run as a stand-alone visit. Either way the clippings and branches go on the trailer, not in a pile at your curb.",
  ],
  includes=[
   "Shrub trimming &amp; shaping",
   "Hedge lines kept tight",
   "Tree trimming",
   "Walkways, entries &amp; windows cleared",
   "Beds cleaned up after the cut",
   "All debris hauled off",
  ],
  photo="g-entry-beds.webp", photo_alt="A home entry walkway with trimmed shrubs and a clean rock border",
  photo_cap="An entry kept clear &mdash; shrubs shaped, borders clean.",
  faqs=[
   ("How often should shrubs be trimmed?", "It depends on the plant and the season &mdash; most Coastal Bend hedges look their best trimmed a few times a year. If you&rsquo;re on the weekly or bi-weekly route we can keep an eye on them and trim as needed."),
   ("Do you haul the branches away?", "Yes. Everything we cut leaves with us on the trailer &mdash; nothing bagged and left at the curb."),
   ("How big a tree can you take on?", "We handle standard residential and commercial trimming. Tell us what you&rsquo;ve got &mdash; if a job genuinely needs a specialty tree crew, we&rsquo;ll say so instead of winging it."),
   ("How is it priced?", "Quoted per job, free and no obligation. Send a photo by text and you&rsquo;ll usually have a number the same day."),
  ],
  related=["residential-lawn-care","seasonal-cleanups-haul-off","residential-landscaping"],
 ),
 dict(
  slug="mulch-sod-installation", kind="Project &middot; one-time install", name="Mulch &amp; Sod Installation", icon="shovel",
  card_photo="g-path-tall.webp", card_alt="A curved decomposed granite walkway running through thick green turf",
  card_desc="Fresh mulch in the beds and new sod where the yard needs it &mdash; prepped, installed and edged so it takes.",
  tags=["Mulch install","Sod install","Bed prep"],
  title="Mulch &amp; Sod Installation | Coastal Bend, TX",
  desc="Mulch and sod installation in Portland, Corpus Christi and the Coastal Bend — beds prepped, mulch laid, sod installed and edged. Free quotes — call or text (361) 765-5258.",
  h1="Fresh mulch and new sod, <em>put down right</em>.",
  sub="Beds prepped and mulched, worn turf replaced with new sod &mdash; and the leftovers hauled off.",
  hero_photo="g-path-tall.webp", hero_alt="A curved decomposed granite walkway running through thick green turf",
  intro=[
   "Mulch is the fastest way to make a property look cared for &mdash; it sharpens every bed line, holds moisture through the Coastal Bend heat and keeps the weeds down. We prep the beds first, so the mulch goes down on clean ground instead of burying the problem.",
   "Sod fixes what seed can&rsquo;t: bare patches, dog runs, builder-grade dirt yards and turf that&rsquo;s past saving. We install it, edge it in, and it can go straight onto the mowing route once it takes.",
  ],
  includes=[
   "Bed preparation &amp; weed removal",
   "Mulch installation",
   "Sod installation",
   "Edging &amp; clean bed lines",
   "Old material &amp; debris hauled off",
   "Onto the mowing route once it takes",
  ],
  photo="g-rock-bed.webp", photo_alt="A white rock bed built around a tree with an address stone set in the middle",
  photo_cap="A rock bed built around a tree, address stone set in the middle.",
  faqs=[
   ("When&rsquo;s the best time to lay sod here?", "The Coastal Bend&rsquo;s long warm season gives sod a wide window &mdash; the main thing is water while it establishes. We&rsquo;ll tell you what your timing and yard realistically need."),
   ("Do you remove the old mulch or grass first?", "Yes &mdash; beds get cleaned and prepped, and dead turf comes out before new sod goes down. The old material leaves on the trailer."),
   ("How is it priced?", "Quoted per job based on the area and materials &mdash; free and no obligation. A couple of photos by text is enough for a rough number."),
  ],
  related=["residential-landscaping","commercial-landscaping","residential-lawn-care"],
 ),
 dict(
  slug="seasonal-cleanups-haul-off", kind="One-time visits", name="Clean-Ups &amp; Haul-Off", icon="truck",
  card_photo="svc-cleanup.webp", card_alt="LRT's trailer loaded with broken-out concrete ready to be hauled off",
  card_desc="Seasonal clean-ups, leaf removal and yard clean-outs with the debris hauled off &mdash; not bagged and left at the curb.",
  tags=["Seasonal clean-up","Leaf removal","Haul off"],
  title="Yard Clean-Ups, Leaf Removal &amp; Haul-Off | Coastal Bend, TX",
  desc="Seasonal clean-ups, leaf removal and yard clean-outs in Portland, Corpus Christi and the Coastal Bend — debris loaded and hauled off, not left at the curb. Call or text (361) 765-5258.",
  h1="One visit, and the mess is <em>actually gone</em>.",
  sub="Seasonal clean-ups, leaf removal and yard clean-outs &mdash; loaded on the trailer and hauled off, not left bagged at the curb.",
  hero_photo="svc-cleanup.webp", hero_alt="LRT's trailer loaded with broken-out concrete ready to be hauled off",
  intro=[
   "Some yards just need a reset &mdash; a season&rsquo;s worth of leaves, an overgrown stretch that got away, a property changing hands, or a pile of green waste nobody wants to deal with. A clean-up visit knocks it all down in one go.",
   "The part most crews skip is the part we lead with: the haul-off. Everything we cut, rake and pull goes on the trailer and leaves with us. You get your yard back, not a row of bags at the curb waiting on collection day.",
  ],
  includes=[
   "Seasonal clean-ups",
   "Leaf removal",
   "Overgrowth cut back &amp; cleared",
   "Beds cleaned out",
   "Yard clean-up &amp; haul off",
   "Trailer-load debris removal",
  ],
  photo="g-concrete-dig.webp", photo_alt="Breaking out concrete by hand to open a planting hole",
  photo_cap="When the job calls for it, we break it out and haul it off ourselves.",
  faqs=[
   ("The yard is really far gone. Is that a problem?", "No &mdash; overgrown yards are normal work for us, and honestly the before-and-afters are the fun part. No judgment; send a photo and we&rsquo;ll quote it."),
   ("Where does the debris go?", "On our trailer and off your property &mdash; we handle the disposal. Nothing gets left bagged at the curb."),
   ("Can a clean-up turn into regular service?", "That&rsquo;s the most common path: one reset visit, then weekly or bi-weekly service so it never gets back to that point."),
   ("How is it priced?", "Quoted per job &mdash; the honest answer is it depends on how much there is to cut and haul. Photos by text get you a fast, free estimate."),
  ],
  related=["residential-lawn-care","tree-shrub-trimming","mulch-sod-installation"],
 ),
 dict(
  slug="pressure-washing", kind="One-time or add-on", name="Pressure Washing", icon="droplet",
  card_photo="g-walk-edges.webp", card_alt="Two concrete walkways meeting with sharply edged turf on every side",
  card_desc="Driveways, sidewalks, curbs and flatwork washed clean &mdash; as a stand-alone visit or an add-on to your maintenance schedule.",
  tags=["Driveways","Sidewalks","Flatwork"],
  title="Pressure Washing | Coastal Bend, TX",
  desc="Pressure washing for driveways, sidewalks, curbs and flatwork in Portland, Corpus Christi and the Coastal Bend — stand-alone or added to a maintenance schedule. Call or text (361) 765-5258.",
  h1="Concrete that looks as clean as <em>the lawn</em>.",
  sub="Driveways, sidewalks, curbs and flatwork &mdash; washed as a stand-alone visit or added onto your maintenance schedule.",
  hero_photo="g-walk-edges.webp", hero_alt="Two concrete walkways meeting with sharply edged turf on every side",
  intro=[
   "A sharp lawn next to a stained driveway is a half-finished look. Pressure washing brings the concrete back to match the turf &mdash; drives, walks, curbs, patios and storefront flatwork.",
   "For commercial properties it pairs naturally with scheduled maintenance: the same vendor that keeps the grounds cut keeps the hard surfaces clean, so the whole site reads well-run from the street.",
  ],
  includes=[
   "Driveways &amp; sidewalks",
   "Curbs &amp; gutters",
   "Patios &amp; pool surrounds",
   "Storefront walks &amp; pads",
   "Stand-alone visits welcome",
   "Or added to a maintenance schedule",
  ],
  photo="g-front-drive.webp", photo_alt="A crisply edged front lawn meeting a curved concrete driveway",
  photo_cap="Clean lines where turf meets concrete &mdash; the whole point.",
  faqs=[
   ("Is it a stand-alone service?", "Either way &mdash; book a one-time wash, or add it onto a residential or commercial maintenance schedule so it happens on a rhythm."),
   ("What do you wash?", "Concrete and hard surfaces: driveways, sidewalks, curbs, patios and commercial flatwork. Tell us what you&rsquo;ve got and we&rsquo;ll tell you if it&rsquo;s a fit."),
   ("How is it priced?", "Quoted per job based on the area &mdash; free and no obligation. Call or text a photo for a fast number."),
  ],
  related=["commercial-lawn-maintenance","residential-lawn-care","seasonal-cleanups-haul-off"],
 ),
]

SVC_BY_SLUG = {s["slug"]: s for s in SERVICES}

# the six services featured on the home page
HOME_SERVICES = ["commercial-lawn-maintenance","residential-lawn-care","commercial-landscaping",
                 "residential-landscaping","tree-shrub-trimming","seasonal-cleanups-haul-off"]

# ============================================================
# SERVICE AREAS
# All towns sit inside the ~45-mile radius from Portland that
# LaChristian gave on his onboarding form. The first five are the
# towns he names publicly on Facebook as his service area.
# ============================================================
TOWNS = [
 dict(slug="portland", name="Portland", named=True,
  card="Home base. The trailers roll out from Portland every morning, and most of the weekly route runs through town.",
  intro=[
   "LRT Lawn Care &amp; Landscaping is based right here in Portland &mdash; this is home base, not the far end of a service map. Most of the weekly route runs through town, which usually means a new Portland address can slot into an existing route day the same week.",
   "From tight residential yards to commercial sites and rental properties, Portland is where LRT&rsquo;s work is easiest to see in person. Drive around &mdash; the striped lawns are the portfolio.",
  ],
  note="Home base &mdash; fastest scheduling on the route."),
 dict(slug="corpus-christi", name="Corpus Christi", named=True,
  card="Across the bridge and on the route &mdash; residential yards and commercial properties throughout the city.",
  intro=[
   "Corpus Christi is the biggest stop on LRT&rsquo;s route &mdash; just across the bridge from home base in Portland. We service residential yards and commercial properties throughout the city.",
   "For offices, retail centers and rental properties especially, Corpus Christi is where a fixed maintenance schedule earns its keep: one vendor, one invoice, and grounds that look the same sharp way every week of the year.",
  ],
  note="On the regular route, minutes from home base."),
 dict(slug="ingleside", name="Ingleside", named=True,
  card="On the north shore of the bay and on LRT's named service area — residential and commercial alike.",
  intro=[
   "Ingleside sits an easy run down the highway from Portland, and it&rsquo;s part of the service area LRT has covered from the start &mdash; residential yards, rental properties and commercial sites alike.",
   "Coastal lots grow fast and salty wind is hard on plantings; a consistent weekly or bi-weekly schedule is what keeps an Ingleside yard from swinging between overgrown and scalped.",
  ],
  note="Part of LRT&rsquo;s core service area."),
 dict(slug="aransas-pass", name="Aransas Pass", named=True,
  card="The gateway town to the island — part of LRT's core service area for lawns and commercial grounds.",
  intro=[
   "Aransas Pass has been on LRT&rsquo;s service map from the beginning &mdash; homes, rentals and the commercial properties that serve traffic headed for the island.",
   "For businesses on the highway frontage, appearance is the whole first impression. A fixed maintenance schedule keeps the grounds sharp without you having to think about it.",
  ],
  note="Part of LRT&rsquo;s core service area."),
 dict(slug="rockport", name="Rockport", named=True,
  card="Rockport-Fulton's homes, rentals and bayfront properties — the north end of LRT's core service area.",
  intro=[
   "Rockport &mdash; and Fulton next door &mdash; marks the north end of LRT&rsquo;s core service area. Homes, vacation rentals and commercial properties here all get the same treatment: a consistent schedule and a full service every visit.",
   "Rental owners especially benefit from a lawn crew that shows up on schedule without being chased &mdash; the yard is guest-ready whether or not you&rsquo;re in town.",
  ],
  note="Core service area &mdash; Fulton included."),
 dict(slug="gregory", name="Gregory", named=False,
  card="Right next door to Portland on US-181 — minutes from home base.",
  intro=[
   "Gregory is right next door to home base &mdash; a few minutes up US-181 from Portland. That makes scheduling easy: Gregory addresses can usually ride the same route days as Portland.",
   "Residential yards, rental properties and commercial lots in Gregory all quote the same way as everywhere else: free, per property, usually same-day.",
  ],
  note="Minutes from home base in Portland."),
 dict(slug="taft", name="Taft", named=False,
  card="A short run up US-181 — well inside LRT's service radius.",
  intro=[
   "Taft sits a short run north on US-181, well inside LRT&rsquo;s service radius from Portland. Homes, rentals and commercial properties in Taft can all get on the schedule.",
   "Bigger small-town lots are exactly what commercial-grade equipment is for &mdash; the same machines that handle multi-acre commercial sites make quick, clean work of a large Taft yard.",
  ],
  note="Well inside the service radius."),
 dict(slug="sinton", name="Sinton", named=False,
  card="The San Patricio County seat — homes, rentals and commercial properties on the schedule.",
  intro=[
   "Sinton, the San Patricio County seat, is comfortably inside LRT&rsquo;s service radius. Residential yards, rental properties and commercial grounds in Sinton can all get a spot on the route.",
   "Like everywhere LRT works, pricing is quoted per property after a real look &mdash; free, no obligation, and usually same-day.",
  ],
  note="Inside the service radius from Portland."),
 dict(slug="odem", name="Odem", named=False,
  card="On the US-77 corridor between Sinton and Corpus — an easy add to the route.",
  intro=[
   "Odem sits on the US-77 corridor between Sinton and Corpus Christi &mdash; an easy add to LRT&rsquo;s route from Portland.",
   "Whether it&rsquo;s a weekly residential cut or a one-time clean-up that hauls the debris off with it, Odem addresses quote free and usually same-day.",
  ],
  note="An easy add to the existing route."),
 dict(slug="robstown", name="Robstown", named=False,
  card="West of Corpus Christi in Nueces County — inside the service radius for lawns and commercial work.",
  intro=[
   "Robstown, on the west side of the Corpus Christi area, is inside LRT&rsquo;s service radius. Residential lawns, rentals and commercial properties can all get on the schedule.",
   "Commercial property owners in Robstown get the same package as everywhere else on the map: a fixed service day, full-service visits and one invoice.",
  ],
  note="Inside the service radius."),
 dict(slug="port-aransas", name="Port Aransas", named=False,
  card="Mustang Island's beach town — vacation rentals and island properties inside the service area.",
  intro=[
   "Port Aransas is the island end of the map &mdash; and with so many vacation rentals, it&rsquo;s a town where a lawn crew that shows up on schedule matters more than anywhere. The yard is guest-ready whether or not the owner is on the island.",
   "Island properties, salt wind and sandy soil have their own rhythm; a consistent schedule keeps them looking deliberate year-round.",
  ],
  note="Island properties &amp; vacation rentals welcome."),
]
TOWN_BY_SLUG = {t["slug"]: t for t in TOWNS}
NAMED_TOWNS = [t for t in TOWNS if t["named"]]

# hero backgrounds rotated across town pages — all from the 2000px hero set,
# matched loosely to each town's character (coastal towns get the bay shots,
# farm towns get the open-field cuts)
TOWN_HEROES = ["hero-lawn.webp","hero-striped-2.webp","hero-pool-2.webp","hero-bay-walk.webp",
               "hero-bayfront.webp","hero-fleet.webp","hero-field-mowers.webp","hero-scag-field.webp",
               "hero-striped-2.webp","hero-pool.webp","hero-bayfront.webp"]

# ============================================================
# SHARED FRAGMENTS
# ============================================================
GEN_NOTE = "<!-- Generated by build.py — edit build.py and re-run; don't hand-edit this file. -->"

# Cache-buster for site.css / pages.css / site.js. Bump whenever those files
# change, or browsers keep serving the stale cached versions (symptom: carousel
# slides stack vertically full-width because the CSS never arrived).
ASSET_V = "16"

def head(title, desc, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#060D08">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/favicon-192.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,400..900,50,1&family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
<link rel="stylesheet" href="/assets/pages.css?v={ASSET_V}">{extra}
</head>
<body class="grain">
{GEN_NOTE}
"""

def nav_menu_links():
    links = "".join(
        f'<a href="/services/{s["slug"]}/">{ic(s["icon"])}{s["name"]}</a>'
        for s in SERVICES
    )
    links += f'<a href="/services/">{ic("arrow")}All services</a>'
    return links

def nav_areas_links():
    links = "".join(
        f'<a href="/service-areas/{t["slug"]}/">{ic("pin")}{t["name"]}</a>' for t in TOWNS
    )
    links += f'<a href="/service-areas/">{ic("arrow")}All service areas</a>'
    return links

def nav():
    return f"""
<!-- ============ NAV ============ -->
<header class="nav" id="nav">
  <div class="shell nav-in">
    <a class="brand" href="/">
      <img src="/assets/lrt-logo.png" alt="{BIZ} logo" width="50" height="50">
      <span class="brand-txt">
        <b><span class="lg">{BIZ}</span><span class="sm">LRT Lawn Care</span></b>
        <span><span class="lg">Portland, TX &amp; the Coastal Bend</span><span class="sm">Portland, TX</span></span>
      </span>
    </a>
    <nav class="nav-links">
      <div class="nav-drop" id="navDrop">
        <button type="button" aria-expanded="false" aria-controls="navMenu">
          Services
          {ic("chevd")}
        </button>
        <div class="nav-menu" id="navMenu">{nav_menu_links()}</div>
      </div>
      <div class="nav-drop" id="navDropAreas">
        <button type="button" aria-expanded="false" aria-controls="navMenuAreas">
          Service Areas
          {ic("chevd")}
        </button>
        <div class="nav-menu cols3" id="navMenuAreas">{nav_areas_links()}</div>
      </div>
      <a href="/our-work/">Our Work</a>
      <a href="/about/">About</a>
      <a href="/contact/">Get a Quote</a>
    </nav>
    <a class="nav-phone" href="{TEL}" aria-label="Call LRT Lawn Care">
      {ic("phone")}
      Call
    </a>
    <button type="button" class="nav-burger" id="navBurger" aria-label="Menu" aria-expanded="false" aria-controls="mnav">
      <span></span><span></span><span></span>
    </button>
    <a class="btn btn-call nav-cta" href="{TEL}">
      {ic("phone2")}
      {PHONE}
    </a>
  </div>

  <!-- mobile menu sheet -->
  <div class="mnav" id="mnav">
    <div class="mnav-in">
      <nav class="mnav-primary" aria-label="Main">
        <a href="/our-work/">Our Work</a>
        <a href="/about/">About</a>
        <a href="/contact/">Get a Quote</a>
      </nav>
      <p class="mnav-label">Services</p>
      <div class="mnav-list">{nav_menu_links()}</div>
      <p class="mnav-label">Service areas</p>
      <div class="mnav-towns">{nav_areas_links()}</div>
      <a class="btn btn-call mnav-call" href="{TEL}">{ic("phone2")}Call {PHONE}</a>
    </div>
  </div>
</header>
"""

def footer():
    svc_links = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    area_links = "".join(f'<li><a href="/service-areas/{t["slug"]}/">{t["name"]}</a></li>' for t in NAMED_TOWNS)
    area_links += '<li><a href="/service-areas/">All service areas</a></li>'
    return f"""
<!-- ============ FOOTER ============ -->
<footer class="foot">
  <div class="shell">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="/assets/lrt-logo.png" alt="" width="74" height="74" aria-hidden="true">
        <div>
          <b>{BIZ_LLC}</b>
          <em>&ldquo;{TAGLINE}&rdquo;</em>
          <p>LaChristian Thomas, Owner / Operator. Fully insured commercial &amp; residential lawn maintenance and landscaping.</p>
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>{svc_links}</ul>
      </div>
      <div>
        <h4>Service Areas</h4>
        <ul>{area_links}</ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="{TEL}">{PHONE}</a></li>
          <li><a href="{SMS}">Text us a photo</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{HOURS}</li>
          <li>Portland, TX &amp; the Coastal Bend</li>
        </ul>
      </div>
    </div>
    <div class="foot-bot">
      <span>&copy; <span id="yr">2026</span> {BIZ_LLC} All rights reserved. &middot;
        <a href="/about/" style="color:inherit">About</a> &middot;
        <a href="/our-work/" style="color:inherit">Our Work</a> &middot;
        <a href="/contact/" style="color:inherit">Contact</a> &middot;
        <a href="/privacy/" style="color:inherit">Privacy</a></span>
      <div class="foot-social">
        <a href="{FB}" target="_blank" rel="noopener" aria-label="LRT on Facebook">{fbic()}</a>
        <a href="{TIKTOK}" target="_blank" rel="noopener" aria-label="LRT on TikTok">{ttic()}</a>
      </div>
    </div>
  </div>
</footer>
"""

def callbar(quote_href="/contact/"):
    return f"""
<!-- ============ STICKY MOBILE CALL BAR ============ -->
<div class="callbar" id="callbar">
  <a class="btn btn-call" href="{TEL}">
    {ic("phone")}
    Call now
  </a>
  <a class="btn btn-ghost" href="{quote_href}">Free quote</a>
</div>
"""

def lightbox():
    return """
<!-- ============ LIGHTBOX ============ -->
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="lb-x" id="lbX" aria-label="Close">&times;</button>
  <img id="lbImg" alt="" hidden>
  <video id="lbVid" controls playsinline loop hidden></video>
</div>
"""

def tail(quote_href="/contact/", with_lightbox=False):
    return (lightbox() if with_lightbox else "") + callbar(quote_href) + f"""
<script src="/assets/site.js?v={ASSET_V}" defer></script>
</body>
</html>
"""

def crumbs(*pairs):
    """pairs: (label, href) — last one has href=None."""
    out = []
    for label, href in pairs:
        if href:
            out.append(f'<a href="{href}">{label}</a>')
            out.append(ic("chev"))
        else:
            out.append(f'<span>{label}</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(out)}</nav>'

def page_hero(h1, sub, photo, alt, crumb_html, short=True, ctas=True):
    cta_html = f"""
    <div class="ph-cta">
      <a class="btn btn-call" href="{TEL}">{ic("phone2")}Call {PHONE}</a>
      <a class="btn btn-ghost" href="{SMS}">Text a photo of your property</a>
    </div>""" if ctas else ""
    return f"""
<!-- ============ PAGE HERO ============ -->
<section class="page-hero{' short' if short else ''}">
  <div class="ph-bg"><img src="/assets/{photo}" alt="{alt}" fetchpriority="high"></div>
  <div class="ph-veil"></div>
  <div class="ph-stripes"></div>
  <div class="ph-in">
    {crumb_html}
    <h1>{h1}</h1>
    <p class="ph-sub">{sub}</p>{cta_html}
  </div>
</section>
"""

def cta_band(h2, p, fine=None, photo="hero-striped-2.webp"):
    fine_html = f'<p class="cta-fine">{fine}</p>' if fine else ""
    return f"""
<!-- ============ CTA ============ -->
<section class="sec cta-band">
  <div class="cta-bg" aria-hidden="true"><img src="/assets/{photo}" alt="" loading="lazy"></div>
  <div class="shell">
    <div class="cta-in rv">
      <p class="eyebrow mswap" style="justify-content:center;margin-bottom:1.1rem"><span class="lg">Free quote &mdash; no obligation</span><span class="sm">Free quote</span></p>
      <h2>{h2}</h2>
      <p>{p}</p>
      <div class="ph-cta">
        <a class="btn btn-call" href="{TEL}">{ic("phone2")}Call {PHONE}</a>
        <a class="btn btn-turf" href="/contact/">Get a free quote{ic("arrow")}</a>
      </div>
      {fine_html}
    </div>
  </div>
</section>
"""

def checks(items, two=True):
    lis = "".join(f'<li>{ic("check")}<span>{i}</span></li>' for i in items)
    return f'<ul class="checks{" two" if two else ""}">{lis}</ul>'

def svc_card(s, photo=None, desc=None):
    photo = photo or s["card_photo"]
    desc = desc or s["card_desc"]
    tags = "".join(f"<i>{t}</i>" for t in s["tags"])
    return f"""<a class="svc rv" href="/services/{s["slug"]}/">
        <div class="svc-photo"><img src="/assets/{photo}" alt="{s["card_alt"]}" loading="lazy" width="880" height="520"></div>
        <div class="svc-body">
          <div class="svc-ic">{ic(s["icon"])}</div>
          <span class="svc-kind">{s["kind"]}</span>
          <h3>{s["name"]}</h3>
          <p>{desc}</p>
          <div class="svc-tags">{tags}</div>
          <span class="svc-more">Learn more {ic("arrow")}</span>
        </div>
      </a>"""

def plans_section(compact=False):
    lead = "" if compact else """
    <div class="sec-head rv">
      <p class="eyebrow">Service plans</p>
      <h2>Pick a schedule. We handle the rest.</h2>
      <p>Recurring customers get a consistent day on the route and a card on file &mdash; no invoices to chase, no texting back and forth every week about when we&rsquo;re coming.</p>
    </div>"""
    return f"""
<!-- ============ SERVICE PLANS (quote-only by the client's choice) ============ -->
<section class="sec" id="plans" style="background:var(--ink-2)">
  <div class="shell">
    {lead}
    <div class="plan-grid">
      <article class="plan rv">
        <span class="plan-k">Every 14 days</span>
        <h3>Bi-Weekly</h3>
        <p class="cadence">Best for slower-growing or shaded lawns.</p>
        <p class="price">Quoted per property</p>
        <p class="price-sub">Priced on lot size &mdash; free estimate, no obligation</p>
        <ul>
          <li>{ic("check")}Mow, edge, weed-eat &amp; blow down</li>
          <li>{ic("check")}Same day every other week</li>
          <li>{ic("check")}Card on file &mdash; billed automatically</li>
        </ul>
        <a class="btn btn-ghost" href="/contact/?service=Bi-weekly%20lawn%20service#quote">Get my price</a>
      </article>

      <article class="plan feat rv">
        <span class="plan-rib">Most popular</span>
        <span class="plan-k">Every 7 days</span>
        <h3>Weekly</h3>
        <p class="cadence">What most Coastal Bend lawns need through the growing season.</p>
        <p class="price">Quoted per property</p>
        <p class="price-sub">Priced on lot size &mdash; free estimate, no obligation</p>
        <ul>
          <li>{ic("check")}Everything in Bi-Weekly</li>
          <li>{ic("check")}A locked-in day on the route</li>
          <li>{ic("check")}Shrub &amp; bed upkeep included on request</li>
          <li>{ic("check")}Priority for clean-ups and extra work</li>
        </ul>
        <a class="btn btn-call" href="/contact/?service=Weekly%20lawn%20service#quote">Get my price</a>
      </article>

      <article class="plan rv">
        <span class="plan-k">One-time &amp; as-needed</span>
        <h3>Per Visit</h3>
        <p class="cadence">One cut, a clean-up, or a property you only need handled now and then.</p>
        <p class="price">Quoted per job</p>
        <p class="price-sub">As much notice as you can give helps us fit you in</p>
        <ul>
          <li>{ic("check")}One-time cuts &amp; seasonal clean-ups</li>
          <li>{ic("check")}Landscaping, sod &amp; mulch installs</li>
          <li>{ic("check")}Pay per visit &mdash; no commitment</li>
        </ul>
        <a class="btn btn-ghost" href="/contact/?service=One-time%20cut#quote">Get my price</a>
      </article>
    </div>

    <p class="plan-note rv">
      {ic("card")}
      <span><b>Card on file for recurring service.</b> Weekly and bi-weekly customers can keep a card securely on file &mdash; service runs on schedule and billing takes care of itself. Pause or cancel anytime; commercial accounts can be invoiced instead.</span>
    </p>
  </div>
</section>
"""

def reviews_section():
    return f"""
<!-- ============ PROOF ============ -->
<section class="sec proof">
  <div class="shell">
    <div class="sec-head rv">
      <p class="eyebrow">What customers say</p>
      <h2>Recommended by the neighbors.</h2>
    </div>
    <div class="proof-grid">
      <article class="rev rv">
        <span class="qm">{ic("quote")}</span>
        <p>He has been mowing my lawn since last year proactively and reliably. Very professional and open to feedback.</p>
        <div class="rev-by">
          <b>Rick Butler</b>
          <span class="fb">{fbic()}Recommends on Facebook</span>
        </div>
      </article>

      <article class="rev rv">
        <span class="qm">{ic("quote")}</span>
        <p>Lachristian came to our house to dig up a busted sewage line. He was quick and efficient and knowledgeable about the job. Highly recommended for anyone needing mowing or landscape work!</p>
        <div class="rev-by">
          <b>Luke Quinn Seibert</b>
          <span class="fb">{fbic()}Recommends on Facebook</span>
        </div>
      </article>
    </div>
    <p class="proof-note rv">Reviews shown as posted to LRT&rsquo;s Facebook page.</p>
  </div>
</section>
"""

def quote_form_section(sec_id="quote"):
    return f"""
<!-- ============ QUOTE (Netlify Forms — set notification email in Netlify → Forms → Notifications) ============ -->
<section class="sec quote" id="{sec_id}">
  <div class="shell">
    <div class="q-grid">
      <div class="q-side rv">
        <p class="eyebrow" style="margin-bottom:1.1rem">Free quote</p>
        <h2>Tell us about the property.</h2>
        <p>Send the address and what you need &mdash; we&rsquo;ll come look at it and give you a number. No charge, no obligation.</p>
        <ul class="q-list">
          <li>{ic("check")}<span>Weekly, bi-weekly, one-time or as-needed &mdash; your call.</span></li>
          <li>{ic("check")}<span>Recurring customers can keep a card on file &mdash; no chasing invoices.</span></li>
          <li>{ic("check")}<span>Fully insured: $1,000,000 general liability, $2,000,000 aggregate.</span></li>
          <li>{ic("check")}<span>Commercial-grade equipment with backups, so the schedule holds.</span></li>
        </ul>
        <div class="q-direct">
          <a href="{TEL}">{ic("phone2")}{PHONE}</a>
          <a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a>
        </div>
      </div>

      <form class="q-form rv" name="lrt-quote" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thank-you/">
        <input type="hidden" name="form-name" value="lrt-quote">
        <p class="hp"><label>Don't fill this out: <input name="bot-field"></label></p>

        <div class="f-row two">
          <label class="field"><span>Name</span><input type="text" name="name" placeholder="First and last" required autocomplete="name"></label>
          <label class="field"><span>Phone</span><input type="tel" name="phone" placeholder="(361) 555-0148" required autocomplete="tel"></label>
        </div>
        <label class="field"><span>Property address</span><input type="text" name="address" placeholder="Street, city" required autocomplete="street-address"></label>
        <div class="f-row two">
          <label class="field"><span>Property type</span>
            <select name="property_type" required>
              <option value="" selected disabled>Choose one</option>
              <option>Residential</option>
              <option>Commercial</option>
              <option>Rental / multi-unit</option>
            </select>
          </label>
          <label class="field"><span>Service needed</span>
            <select name="service" required>
              <option value="" selected disabled>Choose one</option>
              <option>Weekly lawn service</option>
              <option>Bi-weekly lawn service</option>
              <option>One-time cut</option>
              <option>Landscaping / install</option>
              <option>Mulch or sod install</option>
              <option>Clean-up &amp; haul off</option>
              <option>Tree or shrub trimming</option>
              <option>Pressure washing</option>
              <option>Something else</option>
            </select>
          </label>
        </div>
        <label class="field"><span>Anything we should know?</span><textarea name="details" placeholder="Gate code, dogs, how long since the last cut, problem areas&hellip; Feel free to text photos over instead if that's easier."></textarea></label>

        <button class="btn btn-turf" type="submit">
          Send my free quote request
          {ic("arrow")}
        </button>
        <p class="q-fine">Prefer to talk? Call or text <a href="{TEL}" style="color:var(--turf-2);font-weight:600">{PHONE}</a>.</p>
      </form>
    </div>
  </div>
</section>
"""

def faq_section(faqs, eyebrow="Common questions", h2="Answers before you even ask."):
    items = "".join(
        f"<details class=\"rv\"><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    # padding-top trimmed — this always follows the steps section on the same
    # background, and two full section paddings stacked into a dead zone
    return f"""
<!-- ============ FAQ ============ -->
<section class="sec" style="padding-top:0">
  <div class="shell">
    <div class="sec-head rv">
      <p class="eyebrow">{eyebrow}</p>
      <h2>{h2}</h2>
    </div>
    <div class="faq">{items}</div>
  </div>
</section>
"""

def steps_section(bg=""):
    style = f' style="background:{bg}"' if bg else ""
    return f"""
<!-- ============ HOW IT WORKS ============ -->
<section class="sec"{style}>
  <div class="shell">
    <div class="sec-head rv">
      <p class="eyebrow">How it works</p>
      <h2>Three steps. No runaround.</h2>
    </div>
    <div class="steps">
      <div class="step rv"><h3>Call, text or send the form</h3><p>Tell us the address and what you need. A photo by text works great &mdash; and inquiries usually get a same-day response.</p></div>
      <div class="step rv"><h3>We look, then quote it</h3><p>Every property is different, so we price per property after a real look &mdash; free, no obligation, no pressure.</p></div>
      <div class="step rv"><h3>You get on the schedule</h3><p>Pick weekly, bi-weekly or a one-time visit. Recurring customers get a consistent day and can keep a card on file.</p></div>
    </div>
  </div>
</section>
"""

def towns_chips_section(heading="Where we work", h2="Serving the Coastal Bend from Portland."):
    town_links = "".join(
        f'<a class="town" href="/service-areas/{t["slug"]}/">{ic("pin")}{t["name"]}</a>' for t in TOWNS
    )
    return f"""
<!-- ============ SERVICE AREA STRIP ============ -->
<section class="sec stripes" id="area">
  <div class="shell">
    <div class="sec-head rv">
      <p class="eyebrow">{heading}</p>
      <h2>{h2}</h2>
      <p>Based in Portland and running routes across the Coastal Bend &mdash; roughly a 45-mile radius from home base.</p>
    </div>
    <div class="chips-row rv">{town_links}
      <a class="town" href="/service-areas/">All service areas {ic("arrow")}</a>
    </div>
  </div>
</section>
"""

def about_areas_section():
    """Editorial 'Where we work' for the About page — typographic town list
    instead of pill chips. Established towns get the big serif ledger rows;
    radius towns run inline underneath."""
    ww_notes = {
      "portland": "Home base &mdash; the trailers roll out from here",
      "corpus-christi": "The biggest stop on the route",
      "ingleside": "On the weekly loop",
      "aransas-pass": "On the weekly loop",
      "rockport": "The far end of the loop",
    }
    named = "".join(f"""
        <a class="ww-row" href="/service-areas/{t["slug"]}/">
          <span class="ww-town">{t["name"]}</span>
          <span class="ww-note">{ww_notes[t["slug"]]}</span>
          <span class="ww-arrow">{ic("arrow")}</span>
        </a>""" for t in NAMED_TOWNS)
    radius = " &nbsp;&middot;&nbsp; ".join(
        f'<a href="/service-areas/{t["slug"]}/">{t["name"]}</a>'
        for t in TOWNS if not t["named"])
    return f"""
<!-- ============ WHERE WE WORK (editorial) ============ -->
<section class="sec" id="area" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="shell" style="max-width:56rem">
    <div class="sec-head rv">
      <p class="eyebrow">Where we work</p>
      <h2>Portland is home. The Coastal Bend is <em>the route</em>.</h2>
      <p>Routes run roughly a 45-mile radius from home base &mdash; planned by area, so recurring customers keep a consistent day.</p>
    </div>
    <div class="ww-list rv">{named}
    </div>
    <p class="ww-radius rv">Also inside the radius &mdash; {radius} &nbsp;&middot;&nbsp; <a href="/service-areas/">every town we serve {ic("arrow")}</a></p>
  </div>
</section>
"""

# ============================================================
# PAGE BUILDERS
# ============================================================
# Reel carousels — the house portrait-reel pattern (native scroll-snap track,
# arrows + page dots on desktop, swipe on mobile, lazy video attach). Clips are
# silent on purpose (TikTok audio = licensed music), so no sound button.
# reel-route-sign-2 = recut with the two intro stills at 2.5x speed.
# HOME gets the best four; Our Work carries the FULL library (every video the
# client sent except the one with identifiable bystanders and his portrait post).
HOME_REELS = [
    ("reel-mowing", "Knocking Down an Overgrown Backyard",
     "Weeks of growth coming off in one visit &mdash; mowed, then edged and blown down before the trailer leaves."),
    ("reel-route-sign-2", "Before &amp; After on a Weekly Stop",
     "Two quick stills &mdash; overgrown, then knocked down &mdash; and the walk back past the sign."),
    ("clip-commercial", "Commercial Grounds, Edged to the Curb",
     "A hotel frontage on the commercial route &mdash; medians, curbs and entrances kept tight."),
    ("reel-trailer-2", "Loaded Up Between Stops",
     "Commercial-grade SCAG equipment with backups, so the schedule holds."),
]

WORK_REELS = HOME_REELS[:3] + [
    ("clip-walkthrough", "Commercial Beds, Cut In and Rocked",
     "A full walk of a commercial property &mdash; new beds, rock, plantings and edged walks."),
    ("clip-sod", "Sod Day: Dirt to Done",
     "Tilled and graded with a pitch for drainage, then laid wall to wall &mdash; the full install."),
    ("clip-mulch", "Fresh Mulch, Clean Borders",
     "Red and black mulch beds cut in, edged and finished at the front entry."),
    ("clip-rocks", "A Rock Bed, Start to Finish",
     "A long install in half a minute &mdash; weed barrier, river rock and the finished bed."),
    ("clip-field-mow", "Wide Open and Striped",
     "From the trailer to the last pass &mdash; POV from the SCAG on a big open yard."),
    ("clip-bayfront", "The Bayfront Stop",
     "A waterfront lawn on the route, cut clean down to the seawall."),
] + [HOME_REELS[3]] + [
    ("clip-shop", "In the Shop",
     "Where the equipment lives &mdash; cleaned, staged and ready for the next route day."),
]

def reels_section(reels, eyebrow_lg, eyebrow_sm, h2, p):
    slides = "".join(f"""
        <div class="hreel-slide">
          <figure class="hreel-card">
            <div class="hreel-media">
              <img src="/assets/{base}-poster.webp" alt="" loading="lazy">
              <video muted loop playsinline preload="none" poster="/assets/{base}-poster.webp" data-src="/assets/{base}.mp4"></video>
            </div>
            <figcaption><b>{title}</b><span>{cap}</span></figcaption>
          </figure>
        </div>""" for base, title, cap in reels)
    return f"""
<!-- ============ JOB-SITE REELS ============ -->
<section class="sec hreel-sec stripes">
  <div class="shell">
    <div class="sec-head rv" style="margin-bottom:1.9rem">
      <p class="eyebrow mswap"><span class="lg">{eyebrow_lg}</span><span class="sm">{eyebrow_sm}</span></p>
      <h2>{h2}</h2>
      <p>{p}</p>
    </div>
    <div class="hreel rv">
      <button type="button" class="hreel-btn" id="hrPrev" aria-label="Previous clips"><svg class="ic" viewBox="0 0 24 24" style="transform:rotate(180deg)"><path d="m9 18 6-6-6-6"/></svg></button>
      <div class="hreel-track" id="hrTrack">{slides}
      </div>
      <button type="button" class="hreel-btn" id="hrNext" aria-label="More clips">{ic("chev")}</button>
    </div>
    <div class="hreel-dots" id="hrDots" role="tablist" aria-label="Clip pages"></div>
  </div>
</section>
"""

def home_reels_section():
    return reels_section(HOME_REELS,
      "Straight from the job site", "From the job site",
      "From the route, not a stock library.",
      "Every clip is LRT on a real Coastal Bend property. The rest of the library lives on <a href=\"/our-work/\" style=\"color:var(--turf-2);font-weight:600\">Our Work</a>.")

def build_home():
    schema = json.dumps({
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "LRT Lawn Care & Landscaping, LLC",
      "description": "Fully insured commercial and residential lawn maintenance and landscaping in Portland, Corpus Christi and the Coastal Bend, Texas.",
      "url": SITE_URL + "/",
      "image": SITE_URL + "/assets/og-image.jpg",
      "logo": SITE_URL + "/assets/lrt-logo.png",
      "telephone": "+1-361-765-5258",
      "email": EMAIL,
      "slogan": "Taking Pride in Every Property We Maintain.",
      "address": {"@type": "PostalAddress", "addressLocality": "Portland", "addressRegion": "TX", "postalCode": "78374", "addressCountry": "US"},
      "areaServed": [t["name"] + ", TX" for t in TOWNS],
      "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "17:00"},
      "sameAs": [FB.rstrip("/"), TIKTOK],
    }, indent=0)
    extra = f'\n<script type="application/ld+json">{schema}</script>'

    cards = "".join(svc_card(SVC_BY_SLUG[slug]) for slug in HOME_SERVICES)

    html = head(
      "LRT Lawn Care &amp; Landscaping | Portland, Corpus Christi &amp; the Coastal Bend",
      "Fully insured commercial &amp; residential lawn maintenance and landscaping in Portland, Corpus Christi and the Coastal Bend, TX. Free quotes — call or text (361) 765-5258.",
      extra,
    ) + nav() + f"""
<!-- ============ HERO ============ -->
<section class="hero" id="top">
  <div class="hero-bg">
    <picture>
      <source media="(max-width:700px)" srcset="/assets/hero-lawn-mobile.webp">
      <img src="/assets/hero-lawn.webp" alt="A wide residential lot in Portland, Texas mowed into clean stripes by LRT Lawn Care &amp; Landscaping" fetchpriority="high" width="2000" height="1125">
    </picture>
  </div>
  <div class="hero-veil"></div>
  <div class="hero-stripes"></div>

  <div class="hero-in">
   <div class="hero-copy">
    <p class="eyebrow"><span class="lg">Portland &middot; Corpus Christi &middot; Ingleside &middot; Aransas Pass &middot; Rockport</span><span class="sm">Serving the Coastal Bend</span></p>
    <h1>Commercial grounds that always look <em>maintained</em>.</h1>
    <p class="hero-sub">Fully insured commercial lawn maintenance and landscaping across the Coastal Bend &mdash; 12 years in the field, commercial-grade equipment, and a schedule you can set your watch by. Residential welcome, too.</p>
    <div class="hero-cta">
      <a class="btn btn-call" href="{TEL}">
        {ic("phone2")}
        Call {PHONE}
      </a>
      <a class="btn btn-ghost" href="{SMS}">Text a photo of your yard</a>
    </div>
    <div class="trust">
      <div class="titem"><span class="tic">{ic("shield")}</span><span><b>Fully insured</b><i>$1M / $2M policy</i></span></div>
      <div class="titem"><span class="tic">{ic("calendar")}</span><span><b>Weekly &amp; bi-weekly</b><i>A set route day</i></span></div>
      <div class="titem"><span class="tic">{ic("card")}</span><span><b>Card on file</b><i>Automatic billing</i></span></div>
      <div class="titem"><span class="tic">{ic("building")}</span><span><b>12 years</b><i>In the field</i></span></div>
    </div>
   </div>

   <!-- Hero quote wizard — POSTs to Netlify Forms via site.js -->
   <form class="qwiz" id="qwiz" name="lrt-quote-wizard" method="POST" data-netlify="true" netlify-honeypot="bot-field">
     <input type="hidden" name="form-name" value="lrt-quote-wizard">
     <input type="hidden" name="service" id="qw-service">
     <input type="hidden" name="property" id="qw-property">
     <input type="hidden" name="timing" id="qw-timing">
     <p class="hp"><label>Skip this: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>

     <div class="qwiz-hd" id="qwHead">
       <b>Get a free quote</b>
       <i>Four quick taps &mdash; no obligation.</i>
       <div class="qwiz-bar"><span id="qwBar"></span></div>
     </div>

     <div class="qwiz-body">
       <!-- 1 -->
       <div class="qwiz-step active" data-step="1">
         <p class="qwiz-q">What do you need done?</p>
         <div class="qwiz-opts">
           <button type="button" class="qwiz-opt" data-field="service" data-value="Weekly lawn service">
             {ic("calendar")}Weekly or bi-weekly mowing</button>
           <button type="button" class="qwiz-opt" data-field="service" data-value="One-time cut">
             {ic("mower")}A one-time cut</button>
           <button type="button" class="qwiz-opt" data-field="service" data-value="Landscaping / install">
             {ic("grass")}Landscaping or an install</button>
           <button type="button" class="qwiz-opt" data-field="service" data-value="Clean-up &amp; haul off">
             {ic("truck")}Clean-up &amp; haul off</button>
           <button type="button" class="qwiz-opt" data-field="service" data-value="Tree or shrub trimming">
             {ic("tree")}Tree or shrub trimming</button>
         </div>
       </div>

       <!-- 2 -->
       <div class="qwiz-step" data-step="2">
         <p class="qwiz-q">What kind of property?</p>
         <div class="qwiz-opts">
           <button type="button" class="qwiz-opt" data-field="property" data-value="Residential">
             {ic("home")}My home</button>
           <button type="button" class="qwiz-opt" data-field="property" data-value="Commercial">
             {ic("building")}My business</button>
           <button type="button" class="qwiz-opt" data-field="property" data-value="Rental / multi-unit">
             {ic("layers")}A rental or multi-unit</button>
         </div>
         <div class="qwiz-foot">
           <button type="button" class="qwiz-back" data-back>{ic("chev")}Back</button>
         </div>
       </div>

       <!-- 3 -->
       <div class="qwiz-step" data-step="3">
         <p class="qwiz-q">How soon do you need it?</p>
         <div class="qwiz-opts">
           <button type="button" class="qwiz-opt" data-field="timing" data-value="It's gotten away from me">
             {ic("clock")}It&rsquo;s gotten away from me</button>
           <button type="button" class="qwiz-opt" data-field="timing" data-value="Within a week or two">
             {ic("calendar")}Within a week or two</button>
           <button type="button" class="qwiz-opt" data-field="timing" data-value="Just getting a price">
             {ic("handshake")}Just getting a price</button>
         </div>
         <div class="qwiz-foot">
           <button type="button" class="qwiz-back" data-back>{ic("chev")}Back</button>
         </div>
       </div>

       <!-- 4 -->
       <div class="qwiz-step" data-step="4">
         <p class="qwiz-q">Where should we text your quote?</p>
         <div class="qwiz-urgent" id="qwUrgent">
           {ic("phone2")}
           <span>Need it handled this week? <a href="{TEL}">Call {PHONE}</a></span>
         </div>
         <div class="qwiz-field">
           <label for="qw-name">Your name</label>
           <input type="text" id="qw-name" name="name" placeholder="First and last" autocomplete="name">
         </div>
         <div class="qwiz-field">
           <label for="qw-phone">Mobile number</label>
           <input type="tel" id="qw-phone" name="phone" placeholder="(361) 555-0148" autocomplete="tel" inputmode="tel">
         </div>
         <div class="qwiz-field">
           <label for="qw-addr">Property address or city</label>
           <input type="text" id="qw-addr" name="address" placeholder="Street or just the city" autocomplete="street-address">
           <p class="qwiz-err" id="qwErr">Add a name and a number we can text.</p>
         </div>
         <div class="qwiz-foot">
           <button type="button" class="qwiz-back" data-back>{ic("chev")}Back</button>
           <button type="submit" class="btn btn-call">Get my free quote</button>
         </div>
         <p class="qwiz-note">Or skip the form and call or text <a href="{TEL}">{PHONE}</a>.</p>
       </div>

       <!-- done -->
       <div class="qwiz-done" id="qwDone">
         <span class="tick">{ic("check")}</span>
         <b>Got it &mdash; thank you!</b>
         <p>LaChristian will text you back with a price. Usually same day.</p>
         <a class="btn btn-ghost" href="{TEL}">
           {ic("phone")}
           Call now instead
         </a>
       </div>
     </div>
   </form>
  </div>
</section>
<!-- ============ ASSURANCE BAR ============ -->
<section class="bar">
  <div class="shell">
    <div class="bar-grid">
      <div class="bar-cell"><b>$1,000,000</b><span>General liability</span></div>
      <div class="bar-cell"><b>$2,000,000</b><span>Aggregate coverage</span></div>
      <div class="bar-cell"><b>12 Years</b><span>In the field</span></div>
      <div class="bar-cell"><b>Owner-Run</b><span>LaChristian Thomas</span></div>
    </div>
  </div>
</section>
{home_reels_section()}
<!-- ============ SERVICES ============ -->
<section class="sec stripes" id="services">
  <div class="shell">
    <div class="sec-head rv">
      <p class="eyebrow">What we do</p>
      <h2>Built for commercial properties. Open to residential.</h2>
      <p>Offices, storefronts, rentals and multi-building sites kept on a fixed schedule &mdash; one crew, one schedule, one invoice. Residential lawns are still welcome on the route.</p>
    </div>

    <div class="svc-grid">{cards}</div>
    <div style="text-align:center;margin-top:2.2rem" class="rv">
      <a class="btn btn-ghost mswap" href="/services/"><span class="lg">See all services, including mulch, sod &amp; pressure washing</span><span class="sm">See all 8 services</span> {ic("arrow")}</a>
    </div>
  </div>
</section>

<hr class="rule">
{plans_section()}
<hr class="rule">

<!-- ============ BEFORE / AFTER ============ -->
<section class="sec" id="results" style="background:var(--ink-2)">
  <div class="shell">
    <div class="sec-head rv">
      <p class="eyebrow">Drag to see it</p>
      <h2>The difference, on the same property.</h2>
      <p>Both of these are real LRT jobs &mdash; the same camera angle, before the crew showed up and after they left.</p>
    </div>
{ba_sliders()}
    <div style="text-align:center;margin-top:2.4rem" class="rv">
      <a class="btn btn-ghost" href="/our-work/">See the full gallery {ic("arrow")}</a>
    </div>
  </div>
</section>
{reviews_section()}
{towns_chips_section()}
<hr class="rule">
{quote_form_section()}
""" + footer() + tail(quote_href="#quote")
    return html

def ba_sidewalk_card():
    """Third slider — frames pulled from LaChristian's own TikTok of the job
    (same sidewalk, same parked cars/mailbox, before and after the cut)."""
    return f"""
      <div class="ba-card rv">
        <div class="ba" data-ba tabindex="0" role="slider" aria-label="Before and after: sidewalk overgrown, then edged clean" aria-valuemin="0" aria-valuemax="100" aria-valuenow="80">
          <span class="ba-lbl b">Before</span>
          <span class="ba-lbl a">After</span>
          <img class="ba-base" src="/assets/ba3-after.webp" alt="The same sidewalk after the visit — mowed and edged clean to the concrete, with an LRT sign in the yard" width="720" height="540">
          <div class="ba-top"><img src="/assets/ba3-before.webp" alt="A sidewalk nearly swallowed by overgrown grass on both sides" width="720" height="540"></div>
          <div class="ba-handle"><span class="ba-knob">
            {ic("chev")}
            {ic("chev")}
          </span></div>
        </div>
        <div class="ba-cap">
          <h3>Sidewalk swallowed &rarr; edged to the concrete</h3>
          <p>The walk was disappearing under the grass. One visit later it&rsquo;s mowed and edged clean to the concrete &mdash; sign in the yard.</p>
          <span class="ba-hint">Drag the handle
            {ic("arrow")}
          </span>
        </div>
      </div>"""

def ba_sliders(extra=""):
    odd = " odd" if extra else ""
    return f"""
    <div class="ba-wrap{odd}">
      <div class="ba-card rv">
        <div class="ba" data-ba tabindex="0" role="slider" aria-label="Before and after: overgrown backyard mowed and striped" aria-valuemin="0" aria-valuemax="100" aria-valuenow="80">
          <span class="ba-lbl b">Before</span>
          <span class="ba-lbl a">After</span>
          <img class="ba-base" src="/assets/ba1-after.webp" alt="The same backyard after LRT mowed it into clean stripes and blew off the hard surfaces" width="1100" height="825">
          <div class="ba-top"><img src="/assets/ba1-before.webp" alt="An overgrown backyard in Portland, Texas before LRT's crew arrived" width="1100" height="825"></div>
          <div class="ba-handle"><span class="ba-knob">
            {ic("chev")}
            {ic("chev")}
          </span></div>
        </div>
        <div class="ba-cap">
          <h3>Backyard gone long &rarr; striped and blown off</h3>
          <p>Missed a couple of cuts over a wet stretch. One visit: mowed, edged along the slab, weed-eaten to the fence line and blown down.</p>
          <span class="ba-hint">Drag the handle
            {ic("arrow")}
          </span>
        </div>
      </div>

      <div class="ba-card rv">
        <div class="ba" data-ba tabindex="0" role="slider" aria-label="Before and after: concrete slab cut open for a crape myrtle" aria-valuemin="0" aria-valuemax="100" aria-valuenow="80">
          <span class="ba-lbl b">Before</span>
          <span class="ba-lbl a">After</span>
          <img class="ba-base" src="/assets/ba2-after.webp" alt="A clean round opening cut through the concrete slab, backfilled with soil and ready to plant" width="900" height="900">
          <div class="ba-top"><img src="/assets/ba2-before.webp" alt="A solid concrete slab marked with a spray-painted circle before the cut" width="900" height="900"></div>
          <div class="ba-handle"><span class="ba-knob">
            {ic("chev")}
            {ic("chev")}
          </span></div>
        </div>
        <div class="ba-cap">
          <h3>Solid slab &rarr; a planting hole for a crape myrtle</h3>
          <p>The client wanted a crape myrtle where there was nothing but concrete. Marked, broken out, hauled off and backfilled &mdash; ready to plant.</p>
          <span class="ba-hint">Drag the handle
            {ic("arrow")}
          </span>
        </div>
      </div>{extra}
    </div>"""

def build_services_index():
    cards = "".join(svc_card(s) for s in SERVICES)
    html = head(
      "Lawn Care &amp; Landscaping Services | LRT Lawn Care &amp; Landscaping",
      "Commercial and residential lawn maintenance, landscaping, mulch and sod installs, trimming, clean-ups and pressure washing across Portland, Corpus Christi and the Coastal Bend. Call (361) 765-5258.",
    ) + nav() + page_hero(
      "Everything we do, <em>in one place</em>.",
      "Commercial and residential &mdash; from a weekly cut to a full landscape install. Every job quoted per property, free, usually same day.",
      "hero-scag-field.webp", "A SCAG zero-turn mower on a freshly cut open field",
      crumbs(("Home","/"),("Services",None)),
    ) + f"""
<!-- ============ ALL SERVICES ============ -->
<section class="sec stripes">
  <div class="shell">
    <div class="sec-head rv">
      <p class="eyebrow">Services</p>
      <h2>Eight ways to keep a property sharp.</h2>
      <p>Commercial or residential, recurring or one-time &mdash; every job quoted per property, free and no obligation.</p>
    </div>
    <div class="svc-grid">{cards}</div>
  </div>
</section>
<hr class="rule">
{plans_section()}
{steps_section()}
{cta_band("Not sure which service you need?",
          "Describe the property &mdash; or just text a photo &mdash; and we&rsquo;ll tell you what it needs and what it&rsquo;ll take. Free, no obligation.")}
""" + footer() + tail()
    return html

def _plain(s):
    """HTML string -> plain text for JSON-LD (strip tags, decode entities)."""
    return htmllib.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def service_schema(s):
    """FAQPage + BreadcrumbList JSON-LD for a service page."""
    faq = {
      "@context": "https://schema.org", "@type": "FAQPage",
      "mainEntity": [{"@type": "Question", "name": _plain(q),
                      "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}}
                     for q, a in s["faqs"]],
    }
    crumbs_ld = {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
        {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE_URL + "/services/"},
        {"@type": "ListItem", "position": 3, "name": _plain(s["name"])},
      ],
    }
    return (f'\n<script type="application/ld+json">{json.dumps(faq)}</script>'
            f'\n<script type="application/ld+json">{json.dumps(crumbs_ld)}</script>')

def build_service_page(s):
    # optional commercial property-type chips
    prop_html = ""
    if s.get("prop_types"):
        chips = "".join(f'<span class="town">{ic("building")}{p}</span>' for p in s["prop_types"])
        prop_html = f"""
    <div style="margin-top:2rem" class="rv">
      <p class="eyebrow" style="margin-bottom:.9rem">Properties we take on</p>
      <div class="chips-row">{chips}</div>
    </div>"""

    photo_html = ""
    if s["photo"]:
        photo_html = f"""
      <figure class="split-photo rv">
        <img src="/assets/{s["photo"]}" alt="{s["photo_alt"]}" loading="lazy">
        <figcaption>{s["photo_cap"]}</figcaption>
      </figure>"""

    intro_ps = "".join(f"<p>{p}</p>" for p in s["intro"])
    split_inner = f"""
      <div class="rv">
        <div class="sec-head" style="margin-bottom:1.6rem">
          <p class="eyebrow">The service</p>
          <h2>What you&rsquo;re actually getting.</h2>
        </div>
        <div class="prose">{intro_ps}</div>
        {prop_html}
      </div>{photo_html}"""
    split_html = f'<div class="split">{split_inner}</div>' if s["photo"] else f'<div style="max-width:52rem">{split_inner}</div>'

    related = ""
    if s.get("related"):
        links = "".join(
            f'<a class="town" href="/services/{r}/">{ic(SVC_BY_SLUG[r]["icon"])}{SVC_BY_SLUG[r]["name"]}</a>'
            for r in s["related"]
        )
        related = f"""
<!-- ============ RELATED ============ -->
<section class="sec" style="background:var(--ink-2);border-top:1px solid var(--line)">
  <div class="shell">
    <div class="sec-head rv" style="margin-bottom:1.6rem">
      <p class="eyebrow">Goes well with</p>
      <h2 style="font-size:clamp(1.7rem,3.6vw,2.4rem)">Often booked together.</h2>
    </div>
    <div class="chips-row rv">{links}<a class="town" href="/services/">All services {ic("arrow")}</a></div>
  </div>
</section>"""

    html = head(s["title"] + " | " + "LRT Lawn Care &amp; Landscaping", s["desc"], service_schema(s)) + nav() + page_hero(
      s["h1"], f'<span class="svc-kind on-hero">{s["kind"]}</span>' + s["sub"], s["hero_photo"], s["hero_alt"],
      crumbs(("Home","/"),("Services","/services/"),(s["name"],None)),
    ) + f"""
<!-- ============ INTRO ============ -->
<section class="sec stripes">
  <div class="shell">{split_html}</div>
</section>

<!-- ============ WHAT'S INCLUDED ============ -->
<section class="sec" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="shell">
    <div class="sec-head rv" style="margin-bottom:1.4rem">
      <p class="eyebrow">What&rsquo;s included</p>
      <h2 style="font-size:clamp(1.8rem,4vw,2.6rem)">Every visit, the full job.</h2>
    </div>
    <div class="rv">{checks(s["includes"])}</div>
  </div>
</section>
{steps_section()}
{faq_section(s["faqs"])}
{related}
{cta_band(f'Ready for a number on your property?',
          f'Free quote, no obligation &mdash; call or text {PHONE} with the address, or send the form. Inquiries usually get a same-day response.',
          fine='Serving Portland, Corpus Christi, Ingleside, Aransas Pass, Rockport and the surrounding Coastal Bend.')}
""" + footer() + tail()
    return html

def build_our_work():
    html = head(
      "Our Work | LRT Lawn Care &amp; Landscaping",
      "Real LRT jobs across Portland, Corpus Christi and the Coastal Bend — before-and-afters, the full photo gallery and video from the route. No stock, no borrowed work.",
    ) + nav() + page_hero(
      "Every photo here is <em>our work</em>.",
      "Before-and-afters, the gallery and clips from the route &mdash; no stock photos, no borrowed jobs. What you see is what shows up.",
      "hero-striped-2.webp", "A large open lot mowed into clean stripes beside a red masonry wall",
      crumbs(("Home","/"),("Our Work",None)),
    ) + f"""
<!-- ============ BEFORE / AFTER ============ -->
<section class="sec" id="results" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="shell">
    <div class="sec-head rv">
      <p class="eyebrow">Drag to see it</p>
      <h2>The difference, on the same property.</h2>
      <p>The same camera angle, before the crew showed up and after they left.</p>
    </div>
{ba_sliders(extra=ba_sidewalk_card())}
  </div>
</section>

<!-- ============ GALLERY ============ -->
<section class="sec stripes" id="work">
  <div class="shell">
    <div class="sec-head rv">
      <p class="eyebrow">Recent work</p>
      <h2>Coastal Bend properties, kept sharp.</h2>
      <p>Tap any photo to see it full size.</p>
    </div>

    <div class="gal rv" id="gal">
      <figure><img src="/assets/g-striped-lot.webp" alt="A large open lot mowed into clean stripes beside a red masonry wall" loading="lazy" width="1100" height="825"><figcaption>Full lot mow &amp; stripe &mdash; Portland</figcaption></figure>
      <figure><img src="/assets/g-path-tall.webp" alt="A curved decomposed granite walkway running through thick green turf" loading="lazy" width="900" height="1200"><figcaption>Granite walkway through new turf</figcaption></figure>
      <figure><img src="/assets/g-front-drive.webp" alt="A crisply edged front lawn meeting a curved concrete driveway" loading="lazy" width="1100" height="825"><figcaption>Front lawn &amp; drive edge</figcaption></figure>
      <figure><img src="/assets/g-path-wide.webp" alt="A backyard landscape install with a curving granite path through fresh sod" loading="lazy" width="1200" height="900"><figcaption>Backyard landscape install</figcaption></figure>
      <figure><img src="/assets/g-commercial-stripes.webp" alt="A large commercial lawn mowed into stripes along a curved concrete walk" loading="lazy" width="1100" height="825"><figcaption>Commercial grounds &mdash; scheduled service</figcaption></figure>
      <figure><img src="/assets/g-entry-beds.webp" alt="A home entry walkway with trimmed shrubs and a clean rock border" loading="lazy" width="1100" height="825"><figcaption>Entry beds &amp; walkway</figcaption></figure>
      <figure><img src="/assets/g-poolside.webp" alt="A poolside lawn strip mowed and edged beside a planted rock bed" loading="lazy" width="1100" height="825"><figcaption>Poolside turf &amp; planted border</figcaption></figure>
      <figure><img src="/assets/g-rock-bed.webp" alt="A white rock bed built around a tree with an address stone set in the middle" loading="lazy" width="1100" height="825"><figcaption>Rock bed &amp; address stone</figcaption></figure>
      <figure><img src="/assets/g-walk-edges.webp" alt="Two concrete walkways meeting with sharply edged turf on every side" loading="lazy" width="1200" height="900"><figcaption>Edging detail</figcaption></figure>
      <figure><img src="/assets/g-equipment.webp" alt="LRT's commercial mowers, blowers and trimmers staged on a lawn" loading="lazy" width="1100" height="825"><figcaption>Commercial-grade equipment &mdash; plus backups</figcaption></figure>
      <figure><img src="/assets/g-commercial-lot.webp" alt="A newly picked-up commercial property with the grounds mowed to the fence line" loading="lazy" width="1100" height="825"><figcaption>New commercial property, first service</figcaption></figure>
      <figure><img src="/assets/g-concrete-dig.webp" alt="Breaking out concrete by hand to open a planting hole" loading="lazy" width="900" height="1200"><figcaption>Concrete cut-out &amp; haul off</figcaption></figure>
      <figure><img src="/assets/g-fleet.webp" alt="LRT's mowers, blowers and trimmers staged together on a fresh-cut lawn" loading="lazy" width="1400" height="1050"><figcaption>The fleet &mdash; mowers, blowers &amp; trimmers</figcaption></figure>
      <figure><img src="/assets/g-field-mowers.webp" alt="Two SCAG zero-turn mowers on a freshly cut open field" loading="lazy" width="1400" height="1050"><figcaption>Open-field cut &mdash; two machines</figcaption></figure>
      <figure><img src="/assets/g-pool-lawn.webp" alt="A backyard pool bordered by mowed lawn and clean patio" loading="lazy" width="1400" height="1050"><figcaption>Poolside lawn &amp; patio, kept sharp</figcaption></figure>
      <figure><img src="/assets/g-bayfront.webp" alt="A bayfront lawn running down to a private pier and boat" loading="lazy" width="1400" height="1050"><figcaption>Bayfront lawn on the route</figcaption></figure>
    </div>
  </div>
</section>

{reels_section(WORK_REELS,
  "On the route", "On the route",
  "The whole video library.",
  "Every job-site clip from LaChristian&rsquo;s own feed &mdash; mows, installs, commercial walkthroughs and the shop. Nothing staged, nothing borrowed.")}
{reviews_section()}
{cta_band("Want your property in this gallery?",
          f"Call or text {PHONE} with the address &mdash; or send a photo of the yard as it is right now. The before-and-after is the fun part.",
          photo="hero-bayfront.webp")}
""" + footer() + tail(with_lightbox=True)
    return html

def build_about():
    html = head(
      "About LaChristian Thomas | LRT Lawn Care &amp; Landscaping",
      "LRT Lawn Care & Landscaping is owner-run by LaChristian Thomas — 12 years maintaining Coastal Bend properties, fully insured, based in Portland, TX. Call or text (361) 765-5258.",
    ) + nav() + page_hero(
      "Owner-run, <em>and it shows</em>.",
      "LaChristian Thomas has spent 12 years taking care of Coastal Bend properties. The person who quotes your yard is the person who shows up to cut it.",
      "hero-fleet.webp", "LRT's commercial mowers, blowers and trimmers staged on a finished lawn",
      crumbs(("Home","/"),("About",None)),
    ) + f"""
<!-- ============ STORY ============ -->
<section class="sec stripes">
  <div class="shell">
    <div class="split">
      <div class="rv">
        <div class="sec-head" style="margin-bottom:1.6rem">
          <p class="eyebrow">The story</p>
          <h2>Twelve years in the field. Two on his own name.</h2>
        </div>
        <div class="prose">
          <p>LaChristian Thomas has been in lawn care, landscaping and commercial property maintenance for <b>12 years</b> &mdash; ten of them running routes and crews for other companies across the Coastal Bend, learning the trade from some of the best operators in the area.</p>
          <p>In 2024 he put his own name on the trailer. <b>LRT Lawn Care &amp; Landscaping, LLC</b> is built on the things he watched other companies get wrong: show up when you said you would, do the job right the first time so there&rsquo;s no call-back, and treat every property &mdash; a backyard or a multi-building commercial site &mdash; like it has your name on it. Because now it does.</p>
          <p>Today LRT runs weekly and bi-weekly routes from Portland across the Coastal Bend &mdash; residential yards, rental properties and a growing book of commercial accounts &mdash; fully insured, with commercial-grade equipment and backups so the schedule holds.</p>
        </div>
      </div>
      <figure class="split-photo rv">
        <img src="/assets/lachristian-thomas.webp" alt="LaChristian Thomas, owner and operator of LRT Lawn Care &amp; Landscaping" loading="lazy" style="aspect-ratio:3/4;object-position:50% 20%">
        <figcaption>LaChristian Thomas &mdash; Owner / Operator</figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ============ PULL QUOTE ============ -->
<section class="sec" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="shell" style="max-width:52rem">
    <blockquote class="pull rv">
      <p>&ldquo;All you need to do is care a bit and pay attention to detail. Do the job right the first time so there&rsquo;s no call-backs. And just show up.&rdquo;</p>
      <footer><b>LaChristian Thomas</b> &mdash; Owner / Operator, LRT Lawn Care &amp; Landscaping</footer>
    </blockquote>
  </div>
</section>

<!-- ============ FACTS ============ -->
<section class="sec">
  <div class="shell">
    <div class="facts rv">
      <div class="fact"><b>12 Years</b><span>In the field</span></div>
      <div class="fact"><b>Est. 2024</b><span>LRT founded</span></div>
      <div class="fact"><b>$1M / $2M</b><span>Liability insured</span></div>
      <div class="fact"><b>Portland, TX</b><span>Home base</span></div>
    </div>

    <div class="split" style="margin-top:3.4rem">
      <div class="rv">
        <div class="sec-head" style="margin-bottom:1.4rem">
          <p class="eyebrow">How we work</p>
          <h2 style="font-size:clamp(1.8rem,4vw,2.6rem)">The boring stuff, handled.</h2>
        </div>
        {checks([
          "Fully insured &mdash; $1,000,000 general liability, $2,000,000 aggregate",
          f"Hours: {HOURS}",
          "Same-day response to new inquiries",
          "Weekly, bi-weekly, one-time &amp; as-needed schedules",
          "Cash, check, Zelle, Venmo, Cash App or card",
          "Card on file &amp; invoicing for recurring accounts",
        ], two=False)}
      </div>
      <figure class="split-photo rv">
        <img src="/assets/about-rig.webp" alt="LRT's branded trailer and truck loaded up between stops on the route" loading="lazy" style="aspect-ratio:3/4;object-position:50% 50%">
        <figcaption>The rig &mdash; loaded and on the route.</figcaption>
      </figure>
    </div>
  </div>
</section>
{reviews_section()}
{about_areas_section()}
{cta_band("Put a name you can call on your property.",
          f"Call or text LaChristian directly at {PHONE} &mdash; or send the form and get a number back, usually same day.")}
""" + footer() + tail()
    return html

def build_contact():
    html = head(
      "Contact &amp; Free Quotes | LRT Lawn Care &amp; Landscaping",
      "Get a free lawn care or landscaping quote in Portland, Corpus Christi and the Coastal Bend. Call or text (361) 765-5258, email, or send the form — same-day response, Mon–Fri 8–5.",
    ) + nav() + page_hero(
      "Talk to the guy who <em>does the work</em>.",
      "Call, text, email or send the form &mdash; new inquiries usually get a same-day response. No call centers, no runaround.",
      "hero-lawn.webp", "A wide residential lot in Portland, Texas mowed into clean stripes",
      crumbs(("Home","/"),("Contact",None)), ctas=False,
    ) + f"""
<!-- ============ CONTACT CARDS ============ -->
<section class="sec" style="background:var(--ink-2);border-bottom:1px solid var(--line)">
  <div class="shell">
    <div class="contact-cards">
      <a class="ccard rv" href="{TEL}">
        <span class="cic">{ic("phone2")}</span>
        <span><b>Call</b><span>{PHONE}</span><small>Fastest way to reach us</small></span>
      </a>
      <a class="ccard rv" href="{SMS}">
        <span class="cic">{ic("msg")}</span>
        <span><b>Text</b><span>{PHONE}</span><small>Photos of the yard welcome &mdash; great for quick quotes</small></span>
      </a>
      <a class="ccard rv" href="mailto:{EMAIL}">
        <span class="cic">{ic("mail")}</span>
        <span><b>Email</b><span>{EMAIL}</span><small>Good for commercial bids &amp; paperwork</small></span>
      </a>
      <div class="ccard rv">
        <span class="cic">{ic("clock")}</span>
        <span><b>Hours</b><span>{HOURS}</span><small>Same-day response to new inquiries</small></span>
      </div>
    </div>
  </div>
</section>
{quote_form_section()}

<!-- ============ MAP ============ -->
<section class="sec" style="background:var(--ink-2);border-top:1px solid var(--line)">
  <div class="shell">
    <div class="area-grid">
      <div class="rv">
        <p class="eyebrow" style="margin-bottom:1.1rem">Where we work</p>
        <h2 style="font-size:clamp(2.1rem,4.6vw,3.2rem)">Based in Portland. Serving the Coastal Bend.</h2>
        <p style="color:var(--muted);margin-top:1.05rem">Routes run roughly a 45-mile radius from Portland &mdash; Corpus Christi, Ingleside, Aransas Pass, Rockport and the towns in between. <a href="/service-areas/" style="color:var(--turf-2);font-weight:600">See every town we serve.</a></p>
        <div class="towns">
          {"".join(f'<a class="town" href="/service-areas/{t["slug"]}/">{ic("pin")}{t["name"]}</a>' for t in NAMED_TOWNS)}
          <a class="town" href="/service-areas/">&amp; surrounding areas</a>
        </div>
      </div>
      <div class="map rv">
        <iframe title="LRT Lawn Care &amp; Landscaping service area map — Portland, Texas and the Coastal Bend"
          src="https://www.google.com/maps?q=Portland,+TX&amp;z=10&amp;output=embed"
          loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </div>
</section>
""" + footer() + tail(quote_href="#quote")
    return html

def build_privacy():
    html = head(
      "Privacy Policy | LRT Lawn Care &amp; Landscaping",
      "How LRT Lawn Care & Landscaping handles the information you share when you call, text, or request a quote. Plain language, no surprises.",
    ) + nav() + f"""
<!-- ============ PRIVACY ============ -->
<section class="sec" style="padding-top:9.5rem">
  <div class="shell" style="max-width:46rem">
    <div class="sec-head" style="margin-bottom:2.2rem">
      <p class="eyebrow">The fine print</p>
      <h2 style="font-size:clamp(2.2rem,5vw,3.2rem)">Privacy Policy</h2>
      <p>Effective August 14, 2026. Plain language, because that&rsquo;s how we do everything else.</p>
    </div>
    <div class="prose">
      <p><b>Who we are.</b> {BIZ_LLC} is an owner-run lawn care and landscaping company based in Portland, Texas. Questions about this policy go straight to the owner: call or text {PHONE}, or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

      <p><b>What we collect.</b> Only what you give us. When you call, text, email or send a form on this site, that can include your name, phone number, email address, the property address, what work you&rsquo;re asking about, and any photos of the property you choose to send.</p>

      <p><b>How we use it.</b> To respond to you, quote the work, schedule it, and keep normal business records of the jobs we do. That&rsquo;s it. We don&rsquo;t sell your information, share it for marketing, or add you to mailing lists.</p>

      <p><b>Forms.</b> Quote forms on this site are processed by Netlify Forms, which stores the submission so we get notified. Netlify&rsquo;s own <a href="https://www.netlify.com/privacy/" target="_blank" rel="noopener">privacy policy</a> covers that processing.</p>

      <p><b>Calls &amp; texts.</b> The number on this site rings the owner&rsquo;s phone. Texting it is a normal person-to-person text &mdash; standard message rates from your carrier apply, and we only text you back about your own inquiry or job. No automated marketing texts.</p>

      <p><b>Third-party embeds.</b> This site loads fonts from Google Fonts and embeds a Google Map on the contact and service-area pages. Loading those means Google receives standard technical data like your IP address, covered by <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google&rsquo;s privacy policy</a>. We don&rsquo;t run advertising trackers or analytics cookies on this site.</p>

      <p><b>Job photos.</b> Before-and-after photos on this site are of properties we&rsquo;ve serviced. We don&rsquo;t publish anything that identifies a customer &mdash; no names, no addresses &mdash; and if a photo of your property appears here and you&rsquo;d like it removed, one call or text takes care of it.</p>

      <p><b>Your choices.</b> Want to know what we have on file for you, have it corrected, or have it deleted? Call, text or email and we&rsquo;ll take care of it &mdash; usually the same day.</p>

      <p><b>Changes.</b> If this policy changes, the new version gets posted here with a new effective date.</p>
    </div>
  </div>
</section>
""" + footer() + tail()
    return html

def build_areas_index():
    cards = "".join(f"""
      <a class="area-card rv" href="/service-areas/{t["slug"]}/">
        <h3>{ic("pin")}{t["name"]}, TX</h3>
        <p>{t["card"]}</p>
        <i>Lawn care &amp; landscaping in {t["name"]} {ic("arrow")}</i>
      </a>""" for t in TOWNS)
    html = head(
      "Service Areas | LRT Lawn Care &amp; Landscaping",
      "LRT Lawn Care & Landscaping serves Portland, Corpus Christi, Ingleside, Aransas Pass, Rockport and the surrounding Coastal Bend — roughly a 45-mile radius from Portland, TX. Call (361) 765-5258.",
    ) + nav() + page_hero(
      "Portland to Rockport, and <em>everything in between</em>.",
      "Based in Portland and running routes across the Coastal Bend &mdash; roughly a 45-mile radius from home base. Routes are planned by area, so recurring customers get a consistent day.",
      "hero-bay-walk.webp", "A maintained walkway leading down to the bay",
      crumbs(("Home","/"),("Service Areas",None)),
    ) + f"""
<!-- ============ TOWNS ============ -->
<section class="sec stripes">
  <div class="shell">
    <div class="sec-head rv">
      <p class="eyebrow">The map</p>
      <h2>Towns on the route.</h2>
      <p>Don&rsquo;t see your town? If it&rsquo;s within about 45 miles of Portland, call anyway &mdash; odds are we can work you in.</p>
    </div>
    <div class="area-cards">{cards}</div>
  </div>
</section>

<!-- ============ MAP ============ -->
<section class="sec" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="shell">
    <div class="area-grid">
      <div class="rv">
        <p class="eyebrow" style="margin-bottom:1.1rem">Route planning</p>
        <h2 style="font-size:clamp(2.1rem,4.6vw,3.2rem)">Routes by area, days that hold.</h2>
        <p style="color:var(--muted);margin-top:1.05rem">Routes are planned by area, so recurring customers get a consistent day &mdash; and we can usually work a new address into an existing route the same week.</p>
      </div>
      <div class="map rv">
        <iframe title="LRT Lawn Care &amp; Landscaping service area map — Portland, Texas and the Coastal Bend"
          src="https://www.google.com/maps?q=Portland,+TX&amp;z=9&amp;output=embed"
          loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </div>
</section>
{cta_band("On the map? Get a number.",
          f"Call or text {PHONE} with your address &mdash; free quote, no obligation, usually same day.")}
""" + footer() + tail()
    return html

def build_area_page(t, hero_photo):
    intro_ps = "".join(f"<p>{p}</p>" for p in t["intro"])
    svc_links = "".join(
        f'<a class="town" href="/services/{s["slug"]}/">{ic(s["icon"])}{s["name"]}</a>' for s in SERVICES
    )
    others = [x for x in TOWNS if x["slug"] != t["slug"]][:6]
    other_links = "".join(f'<a class="town" href="/service-areas/{x["slug"]}/">{ic("pin")}{x["name"]}</a>' for x in others)
    html = head(
      f'Lawn Care &amp; Landscaping in {t["name"]}, TX | LRT Lawn Care &amp; Landscaping',
      f'Lawn care and landscaping in {t["name"]}, TX — weekly and bi-weekly mowing, landscaping, clean-ups and commercial maintenance from LRT Lawn Care &amp; Landscaping. Free quotes: (361) 765-5258.',
    ) + nav() + page_hero(
      f'Lawn care &amp; landscaping in <em>{t["name"]}, TX</em>.',
      f'{t["note"]} Weekly and bi-weekly routes, landscaping and clean-ups &mdash; quoted free, usually same day.',
      hero_photo, "A Coastal Bend property maintained by LRT Lawn Care & Landscaping",
      crumbs(("Home","/"),("Service Areas","/service-areas/"),(t["name"],None)),
    ) + f"""
<!-- ============ TOWN INTRO ============ -->
<section class="sec stripes">
  <div class="shell">
    <div class="split">
      <div class="rv">
        <div class="sec-head" style="margin-bottom:1.6rem">
          <p class="eyebrow">{t["name"]}, Texas</p>
          <h2>On the route from Portland.</h2>
        </div>
        <div class="prose">{intro_ps}</div>
        {checks([
          "Fully insured &mdash; $1M general liability / $2M aggregate",
          "Owner-run &mdash; 12 years in the field",
          "Weekly, bi-weekly, one-time &amp; as-needed",
          "Free quotes, usually same day",
        ], two=False)}
      </div>
      <div class="map rv">
        <iframe title="Map of {t["name"]}, Texas"
          src="https://www.google.com/maps?q={t["name"].replace(" ", "+")},+TX&amp;z=12&amp;output=embed"
          loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </div>
</section>

<!-- ============ SERVICES IN TOWN ============ -->
<section class="sec" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="shell">
    <div class="sec-head rv" style="margin-bottom:1.6rem">
      <p class="eyebrow">Available in {t["name"]}</p>
      <h2 style="font-size:clamp(1.8rem,4vw,2.6rem)">Every LRT service, on your side of the map.</h2>
    </div>
    <div class="chips-row rv">{svc_links}</div>
  </div>
</section>
{steps_section()}
{cta_band(f'Need a lawn crew in {t["name"]}?',
          f'Call or text {PHONE} with your address &mdash; free quote, no obligation, usually same day.',
          fine='Also serving: ' + ", ".join(x["name"] for x in others) + ' and the surrounding Coastal Bend.')}
<!-- ============ NEARBY ============ -->
<section class="sec" style="padding-top:0">
  <div class="shell">
    <div class="sec-head rv" style="margin-bottom:1.4rem">
      <p class="eyebrow">Nearby</p>
      <h2 style="font-size:clamp(1.6rem,3.4vw,2.2rem)">Other towns on the route.</h2>
    </div>
    <div class="chips-row rv">{other_links}<a class="town" href="/service-areas/">All service areas {ic("arrow")}</a></div>
  </div>
</section>
""" + footer() + tail()
    return html

def build_thank_you():
    html = head(
      "Thank You | LRT Lawn Care &amp; Landscaping",
      "Your quote request is in. LaChristian will get back to you — usually same day.",
      '\n<meta name="robots" content="noindex">',
    ) + nav() + f"""
<!-- ============ THANK YOU ============ -->
<section class="page-hero" style="min-height:78svh;align-items:center">
  <div class="ph-bg"><img src="/assets/hero-lawn.webp" alt="" aria-hidden="true"></div>
  <div class="ph-veil"></div>
  <div class="ph-stripes"></div>
  <div class="ph-in" style="text-align:center">
    <p class="eyebrow" style="justify-content:center;margin-bottom:1.2rem">Request received</p>
    <h1 style="margin-inline:auto">Got it &mdash; <em>thank you</em>.</h1>
    <p class="ph-sub" style="margin-inline:auto">Your quote request is in. LaChristian will get back to you with a number &mdash; usually the same day. If it&rsquo;s urgent, skip the wait and call.</p>
    <div class="ph-cta" style="justify-content:center">
      <a class="btn btn-call" href="{TEL}">{ic("phone2")}Call {PHONE}</a>
      <a class="btn btn-ghost" href="/">Back to the site</a>
    </div>
  </div>
</section>
""" + footer() + tail()
    return html

# ============================================================
# EMIT
# ============================================================
def write(path, html):
    # canonical + social tags, derived from the page's own <title>/description
    # so they can't drift. Skipped on noindex pages (thank-you).
    if 'name="robots" content="noindex"' not in html:
        url = SITE_URL + "/" + path.replace("index.html", "")
        t = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
        d = re.search(r'<meta name="description" content="(.*?)">', html, re.S).group(1)
        social = f"""<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="LRT Lawn Care &amp; Landscaping">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
</head>"""
        html = html.replace("</head>", social, 1)
    if BASE:
        # every internal URL is root-relative (href/src/action/poster/data-src),
        # so prefixing at the ="/ boundary rewrites all of them at once
        html = html.replace('="/', f'="{BASE}/')
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  {path}")

def main():
    print("Building LRT site:")
    write("index.html", build_home())
    write("services/index.html", build_services_index())
    for s in SERVICES:
        write(f"services/{s['slug']}/index.html", build_service_page(s))
    write("our-work/index.html", build_our_work())
    write("about/index.html", build_about())
    write("contact/index.html", build_contact())
    write("service-areas/index.html", build_areas_index())
    for i, t in enumerate(TOWNS):
        write(f"service-areas/{t['slug']}/index.html", build_area_page(t, TOWN_HEROES[i % len(TOWN_HEROES)]))
    write("thank-you/index.html", build_thank_you())
    write("privacy/index.html", build_privacy())

    # sitemap.xml + robots.txt (thank-you is noindex — leave it out)
    paths = (["", "services/", "our-work/", "about/", "contact/", "service-areas/", "privacy/"]
             + [f"services/{s['slug']}/" for s in SERVICES]
             + [f"service-areas/{t['slug']}/" for t in TOWNS])
    urls = "\n".join(f"  <url><loc>{SITE_URL}/{p}</loc></url>" for p in paths)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print("  sitemap.xml + robots.txt")

    n = 8 + len(SERVICES) + len(TOWNS)
    print(f"Done - {n} pages.")

if __name__ == "__main__":
    main()
