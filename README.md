# Medura

An interactive [Rive](https://rive.app) prototype published as a static site on GitHub Pages.

## Contents

| Path | Purpose |
| --- | --- |
| `index.html` | The whole site: full-screen canvas, loader, Rive bootstrapping |
| `rive/medura_project_v1.riv` | The Rive file (~1.6 MB) |
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

- `MAX_DPR` caps the drawing surface at 2x. Cost scales with pixel count, and an
  uncapped 3x screen is 10.5M pixels per frame against 4.7M at 2x. Measured on
  the canvas renderer, dropping 3x → 1x cut median frame time from 133ms to
  50ms; the same fill-rate arithmetic applies on the GPU.
- `autoBind` and `automaticallyHandleEvents` are on, so the file's data-bound
  view models and its authored Rive events drive themselves.
- Fit is `Fill`, so the artboard covers the viewport with no letterbox bars.
  Fill stretches, which is invisible near the artboard's own ~16:9 shape but
  unreadable on a phone held portrait, so past `MAX_STRETCH` (35%) it falls
  back to `Contain`. Set `MAX_STRETCH = 0` in `index.html` to always stretch.
- The canvas tracks the real device pixel ratio and re-renders on resize and
  rotation, which also keeps pointer hit-testing aligned with the artwork.
- Playback pauses while the tab is hidden.
- Portrait phones get a brief "rotate your device" hint.

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
npm pack @rive-app/canvas@latest
tar xzf rive-app-canvas-*.tgz
cp package/rive.js package/rive.wasm package/rive_fallback.wasm vendor/rive/
```
