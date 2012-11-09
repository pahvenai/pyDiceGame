# -*- coding: utf-8 -*-
'''
Created on 10 Apr 2010

@author: pate
'''

import Tkinter as T
import tkFont
import Game.Combination as Yhd
from Game.Game import Logger
import GUI as G

class ScoreBoard(T.Frame):
    '''
    Score board is the place where player names, combination names
    and player scores are visualised. It is a Tkinter Frame object
    and the items are packed in a grid formation using grid(row, column). 
    '''


    def __init__(self, master, game):
        '''
        Constructor
        '''
        self.master = master
        self.game = game
        T.Frame.__init__(self, master)
        self.pack(side = T.LEFT)
        self.createScoreBoard()
        
        # Creates self.logger which is a logging object
        self.logsetting = Logger.Logger(self, 'GUI.ScoreBoard')
        self.logger.info('New score board created')
        
        
        
    def createScoreBoard(self):
        '''
        Create a score board from the game information, mainly
        the player names, combination names and combination list.
        Each score board item is created as a Tkinter Button in order
        to facilitate access to different actions related to the item.
        '''
        
        self.RegularFont = tkFont.Font(family="Times", size=10, slant=tkFont.ITALIC)
        
        # Create the combination names
        combButton = [] # Initialise a list of Combination names
        for index, combination in enumerate(self.game.settings.combinations):
            combination_name = ""
            # If combination is numberable, add this number to the front of the name
            if self.game.settings.combinations[index].index > 0:
                combination_name = str(self.game.settings.combinations[index].index)
            combination_name += str(Yhd.Combination.CodeList[self.game.settings.combinations[index].code]['name'])
            combButton.append(T.Button( text=combination_name, master = self, borderwidth=0, pady=0, takefocus=0))
            combButton[index].grid(row = index+1, column = 0)
        combButton.append(T.Button( text="TOTAL", master = self, takefocus=0))
        combButton[index+1].grid(row = index+2, column = 0)
            
        # Add scores for every player and for every combination 
        self.scoreButton = [] # Initialize Scoreboard 
        # Loop over players
        for index, player in enumerate(self.game.player_list):
            self.scoreButton.append([])
            # Loop over combinations
            for index2, score in enumerate(player.score_list.combinations):
                self.scoreButton[index].append(ScoreBoardScore( text="", score_board = self, score=score, player=player,\
                                                                row=index2+1, column=index+1, borderwidth=1, pady=0, \
                                                                font = self.RegularFont))
                self.scoreButton[index][index2].grid(row = index2+1, column = index + 1)
            self.no_of_scores = index        
        
        # Add total score buttons
        self.totals = []
        for index, player in enumerate(self.game.player_list):
            self.totals.append(TotalScore( text="-", player=player, master = self,row=len(self.game.settings.combinations)+1, column= index+1))
            self.totals[index].grid(row = len(self.game.settings.combinations)+1, column = index+1)         
        
        # Add player name buttons
        self.nameButton = []
        for index, player in enumerate(self.game.player_list):
            self.nameButton.append(T.Button( text=self.game.player_list[index].name, master = self, takefocus=0))
            self.nameButton[index].grid(row = len(self.game.settings.combinations)+2, column = index+1) 
            
        
class ScoreBoardScore(T.Button):
    '''
    ScoreBoardScore instances are Tkinter Buttons with 
    a few other attributes. They have a funtion that should be used
    when a player is trying to mark a score.
    '''


    def __init__(self, score_board, text, score, player, row, column, borderwidth, pady, font):
        '''
        Add column, row, master item, score and player as 
        attributes and initialise the Tkinter Button
        '''
        self.score_board = score_board
        self.score = score
        self.player = player
        self.column = column
        self.row = row

        T.Button.__init__(self, score_board, text=text, command=self.markScore, borderwidth=borderwidth, \
                          pady=pady, font=font, height = 1)
        
    def markScore(self):
        '''
        This function should be used when a player is trying to mark a score.
        Only current player can mark scores and only if the score is not
        already used.
        '''
        # Only marked available scores
        if not self.score.locked:
            # Only mark scores for current player
            if self.player == self.score_board.game.currentPlayer:
                # Mark the score in the score board of the game
                self.player.score_list.value = self.row-1
                UsedFont = tkFont.Font(family="Times", size=10, weight=tkFont.BOLD)
                self.config(text=self.score.value, font=UsedFont)
                self.grid(row = self.row, column = self.column)
                # Update total values of all players
                for label in self.score_board.totals:
                    label.updateScore()
                # Print new dices and update state values
                self.score_board.master.dices.createDices()
                self.score_board.master.states.updateStateValues()
                self.master.master.states.keyBoardFocus()
                if self.score_board.game.end:
                    G.viewHighScores(self.score_board.master)
            # Log a warning if trying to access non-current player scores
            else:
                try:
                    warningstring = '\n\tAttempting to give scores to non-current player.\n ' + \
                                     '\tTried to access player \'%s\' when current player is \'%s\'' % \
                                     (self.player.name, self.master.game.currentPlayer.name)
                    self.score_board.logger.warning(warningstring)
                    print warningstring
                # if there is no current player, catch resulting AttributeError and log a warning
                except AttributeError:
                    warningstring = '\n\tAttempting to give scores to player when no player is up.\n ' + \
                                     '\tTried to access player \'%s\' ' % self.player.name
                    self.score_board.logger.warning(warningstring)
                    print warningstring 
        else:
            warningstring = 'The score is already marked and cannot be used again in this game'
            self.score_board.logger.warning(warningstring)
            print warningstring


class TotalScore(T.Button):
    '''
    Total score is a Tkinter Button-object which has
    an updateScore function which queries the total
    from the game and updates the Button text
    '''


    def __init__(self, master, text, player, row, column):
        '''
        Add column, row, master item, and player as 
        attributes and initialise the Tkinter Button
        '''
        self.column = column
        self.row = row
        self.master = master
        self.player = player
        
        T.Button.__init__(self, master, text=text, command=self.updateScore, takefocus=0)    
        
    def updateScore(self):
        '''
        Total score should be updated every time a score is marked
        on the score board. This function calculates the total 
        from the scores of the player to whose score board this total
        score belongs to.
        '''
        self.config(text=self.player.score_list.total)
        self.update()
        self.grid(row = self.row, column = self.column)
        
        