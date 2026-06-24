#!/usr/bin/env python3
"""
plot_fig07.py  -  Clean re-plot of Figure 7
"Integrated Soil Ecosystem Service (SES) Modelling Framework" +
"Workflow for Soil Pollution Risk Assessment".

Pure schematic (boxes / sub-boxes / text / connectors only) in a clean
rounded-card style.  Palette: matplotlib tab20c.  Block heights are driven by
their content so every block is compact (minimal empty space) and fonts are
large.  Spelling fixed per the MDPI proof comments.

Output: Fig_07.png      Requires: matplotlib, numpy
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib import cm

plt.rcParams["font.family"] = "DejaVu Sans"

# ----------------------------------------------------------------- tab20c palette
_t = [tuple(int(round(c * 255)) for c in cm.tab20c(i)[:3]) for i in range(20)]
def _hex(rgb): return "#%02x%02x%02x" % rgb
def shade(rgb, f): return _hex(tuple(int(c * f) for c in rgb))
def tint(rgb, t):  return _hex(tuple(int(c + (255 - c) * t) for c in rgb))
def fam(i0, i1, i3):
    return (_hex(_t[i3]), _hex(_t[i1]), shade(_t[i0], 0.82),
            shade(_t[i0], 0.70), tint(_t[i3], 0.55))
BLUE   = fam(0, 1, 3)
ORANGE = fam(4, 5, 7)
GREEN  = fam(8, 9, 11)
PURPLE = fam(12, 13, 15)
GRAY   = fam(16, 17, 19)
INK    = "#1f1f1f"
STEP_PAL = [BLUE, ORANGE, GREEN, PURPLE, GRAY, BLUE]

# ----------------------------------------------------------------- scale helpers
W = 2000
FIGW = 20.0
DP = W / (FIGW * 72.0)
def line_h(fs, mult=1.5): return fs * mult * DP
def wrap_to(text, box_w, fs, side=28, cwf=0.515):
    maxc = max(4, int((box_w - side) / (fs * cwf * DP)))
    return textwrap.wrap(text, maxc)

def panel(ax, x, y, w, h, fill, edge, lw=2.0, r=14):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0,rounding_size={r}",
                 linewidth=lw, edgecolor=edge, facecolor=fill, zorder=2))
def arrow(ax, p0, p1, color="#7a7a7a", lw=2.6, mut=20):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=mut,
                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=6))
def title_block(ax, cx, top, title, fs, color, tlh=1.4):
    tl = title.split("\n")
    for i, t in enumerate(tl):
        ax.text(cx, top - i*line_h(fs, tlh), t, ha="center", va="top",
                fontsize=fs, fontweight="bold", color=color, zorder=5)
    return top - len(tl)*line_h(fs, tlh) - 4

# ----------------------------------------------------------------- content (corrected)
ENV_VARS = ["Climate", "Geology", "Topography", "Hydrology", "Vegetation", "Human activities"]
SOIL_PROPS = ("Type, mineralogy, T, soil profile depth, water table, texture, "
              "density, porosity, organic matter, carbon, N content, pH, infiltration")
SOIL_FUNC = ["Biodiversity", "Human activities", "Carbon pool", "Raw materials",
             "Biomass production", "Essential nutrients", "Water regulator"]
PROVISION = ["Food", "Fiber", "Fuel", "Wood", "Wood", "Raw materials", "Physical support"]
REGULATE  = ["Nutrient level", "Flood control", "Erosion control", "Climate regulation",
             "Carbon storage", "Carbon storage", "Waste decomposition"]
CULTURAL  = ["Aesthetic", "Historical knowledge", "Geographic place", "Geographic place",
             "Archaeology", "Heritage values", "Land identity"]
STEPS = [
    ("1. DETECTION OF POLLUTION SOURCES",
     ["Measure initial conditions: Hotspot mapping (QGIS)",
      "Laboratory analysis: Existing soil samples (heavy metals, pH, etc.)",
      "Principal Component Analysis (PCA): Assessing spatial distribution"]),
    ("2. MODELLING THE BEHAVIOUR OF POLLUTANTS",
     ["Geochemical and dynamic models (mass balance)",
      "Data: Accumulation and attenuation rates",
      "Predict pollutant trends over time"]),
    ("3. PREDICTIVE SCENARIO TESTING",
     ["Scenarios: Default, Optimistic, Pessimistic",
      "Pathway to food chain: Pollutant uptake in soil vs. plant absorption"]),
    ("4. EVALUATING ECOSYSTEM RISK",
     ["Models: $E_f$ and $I_{geo}$ indices, PERI",
      "Soil quality impacts: Heavy metals on soil structure, porosity, "
      "water capacity, erosion potential"]),
    ("5. MULTI-FACTOR ANALYSIS",
     ["Integrated risk assessment", "Fields and natural forest stands",
      "Uncertainty analysis: Monte Carlo simulation"]),
    ("6. PREDICTION AND ENVIRONMENTAL MANAGEMENT",
     ["Remote sensing & time series analysis",
      "Forecasting soil health, biodiversity, food safety",
      "Effective remediation & regulatory policies"]),
]
TABLE_HEAD = ["Model", "Characteristics", "Advantages", "Limitations", "Examples"]
TABLE_ROWS = [
    ("Process-based", "Process-based", "Mechanistic; represents the underlying processes",
     "Data-intensive; complex to parameterise", "Universal Soil Loss Equation (USLE)", GREEN),
    ("Empirical", "Empirical-based", "Simple; based on observed data relationships",
     "Limited transferability beyond calibration range", "Life Cycle Assessment (LCA)", BLUE),
    ("Composite", "Composite-based", "Combines process and empirical strengths",
     "Higher data and computational demands", "Life Cycle Assessment (LCA)", ORANGE),
    ("Statistical", "Statistical-based", "Data-driven; quantifies uncertainty",
     "Needs large datasets; correlation is not causation",
     "Life-Cycle Assessment (LCA); vine copulas", PURPLE),
]

# ----------------------------------------------------------------- fonts (pt)
F_MAIN, F_HEAD, F_CTITLE = 18, 15.5, 13.5
F_BODY = 12.0
F_STITLE, F_SBODY = 12.5, 11.5
F_THEAD, F_TCELL = 12.5, 11.0

# ----------------------------------------------------------------- renderers
def _rule(ax, cx, y, w, frac=0.72):
    ax.add_line(Line2D([cx-w*frac/2, cx+w*frac/2], [y, y], color="#ffffff", lw=1.5, zorder=5))

def list_card(ax, x, y, w, h, pal, title, items, *, fs_t=F_CTITLE, fs_b=F_BODY,
              fill_v=False, top_pad=14, bot_pad=14):
    panel(ax, x, y, w, h, pal[0], pal[1], lw=1.8, r=11)
    cx = x + w/2; top = y + h - top_pad
    ty = title_block(ax, cx, top, title, fs_t, pal[2]); _rule(ax, cx, ty, w); ty -= 12
    body_bottom = y + bot_pad; n = len(items)
    if fill_v:
        slot = (ty - body_bottom)/n
        for k, it in enumerate(items):
            ax.text(cx, ty - slot*(k+0.5), it, ha="center", va="center",
                    fontsize=fs_b, color=pal[3], zorder=5)
    else:
        gap = line_h(fs_b, 1.5)
        for it in items:
            ax.text(cx, ty, it, ha="center", va="top", fontsize=fs_b, color=pal[3], zorder=5)
            ty -= gap

def wrap_card(ax, x, y, w, h, pal, title, lines, *, fs_t=F_CTITLE, fs_b=F_BODY, top_pad=14):
    panel(ax, x, y, w, h, pal[0], pal[1], lw=1.8, r=11)
    cx = x + w/2; top = y + h - top_pad
    ty = title_block(ax, cx, top, title, fs_t, pal[2]); _rule(ax, cx, ty, w); ty -= 12
    for ln in lines:
        ax.text(cx, ty, ln, ha="center", va="top", fontsize=fs_b, color=pal[3], zorder=5)
        ty -= line_h(fs_b, 1.32)

def step_card(ax, x, y, w, h, pal, title, bullets, *, fs_t=F_STITLE, fs_b=F_SBODY):
    panel(ax, x, y, w, h, pal[0], pal[1], lw=1.8, r=12)
    cx = x + w/2; top = y + h - 14
    twrap = "\n".join(textwrap.wrap(title, 26))
    ty = title_block(ax, cx, top, twrap, fs_t, pal[2]); _rule(ax, cx, ty, w, 0.86); ty -= 13
    for b in bullets:
        sub = wrap_to(b, w, fs_b, side=46)
        ax.text(x+16, ty+0.5, "\u2022", ha="left", va="top", fontsize=fs_b, color=pal[1], zorder=5)
        for s in sub:
            ax.text(x+32, ty, s, ha="left", va="top", fontsize=fs_b, color=pal[3], zorder=5)
            ty -= line_h(fs_b, 1.3)
        ty -= line_h(fs_b, 0.28)

# ----------------------------------------------------------------- height estimates
def list_card_h(title, items, fs_t=F_CTITLE, fs_b=F_BODY, tp=14, bp=14):
    tl = len(title.split("\n"))
    return tp + tl*line_h(fs_t,1.4) + 4 + 12 + len(items)*line_h(fs_b,1.5) + bp
def wrap_card_h(title, lines, fs_t=F_CTITLE, fs_b=F_BODY, tp=14, bp=14):
    tl = len(title.split("\n"))
    return tp + tl*line_h(fs_t,1.4) + 4 + 12 + len(lines)*line_h(fs_b,1.32) + bp
def step_card_h(title, bullets, w, fs_t=F_STITLE, fs_b=F_SBODY):
    tl = len(textwrap.wrap(title, 26)); h = 14 + tl*line_h(fs_t,1.4) + 4 + 13
    for b in bullets:
        n = len(wrap_to(b, w, fs_b, side=46)); h += n*line_h(fs_b,1.3) + line_h(fs_b,0.28)
    return h + 14

# ============================================================ LAYOUT
PADC, GAPX = 16, 16
LX, LW = 26, 706
lcw = (LW - 2*PADC - 2*GAPX)/3
lc = [LX+PADC, LX+PADC+lcw+GAPX, LX+PADC+2*(lcw+GAPX)]
env_props_lines = wrap_to(SOIL_PROPS, lcw, F_BODY, side=24)
h_env_card = max(list_card_h("X\nY", ENV_VARS), wrap_card_h("X\nY", env_props_lines),
                 list_card_h("X\nY", SOIL_FUNC))
HEAD_H = line_h(F_HEAD,1.4) + 18
env_panel_h = PADC + HEAD_H + h_env_card + PADC

RX, RW = 752, 1222
scw = (RW - 2*PADC - 2*GAPX)/3
sc = [RX+PADC, RX+PADC+scw+GAPX, RX+PADC+2*(scw+GAPX)]
row1_h = max(step_card_h(t,b,scw) for t,b in STEPS[:3])
row2_h = max(step_card_h(t,b,scw) for t,b in STEPS[3:])
TW = RW - 2*PADC
colw = [150, 188, 322, 300, TW-(150+188+322+300)]
thead_h = line_h(F_THEAD,1.4) + 14
def cell_lines(txt, cw): return max(1, len(wrap_to(txt, cw, F_TCELL, side=20)))
trow_h = []
for r in TABLE_ROWS:
    mx = max(cell_lines(r[1],colw[1]), cell_lines(r[2],colw[2]),
             cell_lines(r[3],colw[3]), cell_lines(r[4],colw[4]))
    trow_h.append(mx*line_h(F_TCELL,1.25) + 16)
table_h = thead_h + sum(trow_h)
ARROWGAP_V, TABLE_GAP = 46, 30
right_panel_h = PADC + HEAD_H + row1_h + ARROWGAP_V + row2_h + TABLE_GAP + table_h + PADC

TOP_TITLE = 56
H = right_panel_h + TOP_TITLE + 40
fig_top = H - TOP_TITLE - 20
env_top = fig_top; env_bot = env_top - env_panel_h
ses_top = env_bot - 78
right_top = fig_top; right_bot = right_top - right_panel_h
ses_bot = right_bot
ses_panel_h = ses_top - ses_bot

# ============================================================ DRAW
fig = plt.figure(figsize=(FIGW, FIGW*H/W), dpi=200)
ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H)
ax.set_aspect("equal"); ax.axis("off"); fig.patch.set_facecolor("white")
ty_title = H - TOP_TITLE/2 - 6
ax.text(LX+LW/2, ty_title, "INTEGRATED SOIL ECOSYSTEM SERVICE (SES) MODELLING FRAMEWORK",
        ha="center", va="center", fontsize=F_MAIN, fontweight="bold", color=INK)
ax.text(RX+RW/2, ty_title, "WORKFLOW FOR SOIL POLLUTION RISK ASSESSMENT",
        ha="center", va="center", fontsize=F_MAIN, fontweight="bold", color=INK)

panel(ax, LX, env_bot, LW, env_panel_h, PURPLE[4], PURPLE[1], lw=2.2, r=16)
ax.text(LX+LW/2, env_top-PADC-line_h(F_HEAD,0.7), "ENVIRONMENTAL PARAMETERS",
        ha="center", va="center", fontsize=F_HEAD, fontweight="bold", color=PURPLE[2])
cy = env_top - PADC - HEAD_H - h_env_card
list_card(ax, lc[0], cy, lcw, h_env_card, PURPLE, "ENVIRONMENTAL\nVARIABLES", ENV_VARS, fill_v=True)
wrap_card(ax, lc[1], cy, lcw, h_env_card, PURPLE, "SOIL\nPROPERTIES", env_props_lines)
list_card(ax, lc[2], cy, lcw, h_env_card, PURPLE, "SOIL\nFUNCTIONS", SOIL_FUNC, fill_v=True)

panel(ax, LX, ses_bot, LW, ses_panel_h, ORANGE[4], ORANGE[1], lw=2.2, r=16)
ax.text(LX+LW/2, ses_top-PADC-line_h(F_HEAD,0.7), "SOIL ECOSYSTEM SERVICES (SES)",
        ha="center", va="center", fontsize=F_HEAD, fontweight="bold", color=ORANGE[2])
ses_card_h = ses_panel_h - PADC - HEAD_H - PADC
syc = ses_bot + PADC
list_card(ax, lc[0], syc, lcw, ses_card_h, ORANGE, "PROVISIONING\nPRODUCTS", PROVISION, fill_v=True)
list_card(ax, lc[1], syc, lcw, ses_card_h, ORANGE, "REGULATING\nAND CONTROL", REGULATE, fill_v=True)
list_card(ax, lc[2], syc, lcw, ses_card_h, ORANGE, "CULTURAL &\nHISTORICAL", CULTURAL, fill_v=True)

panel(ax, RX, right_bot, RW, right_panel_h, GREEN[4], GREEN[1], lw=2.4, r=18)
ax.text(RX+RW/2, right_top-PADC-line_h(F_HEAD,0.7), "SES MODELLING & MANAGEMENT",
        ha="center", va="center", fontsize=F_HEAD, fontweight="bold", color=GREEN[2])
r1_top = right_top - PADC - HEAD_H; r1_bot = r1_top - row1_h
r2_top = r1_bot - ARROWGAP_V;       r2_bot = r2_top - row2_h
for i in range(3): step_card(ax, sc[i], r1_bot, scw, row1_h, STEP_PAL[i], *STEPS[i])
for i in range(3): step_card(ax, sc[i], r2_bot, scw, row2_h, STEP_PAL[i+3], *STEPS[i+3])

tbx = RX + PADC; tb_top = r2_bot - TABLE_GAP; tb_bot = tb_top - table_h
panel(ax, tbx, tb_bot, TW, table_h, GRAY[4], GRAY[1], lw=1.6, r=8)
edges = [tbx]
for c in colw: edges.append(edges[-1]+c)
for i, htxt in enumerate(TABLE_HEAD):
    ax.text((edges[i]+edges[i+1])/2, tb_top-thead_h/2, htxt, ha="center", va="center",
            fontsize=F_THEAD, fontweight="bold", color="#33312a", zorder=5)
ax.add_line(Line2D([tbx,tbx+TW],[tb_top-thead_h,tb_top-thead_h], color="#ffffff", lw=1.6, zorder=5))
yrow = tb_top - thead_h
for ridx, row in enumerate(TABLE_ROWS):
    model, char, adv, lim, ex, pal = row; rh = trow_h[ridx]; ry = yrow - rh
    panel(ax, tbx, ry, colw[0], rh, pal[0], pal[1], lw=0.0, r=6)
    ax.text((edges[0]+edges[1])/2, ry+rh/2, model, ha="center", va="center",
            fontsize=F_TCELL, fontweight="bold", color=pal[2], zorder=5)
    for i, txt in enumerate([char,adv,lim,ex], start=1):
        lines = wrap_to(txt, colw[i], F_TCELL, side=18); n=len(lines); lh0=line_h(F_TCELL,1.25)
        sy = ry+rh/2 + (n-1)*0.5*lh0
        for k, s in enumerate(lines):
            ax.text(edges[i]+10, sy-k*lh0, s, ha="left", va="center",
                    fontsize=F_TCELL, color="#3a3a3a", zorder=5)
    yrow = ry
for xe in edges[1:-1]:
    ax.add_line(Line2D([xe,xe],[tb_bot,tb_top-thead_h], color="#ffffff", lw=1.2, zorder=4))
yy = tb_top - thead_h
for ridx in range(len(TABLE_ROWS)-1):
    yy -= trow_h[ridx]
    ax.add_line(Line2D([tbx,tbx+TW],[yy,yy], color="#ffffff", lw=1.2, zorder=4))

# ============================================================ ARROWS
GREY = "#7d7d7d"
cymid = cy + h_env_card/2
arrow(ax, (lc[0]+lcw, cymid), (lc[1], cymid), color=GREY, lw=2.2)
arrow(ax, (lc[1]+lcw, cymid), (lc[2], cymid), color=GREY, lw=2.2)
arrow(ax, (LX+LW/2, env_bot), (LX+LW/2, ses_top), color=GREY, lw=2.8, mut=22)
arrow(ax, (LX+LW, r1_bot+row1_h/2), (RX, r1_bot+row1_h/2), color=GREY, lw=2.6, mut=22)
arrow(ax, (LX+LW, r2_bot+row2_h/2), (RX, r2_bot+row2_h/2), color=GREY, lw=2.6, mut=22)
arrow(ax, (sc[0]+scw, r1_bot+row1_h/2), (sc[1], r1_bot+row1_h/2), color=GREY, lw=2.2)
arrow(ax, (sc[1]+scw, r1_bot+row1_h/2), (sc[2], r1_bot+row1_h/2), color=GREY, lw=2.2)
arrow(ax, (sc[0]+scw, r2_bot+row2_h/2), (sc[1], r2_bot+row2_h/2), color=GREY, lw=2.2)
arrow(ax, (sc[1]+scw, r2_bot+row2_h/2), (sc[2], r2_bot+row2_h/2), color=GREY, lw=2.2)
arrow(ax, (sc[2]+scw/2, r1_bot), (sc[2]+scw/2, r2_top), color=GREY, lw=2.2)

fig.savefig("Fig_07.png", dpi=300, facecolor="white", bbox_inches="tight", pad_inches=0.14)
print("saved H=%d right_h=%d env_h=%d ses_h=%d" % (H, right_panel_h, env_panel_h, ses_panel_h))
