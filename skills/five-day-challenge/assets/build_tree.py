import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1300

# TrustPager teal tokens (as given, local to this asset, not brand.json)
ACCENT = (41, 198, 198)       # #29c6c6
ACCENT_DEEP = (31, 157, 134)  # #1f9d86
ACCENT_SOFT = (127, 230, 218) # #7fe6da
CYAN = (84, 230, 216)         # #54e6d8
INK = (243, 246, 255)         # #f3f6ff
INK_MUTED = (184, 199, 207)   # #b8c7cf
BOX_INK = (4, 32, 30)         # #04201e

BG_STOPS = [
    (0.0, (12, 51, 47)),   # #0c332f
    (0.46, (5, 22, 20)),   # #051614
    (1.0, (1, 6, 7)),      # #010607
]

_WIN_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
_WIN_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD = _WIN_BOLD if os.path.exists(_WIN_BOLD) else None
FONT_REG = _WIN_REG if os.path.exists(_WIN_REG) else None


def radial_bg(w, h):
    cx, cy = w * 0.5, h * 0.42
    max_r = math.hypot(max(cx, w - cx) * (1 / 1.2), max(cy, h - cy) * (1 / 1.2))
    ys, xs = np.mgrid[0:h, 0:w]
    d = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2) / max_r
    d = np.clip(d, 0, 1)
    out = np.zeros((h, w, 3), dtype=np.float32)
    for i in range(len(BG_STOPS) - 1):
        t0, c0 = BG_STOPS[i]
        t1, c1 = BG_STOPS[i + 1]
        mask = (d >= t0) & (d <= t1)
        local_t = np.clip((d - t0) / (t1 - t0), 0, 1)
        for ch in range(3):
            out[..., ch] = np.where(mask, c0[ch] + (c1[ch] - c0[ch]) * local_t, out[..., ch])
    return Image.fromarray(out.astype(np.uint8), "RGB")


def hexagon(cx, cy, r):
    pts = []
    for i in range(6):
        angle = math.pi / 180 * (60 * i - 30)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


NODE_R = 108
TIER2_R = 108
SUMMIT_R = 100

# fractional (x, y) positions, y=0 top .. 1 bottom
BASE_Y = 0.85
TIER1_Y = 0.60
TIER2_Y = 0.36
SUMMIT_Y = 0.15

BASE = {
    "win":   (0.10, BASE_Y, "WIN WORK"),
    "paid":  (0.26, BASE_Y, "GET PAID"),
    "cust":  (0.42, BASE_Y, "STAY ON TOP\nOF CUSTOMERS"),
    "look":  (0.58, BASE_Y, "LOOK PROFESSIONAL\n& MARKET"),
    "paper": (0.74, BASE_Y, "HANDLE\nPAPERWORK"),
    "plan":  (0.90, BASE_Y, "PLAN & DECIDE"),
}

TIER1 = {
    "value":   (0.08, TIER1_Y, "VALUE EQUATION /\nOFFER TUNE-UP",     "win"),
    "xero":    (0.22, TIER1_Y, "XERO /\nINVOICING SYNC",              "paid"),
    "autom":   (0.36, TIER1_Y, "AUTOMATIONS &\nFOLLOW-UP ENGINE",     "cust"),
    "social":  (0.50, TIER1_Y, "SOCIAL & VIDEO\nSTUDIO",              "look"),
    "ads":     (0.64, TIER1_Y, "META ADS",                            "look"),
    "esign":   (0.78, TIER1_Y, "E-SIGNING &\nDOC WORKFLOWS",          "paper"),
    "team":    (0.92, TIER1_Y, "TEAM &\nREPORTING",                   "plan"),
}

TIER2 = {
    "money": (0.08, TIER2_Y, "ADVANCED\nMONEY MODELS", "value"),
}

SUMMIT = (0.50, SUMMIT_Y, "OPERATE YOUR BUSINESS\nAND WATCH IT SCALE")

LEAVES = ["xero", "autom", "social", "ads", "esign", "team"]  # tier1 with no tier2 child
LEAVES_TIER2 = ["money"]


def px(fx, fy):
    return (fx * W, fy * H)


def draw_glow_line(draw, p0, p1, color, width, glow_layers=3):
    for i in range(glow_layers, 0, -1):
        alpha = int(40 / i)
        draw.line([p0, p1], fill=color + (alpha,), width=width + i * 4)
    draw.line([p0, p1], fill=color + (220,), width=width)


_FONT_CACHE = {}


def _font_at(size):
    if size not in _FONT_CACHE:
        _FONT_CACHE[size] = ImageFont.truetype(FONT_BOLD, size) if FONT_BOLD else ImageFont.load_default()
    return _FONT_CACHE[size]


def fit_label_font(draw, label, max_width, max_height, start_size=19, min_size=11):
    """Shrink font size until every line clears max_width and the block clears max_height."""
    for size in range(start_size, min_size - 1, -1):
        font = _font_at(size)
        lines = label.split("\n")
        widths = [draw.textlength(line, font=font) for line in lines]
        line_h = size + 6
        block_h = line_h * len(lines)
        if max(widths) <= max_width and block_h <= max_height:
            return font, line_h
    return _font_at(min_size), min_size + 6


