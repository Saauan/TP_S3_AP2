#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:script:`main_maze` script

:author: Coignion Tristan, Tayebi Ajwad, Becquembois Logan

:date:  22/11/2018

This script is used to display a maze on a screen

Uses: 
    - graphical_maze
        - tkinter
        - maze.py
            - square.py (Dependancy)
"""
from graphical_maze import * #pylint: disable=W0614
from maze import Maze, CreationError
from tkinter import * #pylint: disable=W0614
from tkinter import filedialog
from functools import partial
import os

SETUP_WIDTH = 800
SETUP_HEIGHT = 600
SAVE_PATH = "../mazes/"

global filename # global variable

####################
# WINDOW FUNCTIONS #
####################

def invert_state(elems):
    """
    Toggles the state of a Tkinter item on the window

    :param elems: (list) a list of the items to toggle
    :side effect: Inverts the state of the items from `disabled` to `normal` and vice-versa
    :return: None
    :UC: items of elems must have a state attribute
    :Examples:

    >>> root = Tk()
    >>> root.withdraw()
    ''
    >>> someObject = Button(root, state="normal")
    >>> anotherObject = Entry(root, textvariable="test", state="disabled")
    >>> invert_state([someObject, anotherObject])
    >>> someObject["state"] == "disabled"
    True
    >>> anotherObject["state"] == "normal"
    True
    """
    for elem in elems:
        if elem["state"] == "normal":
            elem["state"] = 'disabled'
        else:
            elem["state"] = "normal"

def toggle_state_on(elems):
    """
    Toggles on the state of a Tkinter item on the window

    :param elems: (list) a list of items to activate
    :side effect: sets the state of the objects to `normal`
    :return: None
    :UC: items of elems must have a state atribute
    :Examples:

    >>> root = Tk()
    >>> root.withdraw()
    ''
    >>> someObject = Button(root, state="normal")
    >>> anotherObject = Entry(root, textvariable="test", state="disabled")
    >>> toggle_state_on([someObject, anotherObject])
    >>> someObject["state"] == "normal"
    True
    >>> anotherObject["state"] == "normal"
    True
    """
    for elem in elems:
        elem["state"] = "normal"

def toggle_state_off(elems):
    """
    Toggles off the state of a Tkinter item on the window

    :param elems: (list) a list of items to activate
    :side effect: sets the state of the objects to `disabled`
    :return: None
    :UC: items of elems must have a state attributes
    :Examples:

    >>> root = Tk()
    >>> root.withdraw()
    ''
    >>> someObject = Button(root, state="normal")
    >>> anotherObject = Entry(root, textvariable="test", state="disabled")
    >>> toggle_state_off([someObject, anotherObject])
    >>> someObject["state"] == "disabled"
    True
    >>> anotherObject["state"] == "disabled"
    True
    """
    for elem in elems:
        elem["state"] = "disabled"

def strip_filename(c):
    """
    returns just a path of a file using a string coming from the filedialog.askopen() method

    :param c: (str)
    :return: (str) the path of a file
    :UC: c MUST be the return of filedialog.askopenfile()
    :Example:

    >>> strip_filename("<_io.TextIOWrapper name='/TESTPATH' mode='r' encoding='UTF-8'>")
    '/TESTPATH'
    """
    c = c.lstrip("<_io.TextIOWrapper name='")
    c = c.rstrip("' mode='r' encoding='UTF-8'>")
    return c

def askfile():
    """
    asks the user for a file and stores the result in filename
    
    :return: (str) it has the form of "<_io.TextIOWrapper name='/TESTPATH' mode='r' encoding='UTF-8'>"
    """
    global filename
    print("test")
    filename.set((filedialog.askopenfile(initialdir = os.getcwd(), title = "Select a txt file", filetypes = (("text file","*.txt"),("all files","*.*")))))
    filename.set(strip_filename(filename.get()))
    if filename.get() != None:
        print("This file has been selected", filename.get())

def toggle1(widthEntry, heightEntry, fileEntry, fileButton):
    """
    toggles off widthEntry, heightEntry, and toggles on fileEntry and fileButton
    """
    toggle_state_off([widthEntry, heightEntry])
    toggle_state_on([fileEntry, fileButton])

def toggle2(widthEntry, heightEntry, fileEntry, fileButton):
    """
    toggles on widthEntry, heightEntry, and toggles off fileEntry and fileButton
    """
    toggle_state_on([widthEntry, heightEntry])
    toggle_state_off([fileEntry, fileButton])

def setup_winentries(winset):
    """
    Returns the entries items used for the setup_window

    :param: (Tk) a window
    :return:
    TODO
    """
    widthLabel = Label(winset, text="Width of the maze (integer)")
    heightLabel = Label(winset, text="Height of the maze (integer)")
    width = StringVar(winset)
    width.set("20")
    height = StringVar(winset)
    height.set("20")
    widthEntry = Entry(winset, textvariable=width, state="normal")
    heightEntry = Entry(winset, textvariable=height, state="normal")
    fileLabel = Label(winset, text="Generate from which file ? ")
    global filename
    filename = StringVar(winset)
    fileEntry = Entry(winset, textvariable=filename, state="disabled")
    fileButton = Button(winset, text="Browse", command=askfile, state="disabled")
    return widthLabel, heightLabel, width, height, widthEntry, heightEntry, fileLabel, filename, fileEntry, fileButton

def setup_wingen(winset, widthEntry, heightEntry, fileEntry, fileButton):
    """
    Returns the generation items used for the setup_window

    :param: (Tk) a window
    :return:
    TODO
    """
    genLabel = Label(winset, text="Generation Options (Chose only one)")
    varGen = IntVar()
    varGen.set(2)

    # When handgen or randomgen is selected, the width and height entries will be activated, and the file entry and button are disabled
    # When texgen is selected, the reverse operation is done
    handgenCheck = Radiobutton(winset, variable=varGen, value=0, text="Hand generation", command=partial(toggle2, widthEntry, heightEntry, fileEntry, fileButton))
    textgenCheck = Radiobutton(winset, variable=varGen, value=1, text="Generate from text file", command=partial(toggle1, widthEntry, heightEntry, fileEntry, fileButton))
    randomgenCheck = Radiobutton(winset, variable=varGen, value=2, text="Generate randomly", command=partial(toggle2, widthEntry, heightEntry, fileEntry, fileButton))

    return genLabel, varGen, handgenCheck, textgenCheck, randomgenCheck

def setup_winsave(winset):
    """
    Returns the save items used for the setup_window

    :param: (Tk) a window
    :return:
    TODO
    """
    saveLabel = Label(winset, text="Save Options")
    is_save = IntVar(winset, 1)
    saveCheck = Checkbutton(winset, variable= is_save, text="Save into a file")
    is_saveres = IntVar(winset, 0)
    saveresCheck = Checkbutton(winset, variable= is_saveres, text="Save into a file with the resolution")
    is_savehtml = IntVar(winset, 0)
    savehtmlCheck = Checkbutton(winset, variable= is_savehtml, text="Save into a html file")

    return saveLabel, is_save, saveCheck, is_saveres, saveresCheck, is_savehtml, savehtmlCheck

def setup_wingraphic(winset):
    """
    Returns the graphic items used for the setup_window

    :param: (Tk) a window
    :return:
    TODO
    """
    graphicLabel = Label(winset, text="Graphic Options")
    is_graphicres = IntVar(winset, 1)
    graphicresCheck = Checkbutton(winset, variable=is_graphicres, text="Display the resolution on the maze")
    is_dynamic = IntVar(winset, 1)
    dynamicCheck = Checkbutton(winset, variable=is_dynamic, text="Display the resolution dynamically")
    is_graphic = IntVar(winset, 1)
    graphicCheck = Checkbutton(winset, variable=is_graphic, text="Display the maze on a window", command=partial(invert_state, [graphicresCheck, dynamicCheck]))

    return graphicLabel, is_graphicres, graphicresCheck, is_dynamic, dynamicCheck, is_graphic, graphicCheck

def check_if_setup_correct(win, width, height):
    """
    Checks if the inputs the user has types are correct
    If it is correct, the window is destroyed, else, a warning is displayed
    To be correct, width.get() and height.get() must be convertible to integer
    """
    try:
        int(width.get())
        int(height.get())
        win.destroy()
    except:
        winwarning = Tk()
        winwarning.title("Warning")
        warningLabel = Label(winwarning, text="The values you have entered are not correct, please try again. (Width and height must be integer)")
        warningOkButton = Button(winwarning, text="OK", command=winwarning.destroy)
        warningLabel.grid()
        warningOkButton.grid()

##################
# MAIN FUNCTIONS #
##################

def setup_window():
    """
    Opens a window for the user to input parameters and then returns those parameters

    :side effect: Opens a Tkinter window on which the user has to input the parameters of the program
    :return: The function returns 10 values in a tuple listed below:
        - (int) The width of the maze
        - (int) The height of the maze
        - (str) The path of the text file from which we can build a maze
        - (int) The generation the user has chosen
            * 0 : Hand generation
            * 1 : Generate from a text file
            * 2 : Generate randomly
        - (int) 1 if the user wants to save in a text file, 0 otherwise
        - (int) 1 if the user wants the resolution to be saved too, 0 otherwise
        - (int) 1 if the user wants the maze to be saved into a html file, 0 otherwise
        - (int) 1 if the user wants the maze to be displayed graphically, 0 otherwise
        - (int) 1 if the user wants to see the resolution to be displayed, 0 otherwise
        - (int) 1 if the user wants the resolution to be displayed dynamically, 0 otherwise
    :UC: None
    """
    # Setup of the window
    winset = Tk()
    winset.title("Maze setup")
    title = Label(winset, text="Please, select options in order to continue")
    exitButton = Button(winset, text='Exit', command=quit)
    okButton = Button(winset, text="OK")

    # Entries (width, height and filepath) setup
    entries_var = setup_winentries(winset)
    widthLabel, heightLabel, width, height, widthEntry, heightEntry, fileLabel, filename, fileEntry, fileButton = entries_var

    # Generation setup
    gen_var = setup_wingen(winset, widthEntry, heightEntry, fileEntry, fileButton)
    genLabel, varGen, handgenCheck, textgenCheck, randomgenCheck = gen_var

    # Save setup
    save_var = setup_winsave(winset)
    saveLabel, is_save, saveCheck, is_saveres, saveresCheck, is_savehtml, savehtmlCheck = save_var

    # Graphic setup
    graphic_var = setup_wingraphic(winset)
    graphicLabel, is_graphicres, graphicresCheck, is_dynamic, dynamicCheck, is_graphic, graphicCheck = graphic_var

    okButton["command"] = partial(check_if_setup_correct, winset, width, height)

    # Placement
    title.grid(row = 0, column = 0, padx=10) # Places the label in the grid
    exitButton.grid(row=100, column=0)
    okButton.grid(row=100, column=1)

    genLabel.grid(row = 10, column = 0, pady=(10, 0))
    handgenCheck.grid(row = 11, column = 0)
    textgenCheck.grid(row = 12, column = 0)
    randomgenCheck.grid(row = 13, column = 0)

    saveLabel.grid(row = 10, column = 1, pady=(10, 0))
    saveCheck.grid(row = 11, column = 1)
    saveresCheck.grid(row = 12, column = 1)
    savehtmlCheck.grid(row = 13, column = 1)

    widthLabel.grid(row=20, column=0, pady=(10, 0))
    widthEntry.grid(row=20, column=1, pady=(10, 0))
    heightLabel.grid(row=21, column=0)
    heightEntry.grid(row=21, column=1)

    fileLabel.grid(row=22, column=0, padx=(10,0))
    fileEntry.grid(row=22, column=1)
    fileButton.grid(row=22, column=2)

    graphicLabel.grid(row = 30, column = 0, pady=(10, 0))
    graphicCheck.grid(row = 31, column = 0)
    graphicresCheck.grid(row = 32, column = 0 )
    dynamicCheck.grid(row = 33, column = 0)

    winset.mainloop()

    return (int(width.get()), int(height.get()), filename.get(), varGen.get(), 
            is_save.get(), is_saveres.get(), is_savehtml.get(),
            is_graphic.get(), is_graphicres.get(), is_dynamic.get())

def parse_gen(width, height, filepath, varGen):
    """
    Returns a maze generated accordingly to the arguments of the function
    
    :param width: (int) the width of the maze
    :param height: (int) the height of the maze
    :param filepath: (str) a path of a file we want to generate a maze from
    :param varGen: (int) The generation the user has chosen
            * 0 : Hand generation
            * 1 : Generate from a text file
            * 2 : Generate randomly
    :return: (Maze) a maze
    :UC: None
    :Examples:

    >>> maze_test = parse_gen(20, 20, "", 2)
    >>> maze_test.get_height()
    20
    >>> maze_test.get_width()
    20
    """
    if varGen == 1:
        maze = Maze().build_maze_from_text(filepath)
    else:
        try: # TO REMOVE
            width = int(width)
            height = int(height)
        except TypeError:
            raise TypeError("The width and height are not of the correct type !")
        if varGen == 2:
            maze = Maze().random_generation(width, height)
        else:
            # maze = Maze.hand_generation() #TODO
            pass
    return maze

def parse_save(maze, is_save, is_saveres, is_savehtml):
    """
    Saves the maze into different files depending on the arguments of the function

    :param maze: (Maze)
    :param is_save: (bool) if True, the maze will be saved as is in a text file
    :param is_saveres: (bool) if True, the maze and its resolution will be saved in a text file
    :param is_savehtml: (bool) if True, the maze and its resolution will be saved in an html file
    :return: None
    """
    if is_save:
        maze.text_representation(SAVE_PATH+"maze.txt")
    if is_saveres:
        # maze.text_representation(SAVE_PATH+"maze_res.txt", res=True)
        pass
    if is_savehtml:
        maze.picture_representation(SAVE_PATH+"maze_html.html")

def graph_disp(maze, is_graphicres, is_dynamic):
    """
    """
    width = maze.get_width()
    height = maze.get_height()
    win = Tk() # Creates a window object
    win.title(random_word('../ressources/anagrams.txt')) # DEBUG is only valid is Visual Code
    can = Canvas(win, bg=BG_COLOR, width=CAN_WIDTH, height=CAN_HEIGHT)
    can.bind('<Button-1>',
            lambda event: draw_circle(can, event))
    can.pack() # Allows the canvas to be handled as grid and columns
    draw_grid(can, width, height) 
    setup_wall(can, maze)
    if is_graphicres:
        if is_dynamic:
            pass
            # Display all the resolution progressively
        else:
            pass
            # Display all the resolution in one go
    win.mainloop()

def main():
    """
    """
    # We get all the setup variable from the user using a GUI
    setup_var = setup_window()
    width, height, filepath, varGen, is_save, is_saveres, is_savehtml, is_graphic, is_graphicres, is_dynamic = setup_var

    # We generate the maze
    maze = parse_gen(width, height, filepath, varGen)

    # If we must, we save it in files
    parse_save(maze, is_save, is_saveres, is_savehtml)

    # Displays the maze
    if is_graphic:
        graph_disp(maze, is_graphicres, is_dynamic)

    
if __name__ == '__main__':
    main()
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=False)
