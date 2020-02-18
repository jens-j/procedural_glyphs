#!/usr/bin/env python3.6

import cairo
import operator
from random import randint
from functools import reduce

ROWS   = 50
COLS   = 40
X_SIZE = 4
Y_SIZE = 5

SCALE  = 10
BORDER = 100
SPACE  = 30

def genBlock():

    return randint(0, 0x3F) & randint(0, 0x3F)


def genChar():

    while True:
        blocks = [genBlock() for i in range(X_SIZE // 2 * Y_SIZE)]
        signature = reduce(operator.add, [x << (6 * i) for i, x in enumerate(blocks)])

        if signature not in signatures:
            signatures.append(signature)
            print('create new block {:x}'.format(signature))
            return blocks

        print('collision block {:x}'.format(signature))


def drawBlock(block, x_offset, y_offset, mirror=False):

    x = -1 if mirror else 1

    if block & 1:
        drawLine((0, 0), (0, 1), x_offset, y_offset)
    if block & 2:
        drawLine((0, 0), (x, 0), x_offset, y_offset)
    if block & 4:
        drawLine((0, 1), (x, 1), x_offset, y_offset)
    if block & 8:
        drawLine((x, 0), (x, 1), x_offset, y_offset)
    if block & 16:
        drawLine((0, 0), (x, 1), x_offset, y_offset)
    if block & 32:
        drawLine((0, 1), (x, 0), x_offset, y_offset)


def drawLine(a, b, x_offset, y_offset):
    context.move_to(x_offset + a[0] * SCALE, y_offset + a[1] * SCALE)
    context.line_to(x_offset + b[0] * SCALE, y_offset + b[1] * SCALE)


def drawChar(x_offset, y_offset):

    i = 0
    char = genChar()

    for x in range(X_SIZE // 2):
        for y in range(Y_SIZE):
            # block = genBlock()
            drawBlock(char[i], x_offset + x * SCALE, y_offset + y * SCALE)
            drawBlock(char[i], x_offset - x * SCALE, y_offset + y * SCALE, mirror=True)
            i += 1

signatures = []
surface = cairo.PDFSurface("chars.pdf",
                           COLS * X_SIZE * SCALE + (COLS - 1) * SPACE + 2 * BORDER,
                           ROWS * Y_SIZE * SCALE + (ROWS - 1) * SPACE + 2 * BORDER)
context = cairo.Context(surface)
context.set_line_cap(cairo.LineCap.ROUND)

for x in range(COLS):
    for y in range(ROWS):
        drawChar(BORDER + X_SIZE // 2 * SCALE + x * (X_SIZE * SCALE + SPACE),
                 BORDER + y * (Y_SIZE * SCALE + SPACE))

#drawChar(100, 20)


context.stroke()
surface.finish()
