#!/usr/bin/env python3
"""news-image-20261124 -- Sum up 24 November's world news in one image.

A 1024x1024 newspaper front page ("THE WORLD TODAY") drawn entirely with
pure-Python primitives and encoded to PNG by hand (zlib + struct, no PIL).

Stories (all reported 24 November 2026):
  1. Russian drone over Poland (lead)
  2. Four-way talks urged (Zelensky)
  3. US blacklists Megaspeed
  4. Quake shakes Nepal
  5. States sue SpaceX over Grok
  6. EU cuts 60 banks from SWIFT
Plus a markets ticker strip.

Standard library only (zlib, struct, math, os, sys). Fully deterministic:
fixed geometry, fixed palette, fixed zlib level, no randomness, no time,
no environment-dependent layout. Output: $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png), exactly 1024x1024, <= 1 MiB.
"""

import math
import os
import struct
import sys
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette --
PAPER = (250, 246, 236)
PAPER_DARK = (238, 231, 218)
INK = (18, 18, 18)
GREY = (110, 108, 100)
LIGHT_GREY = (200, 196, 186)
RED = (178, 34, 34)
DARK_RED = (140, 20, 20)
BLUE = (28, 72, 150)
DARK_BLUE = (16, 30, 58)
NIGHT = (24, 38, 74)
NIGHT2 = (36, 56, 104)
SKY = (146, 178, 214)
SKY_LIGHT = (196, 214, 232)
GOLD = (214, 164, 32)
GREEN = (46, 110, 58)
DARK_GREEN = (28, 74, 40)
BROWN = (122, 84, 52)
TAN = (196, 164, 118)
MOUNTAIN = (96, 92, 96)
MOUNTAIN2 = (128, 118, 112)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (244, 200, 40)
ORANGE = (224, 110, 30)
TEAL = (24, 128, 128)
STEEL = (90, 104, 122)
LIGHT_BLUE = (120, 160, 210)

