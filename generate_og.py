"""Generate a 1200x630 social-preview (Open Graph) image for the repo / live app."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BLUE_TOP, BLUE_BOT = (37, 99, 235), (22, 44, 120)
WHITE, DARK, MUTED = (255, 255, 255), (20, 28, 46), (200, 214, 245)

def font(path_list, size):
    for p in path_list:
        try: return ImageFont.truetype(p, size)
        except OSError: continue
    return ImageFont.load_default()

BOLD = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
SEMI = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]

def vgrad(w, h, top, bot):
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / (h - 1)
        col.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return col.resize((w, h))

def penta(cx, cy, r, rot=-math.pi / 2):
    return [(cx + r * math.cos(rot + i * 2 * math.pi / 5),
             cy + r * math.sin(rot + i * 2 * math.pi / 5)) for i in range(5)]

def draw_ball(d, cx, cy, R):
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=WHITE)
    cp = penta(cx, cy, R * 0.34)
    d.polygon(cp, fill=DARK)
    sw = max(3, int(R * 0.05))
    for i in range(5):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        d.line([cp[i], (cx + R * math.cos(ang), cy + R * math.sin(ang))], fill=DARK, width=sw)
        ox, oy = cx + R * 0.74 * math.cos(ang), cy + R * 0.74 * math.sin(ang)
        d.polygon(penta(ox, oy, R * 0.27, ang + math.pi / 2), fill=DARK)

SS = 2  # supersample for crisp text/edges
img = vgrad(W * SS, H * SS, BLUE_TOP, BLUE_BOT).convert("RGB")
d = ImageDraw.Draw(img)

draw_ball(d, 300 * SS, 315 * SS, 200 * SS)

tx = 548 * SS
d.text((tx, 150 * SS), "World Cup 2026", font=font(BOLD, 76 * SS), fill=WHITE)
d.text((tx, 246 * SS), "Simulator", font=font(BOLD, 76 * SS), fill=WHITE)
d.text((tx, 372 * SS), "Pick group standings & the best thirds,",
       font=font(SEMI, 30 * SS), fill=MUTED)
d.text((tx, 414 * SS), "then play the bracket to the final.",
       font=font(SEMI, 30 * SS), fill=MUTED)
d.text((tx, 492 * SS), "Installable web app  •  works offline",
       font=font(SEMI, 29 * SS), fill=(150, 180, 240))

img.resize((W, H), Image.LANCZOS).save("og-preview.png")
print("og-preview.png written (1200x630)")
