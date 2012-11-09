# -*- coding: utf-8 -*-
'''
Created on 10 Apr 2010

@author: pate

This is a collection of GUI related functions:
(in alphabetical order)

changeMaxValue(root)
changeNoOfDice(root)
changeNoOfThrows(root)
changePlayers(root)
changeSettingsFile(root)
createMenu(root)
keyboardBindings(root)
newGame(root, event=None)
quit(root, event=None)
updateMaxValue(root, dialog, maxValueSpinbox)
updateNoOfDice(root, dialog, noOfDiceSpinbox)
updateNoOfThrows(root, dialog, NoOfThrowsSpinbox)
updatePlayers(root, dialog)
updateScreen(root, TheGame)
viewHighScores(root, event=None)

root is a Tkinter screen (Tk()) which has the following
attributes:
game - the Game.Game class instance
dices - GUI.DiceRow class instance
scores - GUI.ScoreBoard class instance
states - GUI.GameState class instance
The last three can be created with updateScreen(root, TheGame)


class SimpleCallback() is used to relay parameters
to TKinter Button commands which should be called 
only when the Button is clicked, not when the 
Button is created
'''


# Tkinter related imports
import Tkinter as T
import tkFileDialog, tkMessageBox
import tkFont

# Import Modules from Game Package
import Game.Game as P
import Game.Settings as Settings
import Game.HighScores as HS

import GameState as GS
import ScoreBoard as SB
import DiceRow as DR
from SimpleCallback import SimpleCallback

from datetime import datetime
import logging


def notifyError(root):
    pass
  
    
def changeMaxValue(root):
    '''
    Create a dialog in which the user selects the maximum value of dice
    '''
    # Only update screen before first round because
    # later settings can't be changed
    if root.game.gameround == 0:
        dialog = T.Toplevel()
        dialog.minsize(300, 100)
        dialog.title('Change the maximum value of dice')
        maxValueSpinbox = T.Spinbox(dialog, from_=Settings.SMIN, to=Settings.SMAX, wrap=True, state='readonly')
        maxValueSpinbox.pack()
        callback = SimpleCallback(updateMaxValue, root, dialog, maxValueSpinbox)
        OkButton = T.Button(dialog, text='Ok', command=callback, width=10, padx=5)
        CancelButton = T.Button(dialog, text='Cancel', command=dialog.destroy, width=10, padx=5)
        OkButton.pack(side = T.LEFT)
        CancelButton.pack(side = T.RIGHT)    
        dialog.mainloop()
        
def changeNoOfDice(root):
    '''
    Create a dialog in which the user selects the new number of dice
    '''
    # Only update screen before first round because
    # later settings can't be changed
    if root.game.gameround == 0:
        dialog = T.Toplevel()
        dialog.title('Change the number of dice')
        dialog.minsize(300, 100)
        noOfDiceSpinbox = T.Spinbox(dialog, from_=Settings.NMIN, to=Settings.NMAX, wrap=True, state='readonly')
        noOfDiceSpinbox.pack()
        # function parameters can be given by using the SimpleCallback help function
        callback = SimpleCallback(updateNoOfDice, root, dialog, noOfDiceSpinbox)
        OkButton = T.Button(dialog, text='Ok', command=callback, width=20)
        CancelButton = T.Button(dialog, text='Cancel', command=dialog.destroy, width=20)
        OkButton.pack(side = T.LEFT)
        CancelButton.pack(side = T.RIGHT)    
        dialog.mainloop()
   
def changeNoOfThrows(root):
    '''
    Create a dialog in which the user selects the maximum value of dice
    '''
    # Only update screen before first round because
    # later settings can't be changed
    if root.game.gameround == 0:
        dialog = T.Toplevel()
        dialog.title('Change the number of throws')
        dialog.minsize(300, 100)
        NoOfThrowsSpinbox = T.Spinbox(dialog, from_=Settings.HMIN, to=Settings.HMAX, wrap=True, state='readonly')
        NoOfThrowsSpinbox.pack()
        callback = SimpleCallback(updateNoOfThrows, root, dialog, NoOfThrowsSpinbox)
        OkButton = T.Button(dialog, text='Ok', command=callback, width=20)
        CancelButton = T.Button(dialog, text='Cancel', command=dialog.destroy, width=20)
        OkButton.pack(side = T.LEFT)
        CancelButton.pack(side = T.RIGHT)        
        dialog.mainloop()
        
