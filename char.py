#!/usr/bin/env python3

import cairo
import operator
from math import ceil
from random import randint
from functools import reduce

ROWS       = 32
COLS       = 64
X_SIZE     = 2
Y_SIZE     = 2
BLOCK_BITS = 6

SCALE      = 10
BORDER     = 200
X_SPACE    = 40
Y_SPACE    = 60

def genChar():

    while True:
        length = (BLOCK_BITS - 2) * X_SIZE // 2 * Y_SIZE + X_SIZE // 2 + Y_SIZE
        char = randint(0, 2**length - 1) & randint(0, 2**length - 1)

        if char not in chars:
            print('create new block {:0{:d}x}'.format(char, int(ceil(length / 4))))
            return char

        print('collision block {:0{:d}x}'.format(char, int(ceil(length / 4))))


def drawBlock(block, x_offset, y_offset, leftEdge=False, topEdge=False, mirror=False):

    x = -1 if mirror else 1

    if leftEdge: 
        if block & 1:
            drawLine((0, 0), (0, 1), x_offset, y_offset)
        block >>= 1

    if topEdge:
        if block & 1:
            drawLine((0, 0), (x, 0), x_offset, y_offset)
        block >>= 1

    if block & 1:
        drawLine((0, 1), (x, 1), x_offset, y_offset)
    if block & 2:
        drawLine((x, 0), (x, 1), x_offset, y_offset)
    if block & 4:
        drawLine((0, 0), (x, 1), x_offset, y_offset)
    if block & 8:
        drawLine((0, 1), (x, 0), x_offset, y_offset)


def drawLine(a, b, x_offset, y_offset):
    context.move_to(x_offset + a[0] * SCALE, y_offset + a[1] * SCALE)
    context.line_to(x_offset + b[0] * SCALE, y_offset + b[1] * SCALE)


def drawChar(x_offset, y_offset, char=None):

    if char is None:
        char = genChar()

    for x in range(X_SIZE // 2):
        for y in range(Y_SIZE):

            length = 5 if x == 0 else 4
            length = length + 1 if y == 0 else length
            block = char & (2**length - 1)
            char >>= length

            drawBlock(block, x_offset + x * SCALE, y_offset + y * SCALE, 
                leftEdge=(x == 0), topEdge=(y == 0))
            drawBlock(block, x_offset - x * SCALE, y_offset + y * SCALE, 
                leftEdge=(x == 0), topEdge=(y == 0), mirror=True)


chars = []
surface = cairo.PDFSurface("map.pdf",
                           COLS * X_SIZE * SCALE + (COLS - 1) * X_SPACE + 2 * BORDER,
                           ROWS * Y_SIZE * SCALE + (ROWS - 1) * Y_SPACE + 2 * BORDER)

context = cairo.Context(surface)
context.set_line_cap(cairo.LineCap.ROUND)

context.set_font_size(15)
context.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

# for x in range(COLS):
#     for y in range(ROWS):
#         drawChar(BORDER + X_SIZE // 2 * SCALE + x * (X_SIZE * SCALE + X_SPACE),
#                  BORDER + y * (Y_SIZE * SCALE + Y_SPACE))

i = 0

for y in range(ROWS):
    for x in range(COLS):
        
        drawChar(BORDER + X_SIZE // 2 * SCALE + x * (X_SIZE * SCALE + X_SPACE),
                 BORDER + y * (Y_SIZE * SCALE + Y_SPACE), char=i)

        text = '0x{:03X}'.format(i)
        _, _, textwidth, _, _, _ = context.text_extents(text)

        context.move_to(
            BORDER + x * (X_SIZE * SCALE + X_SPACE) + X_SIZE * SCALE // 2 - textwidth // 2,
            BORDER + y * (Y_SIZE * SCALE + Y_SPACE) + Y_SIZE * SCALE + Y_SPACE // 2)

        context.show_text(text)
        i += 1


context.stroke()
surface.finish()
