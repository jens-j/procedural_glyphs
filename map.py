#!/usr/bin/env python3

import cairo
from glyphs import Glyphs

X_SIZE  = 2
Y_SIZE  = 2
ROWS    = 32
COLS    = 64
SCALE   = 10
BORDER  = 300
X_SPACE = 40
Y_SPACE = 60


surface = cairo.PDFSurface("map.pdf",
                           COLS * X_SIZE * SCALE + (COLS - 1) * X_SPACE + 2 * BORDER,
                           ROWS * Y_SIZE * SCALE + (ROWS - 1) * Y_SPACE + 2 * BORDER)

context = cairo.Context(surface)
context.set_line_cap(cairo.LineCap.ROUND)
context.set_font_size(15)
context.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

glyphs = Glyphs(context, X_SIZE, Y_SIZE, SCALE)

for i in range(ROWS * COLS):

        y = i // COLS
        x = i % COLS
        
        glyphs.drawGlyph(BORDER + X_SIZE // 2 * SCALE + x * (X_SIZE * SCALE + X_SPACE),
                         BORDER + y * (Y_SIZE * SCALE + Y_SPACE), glyph=i)

        text = '0x{:03X}'.format(i)
        _, _, textwidth, _, _, _ = context.text_extents(text)

        context.move_to(
            BORDER + x * (X_SIZE * SCALE + X_SPACE) + X_SIZE * SCALE // 2 - textwidth // 2,
            BORDER + y * (Y_SIZE * SCALE + Y_SPACE) + Y_SIZE * SCALE + Y_SPACE // 2)

        context.show_text(text)

context.stroke()
surface.finish()