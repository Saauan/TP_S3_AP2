#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod: parentheses_checker3 module

:author: Tristan Coignion, Tayebi Ajwad, Becquembois Logan

:date: 16/10/2018
:last revision: 16/10/2018

A module which verifies whether 
or not a file is well parenthesed with correct error messages
(this one ignores comments.)
"""

from os import sys
from stack import Stack, StackEmptyError

# A dictionnary of parentheses and their ending characters
PARENTHESES = {"(" : ")",
               "{" : "}",
               "[" : "]"}
    
# A dictionnary of comments and their ending characters
COMMENTS = {"'" : "'",
            '"' : '"',
            "#": "\n"}

def readlines_of_file(filename):
    """
    reads and returns all the lines of a file

    :param filename: (str) the name of the file we want to read
    :return: A string containing all the lines of the file.
    :returntype: String
    :UC: `filename` is a valid file
    """
    try:
        with open(filename, "r",) as instream:
            lines = instream.readlines()
    except FileNotFoundError:
        print("The file {:s} doesn't exist.".format(filename))
        quit()
    return lines
    
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
    lines = readlines_of_file(filename)

    stack = Stack() # We create a Stack object
    comment = False # True if we are reading comments or strings, false otherwise
    comment_char = ""

    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            # If c is a comment beginner.
            if c in COMMENTS.keys() and not comment:
                comment = True
                comment_char = c
                continue # There's no need to check if comment is False
            # If c is a comment ender.
            elif c in COMMENTS[comment_char] == c and comment:
                comment = False
                continue # We don't want to check for parentheses in case the character is a comment ending one

            if not comment:
                try:
                    if c in PARENTHESES.keys():
                        stack.push((c, i, j))
                        # The values in the stack have the form (char, line, index_in_line)

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

if __name__ == "__main__":
    if len(sys.argv) == 2:
        is_well_parenthesed(sys.argv[1])
    else:
        print("You have to enter only one argument")
        # Display Help

