# -*- coding: utf-8 -*-

'''
Created on 10 Apr 2010

@author: pate
'''

import Tkinter as T
import os
from SimpleCallback import SimpleCallback

MAX_NO_OF_DICES_PER_COLUMN = 5

class DiceRow(T.Frame):
    '''
    classdocs
    '''


    def __init__(self, master, game):
        '''
        Create a dice row from the dices of the game
        '''
        self.master = master
        self.game = game
        T.Frame.__init__(self, master)
        self.createDices()
        self.pack(side = T.LEFT)

        
    def createDices(self):
        '''
        Create all the dices as Buttons
        
        If the number of the dices is more than 5
        create the dices in two columns
        '''
        
#        "/home", "pate", "workspace", "Yleinen noppagame", "src", "GUI"
        
        self.diceButton = []
        self.gifs = []
        self.trash = []
        
        for index, dice in enumerate(self.game.dicelist):
            
            image_path = self.getDicePhotoFileName(dice)
            
            self.gifs.append(T.PhotoImage(file = image_path, master=self))
            callback = SimpleCallback(self.lockDice, dice, index)
            self.diceButton.append(T.Button( self, image=self.gifs[index], width=100, command=callback, bd=0, takefocus=0))
            self.diceButton[index].image = self.gifs[index] # keep a reference!
            # If the number of dices is greater than the maximum per one column divide 
            # dices in two columns
            if len(self.game.dicelist) > MAX_NO_OF_DICES_PER_COLUMN:
                division = int( (len(self.game.dicelist) + 1) / 2)
                if index < division:
                    self.diceButton[index].grid(row=index, column=0)
                else:
                    self.diceButton[index].grid(row=index-division, column=1)
            # draw the dice in one column
            else:
                self.diceButton[index].grid(row=index, column=0)
            
    def lockDice(self, dice, index):
        '''
        lock a dice and redraw that dice
        '''
        dice.toggle_locked()
        image_path = self.getDicePhotoFileName(dice)
        self.gifs[index] = T.PhotoImage(file = image_path, master=self)
        self.diceButton[index].config(image = self.gifs[index])        
        self.diceButton[index].flash()
        
    def getDicePhotoFileName(self, dice):
        '''
        Returns the file name of the image that represents the value
        of the dice.
        
        Dice images are located in ./Kuvat/Musta kuusitahkonoppa
        where ./ represents current path
        The dice image are named 01.gif, 02.gif, ... , 09.gif      
        and the locked dice image are named
        01_locked.gif, 02_locked.gif, ... , 09_locked.gif  
        '''

        help_path = os.path.join("Kuvat", "Musta kuusitahkonoppa")
        filename = str(0)+str(dice.value)
        if dice.locked:
            filename += "_locked"
        filename += ".gif"
        final_path = os.path.join(help_path, filename)   
        return final_path
        