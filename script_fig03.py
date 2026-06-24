#!/usr/bin/env python3
"""
edit_fig03.py
=============
Raster post-processing pipeline for Figure 3 ("Major Sources and Ecological
Impact of Pesticides in Soils") of manuscript environremediat-4365955.

IMPORTANT / HONEST NOTE
-----------------------
This is NOT a plotting / figure-generation script. Figure 3 was supplied as a
finished PNG raster (3920 x 2200). No original vector/plotting source was
available, so every change below is performed by editing pixels of that raster:

  1. Delete every author-year reference label at the bottom of each block
     (Zone 1 green source blocks, Zone 3 red outcome blocks, Zone 2 "D" blocks).
  2. Spelling revisions requested by MDPI:
        "volatilisation"   -> "volatilization"   (2 occurrences)
        "physico-chemical" -> "physicochemical"  (1 occurrence)
  3. Remove the black background (make it transparent).

Method notes
------------
* Deletions: the reference line is the bottom text line of a block. We locate it
  (by colour mask for the green Zone 1, by fixed y-bands for Zone 3 / Zone 2-D),
  then repaint that rectangle with the block's own background colour, which is
  estimated locally as the median of the "light" pixels surrounding the text.
* Spelling fixes: the figure font is matched to Liberation Sans
  (Bold for block titles, Regular for body text). The affected word/line is
  repainted with the local background and re-typeset, supersampled 4x for crisp
  anti-aliasing, centred on the original text centre and baseline. "s"->"z" keeps
  the same width; removing the hyphen in "physico-chemical" shortens the title,
  which is re-centred automatically.
* Background removal: a near-black mask is flood-filled (connected-component
  labelling) from the image borders so ONLY the connected background is removed;
  isolated dark pixels such as the dark-grey main title and the dark text inside
  the light panels are preserved.

Requires: pillow, numpy, scipy, and the Liberation fonts
          (Debian/Ubuntu package: fonts-liberation).
Usage:    python3 edit_fig03.py  Fig_03_original.png  Fig_03_corrected.png
"""

import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

