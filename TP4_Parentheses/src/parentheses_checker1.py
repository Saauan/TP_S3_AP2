#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod: parentheses_checker1 module

:author: Tristan Coignion, Tayebi Ajwad, Becquembois Logan

:date: 16/10/2018
:last revision: 16/10/2018

A module which verifies whether 
or not a file is well parenthesed
"""

from os import sys
from stack import Stack, StackEmptyError
    
def is_well_parenthesed(filename):
    """
    returns wether a file has good parentheses or not

    :param filename: (str) the name of the file we want to check
    :return: True if well parenthesed, False otherwise
    :returntype: Bool
    :UC: `filename` is a valid file
    """
    try:
        with open(filename, "r",) as instream:
            lines = instream.readlines()
            stack = Stack()
    except FileNotFoundError:
        print("The file {:s} doesn't exist.".format(filename))
        return False

    for line in lines:
        for c in line:
            try:
                if c in {"(", "{", "["}:
                    stack.push(c)

                if c == ")":
                    if stack.pop() != "(":
                        return False

                if c == "}":
                    if stack.pop() != "{":
                        return False

                if c == "]":
                    if stack.pop() != "[":
                        return False
            except StackEmptyError:
                return False
    return stack.is_empty()


if len(sys.argv) == 2:
    if is_well_parenthesed(sys.argv[1]):
        print("Well parenthesed")
    else:
        print("Bad parenthesed")
else:
    print("You have to enter only one argument")
    # Display Help

