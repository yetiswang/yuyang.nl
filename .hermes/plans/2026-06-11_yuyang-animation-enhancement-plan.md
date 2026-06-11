# yuyang.nl Animation & UX Enhancement Plan

> **For Hermes:** Implement phase-by-phase using subagent-driven-development. Each phase is self-contained and deployable independently.

**Goal:** Elevate yuyang.nl from a static-pages site to one with purposeful motion, without adding build tools, npm dependencies, or compromising the ink-wash aesthetic.

**Architecture:** Pure vanilla HTML/CSS/JS — no frameworks, no build step, deploy by pushing to `main` on GitHub Pages. All enhancements use CSS `@keyframes`, CSS `transition`, IntersectionObserver for scroll triggers, and optionally Anime.js (CDN) for the Node Weaver particle system. Everything must support dark mode and `prefers-reduced-motion`.

**Tech Stack:** CSS animations/transitions, IntersectionObserver (vanilla JS), View Transition API (progressive enhancement), Anime.js via CDN (optional, Phase 4).

**Repo:** `yetiswang/yuyang.nl` at `/Users/yuyangwang/dev/yuyang.nl/`
**Key files:**
- `index.html` (EN home, 773 lines — includes Node Weaver overlay)
- `zh/index.html` (ZH home, 781 lines — mirrored Node Weaver overlay)
- `shared.css` (572 lines — site-wide styles)
- `projects/index.html` (241 lines)
- `blog/index.html` (219 lines)
- `reading/index.html`

---

## Phase 1: Quick Wins — Micro-Interactions & Ambient Polish

> **Scope:** shared.css + minimal HTML edits. No JS changes. Deployable in one commit.

### Task 1.1: Nav Link Hover Underline Animation

**Objective:** Replace the instant border-bottom with a smooth scale-X animation for nav links.

**Files:**
- Modify: `shared.css:142-146`
- Test: Open site, hover nav links

**Step 1: Understanding current code**

```css
/* shared.css:142-146 */
nav .links a {
    ...
    border-bottom: 1.5px solid transparent;
    transition: border-color 0.15s;
}
nav .links a:hover { border-bottom-color: var(--text); color: var(--text); }
```

**Step 2: Replace with scale-X underline**

Change the nav link styles to use `::after` pseudo-element with `transform: scaleX()`:

```css
nav .links a {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 15px;
    font-weight: 500;
    color: var(--text);
    text-decoration: none;
    padding: 4px 0;
    position: relative;
}
nav .links a::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1.5px;
    background: var(--text);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}
nav .links a:hover::after {
    transform: scaleX(1);
}
nav .links a:hover { color: var(--text); }
```

**Step 3: Verify**

Open site in browser, hover each nav link. Underline should animate from left to right with a smooth ease-out-expo feel (0.25s cubic-bezier).

**Step 4: Commit**

```bash
git commit -m "feat: smooth scale-X underline for nav links"
```

### Task 1.2: Reading List Staggered Fade-In

**Objective:** On page load, reading items fade in one by one with a slight slide-up.

**Files:**
- Modify: `shared.css` (add animation keyframes)
- Modify: `reading/index.html` (add animation-delay inline style or class)
- Modify: `index.html` and `zh/index.html` (for the featured reading section)

**Step 1: Add keyframes to shared.css**

```css
@keyframes item-fade-in {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
.reading-item {
    opacity: 0;
    animation: item-fade-in 0.5s ease-out forwards;
}
.reading-item:nth-child(1) { animation-delay: 0.05s; }
.reading-item:nth-child(2) { animation-delay: 0.12s; }
.reading-item:nth-child(3) { animation-delay: 0.19s; }
```

**Step 2: Apply to reading page items**

`reading/index.html` — the items already use `.reading-item` class from shared.css. The animation will auto-apply.

**Step 3: Apply same treatment to home page featured reading**

`index.html:285-306` — 3 reading items in the hero section. Same `.reading-item` class.

**Step 4: Verify**

Hard refresh reading page. Items should appear sequentially with smooth fade-up.

**Step 5: Commit**

