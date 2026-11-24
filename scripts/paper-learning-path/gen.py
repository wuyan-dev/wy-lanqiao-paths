# -*- coding: utf-8 -*-
"""风格二：纸质学习路径图（参照 微信图片_202611210926_1）—— Java 组课程
米色纸纹 + 撕纸边白卡 + 马克笔黄标题 + 三列彩色胶囊表头 + 图标行 + 手作贴纸
"""
import math, os, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 900, 450
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
CFG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content.json")
try:
    CFG = json.load(open(CFG_PATH, encoding="utf-8"))
except Exception:
    CFG = {}
F_B = "C:/Windows/Fonts/msyhbd.ttc"
F_R = "C:/Windows/Fonts/msyh.ttc"

INK = (46, 38, 28)
INK_SOFT = (74, 62, 48)
BLUE = (43, 106, 220)
ORANGE = (241, 132, 42)
PURPLE = (124, 143, 222)
MARKER = (247, 201, 58)
YELLOW = (253, 231, 160)
YELLOW_D = (221, 158, 24)
LILAC = (223, 229, 250)
NAVY = (45, 58, 98)
CREAM = (255, 252, 245)


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(draw, text, f):
    return draw.textlength(text, font=f)


def fit_font(draw, text, max_w, start, path=F_B, min_size=9):
    s = start
    while s > min_size and tw(draw, text, font(path, s)) > max_w:
        s -= 1
    return font(path, s)


# ---------------- 纸背景 ----------------
def paper_bg(w, h, seed=7):
    rng = np.random.default_rng(seed)
    arr = np.zeros((h, w, 3), dtype=np.float64)
    arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = 238, 226, 205

    low = rng.normal(0, 1, (12, 24))
    low = (low - low.min()) / (np.ptp(low) + 1e-6) * 255
    lowimg = Image.fromarray(low.astype(np.uint8)).resize((w, h), Image.BICUBIC)
    lv = (np.array(lowimg).astype(np.float64) / 255 - 0.5) * 13

    hi = rng.normal(0, 1, (h, w))
    hiimg = Image.fromarray(np.uint8(np.clip(hi * 40 + 128, 0, 255))).filter(ImageFilter.GaussianBlur(0.4))
    hv = (np.array(hiimg).astype(np.float64) - 128) / 128 * 5

    g = lv + hv
    for c in range(3):
        arr[:, :, c] += g

    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w * 0.62)) ** 2 + ((yy - h / 2) / (h * 0.66)) ** 2)
    a = np.clip((d - 0.55) * 0.5, 0, 0.42)
    arr[:, :, 0] -= a * 26
    arr[:, :, 1] -= a * 30
    arr[:, :, 2] -= a * 36
    return Image.fromarray(np.uint8(np.clip(arr, 0, 255)))


def torn_mask(w, h, box, seed, amp=4.6, step=4):
    x0, y0, x1, y1 = box
    rng = np.random.default_rng(seed)
    n = max(2, int((x1 - x0) / step))
    top, bot = [], []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        # 低频起伏 + 高频碎口 + 偶发深撕口
        base = math.sin(t * 9.0) * amp * 0.55 + math.sin(t * 31.0) * amp * 0.25
        tear = -amp * 1.6 if rng.random() < 0.05 else 0.0
        top.append((x, y0 + base + rng.uniform(-amp, amp) * 0.8 + tear))
        tear2 = amp * 1.6 if rng.random() < 0.05 else 0.0
        bot.append((x, y1 - math.sin(t * 7.0 + 1.1) * amp * 0.5 + rng.uniform(-amp, amp) * 0.8 + tear2))
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.polygon(top + bot[::-1], fill=255)
    for x, y in top + bot:  # 边缘纸纤维
        d.ellipse([x - rng.uniform(0.5, 1.4), y - rng.uniform(0.5, 1.4),
                   x + rng.uniform(0.5, 1.4), y + rng.uniform(0.5, 1.4)], fill=255)
    return m


