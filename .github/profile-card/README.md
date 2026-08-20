Regenerating the profile card
=============================

The card in the repository README is a static SVG built from `portrait.png` and `panel.json`.

```bash
python3 asciifyA.py portrait.png 62 1.35 0.14 1.6 0.17 0.87 0.0 0.78 | python3 clean.py | head -31 > art.txt
python3 gen_svg.py ../profile-card.svg
```

The `asciifyA.py` arguments are width, contrast, cutoff, gamma and the crop box as fractions
(left, right, top, bottom).
A higher gamma makes the face lighter and keeps only hair and features dense.
Edit `panel.json` to change the text on the right side.
Requires Python with Pillow.
