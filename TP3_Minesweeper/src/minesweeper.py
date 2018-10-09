#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`minesweeper` module

:author: Coignion Tristan, Tayebi Ajwad

:date:  10/04/2018

This module provides functions and a class for minesweeper's game's management.

This module uses from :mod:`cell`:

* :class: `Cell`
"""

import random
from enum import Enum
from cell import Cell
from copy import copy


################################################
# Type declaration
################################################

class GameState(Enum):
    """
    A class to define an enumerated type with three values :

    * ``winning``
    * ``losing``
    * ``unfinished``

    for the three state of minesweeper game.
    """
    winning = 1
    losing = 2
    unfinished = 3


##############################################
# Function for game's setup and management
##############################################


def neighborhood(x, y, width, height):
    """
    :param x: x-coordinate of a cell
    :type x: int
    :param y: y-coordinate of a cell
    :type y: int
    :param height: height of the grid
    :type height: int
    :param width: widthof the grid
    :type width: int
    :return: the list of coordinates of the neighbors of position (x,y) in a
             grid of size width*height
    :rtype: list of tuple
    :UC: 0 <= x < width and 0 <= y < height
    :Examples:

    >>> neighborhood(3, 3, 10, 10)
    [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]
    >>> neighborhood(0, 3, 10, 10)
    [(0, 2), (0, 4), (1, 2), (1, 3), (1, 4)]
    >>> neighborhood(0, 0, 10, 10)
    [(0, 1), (1, 0), (1, 1)]
    >>> neighborhood(9, 9, 10, 10)
    [(8, 8), (8, 9), (9, 8)]
    >>> neighborhood(3, 9, 10, 10)
    [(2, 8), (2, 9), (3, 8), (4, 8), (4, 9)]
    """
    potential_neighbours = [(x-1, y+1), (x, y+1), (x+1, y+1),
                            (x-1, y),             (x+1, y),
                            (x-1, y-1), (x, y-1), (x+1, y-1)]

    neighbours = [neigh for neigh in potential_neighbours 
                  if (neigh[0]>= 0 and neigh[0] < width
                  and neigh[1] >= 0 and neigh[1] < height)]
    return sorted(neighbours)


class Minesweeper():
    """
    >>> game = Minesweeper(20, 10, 4)
    >>> game.get_width()
    20
    >>> game.get_height()
    10
    >>> game.get_nbombs()
    4
    >>> game.get_state() == GameState.unfinished 
    True
    >>> cel = game.get_cell(1, 2)
    >>> cel.is_revealed()
    False
    >>> 
    """

    def __init__(self, width=30, height=20, nbombs=99):
        """
        build a minesweeper grid of size width*height cells
        with nbombs bombs randomly placed.  

        :param width:[optional] horizontal size of game (default = 30)
        :type width: int
        :param height: [optional] vertical size of game (default = 20)
        :type height: int
        :param nbombs: [optional] number of bombs (default = 99)
        :type nbombs: int
        :return: a fresh grid of  width*height cells with nbombs bombs randomly placed.
        :rtype: Minesweeper
        :UC: width and height must be positive integers, and
             nbombs <= width * height
        :Example:

        >>> game = Minesweeper(20, 10, 4)
        >>> game.get_width()
        20
        >>> game.get_height()
        10
        >>> game.get_nbombs()
        4
        >>> game.get_state() == GameState.unfinished 
        True
        """
        self.__width = width
        self.__height = height
        self.__nbombs = nbombs
        self.__state = GameState.unfinished
        self.grid = [[Cell() for j in range(width)] for i in range(height)]
        self.__place_bombs()
        self.__neighbombs()


    def __place_bombs(self):
        """
        places randomly `self.__nbombs` bombs on the game's board.

        :board effect: modifies self.__bomb_state to True for some cells in self.grid
        """
        # sample_row = random.sample(self.grid, self.__nbombs)
        # sample_col = []
        # for row in sample_row:
        #     sample_col += random.sample(row, 1)
        # for mine in sample_col:
        #     mine.set_bomb()

        sample_coord = random.sample([i for i in range(self.__height*self.__width)], self.__nbombs)
        for coord in sample_coord:
            y = coord // self.__width
            x = coord % self.__width
            self.grid[y][x].set_bomb()

    def __neighbombs(self):
        """
        Changes the values of self.__bombs_neighbours for each cell in the grid
        according to the number of neighbours with bombs they each have.

        :board effect: modifies self.__bombs_neighbours for every cell in self.grid
        """
        for i, row in enumerate(self.grid):
            for j, le_cell in enumerate(row):
                for x1, y1 in neighborhood(j, i, self.__width, self.__height):
                    if self.grid[y1][x1].is_bomb():
                        le_cell.incr_number_of_bombs_in_neighborhood()


    def get_height(self):
        """
        :return: height of the grid in self
        :rtype: int
        :UC: none
        """
        return self.__height


    def get_width(self):
        """
        :return: width of the grid in game
        :rtype: int
        :UC: none
            """
        return self.__width
    
    def get_nbombs(self):
        """
        :return: number of bombs in game
        :rtype: int
        :UC: none
        """
        return self.__nbombs


    def get_cell(self, x, y):
        """
        :param x: x-coordinate of a cell
        :type x: int
        :param y: y-coordinate of a cell
        :type y: int
        :return: the cell of coordinates (x,y) in the game's grid
        :type: cell
        :UC: 0 <= x < width of game and O <= y < height of game
        """
        return self.grid[y][x]


    def get_state(self):
        """
        :return: the state of the game (winning, losing or unfinished)
        :rtype: GameState
        :UC: none
        """
        return self.__state


    def loss(self):
        """
        :return: none, change the GameState in losing, makes the game finished
        :UC: none
        """ 
        self.__state = GameState.losing

    def reveal_all_cells_from(self, x, y):
        """
        :param x: x-coordinate
        :param y: y-coordinate
        :return: none
        :side effect: reveal all cells of game game from the initial cell (x,y).
        :UC: 0 <= x < width of game and O <= y < height of game
        """ 
        if (self.get_cell(x, y).number_of_bombs_in_neighborhood() == 0
        and self.get_cell(x, y).is_revealed() == False):
            self.get_cell(x, y).reveal()
            for x1, y1 in neighborhood(x, y, self.get_width(), self.get_height()):
                self.reveal_all_cells_from(x1, y1)
        self.get_cell(x, y).reveal()


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)


