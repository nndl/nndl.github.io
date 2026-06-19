#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate / adjust the viz card thumbnails (assets/viz/<slug>.svg, 320x200).

The cards on viz/index.md auto-use `/assets/viz/<slug>.svg` whenever a card
passes no explicit `thumb=` (see _includes/viz-card.html). This script is the
home for those hand-drawn SVG thumbnails: a tiny style toolkit (site palette +
primitives, matching the existing assets/viz/*.svg) plus one draw function per
slug.

Usage
-----
  python scripts/gen-viz-thumbs.py --all                 # (re)generate every registered thumbnail
  python scripts/gen-viz-thumbs.py --only lstm-gates,adaboost
  python scripts/gen-viz-thumbs.py --list                # list registered thumbnails
  python scripts/gen-viz-thumbs.py --missing             # cards that need an auto-svg but have no file
  python scripts/gen-viz-thumbs.py --check               # validate registered SVGs (well-formed + in-bounds); no write
  python scripts/gen-viz-thumbs.py --preview [a,b,...]    # rasterize to one PNG montage to eyeball (Edge/Chrome + Pillow)

Add a new thumbnail
-------------------
  1. write a draw function returning svg(...) with the helpers below, e.g.

         def _t_my_slug():
             b = []
             b.append(rect(40, 40, 60, 40, TEALF, TEAL, rx=8))
             b.append(text(70, 65, "示例", 13, TEAL))
             return svg("".join(b))

  2. register it:  THUMBS["my-slug"] = _t_my_slug
  3. run:          python scripts/gen-viz-thumbs.py --only my-slug --preview my-slug

Conventions: viewBox 0 0 320 200, site palette hardcoded (SVG loaded as <img>
can't read CSS vars), plain primitives, Chinese text uses curly quotes.
"""
import argparse
import math
import os
import re
import sys
import xml.dom.minidom as minidom

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "assets", "viz")
INDEX = os.path.join(REPO, "viz", "index.md")

FONT = "-apple-system,Segoe UI,PingFang SC,Microsoft YaHei,sans-serif"
# Site palette (kept in sync with assets/css/style.css variables, hardcoded here).
TEAL = "#155e75"; TEALF = "#e4edf0"; GOLD = "#b7791f"; BLUE = "#2563eb"; RED = "#b5524a"
FOREST = "#266a4f"; INK = "#2a3b36"; AXIS = "#9aa3a8"; EDGE = "#b9c2c7"

# ---------------------------------------------------------------- primitives

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def n(v):
    return f"{round(v, 1):g}"

def rect(x, y, w, h, fill, stroke=None, sw=1.2, rx=0, op=1):
    s = f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if op != 1:
        s += f' opacity="{op}"'
    return s + "/>"

def line(x1, y1, x2, y2, stroke, sw=2, dash=None, cap=None, op=1):
    s = f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        s += f' stroke-dasharray="{dash}"'
    if cap:
        s += f' stroke-linecap="{cap}"'
    if op != 1:
        s += f' opacity="{op}"'
    return s + "/>"

def circ(cx, cy, r, fill, stroke="#fff", sw=2, op=1):
    s = f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if op != 1:
        s += f' opacity="{op}"'
    return s + "/>"

def text(x, y, s, size=13, fill=INK, weight=600, anchor="middle"):
    return (f'<text x="{n(x)}" y="{n(y)}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(s)}</text>')

def poly(pts, stroke, sw=2.5, fill="none", op=1, dash=None):
    p = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
    s = (f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
         f'stroke-linecap="round" stroke-linejoin="round"')
    if dash:
        s += f' stroke-dasharray="{dash}"'
    if op != 1:
        s += f' opacity="{op}"'
    return s + "/>"

def arrow(x1, y1, x2, y2, color, sw=2.4, head=7):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx = x2 - head * 0.9 * math.cos(ang)
    by = y2 - head * 0.9 * math.sin(ang)
    shaft = line(x1, y1, bx, by, color, sw, cap="round")
    a1 = ang + math.radians(150)
    a2 = ang - math.radians(150)
    p1 = (x2 + head * math.cos(a1), y2 + head * math.sin(a1))
    p2 = (x2 + head * math.cos(a2), y2 + head * math.sin(a2))
    hp = (f'<polygon points="{n(x2)},{n(y2)} {n(p1[0])},{n(p1[1])} '
          f'{n(p2[0])},{n(p2[1])}" fill="{color}"/>')
    return shaft + hp

def svg(body, bg="#f6f8f7"):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="320" height="200">'
            f'<rect width="320" height="200" fill="{bg}"/>' + body + "</svg>")

# ---------------------------------------------------------------- thumbnails

def _t_rnn_unroll():
    b = []; xs = [30, 102, 174, 246]; w = 48; h = 38; y = 82
    for x in xs:
        cx = x + w / 2
        b.append(rect(cx - 13, 150, 26, 18, BLUE, op=0.85, rx=3))
        b.append(arrow(cx, 148, cx, y + h + 3, BLUE, 2))
        b.append(arrow(cx, y - 2, cx, 60, TEAL, 2))
        b.append(circ(cx, 52, 7, TEALF, TEAL, 1.6))
    for i in range(len(xs) - 1):
        b.append(arrow(xs[i] + w + 2, y + h / 2, xs[i + 1] - 2, y + h / 2, GOLD, 3))
    for x in xs:
        b.append(rect(x, y, w, h, TEALF, TEAL, 1.4, rx=8))
        b.append(text(x + w / 2, y + 24, "RNN", 13, TEAL))
    b.append(text((xs[0] + w + xs[1]) / 2, y + h / 2 - 7, "h", 12, GOLD, 700))
    b.append(text(160, 189, "同一套权重，沿时间展开 →", 11, AXIS))
    return svg("".join(b))

def _t_rnn_counter():
    b = []; toks = ["(", "(", ")", "(", ")", ")"]; xs = [55, 99, 143, 187, 231, 275]
    y0 = 160; dy = 38
    yc = lambda c: y0 - c * dy
    for c in range(3):
        b.append(line(40, yc(c), 300, yc(c), EDGE, 1, dash="4 4"))
        b.append(text(28, yc(c) + 4, str(c), 11, AXIS))
    for x, t in zip(xs, toks):
        b.append(text(x, 42, t, 20, TEAL if t == "(" else GOLD, 700))
    c = 0; pts = [(40, yc(0))]
    for x, t in zip(xs, toks):
        pts.append((x, yc(c))); c += 1 if t == "(" else -1; pts.append((x, yc(c)))
    pts.append((300, yc(c)))
    b.append(poly(pts, TEAL, 3))
    c = 0
    for x, t in zip(xs, toks):
        c += 1 if t == "(" else -1
        b.append(circ(x, yc(c), 4, GOLD, "#fff", 1.2))
    b.append(text(170, 190, "某个隐状态神经元 = 括号深度", 11, AXIS))
    return svg("".join(b))

def _t_bptt_vanishing():
    b = []; x0, x1 = 40, 300; yb = 170; yt = 40; N = 22
    b.append(line(x0, yb, x1, yb, AXIS, 1)); b.append(line(x0, yt, x0, yb, AXIS, 1))
    rng = yb - yt - 6; dec = []; exp = []
    for k in range(N + 1):
        x = x0 + (x1 - x0) * k / N
        vd = 0.74 ** k; dec.append((x, yb - vd * rng))
        ve = 1.23 ** k; exp.append((x, yb - min((ve - 1) * 8.5, rng)))
    b.append(poly(dec, BLUE, 2.6)); b.append(poly(exp, RED, 3))
    b.append(text(296, 52, "爆炸 wᵏ↑", 11, RED, 700, anchor="end"))
    b.append(text(296, 162, "消失 wᵏ→0", 11, BLUE, 700, anchor="end"))
    b.append(text(170, 192, "误差沿时间回传 →", 11, AXIS))
    return svg("".join(b))

def _t_lstm_gates():
    b = []
    b.append(rect(22, 78, 276, 34, "#eef4f5", TEAL, 1.6, rx=16))
    b.append(arrow(36, 95, 284, 95, GOLD, 2.6, head=8))
    b.append(circ(62, 95, 11, GOLD, "#fff", 1.8)); b.append(text(62, 99, "c", 12, "#fff", 700))
    for gx, lab, col, zh in [(96, "f", GOLD, "遗忘"), (168, "i", BLUE, "输入"), (240, "o", TEAL, "输出")]:
        b.append(line(gx, 135, gx, 112, EDGE, 1.4))
        b.append(circ(gx, 150, 15, col, "#fff", 2)); b.append(text(gx, 155, lab, 14, "#fff", 700))
        b.append(text(gx, 182, zh, 11, INK))
    b.append(text(30, 70, "cₜ₋₁", 10, AXIS, 600, anchor="start"))
    b.append(text(290, 70, "cₜ 记忆传送带", 10, AXIS, 600, anchor="end"))
    return svg("".join(b))

def _t_bidirectional_rnn():
    b = []; toks = ["我", "买", "苹果", "手机"]; xs = [40, 108, 176, 244]; w = 52; h = 34; y = 84
    cen = [x + w / 2 for x in xs]; fy = 54; by = 150
    for cx in cen: b.append(line(cx, y - 2, cx, fy + 9, EDGE, 1.2))
    for cx in cen: b.append(line(cx, y + h + 2, cx, by - 9, EDGE, 1.2))
    for i in range(len(cen) - 1): b.append(arrow(cen[i] + 9, fy, cen[i + 1] - 9, fy, BLUE, 2))
    for i in range(len(cen) - 1): b.append(arrow(cen[i + 1] - 9, by, cen[i] + 9, by, GOLD, 2))
    for cx in cen: b.append(circ(cx, fy, 9, BLUE, "#fff", 1.8))
    for cx in cen: b.append(circ(cx, by, 9, GOLD, "#fff", 1.8))
    for x, t in zip(xs, toks):
        b.append(rect(x, y, w, h, TEALF, TEAL, 1.4, rx=8))
        b.append(text(x + w / 2, y + 22, t, 13 if len(t) == 1 else 12, TEAL, 700))
    b.append(text(20, fy + 4, "→", 14, BLUE, 700)); b.append(text(20, by + 4, "←", 14, GOLD, 700))
    return svg("".join(b))

def _t_char_rnn():
    b = []; tiles = ["q", "u", "i"]; tx = [28, 72, 116]; w = 40; h = 46; y = 70
    for i, (x, t) in enumerate(zip(tx, tiles)):
        fill = TEALF if i < 2 else "#f0e9da"; st = TEAL if i < 2 else GOLD
        b.append(rect(x, y, w, h, fill, st, 1.4, rx=8)); b.append(text(x + w / 2, y + 30, t, 22, st, 700))
    b.append(arrow(162, y + h / 2, 176, y + h / 2, AXIS, 2))
    labels = ["u", "e", "o", "i", "a"]; hs = [64, 30, 22, 16, 12]; bx = 180; bw = 18; step = 26; base = 150
    for i, (lb, hgt) in enumerate(zip(labels, hs)):
        x = bx + i * step; col = GOLD if i == 0 else TEAL; op = 1 if i == 0 else 0.5
        b.append(rect(x, base - hgt, bw, hgt, col, op=op, rx=2)); b.append(text(x + bw / 2, base + 14, lb, 12, INK))
    b.append(text(180, 66, "下一字符概率", 11, AXIS, 600, anchor="start"))
    return svg("".join(b))

def _t_hmm_viterbi():
    b = []; cols = [52, 108, 164, 220, 276]; rows = {"晴": 74, "雨": 132}
    path = ["晴", "晴", "雨", "雨", "晴"]
    for i in range(len(cols) - 1):
        for r1 in rows.values():
            for r2 in rows.values():
                b.append(line(cols[i] + 11, r1, cols[i + 1] - 11, r2, EDGE, 1, op=0.7))
    b.append(poly([(cols[i], rows[path[i]]) for i in range(5)], TEAL, 3))
    for i, x in enumerate(cols):
        for name, ry in rows.items():
            on = path[i] == name
            b.append(circ(x, ry, 11, TEAL if on else "#fff", TEAL if on else AXIS, 2 if on else 1.4))
    b.append(text(26, 78, "晴", 12, GOLD, 700)); b.append(text(26, 136, "雨", 12, BLUE, 700))
    for i, x in enumerate(cols):
        filled = i in (1, 2, 4)
        b.append(rect(x - 6, 172, 12, 12, BLUE if filled else "#dfe6e3", None, rx=2))
    b.append(text(160, 196, "观测：带伞□ / 没带", 10, AXIS))
    return svg("".join(b))

def _t_gcn_node_classification():
    b = []
    blue = [(58, 66), (92, 108), (48, 140), (104, 56), (120, 150)]
    red = [(262, 66), (228, 108), (272, 140), (216, 56), (200, 150)]
    mid = [(160, 84), (160, 128)]
    edges = [(0, 3), (0, 1), (1, 2), (2, 4), (1, 4), (3, 1)]
    for a, c in edges: b.append(line(blue[a][0], blue[a][1], blue[c][0], blue[c][1], EDGE, 1.6))
    for a, c in edges: b.append(line(red[a][0], red[a][1], red[c][0], red[c][1], EDGE, 1.6))
    b.append(line(120, 150, 160, 128, EDGE, 1.6)); b.append(line(104, 56, 160, 84, EDGE, 1.6))
    b.append(line(160, 84, 160, 128, EDGE, 1.6))
    b.append(line(160, 84, 216, 56, EDGE, 1.6)); b.append(line(160, 128, 200, 150, EDGE, 1.6))
    for x, y in mid: b.append(circ(x, y, 13, "#e9eef0", AXIS, 1.6))
    for x, y in blue: b.append(circ(x, y, 13, BLUE, "#fff", 2))
    for x, y in red: b.append(circ(x, y, 13, RED, "#fff", 2))
    b.append(circ(58, 66, 17, "none", GOLD, 2.8)); b.append(circ(262, 66, 17, "none", GOLD, 2.8))
    b.append(text(58, 40, "标注", 10, GOLD, 700)); b.append(text(262, 40, "标注", 10, GOLD, 700))
    return svg("".join(b), bg="#f4f1ec")

def _t_adaboost():
    b = []
    stairs = [(44, 40), (44, 72), (96, 72), (96, 104), (160, 104), (160, 136), (224, 136), (224, 168), (288, 168)]
    for x in (96, 160, 224): b.append(line(x, 28, x, 182, EDGE, 1.2, dash="5 4"))
    for y in (72, 104, 136): b.append(line(38, y, 294, y, EDGE, 1.2, dash="5 4"))
    b.append(poly(stairs, TEAL, 3))
    blue = [(64, 44), (58, 66), (92, 52), (120, 80), (140, 96), (80, 58), (150, 92)]
    red = [(182, 150), (206, 160), (214, 150), (178, 168), (204, 166), (190, 150), (220, 158)]
    for x, y in blue: b.append(circ(x, y, 6, BLUE, "#fff", 1.5))
    for x, y in red: b.append(circ(x, y, 6, RED, "#fff", 1.5))
    b.append(text(70, 182, "弱分类器拼出阶梯边界", 10, AXIS, 600, anchor="start"))
    return svg("".join(b))

def _t_rbm_reconstruction():
    b = []; vis = [60, 98, 136, 174, 212, 250]; vy = 150; hid = [100, 160, 220]; hy = 68
    for hx in hid:
        for vx in vis: b.append(line(hx, hy + 13, vx, vy - 11, EDGE, 1, op=0.65))
    b.append(arrow(284, 148, 284, 82, FOREST, 2.4, head=8)); b.append(text(300, 118, "编", 10, FOREST, 600))
    b.append(arrow(26, 82, 26, 148, GOLD, 2.4, head=8)); b.append(text(12, 118, "构", 10, GOLD, 600))
    noisy = [1, 0, 1, 0, 0, 1]
    for i, vx in enumerate(vis):
        b.append(rect(vx - 11, vy - 11, 22, 22, INK if noisy[i] else "#dfe6e3", TEAL, 1.4, rx=4))
    for hx in hid: b.append(circ(hx, hy, 15, TEAL, "#fff", 2))
    b.append(text(160, 32, "隐单元（特征）", 11, TEAL, 600))
    b.append(text(160, 190, "可见单元（含噪输入）", 11, INK, 600))
    return svg("".join(b))

def _t_llm_internals():
    b = []
    b.append(text(160, 26, "词元逐层流过 Transformer", 11, TEAL, 600))
    # input token
    b.append(rect(14, 84, 28, 30, TEALF, TEAL, 1.4, rx=6)); b.append(text(28, 104, "词", 13, TEAL, 700))
    b.append(arrow(44, 99, 52, 99, AXIS, 1.8))
    # embedding vector (a small tensor column)
    ex = 54
    for i in range(4):
        b.append(rect(ex, 78 + i * 12, 16, 11, BLUE, op=0.78, rx=2))
    b.append(text(ex + 8, 140, "嵌入", 10, AXIS))
    b.append(arrow(72, 99, 92, 99, AXIS, 1.8))
    # transformer layers: 3 cards (slight 3D shadow) with a residual stream along the top
    xs = [94, 148, 202]; cw = 40; cy = 66; chh = 66
    b.append(line(xs[0] + cw / 2, 52, xs[-1] + cw / 2, 52, GOLD, 2.4, cap="round"))
    for x in xs:
        cx = x + cw / 2
        b.append(line(cx, 52, cx, cy, GOLD, 1.6)); b.append(circ(cx, 52, 4, GOLD, "#fff", 1.4))
    for x in xs:
        b.append(rect(x + 4, cy + 4, cw, chh, "#e7edef", None, rx=7))
        b.append(rect(x, cy, cw, chh, "#ffffff", TEAL, 1.5, rx=7))
        b.append(rect(x + 6, cy + 10, cw - 12, 20, TEAL, None, rx=4, op=0.20))
        b.append(text(x + cw / 2, cy + 24, "注意力", 9, TEAL, 700))
        b.append(rect(x + 6, cy + 36, cw - 12, 20, GOLD, None, rx=4, op=0.22))
        b.append(text(x + cw / 2, cy + 50, "MLP", 9, GOLD, 700))
    for i in range(len(xs) - 1):
        b.append(arrow(xs[i] + cw + 2, cy + chh / 2, xs[i + 1] - 2, cy + chh / 2, AXIS, 1.8))
    b.append(text(168, 150, "注意力 + MLP + 残差", 10, AXIS))
    # next-token logits
    b.append(arrow(xs[-1] + cw + 2, 99, xs[-1] + cw + 14, 99, AXIS, 1.8))
    lx = xs[-1] + cw + 18; hs = [44, 26, 18, 12]; bw = 11; step = 13; base = 128
    for i, h in enumerate(hs):
        col = GOLD if i == 0 else TEAL; op = 1 if i == 0 else 0.5
        b.append(rect(lx + i * step, base - h, bw, h, col, op=op, rx=2))
    b.append(text(lx + 1.5 * step, 144, "logits", 10, AXIS))
    return svg("".join(b))

def _t_sparse_autoencoder():
    b = []
    inx, outx, hx = 46, 274, 160
    iny = [60, 90, 120, 150]
    hy = [34 + i * (142.0 / 11) for i in range(12)]
    active = [2, 6, 9]
    for hi in active:
        for yy in iny:
            b.append(line(inx + 9, yy + 8, hx - 6.5, hy[hi], TEAL, 1, op=0.22))
            b.append(line(hx + 6.5, hy[hi], outx - 9, yy + 8, TEAL, 1, op=0.22))
    for yy in iny:
        b.append(rect(inx - 9, yy, 18, 16, TEALF, TEAL, 1.4, rx=3))
        b.append(rect(outx - 9, yy, 18, 16, TEALF, TEAL, 1.4, rx=3))
    for i, yy in enumerate(hy):
        on = i in active
        b.append(circ(hx, yy, 6.5, TEAL if on else "#dfe3e6", "#fff" if on else AXIS, 2 if on else 1.2))
    b.append(text(103, 26, "编码", 10, AXIS))
    b.append(text(217, 26, "解码", 10, AXIS))
    b.append(text(inx, 180, "输入", 10, AXIS))
    b.append(text(outx, 180, "重构", 10, AXIS))
    b.append(text(hx, 196, "稀疏隐层（多数为 0）", 10, AXIS))
    return svg("".join(b))

def _t_l1_l2_geometry():
    b = []
    ox, oy = 70, 120          # origin on axes
    # axes
    b.append(line(ox, 178, ox, 28, AXIS, 1.4))
    b.append(line(40, oy, 300, oy, AXIS, 1.4))
    b.append(text(296, oy - 6, "w₁", 11, AXIS, 600, anchor="end"))
    b.append(text(ox + 12, 34, "w₂", 11, AXIS, 600, anchor="start"))
    # L2 unconstrained optimum w* (upper right)
    cx, cy = 196, 66
    import math
    # two pale-teal elliptical contours around w*
    for rad in (54, 34):
        pts = []
        for i in range(33):
            t = 2 * math.pi * i / 32
            pts.append((cx + rad * 1.25 * math.cos(t), cy + rad * 0.78 * math.sin(t)))
        b.append(poly(pts, TEAL, 1.8))
    b.append(circ(cx, cy, 3.5, TEAL, "#fff", 1.4))
    b.append(text(cx + 8, cy - 4, "w*", 11, TEAL, 700, anchor="start"))
    # L1 diamond constraint region (corners on axes)
    d = 50
    dia = [(ox + d, oy), (ox, oy - d), (ox - d, oy), (ox, oy + d), (ox + d, oy)]
    b.append(poly(dia, BLUE, 2.6, fill="#e8eefb"))
    b.append(text(ox - d + 4, oy + d - 8, "‖w‖₁≤t", 10, BLUE, 700, anchor="start"))
    # red solution at the right corner (on w₁ axis, w₂=0)
    sx, sy = ox + d, oy
    b.append(circ(sx, sy, 6, RED, "#fff", 2))
    # dashed drop to x-axis (already on axis: short tick label)
    b.append(line(sx, sy, sx, oy + 30, RED, 1.6, dash="4 4"))
    b.append(text(sx, oy + 44, "w₂=0", 10, RED, 700))
    b.append(text(160, 190, "L1 解顶尖角 → 稀疏", 11, AXIS))
    return svg("".join(b))

def _t_eigenvectors():
    b = []
    ox, oy = 110, 140
    # eigenvector direction: green dashed line through origin
    dx, dy = 0.80, -0.60
    b.append(line(ox - dx * 110, oy - dy * 110, ox + dx * 130, oy + dy * 130, FOREST, 2.2, dash="6 5"))
    # origin dot
    b.append(circ(ox, oy, 4, INK, "#fff", 1.5))
    # v (teal) and Av (gold) from origin, slightly different directions
    b.append(arrow(ox, oy, ox + 70, oy - 30, TEAL, 3, head=9))
    b.append(arrow(ox, oy, ox + 95, oy - 88, GOLD, 3, head=9))
    b.append(text(ox + 78, oy - 22, "v", 14, TEAL, 700, anchor="start"))
    b.append(text(ox + 100, oy - 90, "Av", 14, GOLD, 700, anchor="start"))
    # collinear short arrows along eigenvector direction: Av = λv (gold longer)
    px, py = ox + dx * 150, oy + dy * 150
    b.append(arrow(px, py, px + dx * 28, py + dy * 28, TEAL, 2.4, head=7))
    b.append(arrow(px, py, px + dx * 52, py + dy * 52, GOLD, 2.8, head=8))
    b.append(text(px + dx * 30 + 6, py + dy * 30 - 2, "Av=λv", 11, FOREST, 700, anchor="start"))
    b.append(text(160, 190, "特征向量方向：只拉伸不转向", 11, AXIS))
    return svg("".join(b))

def _t_lr_schedule():
    import math
    b = []
    x0, x1 = 40, 300; yb = 172; yt = 30
    xpk = 110  # warmup peak x
    rng = yb - yt
    # warmup shaded region
    b.append(rect(x0, yt, xpk - x0, yb - yt, TEALF, None, 0, op=0.55))
    # axes
    b.append(line(x0, yb, x1, yb, AXIS, 1)); b.append(line(x0, yt, x0, yb, AXIS, 1))
    # build curve: linear warmup then cosine decay
    pts = []
    peak_y = yt + 6
    for k in range(0, 21):
        x = x0 + (xpk - x0) * k / 20
        y = yb - (yb - peak_y) * (k / 20)
        pts.append((x, y))
    N = 40
    for k in range(1, N + 1):
        x = xpk + (x1 - xpk) * k / N
        c = 0.5 * (1 + math.cos(math.pi * k / N))
        y = yb - (yb - peak_y) * (0.04 + 0.96 * c)
        pts.append((x, y))
    b.append(poly(pts, TEAL, 3))
    # peak marker
    b.append(circ(xpk, peak_y, 4, GOLD, "#fff", 1.6))
    b.append(text(xpk + 8, peak_y + 2, "峰值", 11, GOLD, 700, anchor="start"))
    # warmup label
    b.append(text((x0 + xpk) / 2, 150, "预热", 11, TEAL, 700))
    b.append(text(160, 190, "预热 + 余弦退火", 11, AXIS))
    return svg("".join(b))

def _t_explaining_away():
    b = []
    # top two cause nodes
    rx, ry = 78, 52      # rain (blue, left)
    sx, sy = 242, 52     # sprinkler (gold, right)
    gx, gy = 160, 138    # grass wet (forest, bottom center)
    # edges from causes to effect
    b.append(arrow(rx + 14, ry + 22, gx - 22, gy - 20, BLUE, 2.6, head=8))
    b.append(arrow(sx - 14, sy + 22, gx + 22, gy - 20, GOLD, 2.6, head=8))
    # nodes
    b.append(circ(rx, ry, 26, BLUE, "#fff", 2)); b.append(text(rx, ry + 5, "下雨", 13, "#fff", 700))
    b.append(circ(sx, sy, 26, GOLD, "#fff", 2)); b.append(text(sx, sy + 5, "洒水器", 12, "#fff", 700))
    b.append(circ(gx, gy, 28, FOREST, "#fff", 2)); b.append(text(gx, gy + 5, "草湿", 13, "#fff", 700))
    # probability hint beside sprinkler: up then down
    b.append(rect(286, 40, 9, 24, TEALF, GOLD, 1.4, rx=2))   # tall bar (was high)
    b.append(text(294, 30, "↑", 13, RED, 800))
    b.append(text(294, 78, "↓", 13, BLUE, 800))
    b.append(rect(286, 64, 9, 10, "#eef4f5", GOLD, 1.4, rx=2)) # short bar (now low)
    # probability story
    b.append(text(160, 178, "30% → 64% → 34%", 12, INK, 700))
    b.append(text(160, 190, "解释消除", 11, AXIS))
    return svg("".join(b))

def _t_q_learning():
    b = []
    # 4x4 grid layout
    ox, oy = 80, 20; cs = 40; cols, rows = 4, 4
    walls = {(1, 1), (2, 2)}
    trap = (3, 1)
    goal = (3, 0)
    start = (0, 3)
    for r in range(rows):
        for c in range(cols):
            x = ox + c * cs; y = oy + r * cs
            if (c, r) in walls:
                fill = "#9aa6a3"
            elif (c, r) == trap:
                fill = "#f3cdc8"
            elif (c, r) == goal:
                fill = "#f7ecc8"
            else:
                fill = TEALF
            b.append(rect(x, y, cs, cs, fill, EDGE, 1.2, rx=4))
    # treasure star (goal)
    gx = ox + goal[0] * cs + cs / 2; gy = oy + goal[1] * cs + cs / 2
    b.append(text(gx, gy + 6, "★", 20, GOLD, 700))
    # trap skull
    tx = ox + trap[0] * cs + cs / 2; ty = oy + trap[1] * cs + cs / 2
    b.append(text(tx, ty + 6, "☠", 18, RED, 700))
    # start marker
    sx = ox + start[0] * cs + cs / 2; sy = oy + start[1] * cs + cs / 2
    b.append(circ(sx, sy, 9, FOREST, "#fff", 2))
    b.append(text(sx, sy + 4, "S", 12, "#fff", 700))
    # greedy path avoiding trap: (0,3)->(0,2)->(0,1)->(0,0)->(1,0)->(2,0)->(3,0)
    path = [(0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0)]
    cen = lambda cc, rr: (ox + cc * cs + cs / 2, oy + rr * cs + cs / 2)
    for i in range(len(path) - 1):
        x1, y1 = cen(*path[i]); x2, y2 = cen(*path[i + 1])
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** 0.5
        pad = 11
        ax1 = x1 + dx / L * pad; ay1 = y1 + dy / L * pad
        ax2 = x2 - dx / L * pad; ay2 = y2 - dy / L * pad
        b.append(arrow(ax1, ay1, ax2, ay2, GOLD, 2.8, head=7))
    b.append(text(160, 190, "试错学策略（无模型）", 11, AXIS))
    return svg("".join(b))

def _t_rlhf_reward_model():
    b = []
    x0, x1 = 30, 300; yb = 92; yt = 22
    b.append(line(x0, yb, x1, yb, AXIS, 1)); b.append(line(x0, yt, x0, yb, AXIS, 1))
    rng = yb - yt - 6
    b.append(poly([(x0 + (x1 - x0) * k / 30, yb - ((k / 30) ** 0.78) * rng) for k in range(31)], TEAL, 2.6))
    b.append(text(296, 30, "r(x)", 11, TEAL, 700, anchor="end"))
    for px, yg, yr in [(86, 60, 80), (160, 44, 64), (232, 30, 52)]:
        b.append(line(px, yg + 2, px, yr - 2, EDGE, 1.4))
        b.append(circ(px, yr, 4.5, RED, "#fff", 1.6)); b.append(circ(px, yg, 4.5, FOREST, "#fff", 1.6))
    b.append(text(52, 36, "A\u227bB", 10, AXIS, 700, anchor="start"))
    byb = 184; H = 56
    def bump(cx, w, amp):
        return [(30 + 270 * j / 40, byb - amp * math.exp(-((30 + 270 * j / 40 - cx) ** 2) / (2 * w * w))) for j in range(41)]
    b.append(line(30, byb, 300, byb, AXIS, 1))
    b.append(poly(bump(150, 30, H * 0.7), AXIS, 2, dash="5 4"))
    b.append(poly(bump(232, 26, H), GOLD, 2.8))
    b.append(text(150, 150, "\u03c0_ref", 10, AXIS, 700))
    b.append(text(250, 132, "\u03c0", 13, GOLD, 700, anchor="start"))
    b.append(text(160, 196, "\u504f\u597d \u2192 \u5956\u52b1 \u2192 \u7b56\u7565\u53f3\u79fb", 11, AXIS))
    return svg("".join(b))

def _t_learning_curve():
    b = []; x0, x1 = 44, 300; yb = 162; yt = 30; N = 24
    b.append(line(x0, yb, x1, yb, AXIS, 1)); b.append(line(x0, yt, x0, yb, AXIS, 1))
    rng = yb - yt - 8; train = []; valid = []
    for k in range(N + 1):
        x = x0 + (x1 - x0) * k / N; t = k / N
        vt = 0.06 + 0.40 * (1 - 2.718281828 ** (-3.0 * t))
        vv = 0.92 - 0.46 * (1 - 2.718281828 ** (-3.0 * t))
        train.append((x, yb - vt * rng)); valid.append((x, yb - vv * rng))
    fillpts = valid + train[::-1]
    b.append(poly(fillpts, "none", 0, TEALF, 0.7))
    b.append(poly(valid, TEAL, 2.8)); b.append(poly(train, RED, 2.8))
    b.append(text(296, 80, "训练", 11, RED, 700, anchor="end"))
    b.append(text(296, 132, "验证", 11, TEAL, 700, anchor="end"))
    b.append(text(172, 178, "数据量 →", 11, AXIS))
    b.append(text(160, 192, "诊断 偏差 / 方差", 11, AXIS))
    return svg("".join(b))

def _t_confusion_matrix():
    b = []
    gx, gy = 56, 40; cell = 38
    vals = [[31, 3, 2], [4, 27, 5], [2, 6, 29]]
    for r in range(3):
        for c in range(3):
            x = gx + c * cell; y = gy + r * cell
            diag = (r == c)
            fill = TEALF if diag else "#f0f2f1"
            stroke = TEAL if diag else EDGE
            sw = 2.2 if diag else 1.2
            b.append(rect(x, y, cell - 3, cell - 3, fill, stroke, sw, rx=4))
            col = TEAL if diag else AXIS
            wt = 700 if diag else 600
            b.append(text(x + (cell - 3) / 2, y + (cell - 3) / 2 + 4, str(vals[r][c]), 12, col, wt))
    b.append(text(40, gy + 1.5 * cell, "真", 12, INK, 700))
    b.append(text(gx + 1.5 * cell - 1.5, gy - 12, "预测", 12, INK, 700))
    bx = gx + 3 * cell + 14
    accs = [0.86, 0.75, 0.78]
    cols = [TEAL, GOLD, FOREST]
    for i, (a, cc) in enumerate(zip(accs, cols)):
        yb = gy + i * cell + 6
        b.append(rect(bx, yb, 60, 14, "#eef2f1", EDGE, 1, rx=3))
        b.append(rect(bx, yb, max(8, 60 * a), 14, cc, None, 0, rx=3))
        b.append(text(bx + 64, yb + 11, "P" + str(i + 1), 10, AXIS, 600, anchor="start"))
    b.append(text(160, 190, "混淆矩阵 · 宏平均 vs 微平均", 11, AXIS))
    return svg("".join(b))

def _t_calibration():
    b = []
    x0, x1 = 56, 292
    yb, yt = 168, 36
    # axis box
    b.append(rect(x0, yt, x1 - x0, yb - yt, "none", AXIS, 1.4))
    # perfect-calibration diagonal (gray dashed)
    b.append(line(x0, yb, x1, yt, AXIS, 1.6, dash="5 5"))
    b.append(text(x1 - 6, yt + 12, "完美", 10, AXIS, 600, anchor="end"))
    # overconfident curve (blue dots) sagging BELOW the diagonal
    pts = []
    N = 6
    for k in range(N + 1):
        t = k / N
        x = x0 + (x1 - x0) * t
        # below diagonal: subtract a sag bump
        sag = 0.30 * (t * (1 - t)) * 4
        yv = t - sag
        y = yb - (yb - yt) * yv
        pts.append((x, y))
    b.append(poly(pts, BLUE, 2.8))
    for (px, py) in pts:
        b.append(circ(px, py, 3.6, BLUE, "#fff", 1.4))
    b.append(text(x0 + 70, yb - 26, "过度自信", 11, BLUE, 700, anchor="start"))
    # arrow hinting calibration back up to the diagonal
    midx = x0 + (x1 - x0) * 0.5
    msag = yb - (yb - yt) * (0.5 - 0.30 * 0.25 * 4)
    mdiag = yb - (yb - yt) * 0.5
    b.append(arrow(midx, msag - 2, midx, mdiag + 4, GOLD, 2.4, head=7))
    # axes labels
    b.append(text(174, yb + 16, "把握", 11, INK, 600))
    b.append(text(x0 - 8, 102, "正", 11, INK, 600, anchor="end"))
    b.append(text(x0 - 8, 116, "确", 11, INK, 600, anchor="end"))
    b.append(text(160, 190, "过度自信 → 校准回对角线", 11, AXIS))
    return svg("".join(b))

def _t_loss_functions():
    b = []
    x0, x1 = 40, 300; yb = 162; yt = 30; xc = (x0 + x1) / 2
    b.append(line(x0, yb, x1, yb, AXIS, 1)); b.append(line(x0, yt, x0, yb, AXIS, 1))
    b.append(line(xc, yt, xc, yb, EDGE, 1, dash="3 4"))
    b.append(text(xc, 176, "0", 10, AXIS, 600))
    rng = yb - yt - 6; N = 30
    # cross-entropy log(1+e^-z): high at left, →0 at right
    ce = []
    for k in range(N + 1):
        z = -3.0 + 6.0 * k / N
        import math
        v = math.log(1 + math.exp(-z * 1.3))
        x = x0 + (x1 - x0) * k / N
        ce.append((x, yb - min(v * 36, rng)))
    b.append(poly(ce, TEAL, 3))
    # hinge max(0, 1-z): kinked line
    hg = [(x0, yb - min(2.0 * 36, rng))]
    xk = x0 + (x1 - x0) * (4.3 / 6.0)
    hg.append((xk, yb)); hg.append((x1, yb))
    b.append(poly(hg, GOLD, 2.6))
    # mse, flat low cap on left
    ms = []
    for k in range(N + 1):
        z = -3.0 + 6.0 * k / N
        v = (max(0.0, 1 - z * 0.6)) ** 2
        x = x0 + (x1 - x0) * k / N
        ms.append((x, yb - min(v * 7.5, rng)))
    b.append(poly(ms, RED, 2.6))
    # legend
    b.append(line(208, 44, 226, 44, TEAL, 3)); b.append(text(230, 48, "交叉熵", 10, INK, 600, anchor="start"))
    b.append(line(208, 58, 226, 58, GOLD, 2.6)); b.append(text(230, 62, "Hinge", 10, INK, 600, anchor="start"))
    b.append(line(208, 72, 226, 72, RED, 2.6)); b.append(text(230, 76, "MSE", 10, INK, 600, anchor="start"))
    b.append(text(46, 24, "损失", 10, AXIS, 600, anchor="start"))
    b.append(text(160, 190, "MSE / 交叉熵 / Hinge / Focal", 11, AXIS))
    return svg("".join(b))

def _t_svd_lowrank():
    b = []; cell = 13; n = 5
    def grid(ox, oy, vals):
        out = []
        for r in range(n):
            for c in range(n):
                gg = int(255 * (1 - vals[r][c]))
                out.append(rect(ox + c * cell, oy + r * cell, cell - 1, cell - 1, "rgb(%d,%d,%d)" % (gg, gg, gg), EDGE, 0.6))
        return "".join(out)
    orig = [[max(.06, min(.94, .5 + .42 * math.sin(c * 0.9) * math.cos(r * 0.7))) for c in range(n)] for r in range(n)]
    recon = [[max(.1, min(.9, .5 + .34 * math.sin(c * 0.9))) for c in range(n)] for r in range(n)]
    gy = 46
    b.append(grid(40, gy, orig)); b.append(text(40 + n * cell / 2, gy - 8, "\u539f\u56fe", 11, AXIS))
    b.append(arrow(116, gy + n * cell / 2, 150, gy + n * cell / 2, GOLD, 2.6, head=8))
    b.append(grid(160, gy, recon)); b.append(text(160 + n * cell / 2, gy - 8, "\u524d k \u7247\u91cd\u5efa", 11, AXIS))
    sigs = [54, 36, 22, 13, 8, 5, 3, 2]; bx = 240; bw = 8; base = 150
    for i, h in enumerate(sigs):
        b.append(rect(bx + i * (bw + 1), base - h, bw, h, TEAL if i < 3 else AXIS, op=1 if i < 3 else .5, rx=1))
    b.append(text(bx + 4 * (bw + 1), 166, "\u03c3 \u8c31", 10, AXIS, 600))
    b.append(text(160, 190, "\u524d\u51e0\u7247\u6251\u4f4f\u4e3b\u8981\u4fe1\u606f", 11, AXIS))
    return svg("".join(b))

def _t_gan_training():
    b = []
    x0, x1 = 30, 300
    yb = 165
    yt = 30
    b.append(line(x0, yb, x1, yb, AXIS, 1.2))
    b.append(line(x0, yt, x0, yb, AXIS, 1.2))
    # bar layout
    n = 9
    bw = 22
    gap = 6
    # bell-shaped heights, peak shifted right
    real_h = [10, 22, 40, 66, 96, 118, 100, 60, 24]
    fake_h = [8, 18, 34, 58, 88, 110, 92, 54, 20]
    for i in range(n):
        cx = x0 + 14 + i * (bw + gap)
        rh = real_h[i]
        fh = fake_h[i]
        # real data: pale gray, slightly back/wider
        b.append(rect(cx - bw / 2, yb - rh, bw, rh, "#e4e8ea", "#c2cacd", 1, rx=2))
        # fake data: gold, narrower, overlaid on real position
        b.append(rect(cx - bw / 2 + 4, yb - fh, bw - 8, fh, GOLD, "#fff", 0.8, rx=2, op=0.92))
    # D(x) discriminator curve: high on real-only, dipping toward 0.5
    dpts = []
    for i in range(n):
        cx = x0 + 14 + i * (bw + gap)
        # near where fake matches real, D drifts to ~0.5; edges higher
        frac = abs(i - 4) / 4.0
        dval = 0.5 + 0.42 * frac
        dpts.append((cx, yt + 8 + (1 - dval) * 50))
    b.append(poly(dpts, TEAL, 2.8))
    b.append(line(x0, yt + 8 + 0.5 * 50, x1, yt + 8 + 0.5 * 50, TEAL, 1, dash="4 4", op=0.5))
    b.append(text(298, yt + 6, "D(x)", 11, TEAL, 700, anchor="end"))
    b.append(text(298, yt + 8 + 0.5 * 50 - 4, "0.5", 10, AXIS, 600, anchor="end"))
    b.append(text(160, 190, "假分布贴上真分布", 11, AXIS))
    return svg("".join(b))

# slug -> draw function. Add new entries here.
THUMBS = {
    "rnn-unroll": _t_rnn_unroll,
    "rnn-counter": _t_rnn_counter,
    "bptt-vanishing": _t_bptt_vanishing,
    "lstm-gates": _t_lstm_gates,
    "bidirectional-rnn": _t_bidirectional_rnn,
    "char-rnn": _t_char_rnn,
    "hmm-viterbi": _t_hmm_viterbi,
    "gcn-node-classification": _t_gcn_node_classification,
    "adaboost": _t_adaboost,
    "rbm-reconstruction": _t_rbm_reconstruction,
    "llm-internals": _t_llm_internals,
    "sparse-autoencoder": _t_sparse_autoencoder,
    "l1-l2-geometry": _t_l1_l2_geometry,
    "eigenvectors": _t_eigenvectors,
    "lr-schedule": _t_lr_schedule,
    "explaining-away": _t_explaining_away,
    "q-learning": _t_q_learning,
    "rlhf-reward-model": _t_rlhf_reward_model,
    "learning-curve": _t_learning_curve,
    "confusion-matrix": _t_confusion_matrix,
    "calibration": _t_calibration,
    "loss-functions": _t_loss_functions,
    "svd-lowrank": _t_svd_lowrank,
    "gan-training": _t_gan_training,
}

# ---------------------------------------------------------------- validation

def coord_check(s):
    """Return list of coordinates that fall outside the 320x200 viewBox (small slack)."""
    bad = []
    for m in re.finditer(r'(?:x|y|cx|cy|x1|y1|x2|y2)="(-?\d+(?:\.\d+)?)"', s):
        v = float(m.group(1))
        if v < -6 or v > 326:
            bad.append(v)
    for m in re.finditer(r'points="([^"]+)"', s):
        for pair in m.group(1).split():
            xx, yy = pair.split(",")
            if not (-6 <= float(xx) <= 326 and -6 <= float(yy) <= 206):
                bad.append(pair)
    return bad

def validate(s):
    minidom.parseString(s)          # raises on malformed XML
    return coord_check(s)

# ---------------------------------------------------------------- index scan

def _attr(block, name):
    m = re.search(r'\b' + name + r'\s*=\s*(?:"([^"]*)"|(\S+))', block)
    if not m:
        return None
    return (m.group(1) if m.group(1) is not None else m.group(2)).strip()

def scan_index_missing():
    """Cards on viz/index.md that rely on the auto /assets/viz/<slug>.svg
    (internal /viz/ url, no explicit thumb=, not external=true) but whose
    .svg file does not exist."""
    if not os.path.exists(INDEX):
        return []
    txt = open(INDEX, encoding="utf-8").read()
    blocks = re.findall(r"\{%-?\s*include\s+viz-card\.html(.*?)-?%\}", txt, re.S)
    missing = []
    for blk in blocks:
        if _attr(blk, "external") == "true":
            continue
        url = _attr(blk, "url") or ""
        if "/viz/" not in url:
            continue
        if _attr(blk, "thumb"):
            continue
        slug = url.split("/viz/")[1].strip("/")
        if not slug:
            continue
        if not os.path.exists(os.path.join(OUT, slug + ".svg")):
            missing.append(slug)
    return missing

# ---------------------------------------------------------------- write/preview

def write_one(slug):
    s = THUMBS[slug]()
    bad = validate(s)
    path = os.path.join(OUT, slug + ".svg")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print(f"  wrote {slug:26s} {len(s):4d}B  outOfBounds={bad if bad else 'none'}")
    return bad

def find_browser():
    import shutil
    for name in ("chrome", "chromium", "chromium-browser", "google-chrome", "msedge"):
        p = shutil.which(name)
        if p:
            return p
    cands = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    return None

def preview(slugs):
    """Rasterize given slugs to PNG via headless browser, montage with Pillow,
    print the montage path. Best-effort helper for eyeballing while adjusting."""
    import subprocess, tempfile
    browser = find_browser()
    if not browser:
        print("preview: no chrome/edge found; skipping. (SVGs were still written.)")
        return
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("preview: Pillow not installed (pip install pillow); skipping montage.")
        return
    tmp = tempfile.mkdtemp(prefix="vizthumb_")
    pngs = []
    for s in slugs:
        svg_path = os.path.join(OUT, s + ".svg")
        if not os.path.exists(svg_path):
            continue
        png = os.path.join(tmp, s + ".png")
        uri = "file:///" + svg_path.replace("\\", "/")
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--force-device-scale-factor=2",
                        "--virtual-time-budget=1500", f"--screenshot={png}", "--window-size=320,200", uri],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(png):
            pngs.append((s, png))
    if not pngs:
        print("preview: no PNGs produced; skipping montage.")
        return
    cw, ch, pad, lblh, cols = 320, 200, 14, 20, 2
    rows = (len(pngs) + cols - 1) // cols
    W = cols * cw + (cols + 1) * pad
    H = rows * (ch + lblh) + (rows + 1) * pad
    m = Image.new("RGB", (W, H), (245, 245, 245))
    d = ImageDraw.Draw(m)
    for i, (s, png) in enumerate(pngs):
        r, c = divmod(i, cols)
        x = pad + c * (cw + pad); y = pad + r * (ch + lblh + pad)
        im = Image.open(png).convert("RGB").resize((cw, ch))
        m.paste(im, (x, y + lblh))
        d.rectangle([x, y + lblh, x + cw - 1, y + lblh + ch - 1], outline=(170, 170, 170))
        d.text((x + 3, y + 5), s, fill=(10, 10, 10))
    out = os.path.join(tmp, "_montage.png")
    m.save(out)
    print(f"preview montage: {out}  ({m.size[0]}x{m.size[1]})")

# ---------------------------------------------------------------- cli

def main():
    try:  # so ✓ / Chinese print on a GBK Windows console without crashing
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Generate/adjust viz card thumbnails (assets/viz/<slug>.svg).")
    ap.add_argument("--all", action="store_true", help="(re)generate every registered thumbnail")
    ap.add_argument("--only", metavar="SLUGS", help="comma-separated slugs to (re)generate")
    ap.add_argument("--list", action="store_true", help="list registered thumbnails")
    ap.add_argument("--missing", action="store_true", help="cards needing an auto-svg but missing the file")
    ap.add_argument("--check", action="store_true", help="validate registered SVGs without writing")
    ap.add_argument("--preview", nargs="?", const="*", metavar="SLUGS",
                    help="rasterize to a PNG montage to eyeball (default: the slugs just generated)")
    args = ap.parse_args()

    if not any([args.all, args.only, args.list, args.missing, args.check, args.preview is not None]):
        ap.print_help()
        return

    if args.list:
        print(f"{len(THUMBS)} registered thumbnail(s):")
        for s in THUMBS:
            exists = "✓" if os.path.exists(os.path.join(OUT, s + ".svg")) else "·"
            print(f"  {exists} {s}")

    if args.missing:
        miss = scan_index_missing()
        if not miss:
            print("missing: none — every auto-svg card on viz/index.md has its .svg file.")
        else:
            print(f"missing: {len(miss)} card(s) need an auto-svg thumbnail but the file is absent:")
            for s in miss:
                tag = "registered → --only " + s if s in THUMBS else "NO draw fn yet — add one"
                print(f"  - {s}  [{tag}]")

    if args.check:
        print(f"check: validating {len(THUMBS)} registered thumbnail(s)…")
        problems = 0
        for s, fn in THUMBS.items():
            try:
                bad = validate(fn())
            except Exception as e:  # noqa
                print(f"  ✗ {s}: {e}"); problems += 1; continue
            if bad:
                print(f"  ✗ {s}: out-of-bounds {bad}"); problems += 1
        print("check: all good." if not problems else f"check: {problems} problem(s).")

    generated = []
    if args.all or args.only:
        os.makedirs(OUT, exist_ok=True)
        slugs = list(THUMBS) if args.all else [s.strip() for s in args.only.split(",") if s.strip()]
        unknown = [s for s in slugs if s not in THUMBS]
        if unknown:
            sys.exit(f"unknown slug(s): {', '.join(unknown)} (see --list)")
        print(f"generating {len(slugs)} thumbnail(s) → {OUT}")
        for s in slugs:
            write_one(s); generated.append(s)
        print("done.")

    if args.preview is not None:
        sel = generated if args.preview == "*" else [s.strip() for s in args.preview.split(",") if s.strip()]
        if not sel:
            sel = list(THUMBS)
        preview(sel)

if __name__ == "__main__":
    main()