```bash
git commit -m "feat: staggered fade-in for reading list items"
```

### Task 1.3: Hero Button Subtle Hover Lift

**Objective:** Hero link buttons (`LinkedIn`, `Email`, `GitHub`) get a subtle `translateY(-1px)` + shadow lift on hover.

**Files:**
- Modify: `shared.css:227-246`

**Step 1: Enhance hero link transitions**

```css
.hero .links-row a {
    ...
    transition: background 0.15s, transform 0.2s, box-shadow 0.2s;
}
.hero .links-row a:hover {
    background: var(--btn-hover);
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-bottom: none;
}
.hero .links-row a.primary {
    background: var(--link);
    color: #ffffff;
}
.hero .links-row a.primary:hover {
    background: var(--link-hover);
    transform: translateY(-1px);
    box-shadow: 0 2px 10px rgba(0,100,200,0.2);
}
```

**Step 2: Verify**

Hover hero buttons — subtle lift, no layout shift (use `transform`, not `margin`).

**Step 3: Commit**

```bash
git commit -m "feat: subtle hover lift on hero buttons"
```

---

## Phase 2: Scroll-Reveal — Sections That Animate Into View

> **Scope:** Add a lightweight IntersectionObserver that adds a CSS class to sections when they scroll into view. Reused across all pages. This is the single highest-impact change.

**Design:** Sections slide up 20px and fade in over 0.6s when they enter the viewport. Uses a single `scroll-reveal` CSS class and one tiny JS snippet.

### Task 2.1: Add Scroll-Reveal CSS to shared.css

**Objective:** Define reusable `scroll-reveal` CSS that works with an `.in-view` class.

**Files:**
- Modify: `shared.css`

**Step 1: Add to shared.css (before the featured card styles)**

```css
/* === Scroll Reveal === */
.scroll-reveal {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s cubic-bezier(0.22, 1, 0.36, 1),
                transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}
.scroll-reveal.in-view {
    opacity: 1;
    transform: translateY(0);
}
@media (prefers-reduced-motion: reduce) {
    .scroll-reveal {
        opacity: 1;
        transform: none;
        transition: none;
    }
}
```

**Step 2: Verify**

CSS only — no visible change yet. JS in next task makes it work.

**Step 3: Commit**

```bash
git commit -m "feat: add scroll-reveal CSS class"
```

### Task 2.2: Add Scroll-Reveal JS Snippet

**Objective:** A tiny (≈20-line) IntersectionObserver script that runs on all pages.

**Files:**
- Modify: `shared.css` wasn't enough — we need to add JS. Best approach: add the script inline to `shared.css`? No — JS goes in each HTML. But to avoid duplication across 5+ pages, create `scroll-reveal.js` as a shared asset.

Create: `/assets/scroll-reveal.js`

**Step 1: Create scroll-reveal.js**

```js
/**
 * Scroll Reveal — lightweight IntersectionObserver for yuyang.nl
 * Adds `.in-view` class to `.scroll-reveal` elements when they enter viewport.
 * No dependencies, ≈300 bytes gzipped.
 */
(function() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var els = document.querySelectorAll('.scroll-reveal');
  if (!els.length) return;
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) {
        e.target.classList.add('in-view');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  els.forEach(function(el) { obs.observe(el); });
})();
```

**Step 2: Add the script reference to every page**

In each HTML file's `<head>` section (or before `</body>`):

```html
<script src="/assets/scroll-reveal.js" defer></script>
```

**Pages to modify:**
- `index.html`
- `zh/index.html`
- `projects/index.html`
- `blog/index.html`
- `reading/index.html`

**Step 3: Add `scroll-reveal` class to sections**

On `index.html`:
- `<section>` after hero: lines 271, 283, 309, 317 — add `class="scroll-reveal"`
- Also the featured card: line 274 `<div class="featured">`

On `zh/index.html`: same treatment for all `<section>` elements.

On `projects/index.html`: add to each `.project` div.

On `blog/index.html`: add to each blog post entry.

On `reading/index.html`: add to each `.reading-item`.

**Step 4: Verify**