def white_card(base, box, seed):
    w, h = base.size
    m = torn_mask(w, h, box, seed)
    # 投影（向下偏移）
    sh = m.filter(ImageFilter.GaussianBlur(7))
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow.paste(Image.new("RGBA", (w, h), (118, 92, 58, 78)), (0, 0), sh)
    shadow = Image.fromarray(np.roll(np.array(shadow), 6, axis=0))
    base.alpha_composite(shadow)
    # 卡面
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card.paste(Image.new("RGBA", (w, h), CREAM + (255,)), (0, 0), m)
    # 卡面淡纹（只在卡内）
    rng = np.random.default_rng(seed + 5)
    noise = np.clip(rng.normal(0, 1, (h, w)) * 0.55 + 0.5, 0, 1)
    strength = Image.fromarray(np.uint8(noise * 255)).filter(ImageFilter.GaussianBlur(0.6))
    a = strength.point(lambda v: int(abs(v - 128) * 0.20))
    a = Image.composite(a, Image.new("L", (w, h), 0), m)
    warm = Image.new("RGBA", (w, h), (200, 182, 154, 255))
    warm.putalpha(a)
    card = Image.alpha_composite(card, warm)
    # 纸张边缘：一圈浅棕，让撕口有厚度
    eroded = m.filter(ImageFilter.MinFilter(5))
    edge = Image.fromarray(np.clip(np.array(m, dtype=np.int16) - np.array(eroded, dtype=np.int16), 0, 255).astype(np.uint8))
    edge_l = Image.new("RGBA", (w, h), (222, 204, 176, 255))
    edge_l.putalpha(edge.point(lambda v: int(v * 0.85)))
    card = Image.alpha_composite(card, edge_l)
    base.alpha_composite(card)
    return base


# ---------------- 马克笔笔触 ----------------
def marker_stroke(size, box, seed, color=MARKER):
    """马克笔涂色块：实心笔触 + 毛边 + 内部深浅刷痕"""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    hgt = y1 - y0
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    # 一整块笔触，不做层叠，避免出现横条边缘
    d.rounded_rectangle([x0, y0, x1, y1], radius=int(hgt * 0.42), fill=255)
    # 毛边：模糊后重新二值化，再啃掉小缺口
    m = m.filter(ImageFilter.GaussianBlur(2.6)).point(lambda v: 255 if v > 116 else 0)
    dd0 = ImageDraw.Draw(m)
    for _ in range(int((x1 - x0) / 7)):
        ex = rng.uniform(x0, x1)
        ey = rng.choice([y0 + rng.uniform(-1, 3), y1 + rng.uniform(-3, 1)])
        rr = rng.uniform(1.2, 4.2)
        dd0.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=0)
    m = m.filter(ImageFilter.GaussianBlur(1.2))

    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    layer.paste(Image.new("RGBA", size, color + (255,)), (0, 0), m)
    # 内部刷痕（淡，只在中间）
    d2 = ImageDraw.Draw(layer)
    for i in range(4):
        yy = y0 + hgt * (0.24 + 0.20 * i) + rng.uniform(-1.2, 1.2)
        d2.line([(x0 + rng.uniform(16, 44), yy), (x1 - rng.uniform(16, 44), yy + rng.uniform(-1, 1))],
                fill=(228, 172, 32, int(rng.integers(24, 44))), width=int(rng.integers(7, 12)))
    layer = layer.filter(ImageFilter.GaussianBlur(1.0))
    return layer


# ---------------- 小图标 ----------------
def icon_laptop(d, cx, cy, s, col):
    w, h = s * 1.16, s * 0.94
    # 屏幕
    d.rounded_rectangle([cx - w / 2, cy - h * 0.54, cx + w / 2, cy + h * 0.08],
                        radius=int(s * 0.10), outline=col, width=max(2, int(s * 0.12)))
    # 屏幕里的三行"代码"
    for i in range(3):
        yy = cy - h * 0.36 + i * h * 0.16
        d.line([(cx - w * 0.32, yy), (cx - w * 0.32 + w * (0.64 - 0.16 * i), yy)],
               fill=col, width=max(1, int(s * 0.055)))
    # 键盘底座（梯形）
    d.polygon([(cx - w * 0.58, cy + h * 0.22), (cx + w * 0.58, cy + h * 0.22),
               (cx + w * 0.44, cy + h * 0.40), (cx - w * 0.44, cy + h * 0.40)], fill=col)


