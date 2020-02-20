#!/usr/bin/env python3

import cairo
from glyphs import Glyphs

X_SIZE  = 4
Y_SIZE  = 6
ROWS    = 64
COLS    = 50
SCALE   = 10
BORDER  = 400
X_SPACE = 50
Y_SPACE = 50


surface = cairo.PDFSurface("matrix.pdf",
                           COLS * X_SIZE * SCALE + (COLS - 1) * X_SPACE + 2 * BORDER,
                           ROWS * Y_SIZE * SCALE + (ROWS - 1) * Y_SPACE + 2 * BORDER)

context = cairo.Context(surface)
glyphs = Glyphs(context, X_SIZE, Y_SIZE, SCALE)

context.set_line_cap(cairo.LineCap.ROUND)

for x in range(COLS):
    for y in range(ROWS):
        glyphs.drawGlyph(BORDER + X_SIZE // 2 * SCALE + x * (X_SIZE * SCALE + X_SPACE),
                         BORDER + y * (Y_SIZE * SCALE + Y_SPACE))

context.stroke()
surface.finish()