Scroll down the home page — each section should fade+slide up as it enters view. Sections below the fold do not animate until scrolled to.

**Step 5: Commit**

```bash
git commit -m "feat: scroll-reveal via IntersectionObserver on all pages"
```

### Task 2.3: Quick Subtle Section Dividers

**Objective:** Between sections, add a very subtle visual cue that there's more content below the fold. Currently the section transitions are abrupt (hard border-top).

**Files:**
- Modify: `shared.css:249-251`

**Step 1: Soften section borders**

Change from solid border to a subtler treatment:

```css
section + section {
    border-top: none;
    /* Soft divider with gradient */
    position: relative;
}
section + section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 25%;
    width: 50%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
}
```

This creates a gradient-that-fades-in-and-out line instead of a full-width solid line.

**Step 2: Verify**

Scroll — section dividers should appear as soft, centered hairlines.

**Step 3: Commit**

```bash
git commit -m "feat: softer gradient section dividers"
```

---

## Phase 3: Sub-Page Hero Presence

> **Scope:** `/projects/`, `/blog/`, `/reading/` currently have no hero area — just a `<nav>` then straight into content. Give them a gentle page header with a small fade-in animation.

### Task 3.1: Add Page Headers to Sub-pages

**Objective:** Each sub-page gets an `<h1>` hero area with description, styled consistently with the home page but much smaller.

**Files:**
- Modify: `projects/index.html`
- Modify: `blog/index.html`
- Modify: `reading/index.html`

**Step 1: Add header after nav in each sub-page**

Template for all three:

```html
<header class="page-hero">
    <div class="page-hero-bg"></div>  <!-- subtle ink wash bg effect -->
    <h1>Projects</h1>
    <p class="page-blurb">Research infrastructure, institutional coordination, and lab operations — the work behind the science.</p>
</header>
```

The `page-hero` CSS goes in `shared.css`:

```css
/* === Page Hero (sub-pages) === */
.page-hero {
    position: relative;
    text-align: center;
    padding: 60px 24px 40px;
    overflow: hidden;
}
.page-hero h1 {
    font-family: var(--body-font);
    font-size: 36px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 12px;
    letter-spacing: -0.5px;
    animation: hero-fade-in 0.6s ease-out both;
}
.page-hero .page-blurb {
    font-size: 16px;
    color: var(--text-secondary);
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.5;
    animation: hero-fade-in 0.6s 0.1s ease-out both;
}
.page-hero-bg {
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, var(--bg-alt) 0%, transparent 70%);
    pointer-events: none;
    opacity: 0.5;
}
@media (max-width: 600px) {
    .page-hero { padding: 40px 24px 24px; }
    .page-hero h1 { font-size: 28px; }
    .page-hero .page-blurb { font-size: 15px; }
}
```

**Step 2: Apply to each page**

`projects/index.html` — current structure starts with `<nav>` then `<section>`. Add `page-hero` between nav and first section.

`blog/index.html` — same pattern.

`reading/index.html` — same pattern.

**Step 3: Wrap content sections in `.container`**

Each sub-page's content area should be wrapped in `<div class="container">` so it stays centered at 720px max-width, consistent with the home page.

**Step 4: Verify**

Visit each sub-page — a clean, centered header with fade-in animation should welcome the user before the content.

**Step 5: Commit**

```bash
git commit -m "feat: page heroes on sub-pages with fade-in"
```

### Task 3.2: Blog / Projects Staggered Entry

**Objective:** Blog post list items and project cards also fade in sequentially, like reading items.

**Files:**
- Modify: `shared.css`
- Modify: `blog/index.html`
- Modify: `projects/index.html`

**Step 1: Add staggered animation class to shared.css**

```css
/* Staggered entry for list items */
.stagger-item {
    opacity: 0;
    animation: item-fade-in 0.5s ease-out forwards;
}
.stagger-item:nth-child(1) { animation-delay: 0.05s; }
.stagger-item:nth-child(2) { animation-delay: 0.10s; }
.stagger-item:nth-child(3) { animation-delay: 0.15s; }
.stagger-item:nth-child(4) { animation-delay: 0.20s; }
.stagger-item:nth-child(5) { animation-delay: 0.25s; }
.stagger-item:nth-child(6) { animation-delay: 0.30s; }
.stagger-item:nth-child(7) { animation-delay: 0.35s; }
.stagger-item:nth-child(8) { animation-delay: 0.40s; }
```

