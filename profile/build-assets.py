#!/usr/bin/env python3
"""Render the profile README's SVG artwork in a light and a dark variant.

Every asset in `assets/` comes out of this file. Nothing is fetched at render
time — the README embeds plain SVG that lives in the repository, so the page
has no third-party requests and no service that can go down or rate-limit it.

    python3 build-assets.py

Retheming is a matter of editing THEMES below and re-running.
"""

from pathlib import Path
from string import Template

OUT = Path(__file__).parent / "assets"

THEMES = {
    # Matched to GitHub's own canvas colours so the artwork sits flush with the
    # page instead of floating on a card.
    "dark": dict(
        bg="#0D1117",
        fg="#E6EDF3",
        dim="#8B949E",
        hair="#30363D",
        grid="#FFFFFF",
        grid_op="0.045",
        accent="#FF6A3D",
    ),
    "light": dict(
        bg="#FFFFFF",
        fg="#0D1117",
        dim="#57606A",
        hair="#D0D7DE",
        grid="#000000",
        grid_op="0.055",
        accent="#D93A14",
    ),
}

# Only ever interpolated inside <style><![CDATA[ ]]>, so these are raw CSS —
# quotes must be literal, not XML entities.
MONO = 'ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace'
SANS = '"Helvetica Neue",Helvetica,Arial,"Segoe UI",sans-serif'

# --------------------------------------------------------------------------
# 01 — header
# --------------------------------------------------------------------------

HEADER = Template(
    """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 400" width="1280" height="400" role="img" aria-label="Parya Bahrami, design technologist. Interaction, motion, design systems and front-end. A cubic-bezier easing curve is plotted at the right with a dot tracing it.">
<title>Parya Bahrami — Design Technologist</title>
<style><![CDATA[
  .mono{font-family:$mono}
  .sans{font-family:$sans}
  .scan{animation:scan 9s linear infinite}
  @keyframes scan{from{transform:translateX(-60px)}to{transform:translateX(1280px)}}
  .cur{animation:blink 1.1s steps(1,end) infinite}
  @keyframes blink{0%,49.9%{opacity:1}50%,100%{opacity:0}}
  /* The dot travels linearly in x and eased in y, so it traces exactly the
     curve drawn beneath it rather than merely approximating it. */
  .mx{animation:mx 4s infinite}
  @keyframes mx{0%{transform:translateX(0);animation-timing-function:linear}70%,100%{transform:translateX(380px)}}
  .my{animation:my 4s infinite}
  @keyframes my{0%{transform:translateY(0);animation-timing-function:cubic-bezier(.4,0,.2,1)}70%,100%{transform:translateY(-230px)}}
  @media (prefers-reduced-motion:reduce){
    .scan,.cur,.mx,.my{animation:none}
    .scan{opacity:0}
  }
]]></style>

<defs>
  <linearGradient id="sweep" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="$accent" stop-opacity="0"/>
    <stop offset="1" stop-color="$accent" stop-opacity="0.14"/>
  </linearGradient>
</defs>

<rect width="1280" height="400" fill="$bg"/>
<g stroke="$grid" stroke-opacity="$grid_op" stroke-width="1">$gridlines</g>
<g class="scan"><rect x="0" y="0" width="60" height="400" fill="url(#sweep)"/><rect x="59" y="0" width="1.5" height="400" fill="$accent" opacity="0.28"/></g>
<rect x="0.5" y="0.5" width="1279" height="399" fill="none" stroke="$hair"/>
<g fill="none" stroke="$hair" stroke-width="1.5">
  <path d="M20 44 V20 H44"/><path d="M1236 20 H1260 V44"/>
  <path d="M20 356 V380 H44"/><path d="M1236 380 H1260 V356"/>
</g>

<text x="64" y="84" class="mono" font-size="13" letter-spacing="3" fill="$dim">PARYABHRMI &#183; DESIGN TECHNOLOGIST &#183; PARYABAHRAMI.IR</text>

<g class="sans" fill="$fg" font-size="84" font-weight="700" letter-spacing="1">
  <text x="64" y="200" textLength="300" lengthAdjust="spacing">PARYA</text>
  <text x="64" y="282" textLength="430" lengthAdjust="spacing">BAHRAMI</text>
</g>
<rect class="cur" x="510" y="240" width="15" height="44" fill="$accent"/>
<rect x="64" y="306" width="430" height="5" fill="$accent"/>
<text x="64" y="346" class="mono" font-size="13" letter-spacing="2" fill="$dim">INTERACTION &#183; MOTION &#183; DESIGN SYSTEMS &#183; FRONT-END</text>

<g>
  <text x="800" y="80" class="mono" font-size="13" letter-spacing="2" fill="$dim">EASING &#183; cubic-bezier(0.4, 0, 0.2, 1)</text>
  <rect x="800" y="110" width="380" height="230" fill="none" stroke="$grid" stroke-opacity="$grid_op" stroke-dasharray="3 5"/>
  <path d="M800 110 V340 H1180" fill="none" stroke="$hair" stroke-width="1.5"/>
  <g stroke="$accent" stroke-width="1.2" stroke-dasharray="4 4" opacity="0.75">
    <line x1="800" y1="340" x2="952" y2="340"/>
    <line x1="1180" y1="110" x2="876" y2="110"/>
  </g>
  <g fill="$bg" stroke="$accent" stroke-width="2">
    <circle cx="952" cy="340" r="5"/><circle cx="876" cy="110" r="5"/>
  </g>
  <path d="M800 340 C952 340 876 110 1180 110" fill="none" stroke="$fg" stroke-width="2.5" stroke-linecap="round"/>
  <g class="mx"><circle class="my" cx="800" cy="340" r="6.5" fill="$accent"/></g>
  <text x="800" y="366" class="mono" font-size="11" fill="$dim">t = 0</text>
  <text x="1180" y="366" class="mono" font-size="11" fill="$dim" text-anchor="end">t = 1</text>
</g>
</svg>
"""
)


