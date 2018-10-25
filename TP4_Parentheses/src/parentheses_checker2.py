#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod: parentheses_checker2 module

:author: Tristan Coignion, Tayebi Ajwad, Becquembois Logan

:date: 16/10/2018
:last revision: 16/10/2018

A module which verifies whether 
or not a file is well parenthesed with correct error messages
"""

from os import sys
from stack import Stack, StackEmptyError

PARENTHESES = {"(" : ")",
               "{" : "}",
               "[" : "]"}
    
def is_well_parenthesed(filename):
    """
    returns wether a file has good parentheses or not

    :param filename: (str) the name of the file we want to check
    :return: True if well parenthesed, False otherwise
    :returntype: Bool
    :side effect: if the file is not well parenthesed,
                  prints an error message indicating why it isn't.
    :UC: `filename` is a valid file
    """
    try:
        with open(filename, "r",) as instream:
            lines = instream.readlines()
            stack = Stack()

    except FileNotFoundError:
        print("The file {:s} doesn't exist.".format(filename))
        return False

    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            try:
                if c in PARENTHESES.keys():
                    stack.push((c, i, j))

                if c in PARENTHESES.values():
                    top_char = stack.pop()
                    if PARENTHESES[top_char[0]] != c:
                        print("Closed parenthese {} at line {:d} char {:d} doesn't match the open parenthese {} at line {:d} char {:d}".format(c, i+1, j+1, top_char[0], top_char[1]+1, top_char[2]+1)) 
                        return False

            except StackEmptyError:
                print("No open parenthese matching parenthese {} at line {:d} char {:d}".format(c, i+1, j+1))
                return False

    if not stack.is_empty():
        print("Parenthese {} at line {:d} char {:d} has no matching closed parenthese".format(stack.top()[0], stack.top()[1]+1, stack.top()[2]+1))
    return stack.is_empty()


if len(sys.argv) == 2:
    is_well_parenthesed(sys.argv[1])
else:
    print("You have to enter only one argument")
    # Display Help

