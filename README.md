# EquaLex.com website

Static bilingual site for EquaLex GmbH. English is the default (`/`), German lives in `/de/`.

- `assets/style.css` – shared styles (light and dark)
- `assets/fonts/` – self-hosted Atkinson Hyperlegible Next (SIL Open Font License)
- `impressum.html`, `de/impressum.html` – legal notice

No build step: the files are served as they are by GitHub Pages.

To regenerate the pages after editing text in `tools/build.py` or styles in `assets/style.css`, run `python3 tools/build.py .` from the repo root. It also updates the stylesheet version tag so browsers fetch the new styles.
- `assets/logo/` – EquaLex logo as SVG, for dark and light backgrounds (rebuilt from the original logos.psd; regenerate with `tools/logo/make_logo.py`)
