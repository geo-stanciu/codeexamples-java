import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

SRC, W = sys.argv[1], int(sys.argv[2])
CONTRAST, CUT, GAMMA = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
X0, X1, Y0, Y1 = [float(a) for a in sys.argv[6:10]]
ASPECT = 0.5
RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

img = Image.open(SRC).convert("L")
img = img.crop((int(X0*img.width), int(Y0*img.height), int(X1*img.width), int(Y1*img.height)))
img = ImageOps.autocontrast(img, cutoff=1)
img = ImageEnhance.Contrast(img).enhance(CONTRAST)
img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=70))
h = int(img.height / img.width * W * ASPECT)
img = img.resize((W, h), Image.LANCZOS)
p = img.load()

out = []
for y in range(h):
    row = ""
    for x in range(W):
        d = (1.0 - p[x, y] / 255.0) ** GAMMA
        row += " " if d < CUT else RAMP[min(len(RAMP)-1, int((d-CUT)/(1-CUT)*len(RAMP)))]
    out.append(row.rstrip())
print("\n".join(out))