def changePlayers(root, event=None):
    '''
    Asks the user for names of the new players
    '''

    dialog = T.Toplevel()
    dialog.title('Change the players')
    dialog.minsize(400, 100)
    dialog.PlayerCB_variables = []
    dialog.PlayerName_variables = []
    dialog.PlayerCB = []
    dialog.PlayerNameEntries = []
    for i in range(6):
        dialog.PlayerCB_variables.append( T.IntVar() )
        dialog.PlayerCB.append( T.Checkbutton(dialog, variable=dialog.PlayerCB_variables[i]) )
        dialog.PlayerName_variables.append( T.StringVar() )
        dialog.PlayerNameEntries.append( T.Entry(dialog, textvariable=dialog.PlayerName_variables[i]) )
        # Add Player 1 and Player 2 as the default names and select these two players
        if i in range(2):
            dialog.PlayerCB_variables[i].set(1)
            P_name = "Player " + str(i+1)
            dialog.PlayerName_variables[i].set(P_name)
        dialog.PlayerCB[i].grid(row=i, column = 0)
        dialog.PlayerNameEntries[i].grid(row=i, column = 1)

    # Create a frame for the buttons and reserve space for it below the 
    # CheckButtons and Entry's
    dialog.buttonFrame = T.Frame(dialog)
    dialog.buttonFrame.grid(row=i+1, column = 0, columnspan = 2)

    # Create the buttons and grid them on the buttonFrame, right below
    # CheckButtons and Entry's
    callback = SimpleCallback(updatePlayers, root, dialog)
    dialog.start_button = T.Button(dialog.buttonFrame, command = callback, text="Start new game!")    
    dialog.cancel_button = T.Button(dialog.buttonFrame, command = dialog.destroy, text="Cancel")    
    dialog.start_button.grid(row = 0, column = 0) 
    dialog.cancel_button.grid(row = 0, column = 1) 
    
    dialog.mainloop()
        

def changeSettingsFile(root):
    '''
    Create a dialog in which the user selects the number of dice
    '''
    # Only update screen before first round because
    # later settings can't be changed
    if root.game.gameround == 0:
        filename = tkFileDialog.askopenfilename()
        if root.game.log: root.logger.info("Reading file setting from %s", filename)
        root.game.settings.new_settings(filename)
        checkForErrors(root)
        updateScreen(root)
        
def checkForErrors(root):
    '''
    Checks whether there are any errors in game for which
    notification has not been done for the user. Notify
    for all such errors and remove them from the list.
    
    '''
    
    print "ERRORS: " + str(root.game.unNotifiedErrors)
    if len(root.game.unNotifiedErrors) > 0:
        length_of_list = len(root.game.unNotifiedErrors)
        for index in range(0, length_of_list):
            newError = root.game.unNotifiedErrors[0]
            root.game.unNotifiedErrors.remove(newError)
            root.game.NotifiedErrors.append(newError)
            tkMessageBox.showerror("Error", newError)


def createMenu(root):
    '''
    Creates the menu on the top of the screen which
    has the following menu items
    
    Game
        Forward (Advance in game)
        View High Scores
        -----------
        Restart
        New Players
        -----------
        Exit
    Settings
        Change the number of dice
        Change the maximum value of dice
        Change the maximum number of allowed throws
        -----------
        New settings
        
    '''
    # create a toplevel menu
    menubar = T.Menu(root)
    
    # create a pulldown menu, and add it to the menu bar
    filemenu = T.Menu(menubar, tearoff=0)
    callback = SimpleCallback(root.states.goForward) 
    filemenu.add_command(label="Roll dices <r>", command=callback)
    callback = SimpleCallback(viewHighScores, root)    
    filemenu.add_command(label="View High Scores <ctrl-h>", command=callback)    
    filemenu.add_separator()  
    callback = SimpleCallback(newGame, root)
    filemenu.add_command(label="Restart <ctrl-n>", command=callback)
    callback = SimpleCallback(changePlayers, root)
    filemenu.add_command(label="New players <ctrl-p>", command=callback)
    filemenu.add_separator()  
    filemenu.add_command(label="Exit <ESC>", command=root.destroy)


    
    # create a pulldown menu, and add it to the menu bar
    settingsmenu = T.Menu(menubar, tearoff=0)
    # function parameters can be given by using the SimpleCallback help function
    callback = SimpleCallback(changeNoOfDice, root)
    settingsmenu.add_command(label="Change the number of dice", command=callback)
    callback = SimpleCallback(changeMaxValue, root)
    settingsmenu.add_command(label="Change the maximum value of dice", command=callback)
    callback = SimpleCallback(changeNoOfThrows, root)
    settingsmenu.add_command(label="Change the maximum number of allowed throws", command=callback)
    settingsmenu.add_separator()  
    callback = SimpleCallback(changeSettingsFile, root)
    settingsmenu.add_command(label="New settings", command=callback)
      
        
    menubar.add_cascade(label="Game", menu=filemenu)
    menubar.add_cascade(label="Settings", menu=settingsmenu)

    # display the menu
    root.config(menu=menubar)
    