**Step 2: Add classes to blog and project items**

Blog posts: each entry gets `class="stagger-item scroll-reveal"`.
Project cards: each `.project` gets `class="stagger-item scroll-reveal"`.

(The classes stack — `scroll-reveal` handles the scroll trigger, `stagger-item` handles the sequential delay.)

**Step 3: Verify**

Blog page: posts should slide up one after another on scroll. Projects page: same pattern.

**Step 4: Commit**

```bash
git commit -m "feat: staggered entry for blog posts and project cards"
```

---

## Phase 4: Node Weaver Enhancements

> **Scope:** Polish the overlay experience. Fix skip behavior, add a hover ink drip effect, consider Anime.js for particle simplification.

### Task 4.1: Fix Skip Behavior — Persist Dismissal

**Objective:** Currently `sessionStorage` skip only lasts for current tab. After user completes the game once, they shouldn't see it on a new tab either.

**Files:**
- Modify: `index.html` (Node Weaver JS section, around line 554-563)
- Modify: `zh/index.html` (same)

**Step 1: Change sessionStorage to localStorage for game completion**

In `index.html:557`:
```js
// Current:
if (skip) { try { sessionStorage.setItem('nw-done', '1'); } catch(e) {} }
// Also need to save on game completion, not just skip
```

Change the completion handler (line 546-548):
```js
if (allDone) {
    try { localStorage.setItem('nw-done', '1'); } catch(e) {}
    ...
}
```

And change the skip handler (line 600):
```js
skipBtn.addEventListener('click', function(){
    try { localStorage.setItem('nw-done', '1'); } catch(e) {}
    dismissOverlay(true);
});
```

**Step 2: Add localStorage check at overlay init**

Near the top of the overlay JS (~line 391):
```js
// Check if user has completed before
try {
    if (localStorage.getItem('nw-done') === '1') {
        document.getElementById('node-weaver-overlay').style.display = 'none';
        return; // exit the entire IIFE early
    }
} catch(e) {}
```

**Step 3: Apply same changes to zh/index.html**

**Step 4: Verify**

Complete the game, then open a new tab. Overlay should be gone. Skip, then reload. Also gone.

**Step 5: Commit**

```bash
git commit -m "fix: persist Node Weaver completion across sessions"
```

### Task 4.2: Hover Ink Drip Effect on Nodes

**Objective:** When mouse hovers over an unconnected node, a subtle ink drip particle appears from the node, falling downward with gravity. Pure visual delight.

**Files:**
- Modify: `index.html` (Node Weaver JS)
- Modify: `zh/index.html`

**Step 1: Add drip particle system**

In the draw loop, near the mouse hover handling section (~line 585-598):

Add state:
```js
var drips = [];
var dripTimer = 0;
```

In the hover update, spawn drips periodically:
```js
function updateHoverState() {
    hoveredNode = -1;
    if (gameComplete) return;
    for (var i = 0; i < 5; i++) {
        var n = nodes[i];
        var dx = mouseX - n.x, dy = mouseY - n.y;
        if (Math.sqrt(dx*dx+dy*dy) < Math.min(w,h)*0.16 && !connected[i]) {
            hoveredNode = i;
            // Spawn drip every ~4 frames
            if (dripTimer++ % 4 === 0) {
                drips.push({
                    x: n.x + (Math.random()-0.5)*8,
                    y: n.y + Math.min(W,H)*0.06,
                    vy: 0.3 + Math.random()*0.5,
                    size: 1.5 + Math.random()*2.5,
                    alpha: 0.6 + Math.random()*0.3,
                    decay: 0.008 + Math.random()*0.01
                });
            }
            break;
        }
    }
    if (hoveredNode === -1) dripTimer = 0;
}
```

