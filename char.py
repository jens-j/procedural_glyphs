#!/usr/bin/env python3.6

import cairo
from random import random

ROWS   = 9
COLS   = 8
X_SIZE = 4
Y_SIZE = 6

SCALE  = 10
BORDER = 20

def genBlock():

    lines = []

    if random() < 0.25:
        lines.append(((0, 0), (0, 1)))
    if random() < 0.25:
        lines.append(((0, 0), (1, 0)))
    if random() < 0.25:
        lines.append(((0, 1), (1, 1)))
    if random() < 0.25:
        lines.append(((1, 0), (1, 1)))
    if random() < 0.25:
        lines.append(((0, 0), (1, 1)))
    if random() < 0.25:
        lines.append(((0, 1), (1, 0)))

    return lines


def mirror(lines):

    return [((-1 * i, j), (-1 * k, l)) for ((i, j), (k, l)) in lines]


def drawBlock(lines, x_offset, y_offset):

    for a, b in lines:
        context.move_to(x_offset + a[0] * SCALE, y_offset + a[1] * SCALE)
        context.line_to(x_offset + b[0] * SCALE, y_offset + b[1] * SCALE)


def drawChar(x_offset, y_offset):

    for x in range(X_SIZE // 2):
        for y in range(Y_SIZE):

            lines = genBlock()
            drawBlock(lines, x_offset + x * SCALE, y_offset + y * SCALE)
            drawBlock(mirror(lines), x_offset - x * SCALE, y_offset + y * SCALE)

surface = cairo.PDFSurface("test.pdf",
                           COLS * X_SIZE * SCALE + (COLS + 1) * BORDER,
                           ROWS * Y_SIZE * SCALE + (ROWS + 1) * BORDER)
context = cairo.Context(surface)
context.set_line_cap(cairo.LineCap.ROUND)

for x in range(COLS):
    for y in range(ROWS):
        drawChar(2 * BORDER + x * (X_SIZE * SCALE + BORDER),
                 BORDER + y * (Y_SIZE * SCALE + BORDER))

#drawChar(100, 20)


context.stroke()
surface.finish()