def gridlines() -> str:
    parts = [f'<path d="M{x} 0 V400"/>' for x in range(64, 1280, 64)]
    parts += [f'<path d="M0 {y} H1280"/>' for y in range(64, 400, 64)]
    return "".join(parts)


# --------------------------------------------------------------------------
# 02 — practice map
# --------------------------------------------------------------------------

PRACTICE = Template(
    """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 360" width="1280" height="360" role="img" aria-label="Practice map. A design set containing Figma, Rive, motion and type and grid, overlapping an engineering set containing TypeScript, React, Canvas and WebGL, and Git and CI. The overlap is labelled prototypes, design systems, tokens and motion spec.">
<title>Practice map — where design and engineering overlap</title>
<style><![CDATA[
  .mono{font-family:$mono}
  .sans{font-family:$sans}
  .pulse{animation:pulse 7s ease-in-out infinite}
  @keyframes pulse{0%,100%{opacity:.10}50%{opacity:.20}}
  .ants{animation:ants 3.5s linear infinite}
  @keyframes ants{to{stroke-dashoffset:-32}}
  @media (prefers-reduced-motion:reduce){.pulse,.ants{animation:none}}
]]></style>
<defs>
  <clipPath id="setA"><rect x="100" y="70" width="640" height="220" rx="110"/></clipPath>
</defs>

<rect width="1280" height="360" fill="$bg"/>
<text x="64" y="44" class="mono" font-size="13" letter-spacing="3" fill="$dim">02 &#8212; PRACTICE MAP</text>
<path d="M64 58 H1216" stroke="$hair"/>

<g clip-path="url(#setA)">
  <rect class="pulse" x="540" y="70" width="640" height="220" rx="110" fill="$accent"/>
</g>
<g fill="none" stroke="$hair" stroke-width="1.5">
  <rect x="100" y="70" width="640" height="220" rx="110"/>
  <rect x="540" y="70" width="640" height="220" rx="110"/>
</g>
<path class="ants" d="M640 70 V290" stroke="$accent" stroke-width="1" stroke-dasharray="6 10" opacity="0.5"/>

<g text-anchor="middle">
  <text x="320" y="132" class="sans" font-size="21" font-weight="700" letter-spacing="4" fill="$fg">DESIGN</text>
  <text x="960" y="132" class="sans" font-size="21" font-weight="700" letter-spacing="4" fill="$fg">ENGINEERING</text>
  <g class="mono" font-size="13" letter-spacing="1" fill="$dim">
    <text x="320" y="176">FIGMA</text>
    <text x="320" y="202">RIVE</text>
    <text x="320" y="228">MOTION</text>
    <text x="320" y="254">TYPE &amp; GRID</text>
    <text x="960" y="176">TYPESCRIPT</text>
    <text x="960" y="202">REACT</text>
    <text x="960" y="228">CANVAS / WEBGL</text>
    <text x="960" y="254">GIT &amp; CI</text>
  </g>
  <g class="mono" font-size="12" font-weight="700" letter-spacing="0.5" fill="$accent">
    <text x="640" y="176">PROTOTYPES</text>
    <text x="640" y="202">DESIGN SYSTEMS</text>
    <text x="640" y="228">TOKENS</text>
    <text x="640" y="254">MOTION SPEC</text>
  </g>
  <text x="640" y="330" class="mono" font-size="13" letter-spacing="2" fill="$dim">THE OVERLAP IS THE JOB</text>
</g>
</svg>
"""
)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        subs = dict(theme, mono=MONO, sans=SANS)
        (OUT / f"header-{name}.svg").write_text(
            HEADER.substitute(subs, gridlines=gridlines()), encoding="utf-8"
        )
        (OUT / f"practice-{name}.svg").write_text(
            PRACTICE.substitute(subs), encoding="utf-8"
        )
    print(f"wrote {len(THEMES) * 2} files to {OUT}")


if __name__ == "__main__":
    main()