In the draw loop, render drips:
```js
// Ink drips
for (var d = drips.length-1; d >= 0; d--) {
    var dp = drips[d];
    dp.y += dp.vy;
    dp.alpha -= dp.decay;
    if (dp.alpha <= 0) { drips.splice(d,1); continue; }
    ctx.save();
    ctx.globalAlpha = dp.alpha;
    ctx.fillStyle = dark ? '#e8ddd0' : '#2c2c2c';
    ctx.beginPath();
    ctx.arc(dp.x, dp.y, dp.size * (0.5 + Math.random()*0.5), 0, Math.PI*2);
    ctx.fill();
    ctx.restore();
}
```

**Step 2: Apply same changes to zh/index.html**

**Step 3: Verify**

Hover over an unconnected node — small ink drips should fall from below the node character.

**Step 4: Commit**

```bash
git commit -m "feat: ink drip effect on node hover"
```

### Task 4.3 (Optional): Anime.js Refactor of Particle System

**Objective:** Replace the hand-rolled particle animation (`requestAnimationFrame` loop lines 527-534, 690-696) with Anime.js for cleaner code and smoother animation.

**Files:**
- Modify: `index.html` (Node Weaver JS)
- Modify: `zh/index.html`

**When to attempt:** Only if the current particle system (draw loop, particles rendering) has performance issues or the code quality bothers you. The existing implementation already works well.

**Approach:**
1. Add Anime.js CDN before the Node Weaver script:
```html
<script src="https://cdn.jsdelivr.net/npm/animejs@4.0.2/lib/anime.iife.min.js"></script>
```
2. Replace the `burstParticles()` and particles rendering loop with:
```js
function burstParticles() {
    var dark = isDark();
    var items = [];
    for (var i = 0; i < 80 + Math.random()*30; i++) {
        items.push({
            x: centerX, y: centerY,
            vx: (Math.random()-0.5)*5, vy: (Math.random()-0.5)*5,
            size: 8+Math.random()*28,
            alpha: 0.95
        });
    }
    anime({
        targets: items,
        x: function(el) { return el.x + el.vx * anime.random(40, 120); },
        y: function(el) { return el.y + el.vy * anime.random(60, 180); },
        alpha: [0.95, 0],
        duration: function() { return anime.random(1200, 2500); },
        easing: 'easeOutQuad',
        update: function(anim) {
            // Anime.js doesn't render Canvas — we need a custom render callback
            // This makes the Anime.js approach actually more complex, not simpler
            // for Canvas-based particles. Stick with requestAnimationFrame.
        }
    });
}
```

**Recommendation: Skip this task.** Anime.js animates DOM elements, not Canvas draw calls. For Canvas particles, `requestAnimationFrame` is the correct approach and Anime.js adds complexity rather than reducing it. The current implementation is already optimal for Canvas-based animation.

**Step 3: Commit (if proceeding)**

```bash
git commit -m "refactor: use Anime.js for particle burst"
```

---

## Phase 5: Cross-Page Transitions

> **Scope:** Add seamless page transitions using the CSS View Transitions API. Zero JS library, modern browser feature.

### Task 5.1: Add View Transition Styles

**Objective:** When navigating between pages on the same site, crossfade smoothly instead of a hard white flash.

**Files:**
- Modify: `shared.css`

**Step 1: Add view-transition styles to shared.css**

```css
/* === View Transitions (progressive enhancement) === */
@view-transition {
    navigation: auto;
}
::view-transition-old(root) {
    animation: 0.3s ease-out both fade-out;
}
::view-transition-new(root) {
    animation: 0.3s 0.1s ease-out both fade-in;
}
@keyframes fade-out {
    to { opacity: 0; }
}
@keyframes fade-in {
    from { opacity: 0; }
}
```

Note: `@view-transition` is still experimental (Chrome 120+). Add as progressive enhancement — it won't break older browsers, they just get the normal instant transition.

**Step 2: Verify**

Navigate between home → projects → blog → reading. If browser supports View Transitions, pages should crossfade.

**Step 3: Commit**

```bash
git commit -m "feat: crossfade page transitions via View Transition API"
```

---

## Phase 6: Refinement & Polish