def keyboardBindingsDice(root, dice, x, event):
    root.dices.lockDice(dice, x)
def keyboardBindingsRoll(root, event):
    root.states.goForward()
    
def keyboardBindings(root):
    '''
    Handle keyBoard bindings:
    i=1..n        lock dice i
    r             goForward, roll
    <Escape>      Quit game
    <Control-x>   Quit game
    <Control-q>   Quit game
    <Control-n>   New game
    <Control-p>   New Players
    <Control-h>   View High Scores
    '''
    
    for x in range(len(root.dices.diceButton)):
        callback = SimpleCallback(keyboardBindingsDice, root, root.game.dicelist[x], x)
        root.bind(x+1, callback)
        
    callback = SimpleCallback(keyboardBindingsRoll, root)
    root.bind("r", callback)
    
    callback = SimpleCallback(quit, root)
    root.bind("<Escape>", callback)
    root.bind("<Control-x>", callback)
    root.bind("<Control-q>", callback)

    callback = SimpleCallback(newGame, root)
    root.bind("<Control-n>", callback)

    callback = SimpleCallback(changePlayers, root)
    root.bind("<Control-p>", callback)
    
    callback = SimpleCallback(viewHighScores, root)
    root.bind("<Control-h>", callback)    
         
    
def newGame(root, event=None):
    '''
    Start a new game and update the screen.
    Use the current player names and setting file and 
    maximum number of combinations
    '''
    if tkMessageBox.askokcancel("New Game", "Quit current game and start a new game?"):
        root.game.newGame()
        updateScreen(root)

def quit(root, event=None):
    if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()

    
def updateMaxValue(root, dialog, maxValueSpinbox):
    '''
    Change the number of dice in the game and close the dialog
    '''
    root.game.settings.max_value = int(maxValueSpinbox.get())
    updateScreen(root)
    dialog.destroy()  
    
def updateNoOfDice(root, dialog, noOfDiceSpinbox):
    '''
    Change the number of dice in the game and close the dialog
    '''
    root.game.settings.no_of_dice = int(noOfDiceSpinbox.get())
    updateScreen(root)
    dialog.destroy()
    
def updateNoOfThrows(root, dialog, NoOfThrowsSpinbox):
    '''
    Change the number of dice in the game and close the dialog
    '''
    root.game.settings.no_of_throws = int(NoOfThrowsSpinbox.get())
    updateScreen(root)
    dialog.destroy()  

def updatePlayers(root, dialog):
    '''
    Updates the players in the game as selected in dialog
    
    Player names cannot by empty of white space otherwise
    they are ignored even if the are chosen ('ticked')
    
    Only 21 character names are allowed. Longer names are
    shortened to 21 characters.
    '''
    newPlayers = []
    for index, name in enumerate(dialog.PlayerName_variables):
        if dialog.PlayerCB_variables[index].get() == 1:
            # Empty names or names containing only spaces are ignored
            if not name.get().isspace() and not name.get()=="":
                # Use only 21 characters of long names
                if len(name.get()) > 20:
                    name.set(name.get()[0:20])
                newPlayers.append(name.get())
    if len(newPlayers) == 0:
        root.game.unNotifiedErrors.append('You did not select any players!')
        checkForErrors(root)
    else:
        root.game.newGame(newPlayers)
        updateScreen(root)
        dialog.destroy()
    
