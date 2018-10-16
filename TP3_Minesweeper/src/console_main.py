#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`main` module

:author: Tristan Coignion, Ajwad Tayebi, Becquembois Logan, `FIL - IEEA - Univ. Lille1.fr <http://portail.fil.univ-lille1.fr>`_

:date:  2018, september. Last revision: 2018, october

Main module to play the minesweeper's game : textual version


"""

import sys
from minesweeper import Minesweeper, GameState

def main():
    """
    main function for textual minesweeper game
    """
    # Takes arguments from the console
    if len(sys.argv) == 4:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        nbombs = int(sys.argv[3])
    else:
        width = 20
        height = 20
        nbombs = int(0.15*(width*height))
    game = Minesweeper(width, height, nbombs)
    
    redraw(width, height, game) # Draws the grid for the first time.

    # While the game is not won or lost
    while game.get_state() == GameState.unfinished:
        x, y, action = userAction(width, height) # Takes input from the user
        actionProcess(x, y, action, game) 
        redraw(width, height, game)
        game.test_win()
    endGame(game)

def userAction(width, height):
    """
    takes input from the user and returns it as a tuple in the form (x, y, action)
    Actions can take the form of "R", "S", and "U"

    :param width: (int) the width of the grid
    :param height: (int) the height of the game
    :return: The action of the players in the form of a tuple
    :rtype: (int, int, str)
    :UC: none
    """

    finished = False
    while not finished:
        A = input("Your play: x,y,Action (A = (R)eveal | (S)et | (U)nset) : ").split(',')
        try:
            assert len(A) == 3, "You have to enter 3 arguments"
            x = int(A[0])
            y = int(A[1])
            action = A[2].strip()
            assert action in {"R", "U", "S"}, "The action can be R, S or U"
            assert 0<=x<width and 0 <=y<height, "x and y must be between 0 and the width and the height of the grid"
        
        except ValueError:
            print("Please enter an integer for x and y")
            continue
        except AssertionError as error:
            print(error)
            continue

        # This line executes only if there are no errors
        finished = True

    return (x, y, A[2].strip())

def actionProcess(x, y, action, game):
    """
    Process an action given, it can reveal a cell, flag it, or unflag it.
    If a revealed cell is a bomb
    If an action cannot be done because the cell is revealed or already flagged, 
    an error message is printed

    :param x: (int) the x coordinate of the cell
    :param y: (int) the y coordinate of the cell
    :param action: (str) the action to be made
    :param game: (Minesweeper) the game

    :return: none
    :side effect: Described in the paragraph above
    :UC: 0 <= x < width and 0 <= y < height, action in {"R", "U", "S"}
    """
    assert action in {"R", "U", "S"}, "Error with the action type"
    leCell = game.grid[y][x]
    
    # If the action is Reveal
    if action == "R":
        if leCell.is_revealed():
            print("The cell is already revealed!")
            return
        else:
            game.reveal_all_cells_from(x, y)
            if game.grid[y][x].is_bomb():
                game.change_state_to_losing()
            return
    
    # If the action is Set flag.
    if action == "S":
        if leCell.is_hypothetic():
            print("The cell is already flagged!")
        else:
            leCell.set_hypothetic()
            return

    # If the action is Unset flag.
    if action == "U":
        if not leCell.is_hypothetic():
            print("The cell is already unflagged!")
        else:
            leCell.unset_hypothetic()
            return

def redraw(width, height, game):
    """
    Draws a board of the game
    
    :param width: (int) the width of the grid
    :param height: (int) the height of the game
    :param game: (Minesweeper) the game
    """
    # Prints the first line of the grid (with the numerals)
    print(" ", end='')
    for i in range(width):
        print(" {:3d}".format(i), end="")
    print("")

    for i, line in enumerate(game.grid):
        # Above line
        print("{:2s}".format("") + width*"+---" + "+")

        # Beginning of the second line
        print("{:2d} |".format(i), end="")
        
        # The rest of the second line (every cell and the separator)
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

    # Prints the last line of the grid
    print("  " + width*"+---" + "+")

def endGame(game):
    """
    Ends the game.

    :param game: (Minesweeper) the game
    :return: none
    :side effect: prints wether the user won or lost the game
    """
    if game.get_state() == GameState.losing:
        print("You Lost the Game.")
    if game.get_state() == GameState.winning:
        print("You Won the Game.")
        
if __name__ == '__main__':
    main()