def draw_node(draw, cx, cy, r, label, filled=False, fill_color=None, text_color=None):
    pts = hexagon(cx, cy, r)
    if filled:
        draw.polygon(pts, fill=fill_color + (255,), outline=ACCENT + (255,), width=4)
    else:
        draw.polygon(pts, fill=(8, 28, 27, 220), outline=ACCENT + (255,), width=4)
        # inner soft hex for a "wireframe node" feel
        inner = hexagon(cx, cy, r - 10)
        draw.polygon(inner, outline=ACCENT_SOFT + (140,), width=1)

    # text sits INSIDE the hex, sized to fit its widest point, not below it
    max_width = r * 1.5   # conservative vs. the true 1.73r mid-line width
    max_height = r * 1.5
    font, line_h = fit_label_font(draw, label, max_width, max_height)
    lines = label.split("\n")
    tc = text_color or INK
    total_h = line_h * len(lines)
    ty = cy - total_h / 2 + line_h / 2
    for i, line in enumerate(lines):
        draw.text((cx, ty + i * line_h), line, font=font, fill=tc, anchor="mm")


def draw_highlight_box(draw, cx, cy, label, font_bold, text_color, fill_color):
    lines = label.split("\n")
    line_h = 40
    pad_x, pad_y = 44, 30
    widths = [draw.textlength(line, font=font_bold) for line in lines]
    box_w = max(widths) + pad_x * 2
    box_h = line_h * len(lines) + pad_y * 2
    box = (cx - box_w / 2, cy - box_h / 2, cx + box_w / 2, cy + box_h / 2)
    draw.rounded_rectangle(box, radius=22, fill=fill_color + (255,), outline=CYAN + (255,), width=3)
    ty = cy - (line_h * len(lines)) / 2 + line_h / 2 - 4
    for i, line in enumerate(lines):
        draw.text((cx, ty + i * line_h), line, font=font_bold, fill=text_color, anchor="mm")
    return box


def build():
    bg = radial_bg(W, H).convert("RGBA")
    line_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(line_layer, "RGBA")

    if FONT_BOLD:
        font_summit = ImageFont.truetype(FONT_BOLD, 26)
    else:
        font_summit = ImageFont.load_default()

    # pre-measure the summit box so lines can target its bottom edge, not its center
    summit_cx, summit_cy = px(*SUMMIT[:2])
    lines_txt = SUMMIT[2].split("\n")
    widths = [ldraw.textlength(line, font=font_summit) for line in lines_txt]
    summit_box_w = max(widths) + 44 * 2
    summit_box_h = 40 * len(lines_txt) + 30 * 2
    summit_target = (summit_cx, summit_cy + summit_box_h / 2)

    # base -> tier1 lines
    for key, (fx, fy, label, parent) in TIER1.items():
        p0 = px(*BASE[parent][:2])
        p1 = px(fx, fy)
        draw_glow_line(ldraw, p0, p1, ACCENT_DEEP, 5)

    # tier1 -> tier2 lines
    for key, (fx, fy, label, parent) in TIER2.items():
        p0 = px(*TIER1[parent][:2])
        p1 = px(fx, fy)
        draw_glow_line(ldraw, p0, p1, ACCENT_DEEP, 5)

    # leaves -> summit (target the box's bottom edge, not its center)
    for key in LEAVES:
        fx, fy = TIER1[key][0], TIER1[key][1]
        draw_glow_line(ldraw, px(fx, fy), summit_target, CYAN, 4)
    for key in LEAVES_TIER2:
        fx, fy = TIER2[key][0], TIER2[key][1]
        draw_glow_line(ldraw, px(fx, fy), summit_target, CYAN, 4)

    composed = Image.alpha_composite(bg, line_layer)
    draw = ImageDraw.Draw(composed, "RGBA")

    if FONT_BOLD:
        font_summit = ImageFont.truetype(FONT_BOLD, 26)
        font_eyebrow = ImageFont.truetype(FONT_BOLD, 20)
    else:
        font_summit = font_eyebrow = ImageFont.load_default()

    # eyebrow (kept clear of the summit node's top edge)
    draw.text((W / 2, 26), "YOUR BUSINESS OPERATING SYSTEM", font=font_eyebrow,
              fill=ACCENT_SOFT, anchor="ma")

    for key, (fx, fy, label) in BASE.items():
        cx, cy = px(fx, fy)
        draw_node(draw, cx, cy, NODE_R, label)

    for key, (fx, fy, label, parent) in TIER1.items():
        cx, cy = px(fx, fy)
        draw_node(draw, cx, cy, NODE_R, label)

    for key, (fx, fy, label, parent) in TIER2.items():
        cx, cy = px(fx, fy)
        draw_node(draw, cx, cy, TIER2_R, label)

    draw_highlight_box(draw, summit_cx, summit_cy, SUMMIT[2], font_summit, BOX_INK, ACCENT)

    # tier captions sit ABOVE each row (clear of the enlarged hexes), left-aligned to the margin
    caption_font = font_eyebrow
    draw.text((30, BASE["win"][1] * H - NODE_R - 20), "THE FLOOR", font=caption_font, fill=INK_MUTED, anchor="lb")
    draw.text((30, TIER1["value"][1] * H - NODE_R - 20), "ADD-ONS", font=caption_font, fill=INK_MUTED, anchor="lb")
    draw.text((30, TIER2["money"][1] * H - TIER2_R - 20), "SCALING", font=caption_font, fill=INK_MUTED, anchor="lb")

    composed.convert("RGB").save(os.path.join(HERE, "capability-tree.png"), optimize=True)
    print("saved")


if __name__ == "__main__":
    build()
