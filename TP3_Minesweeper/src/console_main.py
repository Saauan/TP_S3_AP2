#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`main` module

:author: `FIL - IEEA - Univ. Lille1.fr <http://portail.fil.univ-lille1.fr>`_

:date:  2018, september. Last revision: 2018, october

Main module to play the minesweeper's game : textual version


"""

import sys
from minesweeper import *

def main():
    """
    main function for textual minesweeper game
    """
    if len(sys.argv) == 4:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        nbombs = int(sys.argv[3])
    else:
        width = 5
        height = 5
        nbombs = int(0.12*(width*height))
    game = Minesweeper(width, height, nbombs)
    
    inplace(width,height) # Prints the grid DEBUG
    
    while game.get_state() == GameState.unfinished:
        x, y, action = userAction()
        actionProcess(x, y, action, game)
        redraw(width, height, game)
        game.test_win()
        # testEnd(game)
    end(game)


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
    print("  " + width*"+---" + "+")

def userAction():
    """
    takes input from the user and returns it as a tuple in the form (x, y, action)
    Actions can take the form of "R", "S", and "U"
    """
    finished = False
    while not finished:
        A = input("Your play x,y,C (C = (R)eveal | (S)et | (U)nset) : ").split(',')
        try:
            assert len(A) == 3, "You have to enter 3 arguments"
            x = int(A[0])
            y = int(A[1])
            action = A[2].strip()
            assert action in {"R", "U", "S"}, "The action can be R, S or U"
        
        except ValueError:
            print("Please enter an integer for x and y")
            continue
        except AssertionError as error:
            print(error)
            continue
        finished = True
    return (x, y, A[2].strip())

def actionProcess(x, y, action, game):
    """
    Process an action given, it can reveal a cell, flag it, or unflag it.
    If a revealed cell is a bomb
    If an action cannot be done because the cell is revealed or already flagged, 
    an error message is printed
    """
    assert action in {"R", "U", "S"}, "Error with the action type"
    leCell = game.grid[y][x]
    if action == "R":
        if leCell.is_revealed():
            print("The cell is already revealed!")
            return
        else:
            game.reveal_all_cells_from(x, y)
            if game.grid[y][x].is_bomb():
                game.change_state_to_losing()
            return
    if action == "S":
        if leCell.is_hypothetic():
            print("The cell is already flagged!")
        else:
            leCell.set_hypothetic()
            return
    if action == "U":
        if not leCell.is_hypothetic():
            print("The cell is already unflagged!")
        else:
            leCell.unset_hypothetic()
            return

def redraw(width, height, game):
    """
    Draws a board of the game
    """

    print(" ",end="")
    for i in range(width):
        print(" {:3d}".format(i), end="")
    print("")

    for i, line in enumerate(game.grid):
        print("{:2s}".format("") + width*"+---" + "+")
        print("{:2d} |".format(i), end="")
        for cell in line:
            if cell.is_revealed() and not cell.is_bomb():
                print(cell.number_of_bombs_in_neighborhood(), end="")
            elif cell.is_revealed() and cell.is_bomb():
                print("X", end="")
            elif cell.is_hypothetic():
                print("?", end="")
            else:
                print(" ", end="")
            print(" | ", end="")
        print("")

    print("  " + width*"+---" + "+")

# def testEnd(game):
#     """
#     This function tests if the game is finished or not. 

#     :param game: the minesweeper game
#     :type game: Minesweeper
#     """
#     state = game.get_state()
#     if state == GameState.losing
    

def end(game):
    """
    """
    if game.get_state() == GameState.losing:
        print("Lost")
    if game.get_state() == GameState.winning:
        print("Won")
if __name__ == '__main__':
    main()