def updateScreen(root):
    '''
    Draws the screen, by adding dices, score board
    and game state information
    
    If any of the object are already drawn they are destroyed
    and redrawn to match the current properties of the game
    '''
    
    # First make sure that screen is empty
    
    # if root.dices does not exist --> AttributeError and pass
    # else destroy root.dices
    try: root.dices.destroy()
    except AttributeError: pass
    # if scores does not exist --> AttributeError and pass
    # else destroy root.scores
    try: root.scores.destroy()
    except AttributeError: pass
    # if scores does not exist --> AttributeError and pass
    # else destroy root.scores
    try: root.states.destroy()   
    except AttributeError: pass
    root.update()
    
    root.dices = DR.DiceRow(root, root.game)
    root.scores = SB.ScoreBoard(root, root.game)
    root.states = GS.GameState(root, root.game) 
    keyboardBindings(root)

def viewHighScores(root, event=None):
    '''
    View the high score board
    '''
    root.high_scores = HS.HighScores(root.game)
    dialog = T.Toplevel()
    dialog.title('High Scores')
    
    h1Font = tkFont.Font ( size=20, weight="bold" , family="Times")
    h2Font = tkFont.Font ( size=16, slant="italic", underline = 1, family="Times")
    bodyFont = tkFont.Font ( size=14, family="Times" )
    
    dialog.labels = {}
    dialog.labels['1:Title'] =  T.Label(dialog, text = "Top 10", font = h1Font)
    dialog.labels['2:Settings_file'] =  T.Label(dialog, text = root.high_scores.settingsfile, font = h2Font)
    string_additional = "(n = %d, s = %d, h = %d)" % (root.game.settings.no_of_dice,
                                                     root.game.settings.max_value,
                                                     root.game.settings.no_of_throws)
    dialog.labels['3:Additionals'] =  T.Label(dialog, text = string_additional, font = bodyFont)
    dialog.labels['4:Frame'] =  T.LabelFrame(dialog, text = datetime.now().ctime())
    
#    dialog._text = T.Label(dialog.labels['4:Frame'], text = hs_label_text, font = bodyFont)

    hs_label_text = ""
    dialog._text = [[]]
    dialog._text.append([])
    dialog._text[0].append( T.Label(dialog.labels['4:Frame'], text = 'Rank', font = bodyFont, pady = 10) )
    dialog._text[0].append( T.Label(dialog.labels['4:Frame'], text = 'Total', font = bodyFont, pady = 10) )
    dialog._text[0].append( T.Label(dialog.labels['4:Frame'], text = 'Name', font = bodyFont, pady = 10) )
    dialog._text[0].append( T.Label(dialog.labels['4:Frame'], text = 'Date/Time', font = bodyFont, pady = 10) )
    
    ind = 0
    for key in sorted(root.high_scores.high_scores, reverse = True):
        for score in root.high_scores.high_scores[key]:
            ind += 1
            dialog._text.append([])
            dialog._text[ind].append( T.Label(dialog.labels['4:Frame'], text = ind, font = bodyFont, padx = 30) )
            if 'total' in score:
                dialog._text[ind].append( T.Label(dialog.labels['4:Frame'], text = score['total'], font = bodyFont, padx = 30) )
            if 'name' in score:
                dialog._text[ind].append( T.Label(dialog.labels['4:Frame'], text = score['name'], font = bodyFont, padx = 30) )
            if 'datetime' in score:
                dialog._text[ind].append( T.Label(dialog.labels['4:Frame'], text = score['datetime'], font = bodyFont, padx = 30) )

    dialog.closebutton = T.Button( master = dialog, text = "Close", command = dialog.destroy )
    
    # Grid the labels and text in dialog.labels['4:Frame']
    for index, key in enumerate(sorted(dialog.labels)):
        dialog.labels[key].grid(row = index, column = 0)
    for x in range(ind+1):
        for y in range(len(dialog._text[0])):
            dialog._text[x][y].grid(row = x, column = y)
    dialog.closebutton.grid(row = index + 1, column = 0)


        

