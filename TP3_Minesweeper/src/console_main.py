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
        width = 30
        height = 20
        nbombs = int(0.12*(width*height))
    game = Minesweeper(width, height, nbombs)
    
    inplace(width,height)


    Actions = input("Your play x,y,C (C=(R)eveal,(S)et,(U)nset): ").split(',')
    Actions[0],Actions[1] = int(Actions[0]),int(Actions[1])
    print(Actions)

def inplace(width, height):
    """
    create the textual grid of the game
    """
    print(" ",end="")
    for i in range(width):
        print(" {:3d}".format(i), end="")
    print("")
    
    for j in range(height):
        print("{:2s}".format("") + width*"+---" + "+")
        print("{:2s}".format(str(j)) + width*("|" + "{:^3s}".format("")) + "|")
    print(" " + width*"+---" + "+")


if __name__ == '__main__':
    main()



