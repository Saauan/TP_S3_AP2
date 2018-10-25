#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`square` module

:author: Coignion Tristan, Ajwad Tayebi, Becquembois Logan

:date: 24/10/2018

This module provides functions and a class for maze's squares management.

"""
    
class Square():
    
    def __init__(self, MGauche = False, MHaut = False, MDroit = False, MBas = False, Passage = False):
        """
        :return: a new square of a maze's grid.
        :rtype: Square
        :UC: none
        :Examples:

        >>> square = Square()
        >>> square.has_leftWall()
        False
        >>> square.has_topWall()
        False
        >>> square.has_rightWall()
        False
        >>> square.has_bottomWall()
        False
        >>> square.walls()
        (False, False, False, False)
        """
        self.__leftWall = MGauche
        self.__topWall = MHaut
        self.__rightWall = MDroit
        self.__bottomWall = MBas

    def has_leftWall(self):
        """
        :return: True if self has a left-hand wall, False otherwise
        :rtype: bool
        :UC: none
        :Example:

        >>> square = Square()
        >>> square.has_leftWall()
        False
        """
        return self.__leftWall == True

    def has_topWall(self):
        """
        :return: True if self has an upper wall, False otherwise
        :rtype: bool
        :UC: none
        :Example:

        >>> square = Square()
        >>> square.has_topWall()
        False
        """
        return self.__topWall == True
        
    def has_rightWall(self):
        """
        :return: True if self has a right-hand wall, False otherwise
        :rtype: bool
        :UC: none
        :Example:

        >>> square = Square()
        >>> square.has_rightWall()
        False
        """
        return self.__rightWall == True

    def has_bottomWall(self):
        """
        :return: True if self has a lower wall, False otherwise
        :rtype: bool
        :UC: none
        :Example:

        >>> square = Square()
        >>> square.has_bottomWall()
        False
        """
        return self.__bottomWall == True

    def walls(self):
        """
        Gives the walls composition in the following order:
                Left, Top, Right, Bottom

        :return: a tuple containing True if there is a wall, False otherwise
        :rtype: tuple
        :UC: none
        :Example:

        >>> square = Square()
        >>> square.walls()
        (False, False, False, False)
        """
        return (self.__leftWall, self.__topWall, self.__rightWall, self.__bottomWall)
   


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)