def icon_gear(d, cx, cy, s, col):
    r_out = s * 0.40
    for i in range(8):
        a = math.pi * 2 * i / 8 + math.pi / 8
        x1, y1 = cx + math.cos(a) * r_out * 0.86, cy + math.sin(a) * r_out * 0.86
        x2, y2 = cx + math.cos(a) * r_out * 1.34, cy + math.sin(a) * r_out * 1.34
        d.line([(x1, y1), (x2, y2)], fill=col, width=max(2, int(s * 0.11)))
    d.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out], outline=col, width=max(3, int(s * 0.14)))
    r_h = s * 0.13
    d.ellipse([cx - r_h, cy - r_h, cx + r_h, cy + r_h], fill=col)


def icon_layers(d, cx, cy, s, col):
    w = s * 0.92
    for i, dy in enumerate((-s * 0.30, 0, s * 0.30)):
        pts = [(cx, cy + dy - s * 0.16), (cx + w / 2, cy + dy), (cx, cy + dy + s * 0.16), (cx - w / 2, cy + dy)]
        if i == 2:
            d.polygon(pts, fill=col)
        else:
            d.line(pts + [pts[0]], fill=col, width=max(2, int(s * 0.11)), joint="curve")


def icon_target(d, cx, cy, s, col, col2):
    for r, c, wd in ((s * 0.44, col, 0), (s * 0.30, col2, 0), (s * 0.16, col, 0)):
        if wd == 0 and r == s * 0.16:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
        else:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=max(2, int(s * 0.10)))


def rot_paste(base, layer, center, angle):
    r = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    x = int(center[0] - r.width / 2)
    y = int(center[1] - r.height / 2)
    base.alpha_composite(r, (x, y))


# ---------------- 贴纸 ----------------
def sticker_laptop(size=120):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([9, 9, size - 9, size - 9], radius=24, fill=(43, 106, 220, 255),
                        outline=(255, 255, 255, 255), width=5)
    d.text((size / 2, size * 0.44), "</>", font=font("C:/Windows/Fonts/consolab.ttf", 38),
           fill=(255, 255, 255), anchor="mm")
    d.text((size / 2, size * 0.72), CFG.get("sticker_label", "JAVA"), font=font(F_B, 17), fill=(206, 222, 255), anchor="mm")
    return img


def sticker_books(size=120):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    specs = [((16, size - 40, size - 20, size - 18), (67, 133, 226)),
             ((20, size - 62, size - 26, size - 42), (245, 176, 65)),
             ((24, size - 84, size - 32, size - 64), (235, 106, 96))]
    for box, col in specs:
        d.rounded_rectangle(box, radius=6, fill=col + (255,), outline=(255, 255, 255, 200), width=2)
        d.line([box[2] - 14, box[1] + 4, box[2] - 14, box[3] - 4], fill=(255, 255, 255, 180), width=3)
    return img


def corner_cloth(w, h):
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = [(-10, h + 10), (-10, h - 66), (16, h - 44), (40, h - 54), (68, h + 10)]
    d.polygon(pts, fill=(43, 106, 220, 255))
    d.line([(-10, h - 66), (16, h - 44), (40, h - 54), (68, h + 10)], fill=(255, 255, 255, 90), width=3)
    d.line([(2, h - 30), (30, h - 12)], fill=(255, 255, 255, 55), width=5)
    return layer


def arrow_deco(d, cx, cy, col, n=3, ang=0.0):
    for i in range(n):
        a = -0.5 + i * 0.5
        L = 9 + i * 2
        x1, y1 = cx + math.cos(a) * 6, cy + math.sin(a) * 6
        x2, y2 = cx + math.cos(a) * (6 + L), cy + math.sin(a) * (6 + L)
        d.line([(x1, y1), (x2, y2)], fill=col, width=3)


