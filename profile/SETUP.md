# Putting this on your profile

A GitHub profile README only renders from one specific place: a **public
repository named exactly after your username**, with a `README.md` at its root.
For you that is `paryabhrmi/paryabhrmi` — it does not exist yet.

This folder is that repository's contents, built and previewed here so it can be
reviewed before it goes live.

## Check these first

The artwork and copy make a few assumptions. Correct them before publishing:

| Where | Assumption |
| --- | --- |
| `build-assets.py` → `HEADER` | The name reads **PARYA BAHRAMI**, taken from `paryabahrami.ir`. If that is not how you spell it, change the two `<text>` lines — and adjust `textLength` (`300` and `430`) so the width still matches the accent rule beneath and the cursor block after it. |
| `README.md` → Toolkit | Trim anything you would not want to be asked about in an interview. |
| `README.md` → Elsewhere | Site, LinkedIn and GitHub are in. Add email, Dribbble or Bluesky if you want them reachable. |

## Publish

```bash
# 1. Create the repo on GitHub, public, named exactly: paryabhrmi
#    https://github.com/new  — leave it empty, no README, no .gitignore

# 2. Copy this folder's contents into a fresh clone of it
git clone https://github.com/paryabhrmi/paryabhrmi.git
cp -R profile/. paryabhrmi/
cd paryabhrmi

# 3. Ship
git add .
git commit -m "Profile README"
git push
```

The images are referenced by relative path (`assets/…`), so they resolve as long
as `assets/` sits next to `README.md` in that repo. Nothing else is required —
GitHub picks the README up automatically and it appears at
`github.com/paryabhrmi`.

## Editing the artwork

Both colour schemes come out of one source:

```bash
python3 build-assets.py    # rewrites all four SVGs in assets/
```

`THEMES` at the top of the script holds every colour. The accent is the only
non-neutral value in the whole system — change those two hex codes and the
entire page rethemes.

The README pairs the variants with `<picture>` + `prefers-color-scheme`, which
GitHub honours, so the header sits flush against the page background in both
themes instead of floating on a mismatched card.

## Local preview

The assets are plain files, so any static server shows them as GitHub will:

```bash
python3 -m http.server 8000
# open http://localhost:8000/profile/assets/header-dark.svg
```

Animation notes, if you tune it: the dot on the easing curve moves linearly in
x and eased in y, which is why it traces the drawn curve exactly rather than
approximately — if you change the `cubic-bezier` in the `.my` keyframe, change
the `C` control points of the curve path to match, and the caption too. All
motion is wrapped in `prefers-reduced-motion: reduce`.
