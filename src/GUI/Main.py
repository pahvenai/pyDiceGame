'''
Created on 18 Apr 2010
Last Update 3 May 2010

@author: Patrik Ahvenainen
'''

# These can be changed during the game.
# These are the default values.
SETTINGS_FILE = "Basic Yahtzee.dat"
PLAYERS = "Player 1" , "Player 2"#, "Player 3", "Player 4"
MAX_NO_OF_COMBINATIONS = 30

import os, sys
# Add parent folder in the sys.path if not there already
parent = os.path.split(os.getcwd())[0]
if parent not in sys.path:
    sys.path.append(parent)

import Game.Game as P
import Tkinter as T
import GUI
from Game.Logger import Logger
#import Game.Logger as Logger

if __name__ == '__main__':
    
    root= T.Tk()
    root.title('General Dice Game')
    TheGame = P.Game(PLAYERS, SETTINGS_FILE, 30)
    root.game = TheGame
    
    # Create a logger, referenced as root.logger
    if root.game.log: root.logSettings = Logger(root, 'GUI.main')
       
    GUI.updateScreen(root)
    if root.game.log: root.logger.info("Screen created")
    
    GUI.createMenu(root)
    if root.game.log: root.logger.info("Menu created")
    
    GUI.keyboardBindings(root)
    if root.game.log: root.logger.info("Keyboard bindings created")

    root.mainloop()