# ----- font paths (Liberation Sans, metrically compatible with Arial) ---------
LIB_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
LIB_REG  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def local_bg(arr, x0, y0, x1, y1, light_min=620):
    """Median colour of the 'light' (background) pixels in a region."""
    reg = arr[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    light = reg[reg.sum(axis=1) > light_min]
    if len(light) < 10:
        light = reg[reg.sum(axis=1) > light_min - 100]
    return np.median(light, axis=0).astype(np.uint8)


def fill_bg(arr, x0, x1, y0, y1, pad=3, light_min=620):
    """Repaint rectangle [x0:x1, y0:y1] (+pad) with the locally sampled bg."""
    H, W = arr.shape[:2]
    yy0, yy1 = max(0, y0 - pad), min(H, y1 + pad + 1)
    xx0, xx1 = max(0, x0 - pad), min(W, x1 + pad + 1)
    arr[yy0:yy1, xx0:xx1] = local_bg(arr, xx0, yy0, xx1, yy1, light_min)


def render_centered(im, text, fp, size, cx, baseline, color, ss=4):
    """Typeset `text` centred on x=cx with its baseline at y=baseline.
    Rendered at `ss`x then down-sampled (Lanczos) for crisp small text."""
    measure = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    w = measure.textlength(text, font=ImageFont.truetype(fp, size))
    fs = ImageFont.truetype(fp, size * ss)
    asc, desc = fs.getmetrics()
    tw, th = int(w * ss) + 16 * ss, asc + desc + 8 * ss
    tile = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text((8 * ss, 4 * ss), text, font=fs,
                              fill=tuple(color) + (255,))
    tile = tile.resize((tw // ss, th // ss), Image.LANCZOS)
    bl = (4 * ss + asc) / ss
    im.paste(tile, (int(round(cx - w / 2 - 8)),
                    int(round(baseline - bl))), tile)


# ----------------------------------------------------------------------------
# 1. DELETE REFERENCES
# ----------------------------------------------------------------------------
def delete_references(arr):
    R, G, B = arr[:, :, 0].astype(int), arr[:, :, 1].astype(int), arr[:, :, 2].astype(int)

    # ---- Zone 1 (left, green source blocks): 8 refs --------------------------
    # The reference text is a lighter green than the body; mask greenish, non-bg.
    mask = (G > R) & (G > B + 15) & ((R + G + B) < 560)
    mask[:, :85] = False
    mask[:, 1100:] = False
    z1_blocks = [(90, 612), (665, 1090)]            # inner x of the two columns
    z1_bands  = [(384, 403), (604, 623), (824, 843), (1044, 1063)]  # 4 rows
    for (y0, y1) in z1_bands:
        for (bx0, bx1) in z1_blocks:
            sub = mask[y0:y1 + 1, bx0:bx1 + 1]
            if not sub.any():
                continue
            ys, xs = np.where(sub.any(axis=1))[0], np.where(sub.any(axis=0))[0]
            fill_bg(arr, bx0 + xs[0], bx0 + xs[-1], y0 + ys[0], y0 + ys[-1])

    # ---- Zone 3 (right, red outcome blocks): 6 refs --------------------------
    # body & reference reds are too close to mask reliably -> fixed y-bands.
    z3_bands = [(384, 399), (596, 611), (807, 827),
                (1020, 1035), (1232, 1247), (1444, 1459)]
    for (y0, y1) in z3_bands:
        sub = (arr[y0:y1 + 1, 2900:3780].sum(axis=2) < 600)   # any red text
        cols = np.where(sub.any(axis=0))[0]
        if len(cols):
            fill_bg(arr, 2900 + cols[0], 2900 + cols[-1], y0, y1, pad=2, light_min=640)

    # ---- Zone 2 block "D" (cream sub-blocks): 3 refs -------------------------
    y0, y1 = 1354, 1373
    for (xa, xb) in [(1395, 1705), (1765, 2130), (2200, 2535)]:
        sub = (arr[y0:y1, xa:xb].sum(axis=2) < 470)
        cols = np.where(sub.any(axis=0))[0]
        if len(cols):
            fill_bg(arr, xa + cols[0], xa + cols[-1], y0, y1, light_min=640)
    # "Yasir2025, Marcelino2024" is wide -> one extra sweep to clear its ends
    fill_bg(arr, 1355, 1706, 1348, 1380, pad=0, light_min=640)

    return arr


# ----------------------------------------------------------------------------
# 2. SPELLING REVISIONS
# ----------------------------------------------------------------------------
def fix_spelling(arr):
    im = Image.fromarray(arr)

    # Fix 1: "Drift and volatilisation" -> "...volatilization"  (Zone 2 block A)
    bg = tuple(int(c) for c in local_bg(np.asarray(im), 1360, 326, 1645, 331))
    ImageDraw.Draw(im).rectangle([1360, 327, 1645, 356], fill=bg)
    render_centered(im, "Drift and volatilization", LIB_BOLD, 25.5,
                    cx=1501.5, baseline=350, color=(65, 36, 2))

    # Fix 2: "Drift, volatilisation, rainfall" -> "...volatilization..."  (Zone 1)
    bg = tuple(int(c) for c in local_bg(np.asarray(im), 210, 535, 490, 538))
    ImageDraw.Draw(im).rectangle([210, 535, 490, 559], fill=bg)
    render_centered(im, "Drift, volatilization, rainfall", LIB_REG, 23.5,
                    cx=349, baseline=554, color=(59, 109, 17))

    # Fix 3: "Soil physico-chemical" -> "Soil physicochemical"  (Zone 2 block D)
    bg = tuple(int(c) for c in local_bg(np.asarray(im), 2265, 1238, 2540, 1243))
    ImageDraw.Draw(im).rectangle([2260, 1242, 2545, 1274], fill=bg)
    render_centered(im, "Soil physicochemical", LIB_BOLD, 25.5,
                    cx=2401, baseline=1264, color=(65, 36, 2))

    arr = np.asarray(im).copy()
    # tidy two faint single-pixel remnants below two Zone-3 reference bands
    for (cx, cy) in [(3303, 614), (3254, 1462)]:
        bg = local_bg(arr, cx - 30, cy - 12, cx + 30, cy - 4, light_min=640)
        arr[cy - 8:cy + 9, cx - 18:cx + 19] = bg
    return arr


# ----------------------------------------------------------------------------
# 3. REMOVE BLACK BACKGROUND  (-> transparent)
# ----------------------------------------------------------------------------
def remove_black_background(arr, thresh=40):
    black = arr.max(axis=2) < thresh                 # near-black mask
    lbl, _ = ndimage.label(black)                    # connected components
    border = (set(lbl[0, :]) | set(lbl[-1, :]) |
              set(lbl[:, 0]) | set(lbl[:, -1]))       # comps touching any edge
    border.discard(0)
    bg = np.isin(lbl, list(border))                  # = connected background
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    return np.dstack([arr, alpha])                   # RGBA


# ----------------------------------------------------------------------------
def main(src, dst):
    arr = np.array(Image.open(src).convert("RGB"))
    arr = delete_references(arr)
    arr = fix_spelling(arr)
    rgba = remove_black_background(arr)
    Image.fromarray(rgba, "RGBA").save(dst, optimize=True)
    print("saved", dst, rgba.shape)


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "Fig_03_original.png"
    dst = sys.argv[2] if len(sys.argv) > 2 else "Fig_03_corrected.png"
    main(src, dst)
