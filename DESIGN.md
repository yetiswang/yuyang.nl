# yuyang.nl — design canon

The single source of truth for how this site looks and is built. Read this before adding a page, a post, or a component. When you change a shared pattern, update this file in the same commit.

Site: **yuyang.nl** (GitHub Pages, `yetiswang/yuyang.nl`). Bilingual: English at `/`, Traditional Chinese (`zh-Hant`) at `/zh/`. No build step; hand-authored static HTML + one shared stylesheet (`/shared.css`). Per-page `<style>` blocks hold page-specific rules; per-page inline `<script>` holds behaviour (theme toggle, mobile menu, share links). The ZH pages carry their own copy of the inline scripts, so any script fix must be ported to both languages.

---

## 1. Identity

- **Wordmark / logo:** `Hypomnemata` (EN), `虛室` (ZH). Top-left of the nav, links home.
- **Home intro:** a canvas "node-weaver" ink intro over the content (Three.js procedural ink, vendored in `/vendor/`). Documented separately; do not touch from a blog/post change.
- **Voice:** quiet, serif, warm paper. Minimal chrome. Content first.
- **Domain:** `yuyang.nl` (see `CNAME`). Canonical URLs are absolute `https://yuyang.nl/...` and live in each page's `og:url`.

---

## 2. Design tokens (`/shared.css`)

All colour comes from CSS variables on `:root` / `[data-theme]`. **Never hardcode a hex in a page; use the token.** Theme is set on `<html data-theme="light|dark">` and mirrored to `<body>`.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--text` | `rgba(0,0,0,.92)` | `rgba(235,230,220,.93)` | body text |
| `--text-secondary` | `#5a544c` | `#a89888` | secondary |
| `--text-muted` | `#8a847d` | `#7a7068` | meta, captions, eyebrows |
| `--bg` | `#f4ede5` (warm paper) | `#1c1a18` | page background |
| `--bg-alt` | `#ece5dc` | `#262422` | raised surfaces |
| `--border` | `rgba(0,0,0,.08)` | `rgba(255,255,255,.07)` | hairlines, dividers |
| `--tag-bg` / `--tag-text` | `#eef4fc` / `#0a6fc0` | `#1a2635` / `#7ab8ff` | category pills |
| `--link` / `--link-hover` | `#0066c8` / `#004d99` | `#5ba0e0` / `#7ab8ff` | inline links (used sparingly) |
| `--btn-bg` / `--btn-hover` | `rgba(0,0,0,.04)` / `.08` | `rgba(255,255,255,.06)` / `.10` | buttons |

Theme switch is a **View Transition circular reveal** on the toggle; preference persists in `localStorage['theme']`; default follows `prefers-color-scheme`. A no-flash bootstrap script in `<head>` sets `data-theme` before paint.

---

## 3. Typography

Two type systems, picked by language.

- **English:** body + headings `Source Serif 4` (Georgia fallback); UI / labels / meta `Inter`.
- **Chinese (zh-Hant):** body + headings `'Songti TC', 'Noto Serif TC', 'SimSun', 'STSong', serif`; UI / labels `Inter`. Slightly looser line-height (1.9 vs 1.7) for Han legibility.

Fonts load per page via Google Fonts: `Inter:300..700` always, plus `Source Serif 4` (EN) or `Noto Serif TC` (ZH). The home page also loads display/handwriting faces for the intro; content pages do not.

