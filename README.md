# Medura

An interactive [Rive](https://rive.app) prototype published as a static site on GitHub Pages.

## Contents

| Path | Purpose |
| --- | --- |
| `index.html` | The whole site: full-screen canvas, loader, Rive bootstrapping |
| `rive/medura_project_v1.riv` | The Rive file (~1.6 MB) |
| `vendor/rive/` | Pinned `@rive-app/canvas` 2.39.2 runtime (`rive.js` + WebAssembly) |
| `.github/workflows/pages.yml` | Builds and deploys the site to GitHub Pages |
| `.nojekyll` | Stops Pages from running Jekyll over the files |

Everything is served from this repository — the page makes no third-party
requests, so no CDN outage, version drift, or content blocker can break it.
`index.html` points the runtime at the bundled `.wasm` via
`RuntimeLoader.setWasmUrl()` instead of its default CDN location.

## Enabling GitHub Pages

The deploy workflow is committed and runs on every push, but Pages itself has
to be switched on once by a repository admin — the workflow's `GITHUB_TOKEN`
cannot do it (`Resource not accessible by integration`), so `configure-pages`
fails until this is done:

1. Open **Settings → Pages** in this repository.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Re-run the *Deploy to GitHub Pages* workflow from the **Actions** tab, or push a commit.

The site then lives at `https://paryabhrmi.github.io/Medura/`.

## Running locally

The page uses `fetch()` to read the `.riv` file, which browsers block on
`file://` URLs — serve the folder over HTTP instead:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Notes on behaviour

- The canvas is resized to the real device pixel ratio, so the artwork stays
  sharp on high-DPI screens and re-renders on resize and rotation.
- The page background is sampled from the artboard's own edge colour, which
  makes the letterbox bars invisible at any aspect ratio.
- Playback pauses while the tab is hidden.
- The artboard is a wide desktop layout, so portrait phones get a brief
  "rotate your device" hint.

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
