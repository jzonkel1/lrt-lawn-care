# LRT Lawn Care & Landscaping — client site

Client: **LaChristian Thomas** · (361) 765-5258 · lachristian.thomas@gmail.com · Portland, TX
Facebook: https://www.facebook.com/LRTMowingAndSmallLandscapingProjects/

Multi-page static site, generated from `build.py`. Deploy target: **Netlify** (Netlify Forms).

## How to edit

**Never hand-edit the generated `index.html` files** — they all carry a "generated" banner.
Edit `build.py` (business data, services, towns, copy — everything lives in the DATA section
and the page builders), then:

```
python build.py
```

Preview locally (root-relative URLs require a server, not file://):

```
python -m http.server 8741
```

Shared assets:
- `assets/site.css` — the "Coastal Sunset Turf" design system (verbatim from the demo)
- `assets/pages.css` — interior-page additions (page hero, breadcrumbs, FAQ, steps, etc.)
- `assets/site.js` — nav, wizard (POSTs to Netlify Forms), sliders, gallery, reels
- Images/video are the client's own photos, processed for the demo. No stock anywhere.

## Pages (26)

- `/` home · `/services/` overview · `/our-work/` · `/about/` · `/contact/` · `/thank-you/`
- 8 service pages under `/services/<slug>/`
- `/service-areas/` hub + 11 town pages under `/service-areas/<slug>/`

## Facts & guardrails (from onboarding CSV + research-notes.md in the DEMOS folder)

- **Quote-only pricing** — client's explicit choice. Never print dollar amounts.
- 12 years in the industry, ~2 on his own; LRT founded 2024.
- Service radius ~45 miles from Portland (his onboarding answer).
- Only the 5 "named" towns (Portland, CC, Ingleside, Aransas Pass, Rockport) are claimed as
  his established service area; the rest are framed as "inside the service radius".
- The 2 reviews are real Facebook recommendations — verbatim, attributed, no star ratings.
- Insurance $1M/$2M is **his own claim from a public FB post** — get the certificate before launch.

## Launch checklist (not done yet)

1. Create Netlify site, deploy this folder (publish dir = repo root, no build command
   — or run `python build.py` as the build command).
2. Netlify → Forms → verify `lrt-quote` and `lrt-quote-wizard` are detected; set the
   **notification email**. Forms are NOT lead-ready until this is done and test-submitted.
3. Domain — none registered yet. Check `lrtlawncare.com` etc. with the client.
4. Get the insurance certificate before the $1M/$2M claims go live.
5. GBP: none exists — create from the **agency** Google account with an evidence pack.
6. Tell the client the site isn't taking leads until step 2 is verified.
