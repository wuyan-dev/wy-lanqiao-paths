# -*- coding: utf-8 -*-
"""风格一：蓝色科技商业海报（参照 微信图片_202611222259_1/2/3/5）—— 智能体开发课程
亮蓝径向渐变 + 网格光斑 + 城市天际线 + 居中大标题 + 彩色胶囊标签 + 白色数据卡 + 底部卖点条
"""
import math, os, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 608
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
CFG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content.json")
try:
    CFG = json.load(open(CFG_PATH, encoding="utf-8"))
except Exception:
    CFG = {}
F_B = "C:/Windows/Fonts/msyhbd.ttc"
F_R = "C:/Windows/Fonts/msyh.ttc"

WHITE = (255, 255, 255)
YELLOW = (255, 210, 63)
CYAN = (86, 214, 255)
INKBLUE = (9, 40, 104)
DEEP = (7, 32, 84)
CARD = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, t, f):
    return d.textlength(t, font=f)


def fit(d, t, maxw, start, path=F_B, mins=9):
    s = start
    while s > mins and tw(d, t, font(path, s)) > maxw:
        s -= 1
    return font(path, s)


# ---------------- 背景 ----------------
def background(w, h):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    d = np.sqrt(((xx - w * 0.54) / (w * 0.92)) ** 2 + ((yy - h * 0.40) / (h * 1.05)) ** 2)
    t = np.clip(d, 0, 1) ** 1.10
    center = np.array([64, 152, 255], dtype=np.float64)
    edge = np.array([5, 33, 100], dtype=np.float64)
    arr = np.zeros((h, w, 3), dtype=np.float64)
    for c in range(3):
        arr[:, :, c] = center[c] + (edge[c] - center[c]) * t

    # 斜向光带
    band = np.exp(-(((xx * 0.55 + yy * 0.45) - w * 0.62) ** 2) / (2 * (w * 0.30) ** 2))
    arr += band[:, :, None] * np.array([26, 44, 62])

    # 网格
    grid = np.zeros((h, w))
    gx = (xx % 44) < 1.0
    gy = (yy % 44) < 1.0
    grid[gx | gy] = 1.0
    arr += grid[:, :, None] * 13

    img = Image.fromarray(np.uint8(np.clip(arr, 0, 255)))

    # 光斑
    rng = np.random.default_rng(9)
    bokeh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bokeh)
    for _ in range(16):
        cx, cy = rng.uniform(0, w), rng.uniform(0, h * 0.75)
        r = rng.uniform(18, 90)
        a = int(rng.uniform(8, 26))
        bd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(180, 225, 255, a))
    img = Image.alpha_composite(img.convert("RGBA"), bokeh.filter(ImageFilter.GaussianBlur(14)))

    # 星点
    st = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    for _ in range(150):
        x, y = rng.uniform(0, w), rng.uniform(0, h * 0.72)
        s = rng.uniform(0.6, 1.9)
        a = int(rng.uniform(20, 120))
        sd.ellipse([x, y, x + s, y + s], fill=(255, 255, 255, a))
    img = Image.alpha_composite(img, st.filter(ImageFilter.GaussianBlur(0.4)))

    # 城市天际线
    sky = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    kd = ImageDraw.Draw(sky)
    base_y = int(h * 0.78)
    x = -10
    while x < w:
        bw = int(rng.uniform(24, 62))
        bh = int(rng.uniform(24, 96))
        col = (7, 34, 88, 210)
        kd.rectangle([x, base_y - bh, x + bw, base_y + 60], fill=col)
        # 窗
        for wy in range(base_y - bh + 8, base_y, 14):
            for wx in range(x + 6, x + bw - 6, 12):
                if rng.random() < 0.30:
                    kd.rectangle([wx, wy, wx + 4, wy + 5], fill=(120, 200, 255, 70))
        x += bw + int(rng.uniform(2, 8))
    img = Image.alpha_composite(img, sky)

    # 底部压暗
    dark = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dark)
    for i in range(70):
        y = h - 70 + i
        dd.line([(0, y), (w, y)], fill=(3, 20, 58, int(i * 1.6)))
    img = Image.alpha_composite(img, dark)
    return img.convert("RGB")


# ---------------- 元素 ----------------
def pill(d, box, fill, text, f, tcol=WHITE, outline=None, ow=0):
    d.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=outline, width=ow)
    d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), text, font=f, fill=tcol, anchor="mm")


