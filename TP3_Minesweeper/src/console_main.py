#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`main` module

:author: `FIL - IEEA - Univ. Lille1.fr <http://portail.fil.univ-lille1.fr>`_

:date:  2018, september. Last revision: 2018, october

Main module to play the minesweeper's game : textual version


"""

import sys
from minesweeper import Minesweeper

def main():
    """
    main function for textual minesweeper game
    """
    if len(sys.argv) == 4:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        nbombs = int(sys.argv[3])
    else:
        width = 20
        height = 10
        nbombs = 0.2*(width*height)
    game = Minesweeper(width, height, nbombs)


if __name__ == '__main__':
    main()


