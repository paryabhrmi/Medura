# Medura

An interactive [Rive](https://rive.app) prototype published as a static site on GitHub Pages.

## Contents

| Path | Purpose |
| --- | --- |
| `index.html` | The whole site: full-screen canvas, loader, Rive bootstrapping |
| `rive/medura_project_v2.riv` | The Rive file (~2.6 MB) |
| `vendor/rive-webgl2/` | Pinned `@rive-app/webgl2` 2.39.2 runtime — the renderer actually used |
| `vendor/rive/` | Pinned `@rive-app/canvas` 2.39.2 runtime — fallback without WebGL2 |
| `.nojekyll` | Stops Pages from running Jekyll over the files |

Everything is served from this repository — the page makes no third-party
requests, so no CDN outage, version drift, or content blocker can break it.
`index.html` points the runtime at the bundled `.wasm` via
`RuntimeLoader.setWasmUrl()` instead of its default CDN location.

## Deployment

The site is live at **https://paryabhrmi.github.io/Medura/**.

Pages is configured under **Settings → Pages** as *Deploy from a branch*,
serving this branch from the repository root. GitHub rebuilds and republishes
on every push, so no build step or Actions workflow is involved — the files in
this repository are exactly what is served.

`.nojekyll` matters here: without it Pages would run Jekyll, which excludes
`vendor/` from its output by default and would leave the Rive runtime 404ing.

## Running locally

The page uses `fetch()` to read the `.riv` file, which browsers block on
`file://` URLs — serve the folder over HTTP instead:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Notes on behaviour

**The state machine is named explicitly, and that is load-bearing.** Passing
neither `animations` nor `stateMachines` does *not* start the artboard's state
machine — the runtime's `atLeastOne` picks the first *timeline* and only falls
back to a state machine when the artboard has no timelines at all. Since
`ArtboardMaster` has nine timelines, the file rendered, played `Cover` once,
froze, and ignored every click. `stateMachines: "State Machine 1"` fixes it;
`ensureStateMachineRunning()` falls back to whatever the artboard actually has
if that name is changed in the editor.

**The renderer must be WebGL2.** The CPU `@rive-app/canvas` renderer does not
blur or feather: the soft glow behind the body renders as a hard-edged white
ellipse, the organs lose their translucency, and the whole artboard reads as
flat and posterised. Rendering the same frame through both runtimes, 16.9% of
pixels differ by more than 6/255 — e.g. the liver samples `rgb(147,103,102)` on
canvas against `rgb(195,166,168)` on WebGL2. It is also a main-thread
rasteriser, so it was the source of the interaction lag. `index.html` loads
`@rive-app/webgl2` and only falls back to the canvas build when
`getContext("webgl2")` fails.

**Fit is `Layout`, not `Fill`.** The board is authored at 1440x810. `Fill`
scaled that fixed board up to the window, which stretched it off its aspect
ratio and — because effect cost is not linear in magnification, blur going with
the square of its radius — made this design's large soft glows more expensive
the bigger the display. `Layout` resizes the *artboard* to the canvas instead,
so the file's layout components reflow, nothing stretches, and effects cost the
same at any window size. Verified reflowing correctly at 1024x900, an aspect
ratio nowhere near the authored one.

**Nothing is downscaled.** `resizeDrawingSurfaceToCanvas()` runs at the
display's own pixel ratio — 2560x1440 of surface on a 1280px 2x window. An
earlier revision traded resolution for frame rate adaptively; that is gone.

Honest limit on the above: switching `Fill` → `Layout` measured 1.00–1.03x in
this repo's test environment, which has no GPU and falls back to software GL.
The correctness win is not in doubt; the size of any speedup is not established.

## Where the frame time goes

Each of the file's 71 artboards was instantiated on its own with its state
machine running, and its median frame delta measured — first at 640x360, then
at 160x90, so that cost which tracks pixel count (rasterising: effects, blur,
overdraw) separates from cost which does not (advancing the scene graph).

Ranked, heaviest first — everything not listed sat on the 60fps floor:

| Artboard | 640x360 | 160x90 |
| --- | --- | --- |
| `ArtboardMaster` | ~1400 ms | ~483 ms |
| `TimeLine Page` | 1433 ms | 867 ms |
| `Timeline New` | 850 ms | 383 ms |
| `Overview Page` | 633 ms | 533 ms |
| `Human Anatomy 01` | 450 ms | 217 ms |
| `Card 6`, `TL-3 2`, `Organs/Liver`, `Card 5` | 367–467 ms | 100–233 ms |
| `Organs Page`, `TL-1`, `Organs Table 2`, `Card 2` | 283–333 ms | — |

Two things follow.

**`ArtboardMaster` dominates, and its cost splits in two.** Sweeping it across
four canvas sizes gives roughly a fixed ~420 ms per frame plus ~4.3 µs per
pixel. The fixed half is scene-graph work and does not shrink when you lower
the resolution — which is why capping the pixel ratio never made it feel
smooth. The per-pixel half is invisible on a small canvas and dominant at
full-screen, where it is what a large soft glow and stacked translucent layers
cost.

**The particle systems are not the problem.** `Particles`, `Particle`,
`Particles M` and `Light Fx` all measured at or near the idle floor
(0.07 µs/px). An earlier revision of this file said to cut them; that was a
guess, and measuring refuted it. Effort belongs on `ArtboardMaster` and the
three page artboards.

### What was tried on the embedding side

Every knob the runtime exposes was measured against `ArtboardMaster`, rather
than reasoned about. Two of them paid, and both are applied:

| Change | Result |
| --- | --- |
| WebGL2 renderer instead of canvas | applied — and fixes the colours |
| `Fit.Layout` instead of `Fit.Contain` | **1.18x faster** — applied |
| `autoBind: true` instead of `false` | **3x faster** — applied |
| `automaticallyHandleEvents: false` | no change |
| `useOffscreenRenderer: false` | no change |
| `shouldDisableRiveListeners: true` | no change |
| Skip rendering while idle | impossible — the scene never settles |
| Render in a worker via OffscreenCanvas | impossible — no API to inject pointer events, so interaction would break |
| Coalescing pointer events | pointless — 0, 8 and 40 `pointermove` per frame all cost the same |

`autoBind` is the surprising one: unbinding the view model made it *three times
slower*, so the file's `Inputs and variables` view model is doing real work
deciding what is active. Leave it on.

The embedding has nothing left to give. The remaining cost is in the `.riv`.

### Measuring your own edits

Append `?perf` to the URL for a live HUD — frame rate, median and p95 frame
time, surface size, artboard size and which renderer won. It is not created at
all without the flag, so it costs nothing in normal use. Use it to see whether
an edit in the Rive editor actually bought anything.

Numbers come from a software renderer, so treat them as ratios rather than
milliseconds; the expensive artboards also yield few frames per sample, so
their absolute values are noisy while the ranking is stable.

**Device copy is switched inside the artboard, not by blocking.** The file
carries both the desktop and the mobile/tablet onboarding text and picks between
them from a `desktop` boolean on its view model, so `index.html` classifies the
device and sets the flag rather than refusing to load:

```js
riveInstance.viewModelInstance.boolean("desktop").value = isDesktop();
```

`isDesktop()` is a fine pointer plus a window at least 800px wide, so phones and
tablets alike land on `false` — verified on iPhone 13 (390px, coarse) and iPad
Pro 11 (834px, coarse) against a 1280px desktop. It is re-applied on resize, so
dragging a window across the threshold switches the copy live. `autoBind`
already binds the file's default view model, so the property is reachable
straight off the instance — note it lives on `Inputs and variables`, the only
view model in the file, not on a separate one.

The `#blocked` markup survives purely as a fallback for a `.riv` without that
property. One consequence worth naming: a phone now downloads the full 2.6 MB
file to show a message telling it to switch to a desktop, where the previous
build fetched nothing at all. That is the cost of having the copy live in the
artboard.

Smaller points:

- `autoBind` and `automaticallyHandleEvents` are on, so the file's data-bound
  view models and its authored Rive events drive themselves.
- Resizing is debounced. Under `Fit.Layout` a resize re-lays out the artboard,
  so it is not something to run on every resize event.
- Playback pauses while the tab is hidden.

Interactivity is covered by a Playwright check that hashes canvas pixels before
and after each pointer event — hover and click on the nav tabs, theme toggle,
organ hotspots and zoom controls all produce real frame changes, on mouse and
on touch.

## Replacing the animation

Drop a new `.riv` file into `rive/` and update `RIV_URL` near the top of the
script block in `index.html`. The page deliberately does not pin an artboard or
state-machine name, so it keeps working when those are renamed in the Rive
editor.

To update the runtime:

```bash
npm pack @rive-app/webgl2@latest && tar xzf rive-app-webgl2-*.tgz
cp package/rive.js package/rive.wasm package/rive_fallback.wasm vendor/rive-webgl2/

npm pack @rive-app/canvas@latest && tar xzf rive-app-canvas-*.tgz
cp package/rive.js package/rive.wasm package/rive_fallback.wasm vendor/rive/
```

Keep the two at the same version — they share the `.riv` format.
