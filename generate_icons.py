"""Generate PWA app icons (soccer ball on a blue field) for World Cup 2026 Simulator."""
import math
from PIL import Image, ImageDraw

BLUE_TOP = (37, 99, 235)     # #2563eb
BLUE_BOT = (29, 64, 175)     # #1d40af
WHITE = (255, 255, 255)
DARK = (20, 28, 46)

SS = 1024  # supersample canvas, then downscale

def vgrad(size, top, bot):
    col = Image.new("RGB", (1, size))
    for y in range(size):
        t = y / (size - 1)
        col.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return col.resize((size, size))

def penta(cx, cy, r, rot=-math.pi / 2):
    return [(cx + r * math.cos(rot + i * 2 * math.pi / 5),
             cy + r * math.sin(rot + i * 2 * math.pi / 5)) for i in range(5)]

def draw_ball(d, cx, cy, R):
    # white sphere
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=WHITE,
              outline=(225, 230, 240), width=max(2, int(R * 0.02)))
    # central pentagon
    cp = penta(cx, cy, R * 0.34, -math.pi / 2)
    d.polygon(cp, fill=DARK)
    # five seams from central pentagon vertices outward + outer partial pentagons
    sw = max(3, int(R * 0.05))
    for i in range(5):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        vx, vy = cp[i]
        ex, ey = cx + R * math.cos(ang), cy + R * math.sin(ang)
        d.line([(vx, vy), (ex, ey)], fill=DARK, width=sw)
        # outer dark pentagon nestled near the rim, pointing inward
        ox, oy = cx + R * 0.74 * math.cos(ang), cy + R * 0.74 * math.sin(ang)
        op = penta(ox, oy, R * 0.27, ang + math.pi / 2)
        d.polygon(op, fill=DARK)

def make(size, maskable=False):
    img = Image.new("RGBA", (SS, SS), (0, 0, 0, 0))
    bg = vgrad(SS, BLUE_TOP, BLUE_BOT).convert("RGBA")
    if maskable:
        img.paste(bg, (0, 0))              # full-bleed for mask safe-zone
        R = SS * 0.30
    else:
        mask = Image.new("L", (SS, SS), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, SS - 1, SS - 1],
                                               radius=int(SS * 0.22), fill=255)
        img.paste(bg, (0, 0), mask)
        R = SS * 0.345
    d = ImageDraw.Draw(img)
    draw_ball(d, SS / 2, SS / 2, R)
    return img.resize((size, size), Image.LANCZOS)

make(192).save("icon-192.png")
make(512).save("icon-512.png")
make(512, maskable=True).save("icon-512-maskable.png")
make(180).save("apple-touch-icon.png")
print("icons written: 192, 512, 512-maskable, apple-touch-icon")
