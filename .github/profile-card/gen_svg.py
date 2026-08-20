import html, json, sys

BG, BORDER = "#0d1117", "#30363d"
C_ART   = "#adbac7"
C_HEAD  = "#58a6ff"
C_LABEL = "#58a6ff"
C_DOT   = "#3d444d"
C_VAL   = "#e3b341"
C_RULE  = "#6e7681"
C_PLUS  = "#3fb950"
C_MINUS = "#f85149"

ART_FS, ART_CW, ART_LH = 12.5, 7.5, 14.6
PAN_FS, PAN_CW, PAN_LH = 13.5, 8.1, 19.5
PAD = 26
GAP = 28
PANEL_COLS = 58          # label ... value column width in chars

FONT = "ui-monospace,'SFMono-Regular','JetBrains Mono','Cascadia Mono','Courier New',monospace"

def tl(txt, cw):
    return f' textLength="{len(txt)*cw:.1f}" lengthAdjust="spacingAndGlyphs"'

def esc(s):
    return html.escape(s, quote=False).replace(" ", " ")

art = open("art.txt").read().rstrip("\n").split("\n")
spec = json.load(open("panel.json"))

rows = []   # (kind, payload)
for item in spec:
    t = item["t"]
    if t == "blank":
        rows.append(("blank", None))
    elif t == "head":
        rows.append(("head", item["text"]))
    elif t == "rule":
        rows.append(("rule", item["text"]))
    elif t == "kv":
        rows.append(("kv", (item["k"], item["v"], item.get("style"))))

art_w = max(len(l) for l in art) * ART_CW
pan_w = PANEL_COLS * PAN_CW
W = int(PAD * 2 + art_w + GAP + pan_w)
art_h = len(art) * ART_LH
pan_h = len(rows) * PAN_LH
H = int(PAD * 2 + max(art_h, pan_h))

art_x = PAD
pan_x = PAD + art_w + GAP
art_y0 = PAD + (H - 2 * PAD - art_h) / 2 + ART_FS
pan_y0 = PAD + (H - 2 * PAD - pan_h) / 2 + PAN_FS

out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Lars Vogel - GitHub profile card">',
       '<title>lars@vogella</title>',
       f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
       f'<g font-family="{FONT}" xml:space="preserve">']

out.append(f'<g font-size="{ART_FS}" fill="{C_ART}">')
for i, line in enumerate(art):
    if line.strip():
        out.append(f'<text x="{art_x:.1f}" y="{art_y0 + i*ART_LH:.1f}"{tl(line, ART_CW)}>{esc(line)}</text>')
out.append('</g>')

out.append(f'<g font-size="{PAN_FS}">')
for i, (kind, payload) in enumerate(rows):
    y = pan_y0 + i * PAN_LH
    if kind == "blank":
        continue
    if kind == "head":
        name = payload
        dash = "─" * max(0, PANEL_COLS - len(name) - 2)
        out.append(f'<text x="{pan_x:.1f}" y="{y:.1f}" fill="{C_HEAD}" font-weight="bold"{tl(name, PAN_CW)}>{esc(name)}</text>')
        out.append(f'<text x="{pan_x + (len(name)+1)*PAN_CW:.1f}" y="{y:.1f}" fill="{C_RULE}"{tl(dash, PAN_CW)}>{esc(dash)}</text>')
    elif kind == "rule":
        label = f"─ {payload} "
        dash = "─" * max(0, PANEL_COLS - len(label))
        out.append(f'<text x="{pan_x:.1f}" y="{y:.1f}" fill="{C_RULE}"{tl("─", PAN_CW)}>{esc("─")}</text>')
        out.append(f'<text x="{pan_x + 2*PAN_CW:.1f}" y="{y:.1f}" fill="{C_HEAD}" font-weight="bold"{tl(payload, PAN_CW)}>{esc(payload)}</text>')
        out.append(f'<text x="{pan_x + len(label)*PAN_CW:.1f}" y="{y:.1f}" fill="{C_RULE}"{tl(dash, PAN_CW)}>{esc(dash)}</text>')
    else:
        k, v, style = payload
        key = f" {k}:"
        ndots = max(1, PANEL_COLS - len(key) - len(v) - 1)
        out.append(f'<text x="{pan_x:.1f}" y="{y:.1f}" fill="{C_LABEL}"{tl(key, PAN_CW)}>{esc(key)}</text>')
        out.append(f'<text x="{pan_x + (len(key)+1)*PAN_CW:.1f}" y="{y:.1f}" fill="{C_DOT}"{tl("." * ndots, PAN_CW)}>{esc("." * ndots)}</text>')
        vx = pan_x + (PANEL_COLS - len(v)) * PAN_CW
        if style == "diff":
            plus, minus = v.split(", ")
            out.append(f'<text x="{vx:.1f}" y="{y:.1f}" fill="{C_PLUS}"{tl(plus, PAN_CW)}>{esc(plus)}</text>')
            out.append(f'<text x="{vx + (len(plus)+2)*PAN_CW:.1f}" y="{y:.1f}" fill="{C_MINUS}"{tl(minus, PAN_CW)}>{esc(minus)}</text>')
        else:
            out.append(f'<text x="{vx:.1f}" y="{y:.1f}" fill="{C_VAL}"{tl(v, PAN_CW)}>{esc(v)}</text>')
out.append('</g></g></svg>')
open(sys.argv[1], "w").write("\n".join(out) + "\n")
print(f"{sys.argv[1]}: {W}x{H}")