### Task 6.1: Theme Toggle Circular Reveal

**Objective:** When switching dark/light, use a `clip-path` circle animation for a smooth reveal effect.

**Files:**
- Modify: `index.html:348-355` (theme toggle click handler)
- Modify: `zh/index.html`

This requires a small JS addition to the theme toggle. Approach: temporarily apply a `clip-path: circle(0%)` on the body, then animate it to `circle(100%)` after the theme switches.

```js
btn.addEventListener('click', function() {
    if (document.startViewTransition) {
        var cur = html.getAttribute('data-theme');
        var next = cur === 'dark' ? 'light' : 'dark';
        document.startViewTransition(function() {
            html.setAttribute('data-theme', next);
            syncBodyTheme(next);
            try { localStorage.setItem('theme', next); } catch(e) {}
            updateLabel();
        });
    } else {
        // Fallback: instant switch
        ...
    }
});
```

**Actual implementation in index.html around line 348:**

Replace the entire `btn.addEventListener('click', ...)` block with:

```js
btn.addEventListener('click', function() {
    var cur = html.getAttribute('data-theme');
    var next = cur === 'dark' ? 'light' : 'dark';
    
    if (document.startViewTransition) {
        var vt = document.startViewTransition(function() {
            html.setAttribute('data-theme', next);
            syncBodyTheme(next);
            try { localStorage.setItem('theme', next); } catch(e) {}
            updateLabel();
        });
    } else {
        html.setAttribute('data-theme', next);
        syncBodyTheme(next);
        try { localStorage.setItem('theme', next); } catch(e) {}
        updateLabel();
    }
});
```

**Note:** `document.startViewTransition` requires Chrome 111+.

### Task 6.2: Mobile Nav Slide Animation Polish

**Objective:** The hamburger menu slide-down already exists (`nav-slide-in`) but the close has no animation — it just disappears.

**Files:**
- Modify: `shared.css:377-385`

Add a closing animation. Since CSS can't easily animate `display: none`, use a class-based approach:

Add a `nav-slide-out` keyframe and apply it when closing via JS.

Actually, the current behavior: clicking hamburger toggles `.open` on the `.links` div. When open, it has `display: flex` + `animation: nav-slide-in`. When closed, `display: none` is instant.

**Simpler fix:** Use `max-height` animation instead of `display` + `keyframes`:

```css
nav .links {
    display: flex;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease-out;
}
nav .links.open {
    max-height: 400px;
    transition: max-height 0.3s ease-in;
}
```

But this conflicts with desktop layout where links are always visible. Alternative: apply the max-height only on mobile via media query:

```css
@media (max-width: 600px) {
    nav .links {
        display: flex;
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease-out;
    }
    nav .links.open {
        max-height: 300px;
        transition: max-height 0.3s ease-in;
        animation: none;
        border-top: 1px solid var(--border);
        padding: 12px 0 0 0;
        margin-top: 0;
    }
}
```

This replaces the `nav-slide-in` keyframe animation with a smoother `max-height` transition.

---

## Deployment

No build step. After each task:

```bash
cd /Users/yuyangwang/dev/yuyang.nl
git add -A
git commit -m "description of changes"
git push
```

GitHub Pages auto-deploys from `main`. Allow 1-2 minutes for propagation.

---

## Summary: Phase Order & Impact

| Phase | Description | Files Changed | Impact | Diff |
|-------|-------------|---------------|--------|------|
| 1 | Micro-interactions | shared.css | Medium | ~30 lines CSS |
| 2 | Scroll-reveal | shared.css + 5 pages + new JS | **High** | ~50 lines CSS + ~20 lines JS |
| 3 | Sub-page heroes | 3 pages + shared.css | Medium | ~40 lines CSS + 30 lines HTML |
| 4 | Node Weaver polish | 2 pages | Medium | ~60 lines JS |
| 5 | View transitions | shared.css | Low (progressive) | ~15 lines CSS |
| 6 | Theme + nav polish | 2 pages + shared.css | Low | ~30 lines |

**Total:** ~250 lines of new code across the entire project. No dependencies added. Every change is reversible.