def node(d, box, label, f):
    d.rounded_rectangle(box, radius=10, fill=(14, 74, 168, 255), outline=CYAN + (190,), width=2)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    d.text((cx, cy), label, font=f, fill=WHITE, anchor="mm")


def arrow(d, p1, p2, col=CYAN, wd=3):
    d.line([p1, p2], fill=col + (220,), width=wd)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    L = 9
    for s in (-0.45, 0.45):
        d.line([p2, (p2[0] - L * math.cos(ang - s), p2[1] - L * math.sin(ang - s))], fill=col + (220,), width=wd)


def glow_text(img, xy, text, f, fill, stroke=None, sw=0, glow=22, anchor="ma"):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text(xy, text, font=f, fill=fill, anchor=anchor, stroke_width=sw,
            stroke_fill=stroke if stroke else None)
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).text(xy, text, font=f, fill=fill[:3] + (110,), anchor=anchor, stroke_width=sw,
                               stroke_fill=(stroke[:3] + (90,)) if stroke else None)
        layer = Image.alpha_composite(g.filter(ImageFilter.GaussianBlur(glow)), layer)
    return Image.alpha_composite(img.convert("RGBA"), layer)


# ---------------- 主流程 ----------------
def build():
    img = background(W, H).convert("RGBA")
    d = ImageDraw.Draw(img)

    # logo
    lx, ly, ls = 30, 22, 54
    for i in range(ls):
        t = i / ls
        d.line([(lx, ly + i), (lx + ls, ly + i)],
               fill=(int(60 + 60 * (1 - t)), int(206 - 40 * t), int(238 - 20 * t), 255))
    d.rounded_rectangle([lx, ly, lx + ls, ly + ls], radius=15, outline=(255, 255, 255, 170), width=2)
    d.text((lx + ls / 2, ly + ls / 2 - 1), "梧", font=font(F_B, 30), fill=WHITE, anchor="mm")

    d.text((lx + ls + 14, ly + 8), CFG.get("brand", "梧焰"), font=font(F_B, 18), fill=WHITE, anchor="la")
    d.text((lx + ls + 14, ly + 32), CFG.get("brand_sub", "课程主讲 · 智能体开发"), font=font(F_R, 14), fill=(186, 220, 255), anchor="la")

    # 右上角标：仅放中性课程信息，不放赛事 / 官方名称；留空则完全不绘制
    badge = CFG.get("badge", "7 节实战课")
    if badge:
        d.text((W - 30, ly + 10), badge, font=font(F_R, 14), fill=(200, 226, 255), anchor="ra")

    # 主标题（居中）—— 两行之间留足行距，副标再往下，避免压字
    f_main = font(F_B, 68)
    img = glow_text(img, (W / 2, 78), CFG.get("title", "智能体开发"), f_main, WHITE, stroke=(8, 34, 92), sw=4, glow=16)
    d = ImageDraw.Draw(img)
    # 黄字：先白边再黄字
    img = glow_text(img, (W / 2, 150), CFG.get("highlight", "从 0 到国奖"), f_main, WHITE, stroke=(255, 255, 255), sw=8, glow=0)
    d = ImageDraw.Draw(img)
    d.text((W / 2, 150), CFG.get("highlight", "从 0 到国奖"), font=f_main, fill=YELLOW, anchor="ma", stroke_width=1, stroke_fill=(255, 255, 255))

    # 副标（黄字含描边底约 228，此处 244 起，留 16px 呼吸）
    d.text((W / 2, 244), CFG.get("subtitle", "蓝桥杯赛事 · 十七届 / 十八届样题各跑一遍　·　7 节完整路径"), font=font(F_R, 18),
           fill=(206, 230, 255), anchor="ma")

    # 彩色胶囊一排
    tags = [(t, c) for t, c in zip(CFG.get("tags", ["AI 工作流", "MCP 工具", "知识库", "Prompt 工程", "提交清单"]), [(255, 149, 66), (46, 196, 168), (122, 132, 255), (236, 96, 152), (52, 152, 255)])]
    ftag = font(F_B, 15)
    widths = [tw(d, t, ftag) + 40 for t, _ in tags]
    gap = 10
    total = sum(widths) + gap * (len(tags) - 1)
    x = (W - total) / 2
    for (t, col), wd in zip(tags, widths):
        d.rounded_rectangle([x, 280, x + wd, 306], radius=13, fill=col + (255,))
        d.text((x + wd / 2, 293), t, font=ftag, fill=WHITE, anchor="mm")
        x += wd + gap

    # 左侧：工作流主视觉（压缩高度，整卡落在底部卖点条之上）
    card = Image.new("RGBA", (470, 188), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, 469, 187], radius=18, fill=(8, 44, 122, 215), outline=(120, 206, 255, 120), width=2)
    cd.text((20, 12), CFG.get("flow_title", "一条可复用的工作流"), font=font(F_B, 16), fill=(190, 226, 255), anchor="la")
    fn = font(F_B, 15)
    boxes = {
        "in":  (22, 44, 152, 92),
        "cls": (172, 44, 302, 92),
        "kb":  (322, 44, 452, 92),
        "score": (322, 118, 452, 166),
        "out": (172, 118, 302, 166),
    }
    _fn = CFG.get("flow_nodes", ["输入", "分类", "知识库", "评分", "落表"])
    labels = dict(zip(["in", "cls", "kb", "score", "out"], _fn))
    for k, b in boxes.items():
        node(cd, b, labels[k], fn)
    arrow(cd, (154, 68), (170, 68))
    arrow(cd, (304, 68), (320, 68))
    arrow(cd, (387, 94), (387, 116))
    arrow(cd, (320, 142), (304, 142))
    # 收尾小圆点
    cd.ellipse([22, 44, 28, 50], fill=(120, 226, 255, 255))
    img.alpha_composite(card, (40, 326))
    d = ImageDraw.Draw(img)

    # 右侧 2x2 数据卡
    _st = CFG.get("stats", [["省一 · 国三", "亲历两个赛项"], ["17 / 18 届", "样题各跑一遍"], ["110 分", "评分五档拆解"], ["5 件", "提交物清单"]])
    stats = [(a, b, c) for (a, b), c in zip(_st, [(255, 149, 66), (56, 200, 172), (128, 138, 255), (70, 162, 255)])]
    cw, ch = 248, 90
    for i, (big, sub, col) in enumerate(stats):
        cx = 534 + (i % 2) * (cw + 10)
        cy = 326 + (i // 2) * (ch + 8)
        # 投影
        sh = Image.new("RGBA", (w0 := 300, 130), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([6, 8, cw + 6, ch + 8], radius=16, fill=(2, 20, 58, 90))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (cx - 6, cy - 8))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=15, fill=CARD + (246,))
        # 顶部彩条（裁在圆角内）
        bar = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bar)
        bd.rounded_rectangle([0, 0, cw, ch], radius=15, fill=(0, 0, 0, 0))
        bd.rectangle([0, 0, cw, 7], fill=col + (255,))
        mask = Image.new("L", (cw, ch), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=15, fill=255)
        bar.putalpha(Image.composite(bar.split()[3], Image.new("L", (cw, ch), 0), mask))
        img.alpha_composite(bar, (cx, cy))
        d = ImageDraw.Draw(img)
        d.text((cx + cw / 2, cy + 37), big, font=font(F_B, 32), fill=INKBLUE, anchor="mm")
        d.text((cx + cw / 2, cy + 69), sub, font=font(F_R, 14), fill=(96, 112, 138), anchor="mm")

    # 底部卖点条
    bar_y = 540
    d.rectangle([0, bar_y, W, H], fill=DEEP + (255,))
    d.line([(0, bar_y), (W, bar_y)], fill=(110, 190, 255, 90), width=2)
    items = CFG.get("footer", ["7 节体系", "双届样题", "评分拆解", "提交清单", "亲历复盘", "可复用模板"])
    n = len(items)
    seg = W / n
    fbar = font(F_B, 16)
    for i, t in enumerate(items):
        cx = seg * (i + 0.5)
        # 小图标：圆环 + 点
        d.ellipse([cx - 60, bar_y + 14, cx - 34, bar_y + 40], outline=CYAN + (230,), width=3)
        d.ellipse([cx - 51, bar_y + 23, cx - 43, bar_y + 31], fill=CYAN + (230,))
        d.text((cx + 8, bar_y + 27), t, font=fbar, fill=WHITE, anchor="mm")
        if i:
            d.line([(seg * i, bar_y + 10), (seg * i, bar_y + 48)], fill=(255, 255, 255, 34), width=1)

    return img.convert("RGB")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    im = build()
    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    p = out or os.path.join(OUT, CFG.get("filename", "风格一-蓝色科技-智能体开发-1080x608.png"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    im.save(p)
    print("saved", p, im.size)