**Post type scale** (in each post's `<style>`):

| Element | EN | ZH |
|---|---|---|
| `h1` (post title) | Source Serif 4, 40px / 700 / `-0.5px` | Songti, 38px / 700 / `0` |
| `.standfirst` (lede) | 20px, `--text-muted` | 19px, `--text-muted` |
| body `p` | 18px / line-height 1.7 | 18px / 1.9 |
| `h2` (section) | 26px / 600 | 25px / 700 |
| `.references` | Inter 14px, `--text-muted` | same |
| `.share-strip .share-label` | Inter 12px / 600 / uppercase / `0.08em` | same (label text `分享`) |

---

## 4. Layout

- **Container:** `max-width: 720px; margin: 0 auto; padding: 0 24px;`. One column. Reading measure, not a grid.
- **Nav:** sticky-feel top bar inside the container — logo (left), `.links` (gap 24px), theme toggle, mobile hamburger. The last link in `.links` is the language switch (`.lang`, 13px, letterspaced): `中文` on EN pages, `EN` on ZH pages, pointing at the mirror URL.
- **Footer:** centred, muted — `© 2026 Yuyang Wang · Eindhoven, Netherlands` (EN) / `© 2026 王昱揚 · 荷蘭 埃因霍温` (ZH).

---

## 5. Components

### Nav, theme toggle, hamburger
Shared markup + the inline theme/menu script. Copy verbatim from an existing post; the ZH copy differs only in link labels/hrefs. Keep the toggle script identical across all posts (it is the canonical one in `shared.css`-styled pages).

### Post header
```
<header class="post-header">
  <div class="date">27 June 2026 · 6 min read</div>   <!-- ZH: 2026 年 6 月 27 日 · N min read -->
  <h1>Title</h1>
  <span class="category">Category</span>               <!-- pill, --tag-bg/--tag-text -->
</header>
```

### Category pill (`.tag` / `.category`)
Rounded `9999px`, `--tag-bg` fill, `--tag-text` text, Inter 12px/600. For categories and post tags.

### References (optional, for sourced essays)
`<ol class="references">` at the end of `.post-body`. Inter 14px, `--text-muted`. In-text markers are `<sup><a href="#refN">N</a></sup>`; list items are `<li id="refN">`. Numbers are author-maintained and must stay sequential with no gaps; the browser also auto-numbers the `<ol>`, so list order and `id` order must match. DOIs/arXiv as full `https://` links.

### Share strip (added 2026-06-28; moved below the title same day)
Sits **directly below the post header**, between `</header>` and `.post-body`, so readers can share from the top. Eyebrow label + hairline + bare text links, no icons, no cards, no tinted box (house style: eyebrow + hairline + bare list). The `border-top` hairline separates the title/meta cluster from the share row. Targets: **X, LinkedIn, Bluesky**.

Markup (label `Share` on EN, `分享` on ZH):
```html
<div class="share-strip" aria-label="Share this article">
  <span class="share-label">Share</span>
  <a class="share-link" data-share="x" href="#" target="_blank" rel="noopener">X</a>
  <a class="share-link" data-share="linkedin" href="#" target="_blank" rel="noopener">LinkedIn</a>
  <a class="share-link" data-share="bluesky" href="#" target="_blank" rel="noopener">Bluesky</a>
</div>
```

CSS (in the post `<style>`): hairline `border-top: 1px solid var(--border)`, `display:flex; gap:18px; align-items:center; flex-wrap:wrap`. Label is the uppercase Inter eyebrow; links are `--text-muted`, underline-on-hover to `--text`.

Behaviour (inline `<script>`, identical EN/ZH): build the share URLs at runtime from the page's own `og:url` and `og:title` (title suffix `— Yuyang Wang` / `— 王昱揚` stripped). This keeps every post's links correct with zero per-post hardcoding.
```
X:        https://twitter.com/intent/tweet?text={title}&url={url}
LinkedIn: https://www.linkedin.com/sharing/share-offsite/?url={url}   (pulls OG tags)
Bluesky:  https://bsky.app/intent/compose?text={title}%20{url}
```
To add a network later: add one `<a data-share="...">` and one entry to the script's `map`.

---

## 6. Bilingual rules

- Every content page has an EN original at `/<path>/` and a ZH twin at `/zh/<path>/`. The `.lang` nav link and each post's language toggle must point at the mirror, reciprocally.
- ZH is **Traditional Chinese (`zh-Hant`)**. Use Traditional vocabulary (人工智慧, not 人工智能).
- ZH pages keep their own inline scripts; a script change must be applied to both copies.
- Listings (`/blog/`, `/zh/blog/`) and `sitemap.xml` both need the new entry; newest first.

---

## 7. Content rules (writing, not CSS)

- **No em-dashes in body prose** (any language; in ZH avoid the 破折號 too — use a comma construction). The only `—` allowed is the structural `Title — Name` in `<title>`/`og:title` meta, which is the site convention.
- No software-engineering metaphors in essays.
- DOIs/arXiv as full `https://` URLs in references.
- Hard-refresh with a cache-buster when testing changes; GitHub Pages + browser cache `index.html` aggressively.

---

## 8. Add a new blog post — checklist

1. Create `blog/<slug>/index.html` from an existing post (copy head, `<style>`, nav, article scaffold, scripts). Set `og:url`, `og:title`/`twitter:title` (`Title — Yuyang Wang`), `og:description`, `meta description`, `<title>`.
2. Write the body in `.post-body`; add `.standfirst`, `h2` sections, and `references` if sourced.
3. Keep the **share strip** below the header / before `.post-body` (already in the template).
4. Add the entry to `blog/index.html` (newest first) and to `sitemap.xml`.
5. Create the ZH twin at `zh/blog/<slug>/index.html` (Noto Serif TC fonts, `虛室` nav, `EN` lang link, `分享` share label), add to `zh/blog/index.html` and `sitemap.xml`.
6. Wire reciprocal language links between the two.
7. Commit, push, hard-refresh-verify both URLs live.