# ------------------------------------------------------------- bitmap font --
# Hand-drawn 5x7 glyphs: each glyph is 7 rows of 5-bit masks (bit 4 = left).
FONT = {
    "A": (0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    "B": (0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110),
    "C": (0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110),
    "D": (0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110),
    "E": (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111),
    "F": (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000),
    "G": (0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01111),
    "H": (0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    "I": (0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    "J": (0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100),
    "K": (0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001),
    "L": (0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111),
    "M": (0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001),
    "N": (0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001),
    "O": (0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    "P": (0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000),
    "Q": (0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101),
    "R": (0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001),
    "S": (0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110),
    "T": (0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100),
    "U": (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    "V": (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100),
    "W": (0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001),
    "X": (0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001),
    "Y": (0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100),
    "Z": (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111),
    "0": (0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110),
    "1": (0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    "2": (0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111),
    "3": (0b11111, 0b00010, 0b00100, 0b00010, 0b00001, 0b10001, 0b01110),
    "4": (0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010),
    "5": (0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110),
    "6": (0b00110, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110),
    "7": (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000),
    "8": (0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110),
    "9": (0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100),
    ".": (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b01100, 0b01100),
    ",": (0b00000, 0b00000, 0b00000, 0b00000, 0b01100, 0b00100, 0b01000),
    "%": (0b11001, 0b11010, 0b00010, 0b00100, 0b01000, 0b01011, 0b10011),
    "+": (0b00000, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0b00000),
    "-": (0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000),
    ":": (0b00000, 0b01100, 0b01100, 0b00000, 0b01100, 0b01100, 0b00000),
    "'": (0b00100, 0b00100, 0b01000, 0b00000, 0b00000, 0b00000, 0b00000),
    "/": (0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000),
    "&": (0b01100, 0b10010, 0b10100, 0b01000, 0b10101, 0b10010, 0b01101),
    "$": (0b00100, 0b01111, 0b10100, 0b01110, 0b00101, 0b11110, 0b00100),
    "(": (0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010),
    ")": (0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000),
    " ": (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000),
}

BLANK = (0, 0, 0, 0, 0, 0, 0)


def text_width(text, scale):
    """Pixel width of text at the given scale (6 px per char cell)."""
    if not text:
        return 0
    return len(text) * 6 * scale - scale


def wrap_text(text, max_width, scale):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ canvas --
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        r, g, b = color
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i] = r
                self.px[i + 1] = g
                self.px[i + 2] = b

    def draw_rect(self, x, y, w, h, color, thick=1):
        for t in range(thick):
            self.fill_rect(x + t, y + t, w - 2 * t, 1, color)
            self.fill_rect(x + t, y + h - 1 - t, w - 2 * t, 1, color)
            self.fill_rect(x + t, y + t, 1, h - 2 * t, color)
            self.fill_rect(x + w - 1 - t, y + t, 1, h - 2 * t, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            if thick <= 1:
                self.set_pixel(x, y, color)
            else:
                self.fill_rect(x - thick // 2, y - thick // 2, thick, thick, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def dashed_line(self, x0, y0, x1, y1, color, dash=8, gap=6):
        length = int(math.hypot(x1 - x0, y1 - y0))
        if length == 0:
            return
        ux = (x1 - x0) / length
        uy = (y1 - y0) / length
        pos = 0
        while pos < length:
            end = min(pos + dash, length)
            ax = int(round(x0 + ux * pos))
            ay = int(round(y0 + uy * pos))
            bx = int(round(x0 + ux * end))
            by = int(round(y0 + uy * end))
            self.line(ax, ay, bx, by, color, 2)
            pos = end + gap

    def filled_circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def circle(self, cx, cy, r, color, thick=1):
        for t in range(thick):
            rr = r - t
            if rr <= 0:
                break
            steps = max(8, int(2 * math.pi * rr))
            for i in range(steps):
                a = 2 * math.pi * i / steps
                self.set_pixel(int(round(cx + rr * math.cos(a))),
                               int(round(cy + rr * math.sin(a))), color)

    def filled_ellipse(self, cx, cy, rx, ry, color):
        for dy in range(-ry, ry + 1):
            if ry == 0:
                continue
            f = 1.0 - (dy * dy) / float(ry * ry)
            dx = int(rx * math.sqrt(max(0.0, f)))
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def ellipse(self, cx, cy, rx, ry, color, thick=1):
        steps = max(16, int(2 * math.pi * max(rx, ry)))
        for i in range(steps):
            a = 2 * math.pi * i / steps
            x = int(round(cx + rx * math.cos(a)))
            y = int(round(cy + ry * math.sin(a)))
            if thick <= 1:
                self.set_pixel(x, y, color)
            else:
                self.fill_rect(x - thick // 2, y - thick // 2, thick, thick, color)

    def polygon(self, points, color):
        """Scanline-filled polygon from a list of (x, y) vertices."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        y0, y1 = min(ys), max(ys)
        n = len(points)
        for y in range(y0, y1 + 1):
            xs = []
            for i in range(n):
                x0, yy0 = points[i]
                x1, yy1 = points[(i + 1) % n]
                if yy0 == yy1:
                    continue
                if (y >= min(yy0, yy1)) and (y < max(yy0, yy1)):
                    t = (y - yy0) / float(yy1 - yy0)
                    xs.append(x0 + t * (x1 - x0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                xa = int(math.ceil(xs[k]))
                xb = int(math.floor(xs[k + 1]))
                if xb >= xa:
                    self.fill_rect(xa, y, xb - xa + 1, 1, color)

    def triangle(self, p0, p1, p2, color):
        self.polygon([p0, p1, p2], color)

    def draw_text(self, x, y, text, scale, color):
        text = text.upper()
        cx = x
        for ch in text:
            glyph = FONT.get(ch, BLANK)
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, color)
            cx += 6 * scale

    def draw_text_centered(self, cx, y, text, scale, color):
        self.draw_text(cx - text_width(text, scale) // 2, y, text, scale, color)


# -------------------------------------------------------------- PNG encode --
def png_chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(canvas):
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[y * stride:(y + 1) * stride]
    idat = zlib.compress(bytes(raw), 9)
    return (b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", ihdr)
            + png_chunk(b"IDAT", idat) + png_chunk(b"IEND", b""))


# ------------------------------------------------------------ scene: lead --
def draw_lead_scene(cv, x, y, w, h):
    """Night sky over the Polish border: radar arcs, map outline, drone."""
    # Night sky bands.
    cv.fill_rect(x, y, w, h, NIGHT)
    cv.fill_rect(x, y + h // 2, w, h - h // 2, NIGHT2)
    # Moon.
    cv.filled_circle(x + w - 110, y + 58, 34, (232, 228, 200))
    cv.filled_circle(x + w - 122, y + 50, 8, (210, 204, 172))
    cv.filled_circle(x + w - 98, y + 68, 6, (210, 204, 172))
    # Fixed stars.
    stars = [(40, 26), (120, 60), (210, 30), (300, 70), (390, 24),
             (470, 52), (560, 28), (660, 62), (740, 30), (830, 56),
             (70, 110), (250, 120), (430, 108), (620, 118), (800, 108),
             (160, 88), (520, 84), (700, 92), (900, 40), (330, 42)]
    for sx, sy in stars:
        cv.fill_rect(x + sx, y + sy, 3, 3, WHITE)
    # Distant hills.
    cv.polygon([(x, y + h), (x, y + h - 70), (x + 180, y + h - 120),
                (x + 360, y + h - 78), (x + 540, y + h - 128),
                (x + 720, y + h - 82), (x + w, y + h - 118),
                (x + w, y + h)], (30, 52, 44))
    # Ground.
    cv.fill_rect(x, y + h - 64, w, 64, DARK_GREEN)
    cv.fill_rect(x, y + h - 64, w, 4, GREEN)
    # Simplified Poland map outline, lying on the ground left of centre.
    poland = [(x + 300, y + h - 58), (x + 330, y + h - 118),
              (x + 380, y + h - 132), (x + 430, y + h - 116),
              (x + 470, y + h - 122), (x + 500, y + h - 96),
              (x + 480, y + h - 66), (x + 420, y + h - 52),
              (x + 350, y + h - 50)]
    cv.polygon(poland, (196, 164, 118))
    cv.polygon(poland, (196, 164, 118))
    # Map outline (draw edge lines over the fill).
    for i in range(len(poland)):
        a = poland[i]
        b = poland[(i + 1) % len(poland)]
        cv.line(a[0], a[1], b[0], b[1], (120, 92, 52), 2)
    # Border line: dashed red, vertical, east of the map.
    bx = x + 560
    cv.dashed_line(bx, y + 30, bx, y + h - 70, RED, 10, 7)
    # Border posts along the line.
    for py in (y + 90, y + 170, y + 250):
        cv.fill_rect(bx - 3, py, 6, 26, (220, 220, 210))
        cv.fill_rect(bx - 8, py - 6, 16, 8, RED)
    # Radar station, left ground: dish + sweeping arcs.
    rx, ry = x + 130, y + h - 64
    cv.fill_rect(rx - 4, ry - 46, 8, 46, STEEL)
    cv.polygon([(rx - 34, ry - 78), (rx + 30, ry - 92),
                (rx + 8, ry - 44), (rx - 18, ry - 46)], LIGHT_GREY)
    cv.circle(rx, ry - 52, 52, (120, 200, 120), 2)
    cv.circle(rx, ry - 52, 78, (120, 200, 120), 2)
    cv.circle(rx, ry - 52, 104, (120, 200, 120), 2)
    cv.line(rx, ry - 52, rx + 96, ry - 120, (120, 220, 120), 2)
    # Second small radar, right ground.
    rx2, ry2 = x + w - 130, y + h - 64
    cv.fill_rect(rx2 - 3, ry2 - 34, 6, 34, STEEL)
    cv.polygon([(rx2 - 24, ry2 - 56), (rx2 + 22, ry2 - 66),
                (rx2 + 6, ry2 - 32), (rx2 - 12, ry2 - 34)], LIGHT_GREY)
    cv.circle(rx2, ry2 - 40, 44, (120, 200, 120), 2)
    # Drone flight path: red dashed arc crossing the border, turning back.
    cv.dashed_line(x + 640, y + 96, x + 520, y + 150, (255, 90, 70), 9, 6)
    cv.dashed_line(x + 520, y + 150, x + 430, y + 190, (255, 90, 70), 9, 6)
    cv.dashed_line(x + 430, y + 190, x + 520, y + 130, (255, 200, 80), 9, 6)
    # Drone silhouette: quad-rotor recon drone, mid-sky, left of border.
    dx, dy = x + 470, y + 168
    # Rotor arms from the body out to the four motor hubs.
    for ax, ay in ((dx - 52, dy - 34), (dx + 52, dy - 34),
                   (dx - 52, dy + 34), (dx + 52, dy + 34)):
        cv.line(dx, dy, ax, ay, (12, 12, 14), 4)
    # Spinning propellers: horizontal blades above each hub.
    for ax, ay in ((dx - 52, dy - 34), (dx + 52, dy - 34),
                   (dx - 52, dy + 34), (dx + 52, dy + 34)):
        cv.line(ax - 24, ay - 4, ax + 24, ay - 4, (200, 200, 200), 3)
        cv.filled_circle(ax, ay, 5, (12, 12, 14))
    # Compact rectangular body with a short nose wedge.
    cv.fill_rect(dx - 30, dy - 9, 60, 18, (12, 12, 14))
    cv.polygon([(dx + 30, dy - 9), (dx + 44, dy), (dx + 30, dy + 9)],
               (12, 12, 14))
    # Camera eye under the nose + status light at the tail.
    cv.filled_circle(dx + 30, dy + 4, 7, (200, 40, 40))
    cv.filled_circle(dx + 30, dy + 4, 3, (255, 120, 90))
    cv.filled_circle(dx - 30, dy, 5, (255, 170, 60))
    # Tracking lock brackets around the drone (tracked, not shot down).
    bx0, by0, bw, bh = dx - 96, dy - 62, 190, 124
    cv.line(bx0, by0 + 22, bx0, by0, (120, 220, 120), 3)
    cv.line(bx0, by0, bx0 + 22, by0, (120, 220, 120), 3)
    cv.line(bx0 + bw - 22, by0, bx0 + bw, by0, (120, 220, 120), 3)
    cv.line(bx0 + bw, by0, bx0 + bw, by0 + 22, (120, 220, 120), 3)
    cv.line(bx0, by0 + bh - 22, bx0, by0 + bh, (120, 220, 120), 3)
    cv.line(bx0, by0 + bh, bx0 + 22, by0 + bh, (120, 220, 120), 3)
    cv.line(bx0 + bw, by0 + bh - 22, bx0 + bw, by0 + bh, (120, 220, 120), 3)
    cv.line(bx0 + bw - 22, by0 + bh, bx0 + bw, by0 + bh, (120, 220, 120), 3)
    # Held-fire cue, purely visual: a small shield / crossed-out trigger
    # marker is avoided; instead a green "hold" ring under the radar.
    cv.circle(rx, ry - 52, 14, (120, 220, 120), 2)


# ----------------------------------------------------------- small scenes --
def draw_flag(cv, x, y, w, h, stripes):
    """A small flag on a pole; stripes = list of (colour, height-fraction)."""
    cv.fill_rect(x - 2, y - 6, 3, h + 14, (60, 48, 32))
    yy = y
    for color, frac in stripes:
        hh = max(1, int(round(h * frac)))
        cv.fill_rect(x + 1, yy, w, hh, color)
        yy += hh
    cv.draw_rect(x + 1, y, w, h, INK, 1)


def draw_talks_scene(cv, x, y, w, h):
    """Four flags around a table: Ukraine, Europe, America, Russia."""
    cv.fill_rect(x, y, w, h, SKY_LIGHT)
    cv.fill_rect(x, y + h - 26, w, 26, (150, 128, 96))
    # Table.
    cv.filled_ellipse(x + w // 2, y + h - 52, 92, 16, (122, 84, 52))
    cv.fill_rect(x + w // 2 - 86, y + h - 54, 172, 8, (96, 64, 38))
    cv.fill_rect(x + w // 2 - 8, y + h - 46, 16, 22, (96, 64, 38))
    # Four chairs.
    for cx in (x + 44, x + w - 44):
        cv.fill_rect(cx - 16, y + h - 66, 32, 8, BROWN)
        cv.fill_rect(cx - 16, y + h - 66, 5, 26, BROWN)
        cv.fill_rect(cx + 11, y + h - 66, 5, 26, BROWN)
    # Four flags on poles behind the table.
    fw, fh = 44, 28
    fy = y + 12
    draw_flag(cv, x + 22, fy, fw, fh,
              [(BLUE, 0.5), (YELLOW, 0.5)])                    # Ukraine
    draw_flag(cv, x + 86, fy, fw, fh,
              [(BLUE, 1.0)])                                     # Europe
    cv.filled_circle(x + 86 + 1 + fw // 2, fy + fh // 2, 8, YELLOW)
    draw_flag(cv, x + 150, fy, fw, fh,
              [(RED, 0.15), (WHITE, 0.15), (RED, 0.15), (WHITE, 0.15),
               (RED, 0.14), (WHITE, 0.13), (RED, 0.13)])         # America
    cv.fill_rect(x + 150 + 1, fy, 18, 13, BLUE)
    draw_flag(cv, x + 214, fy, fw, fh,
              [(WHITE, 0.34), (BLUE, 0.33), (RED, 0.33)])        # Russia
    # Papers on the table.
    cv.fill_rect(x + w // 2 - 52, y + h - 60, 26, 10, WHITE)
    cv.fill_rect(x + w // 2 + 18, y + h - 60, 26, 10, WHITE)


def draw_megaspeed_scene(cv, x, y, w, h):
    """Microchip under a red ban mark, with a shipping container."""
    cv.fill_rect(x, y, w, h, (226, 232, 238))
    # Shipping container, bottom left.
    cx, cy, cw, chh = x + 18, y + h - 52, 92, 40
    cv.fill_rect(cx, cy, cw, chh, ORANGE)
    cv.draw_rect(cx, cy, cw, chh, INK, 2)
    for vx in (cx + 22, cx + 45, cx + 68):
        cv.line(vx, cy, vx, cy + chh, INK, 2)
    # Microchip, centre right. Sized for the 76 px row-1 scene box.
    chip_x, chip_y = x + w - 128, y + 12
    cs = 52
    for px in range(5):
        cv.fill_rect(chip_x + 8 + px * 14, chip_y - 10, 6, 10, STEEL)
        cv.fill_rect(chip_x + 8 + px * 14, chip_y + cs, 6, 10, STEEL)
    for py in range(5):
        cv.fill_rect(chip_x - 10, chip_y + 8 + py * 14, 10, 6, STEEL)
        cv.fill_rect(chip_x + cs, chip_y + 8 + py * 14, 10, 6, STEEL)
    cv.fill_rect(chip_x, chip_y, cs, cs, (24, 28, 34))
    cv.draw_rect(chip_x, chip_y, cs, cs, INK, 2)
    cv.fill_rect(chip_x + 14, chip_y + 14, cs - 28, cs - 28, (52, 92, 52))
    cv.draw_rect(chip_x + 14, chip_y + 14, cs - 28, cs - 28, (120, 200, 120), 1)
    cv.fill_rect(chip_x + 26, chip_y + 26, 10, 10, GOLD)
    cv.fill_rect(chip_x + 40, chip_y + 26, 10, 10, GOLD)
    cv.fill_rect(chip_x + 26, chip_y + 40, 10, 10, GOLD)
    # Red ban mark over the chip.
    bcx, bcy, br = chip_x + cs // 2, chip_y + cs // 2, 36
    cv.circle(bcx, bcy, br, RED, 5)
    cv.line(bcx - 25, bcy + 25, bcx + 25, bcy - 25, RED, 5)
    # Small "AI" chip label block, left top.
    cv.fill_rect(x + 18, y + 14, 52, 30, BLUE)
    cv.draw_rect(x + 18, y + 14, 52, 30, INK, 2)
    cv.draw_text(x + 28, y + 22, "AI", 2, WHITE)


def draw_quake_scene(cv, x, y, w, h):
    """Cracked Himalayan peaks and shaking buildings."""
    cv.fill_rect(x, y, w, h, SKY)
    cv.filled_circle(x + w - 46, y + 24, 16, (240, 224, 160))
    # Far peaks.
    cv.polygon([(x, y + h), (x + 40, y + 34), (x + 90, y + h)], MOUNTAIN2)
    cv.polygon([(x + 150, y + h), (x + 210, y + 22), (x + 280, y + h)],
               MOUNTAIN2)
    # Near peaks with snow caps.
    cv.polygon([(x + 60, y + h), (x + 130, y + 40), (x + 200, y + h)],
               MOUNTAIN)
    cv.polygon([(x + 112, y + 58), (x + 130, y + 40), (x + 148, y + 58),
                (x + 138, y + 54), (x + 130, y + 62), (x + 122, y + 54)],
               WHITE)
    cv.polygon([(x + 180, y + h), (x + 250, y + 52), (x + 320, y + h)],
               MOUNTAIN)
    cv.polygon([(x + 236, y + 66), (x + 250, y + 52), (x + 264, y + 66),
                (x + 256, y + 62), (x + 250, y + 68), (x + 244, y + 62)],
               WHITE)
    # Ground.
    cv.fill_rect(x, y + h - 22, w, 22, (96, 84, 66))
    # Crack zigzag through the ground and up the middle peak.
    crack = [(x + 130, y + h - 22), (x + 122, y + h - 40),
             (x + 136, y + h - 58), (x + 124, y + 10),
             (x + 132, y + 2)]
    for i in range(len(crack) - 1):
        cv.line(crack[i][0], crack[i][1], crack[i + 1][0], crack[i + 1][1],
                RED, 3)
    cv.line(x + 60, y + h - 6, x + 90, y + h - 14, RED, 3)
    cv.line(x + 90, y + h - 14, x + 122, y + h - 4, RED, 3)
    cv.line(x + 170, y + h - 8, x + 200, y + h - 16, RED, 3)
    cv.line(x + 200, y + h - 16, x + 232, y + h - 6, RED, 3)
    # Shaking buildings, tilted, with motion lines.
    cv.polygon([(x + 236, y + h - 22), (x + 240, y + h - 66),
                (x + 272, y + h - 60), (x + 268, y + h - 22)], (210, 196, 170))
    cv.polygon([(x + 276, y + h - 22), (x + 282, y + h - 52),
                (x + 306, y + h - 48), (x + 302, y + h - 22)], (190, 176, 150))
    cv.fill_rect(x + 246, y + h - 56, 6, 6, INK)
    cv.fill_rect(x + 258, y + h - 56, 6, 6, INK)
    cv.fill_rect(x + 246, y + h - 42, 6, 6, INK)
    cv.line(x + 226, y + h - 70, x + 218, y + h - 70, INK, 2)
    cv.line(x + 228, y + h - 58, x + 220, y + h - 58, INK, 2)
    cv.line(x + 312, y + h - 60, x + 320, y + h - 60, INK, 2)


def draw_grok_scene(cv, x, y, w, h):
    """Courthouse columns beside a phone carrying a red X."""
    cv.fill_rect(x, y, w, h, (228, 224, 210))
    # Courthouse, left.
    bx, by = x + 14, y + 16
    cv.polygon([(bx, by + 22), (bx + 78, by), (bx + 156, by + 22)], (160, 150, 132))
    cv.fill_rect(bx, by + 22, 156, 10, (140, 130, 112))
    for i in range(4):
        colx = bx + 8 + i * 38
        cv.fill_rect(colx, by + 32, 14, 52, (226, 220, 204))
        cv.fill_rect(colx - 3, by + 28, 20, 6, (200, 192, 172))
        cv.fill_rect(colx - 3, by + 82, 20, 6, (200, 192, 172))
    cv.fill_rect(bx, by + 88, 156, 10, (140, 130, 112))
    # Phone, right.
    px, py, pw, ph = x + w - 84, y + 12, 62, 92
    cv.fill_rect(px, py, pw, ph, (16, 16, 20))
    cv.draw_rect(px, py, pw, ph, INK, 2)
    cv.fill_rect(px + 6, py + 10, pw - 12, ph - 22, (90, 170, 220))
    cv.fill_rect(px + 6, py + 10, pw - 12, 16, WHITE)
    cv.fill_rect(px + 12, py + 34, pw - 24, 8, WHITE)
    cv.fill_rect(px + 12, py + 48, pw - 24, 8, (220, 220, 220))
    cv.fill_rect(px + 12, py + 62, pw - 34, 8, (200, 200, 200))
    # Red X over the phone screen.
    cv.line(px + 4, py + 8, px + pw - 4, py + ph - 8, RED, 5)
    cv.line(px + pw - 4, py + 8, px + 4, py + ph - 8, RED, 5)
    # Gavel in front of the courthouse.
    gx, gy = x + 196, y + h - 34
    cv.line(gx, gy - 6, gx + 34, gy - 22, (96, 64, 38), 4)
    cv.fill_rect(gx + 30, gy - 30, 26, 12, (122, 84, 52))
    cv.fill_rect(gx + 4, gy - 2, 44, 6, (150, 130, 100))


def draw_eu_scene(cv, x, y, w, h):
    """Bank building with a severed cable: cut from SWIFT."""
    cv.fill_rect(x, y, w, h, (214, 226, 238))
    # Bank building, left-centre.
    bx, by = x + 16, y + 14
    cv.polygon([(bx, by + 20), (bx + 82, by), (bx + 164, by + 20)], (120, 128, 150))
    cv.fill_rect(bx, by + 20, 164, 8, (100, 108, 130))
    for i in range(4):
        colx = bx + 10 + i * 40
        cv.fill_rect(colx, by + 28, 16, 48, WHITE)
        cv.fill_rect(colx - 3, by + 24, 22, 5, (200, 200, 200))
        cv.fill_rect(colx - 3, by + 76, 22, 5, (200, 200, 200))
    cv.fill_rect(bx, by + 80, 164, 8, (100, 108, 130))
    cv.fill_rect(bx + 66, by + 52, 32, 28, (60, 60, 70))
    # Cable from the bank to a small pylon, severed mid-span.
    cv.line(x + 200, y + 30, x + 248, y + 44, INK, 3)
    cv.line(x + 292, y + 58, x + 320, y + 66, INK, 3)
    # Cut ends: frayed tips + red X marks.
    cv.line(x + 248, y + 44, x + 256, y + 52, RED, 3)
    cv.line(x + 292, y + 58, x + 284, y + 66, RED, 3)
    cv.line(x + 258, y + 34, x + 282, y + 58, RED, 4)
    cv.line(x + 282, y + 34, x + 258, y + 58, RED, 4)
    # Sparks at the cut.
    cv.line(x + 268, y + 26, x + 272, y + 18, GOLD, 3)
    cv.line(x + 276, y + 30, x + 284, y + 24, GOLD, 3)
    cv.line(x + 262, y + 44, x + 256, y + 52, GOLD, 3)
    # Pylon on the right.
    px = x + w - 40
    cv.line(px, y + h - 24, px, y + 40, INK, 3)
    cv.line(px - 16, y + 52, px + 16, y + 52, INK, 3)
    cv.line(px - 12, y + 66, px + 12, y + 66, INK, 3)


# ------------------------------------------------------------- panel frame --
def draw_panel(cv, x, y, w, h, scene_fn, headline, subhead, scene_h=76):
    # scene_h 76 fits a 1-line headline + 4-line subhead inside a 180 px
    # panel (text ends 5 px above the inner bottom edge). Row-2 panels
    # pass 100: their subheads are only 2 lines and their scenes are
    # drawn for a 100 px box.
    cv.fill_rect(x, y, w, h, WHITE)
    cv.draw_rect(x, y, w, h, INK, 2)
    scene_fn(cv, x + 3, y + 3, w - 6, scene_h)
    cv.fill_rect(x + 3, y + 3 + scene_h, w - 6, 2, INK)
    ty = y + 3 + scene_h + 10
    # Headline, scale 2, wrapped to fit.
    for line in wrap_text(headline, w - 20, 2):
        cv.draw_text(x + 10, ty, line, 2, INK)
        ty += 17
    ty += 2
    # Subhead, scale 2, wrapped to fit.
    for line in wrap_text(subhead, w - 20, 2):
        cv.draw_text(x + 10, ty, line, 2, (60, 58, 52))
        ty += 17


# ------------------------------------------------------------------- main --
def main():
    cv = Canvas(W, H, PAPER)
    cv.draw_rect(0, 0, W, H, INK, 4)

    # ---- masthead ----
    cv.draw_text_centered(W // 2, 22, "THE WORLD TODAY", 7, INK)
    cv.fill_rect(60, 82, W - 120, 3, INK)
    cv.draw_text_centered(W // 2, 90, "TUESDAY 24 NOVEMBER 2026", 2, INK)
    cv.fill_rect(16, 112, W - 32, 2, INK)
    cv.fill_rect(16, 117, W - 32, 1, INK)

    # ---- lead panel ----
    lx, ly, lw, lh = 16, 124, W - 32, 436
    cv.fill_rect(lx, ly, lw, lh, WHITE)
    cv.draw_rect(lx, ly, lw, lh, INK, 3)
    scene_h = 330
    draw_lead_scene(cv, lx + 3, ly + 3, lw - 6, scene_h)
    cv.fill_rect(lx + 3, ly + 3 + scene_h, lw - 6, 3, INK)
    cap_y = ly + 3 + scene_h + 12
    cv.draw_text(lx + 14, cap_y, "RUSSIAN DRONE OVER POLAND", 4, RED)
    cv.draw_text(lx + 14, cap_y + 38,
                 "RECON DRONE ENTERS POLISH AIRSPACE NEAR DOROHUSK; "
                 "TRACKED, NOT SHOT DOWN", 2, INK)

    # ---- grid of five story panels ----
    gap = 10
    row1_y, row1_h = 572, 180
    row2_y, row2_h = 762, 180
    pw3 = (W - 32 - 2 * gap) // 3          # 324
    pw2 = (W - 32 - gap) // 2              # 491
    panels = [
        (16, row1_y, pw3, row1_h, draw_talks_scene,
         "FOUR-WAY TALKS URGED",
         "ZELENSKY: UKRAINE, RUSSIA, US AND EUROPE SHOULD MEET AS SOON AS POSSIBLE"),
        (16 + pw3 + gap, row1_y, pw3, row1_h, draw_megaspeed_scene,
         "US BLACKLISTS MEGASPEED",
         "SINGAPORE CHIP FIRM AND SIX AFFILIATES PUT ON ENTITY LIST OVER NVIDIA CHIPS"),
        (16 + 2 * (pw3 + gap), row1_y, pw3, row1_h, draw_quake_scene,
         "QUAKE SHAKES NEPAL",
         "MAGNITUDE 5.6 TREMOR HITS KOSHI PROVINCE NEAR THE CHINA BORDER"),
        (16, row2_y, pw2, row2_h, draw_grok_scene,
         "STATES SUE SPACEX OVER GROK",
         "OREGON AND VIRGINIA SUE OVER GROK'S SEXUALISED IMAGES OF REAL PEOPLE"),
        (16 + pw2 + gap, row2_y, pw2, row2_h, draw_eu_scene,
         "EU CUTS 60 BANKS",
         "VON DER LEYEN PROPOSES 22ND SANCTIONS PACKAGE CUTTING BANKS FROM SWIFT"),
    ]
    for (px, py, pwid, ph, fn, head, sub) in panels:
        # Row 1 (4-line subheads) gets the 76 px scene; row 2 (2-line
        # subheads, scenes drawn for a taller box) keeps 100 px.
        draw_panel(cv, px, py, pwid, ph, fn, head, sub,
                   scene_h=100 if py == row2_y else 76)

    # ---- market ticker strip ----
    ty0, th = 952, 58
    cv.fill_rect(16, ty0, W - 32, th, DARK_BLUE)
    cv.draw_rect(16, ty0, W - 32, th, INK, 2)
    ticker = ("MARKETS RALLY: S&P 500 +4.7%  NASDAQ +6.5%  "
              "NIKKEI +3.9%  BRENT $86.7")
    cv.draw_text_centered(W // 2, ty0 + 20, ticker, 2, WHITE)

    data = encode_png(cv)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes, %dx%d)" % (out_path, len(data), W, H))
    return 0


if __name__ == "__main__":
    sys.exit(main())
