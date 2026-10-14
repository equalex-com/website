"""Builds EquaLex logo SVGs: traced figure + Source Serif 4 Semibold lettering as outlines."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

D = sys.argv[1]
font = TTFont(D + "/source-serif-4-latin-600-normal.woff2")
gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font["head"].unitsPerEm
TRACK = -0.04  # em, slightly tight like the original

def text_path(s, x, baseline, size):
    sc = size / upm; pen = SVGPathPen(gs); cx = x
    for ch in s:
        gn = cmap[ord(ch)]
        tp = TransformPen(pen, (sc, 0, 0, -sc, cx, baseline))
        gs[gn].draw(tp)
        cx += gs[gn].width * sc + TRACK * size
    return pen.getCommands(), cx - TRACK * size

def ink_width(s, size):
    _, end = text_path(s, 0, 0, size); return end

figure = open(sys.argv[3]).read()

# Original layout (crop space): Equa starts x=61.5 baseline 123.8; Lex starts ~x=208 baseline 138.7; Equa ink width ~149
size = 73.3 * 149 / ink_width("Equa", 73.3)
equa_d, equa_end = text_path("Equa", 61.5, 123.8, size)
lex_d, lex_end = text_path("Lex", equa_end + 0.06 * size, 138.7, size)

VB = "0 0 400 150"
def svg(fig, equa, lex, title="EquaLex"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" role="img" aria-label="{title}">
<title>{title}</title>
<path fill="{fig}" d="{figure}"/>
<path fill="{equa}" d="{equa_d}"/>
<path fill="{lex}" d="{lex_d}"/>
</svg>
'''
out = sys.argv[2]
open(out + "/equalex-logo-on-dark.svg", "w").write(svg("#d9b866", "#f3f1ea", "#c3cad8"))
open(out + "/equalex-logo-on-light.svg", "w").write(svg("#a8842c", "#13233f", "#5b6578"))
# inline fragment for the site header (colours from CSS)
open(out + "/inline.txt", "w").write(
f'<svg class="logo" viewBox="{VB}" aria-hidden="true" focusable="false">'
f'<path class="logo-figure" d="{figure}"/><path class="logo-equa" d="{equa_d}"/><path class="logo-lex" d="{lex_d}"/></svg>')
print("size", round(size,1), "lex end", round(lex_end,1))