# ---------------- 主流程 ----------------
def build():
    base = paper_bg(W, H).convert("RGBA")
    base = white_card(base, (20, 84, 880, 428), 21)
    d = ImageDraw.Draw(base)

    # 标题笔触 + 标题
    stroke = marker_stroke((W, H), (248, 14, 652, 76), 33)
    base.alpha_composite(stroke)
    d = ImageDraw.Draw(base)
    d.text((450, 45), CFG.get("title", "学习路径：从入门到进阶"), font=font(F_B, 31), fill=INK, anchor="mm")

    # 标题两侧装饰
    arrow_deco(d, 214, 47, ORANGE, 3)
    arrow_deco(d, 690, 45, ORANGE, 3)

    rot_paste(base, sticker_laptop(112), (82, 44), -11)
    rot_paste(base, sticker_books(112), (818, 46), 7)

    # 表头胶囊
    _hd = CFG.get("heads", ["学习阶段", "主要内容", "实际目标"])
    heads = [(_hd[0], BLUE, 152, 196), (_hd[1], ORANGE, 440, 340), (_hd[2], PURPLE, 749, 236)]
    fh = font(F_B, 18)
    for txt, col, cx, w in heads:
        d.rounded_rectangle([cx - w / 2, 104, cx + w / 2, 140], radius=18, fill=col)
        d.text((cx, 122), txt, font=fh, fill=(255, 255, 255), anchor="mm")

    _rows = CFG.get("rows", [
        ["第一阶段", "认识赛项 · 读官方文档 · 报名八步", "知道考什么、按时报名"],
        ["第二阶段", "环境搭建 · 三天过完真题 · 定计划", "心里有底、建好题库"],
        ["第三阶段", "Java 基础 · 填空策略 · 暴力解题", "目标省一"],
        ["第四阶段", "算法专题 · 真题实战 · 4 小时时间轴", "冲国奖"],
    ])
    rows = [(a, b, c, ic) for (a, b, c), ic in zip(_rows, [icon_laptop, icon_gear, icon_layers, icon_target])]
    ys = [188, 252, 316, 380]
    f_stage = font(F_B, 20)
    f_sub = font(F_R, 17)
    f_goal = font(F_B, 15)

    # 行间虚线
    for y in (220, 284, 348):
        for x in range(58, 862, 13):
            d.line([(x, y), (x + 7, y)], fill=(198, 188, 170, 190), width=2)

    for (stage, content, goal, icon), cy in zip(rows, ys):
        d.rounded_rectangle([62, cy - 22, 106, cy + 22], radius=11, fill=YELLOW)
        d.rounded_rectangle([62, cy - 22, 106, cy + 22], radius=11, outline=(240, 208, 130), width=2)
        if icon is icon_target:
            icon(d, 84, cy, 20, YELLOW_D, (255, 255, 255))
        else:
            icon(d, 84, cy, 20, YELLOW_D)

        d.text((120, cy), stage, font=f_stage, fill=INK, anchor="lm")

        fc = fit_font(d, content, 318, 17, F_R)
        d.text((274, cy), content, font=fc, fill=INK_SOFT, anchor="lm")

        gw = max(116, tw(d, goal, f_goal) + 46)
        d.rounded_rectangle([749 - gw / 2, cy - 17, 749 + gw / 2, cy + 17], radius=17, fill=LILAC)
        d.text((749, cy), goal, font=f_goal, fill=NAVY, anchor="mm")

    base.alpha_composite(corner_cloth(W, H))
    # 右下靶心（飞镖从左上扎进中心）
    tgt = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    td = ImageDraw.Draw(tgt)
    icon_target(td, 50, 50, 40, (232, 88, 62), (255, 255, 255))
    td.line([(14, 86), (46, 54)], fill=(112, 88, 58), width=3)
    td.polygon([(48, 52), (36, 56), (44, 64)], fill=(112, 88, 58))
    rot_paste(base, tgt, (844, 398), 8)

    return base.convert("RGB")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    img = build()
    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    p = out or os.path.join(OUT, CFG.get("filename", "风格二-纸质学习路径-Java组-900x450.png"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p)
    print("saved", p, img.size)
