#!/usr/bin/env python3

import cairo
from random import randint
from glyphs import Glyphs

X_SIZE  = 4
Y_SIZE  = 5
ROWS    = 1
COLS    = 500
SCALE   = 10
BORDER  = 300
X_SPACE = 40
Y_SPACE = 60

surface = cairo.PDFSurface("evolution.pdf",
                           COLS * X_SIZE * SCALE + (COLS - 1) * X_SPACE + 2 * BORDER,
                           ROWS * Y_SIZE * SCALE + (ROWS - 1) * Y_SPACE + 2 * BORDER)

context = cairo.Context(surface)
context.set_line_cap(cairo.LineCap.ROUND)

glyphs = Glyphs(context, X_SIZE, Y_SIZE, SCALE)

glyph = glyphs.genGlyph()

for y in range(ROWS):
    for x in range(COLS):

        glyphs.drawGlyph(BORDER + X_SIZE // 2 * SCALE + x * (X_SIZE * SCALE + X_SPACE),
                         BORDER + y * (Y_SIZE * SCALE + Y_SPACE), 
                         glyph=glyph)

        # xx = randint(0, X_SIZE // 2 - 1)
        # yy = randint(0, Y_SIZE - 1)
        # length = glyphs.getBitWidth(xx, yy)
        # startBit = glyphs.getStartBit(xx, yy)
        # mask = (2**length - 1) << startBit

        # oldBlock = (glyph & mask) >> startBit

        # while True:
        #     newBlock = randint(0, 2**length - 1) & randint(0, 2**length - 1)
        #     if newBlock != oldBlock:
        #         break

        # glyph &= ~mask
        # glyph |= newBlock << startBit

        print('')
        bit = randint(0, glyphs.getGlyphLength() - 1)
        print(bit)
        mask = 1 << bit
        print(hex(mask))
        print(hex(glyph))
        glyph = glyph ^ mask
        print(hex(glyph))



context.stroke()
surface.finish()