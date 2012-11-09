# -*- coding: utf-8 -*-
'''
Created on 22 Apr 2010
Last modified on 4 May 2010

@author: Patrik Ahvenainen
'''

import Tkinter as T

class GameState(T.Frame):
    '''
    This class instance is a Tkinter Frame item which
    contains all the necessary labels for displaying game 
    state.
    '''


    def __init__(self, master, game):
        '''
        Displays game state on the frame 'master'
        from the game 'game'
        '''
        self.master = master
        self.game = game
        T.Frame.__init__(self, master)
        self.createButtons()
        self.pack(side = T.RIGHT)

    def createButtons(self):
        '''
        Create buttons to show game state
        '''
        
#        self.quitButton = T.Button ( self, text='Quit', command=self.master.destroy )
#        self.quitButton.grid(row=0, column=0, columnspan=2)
        
        self.forwardButton = T.Button (self, text='Roll dices', command=self.goForward, takefocus=0)
        self.forwardButton.grid(row=1, column=0, columnspan=2)
        
        # Create buttons indicating game state
        self.buttonList = {}       
        self.buttonList['Round_text'] = ( T.Button( self, text="Round:", command=None, bd=0, takefocus=0) )
        self.buttonList['Round_text'].grid(row=2, column=0)                    
        self.buttonList['Round_value'] = ( T.Button( self, text=self.game.gameround, command=None, bd=0, takefocus=0) )
        self.buttonList['Round_value'].grid(row=2, column=1)
        self.buttonList['Turn_text'] = ( T.Button( self, text="Turn:", command=None, bd=0, takefocus=0) )
        self.buttonList['Turn_text'].grid(row=3, column=0)    
        self.buttonList['Turn_value'] = ( T.Button( self, text=self.game.gameturn, command=None, bd=0, takefocus=0) )
        self.buttonList['Turn_value'].grid(row=3, column=1)        
        self.buttonList['Throw_turn_text'] = ( T.Button( self, text="Throw:", command=None, bd=0, takefocus=0) )
        self.buttonList['Throw_turn_text'].grid(row=4, column=0)    
        self.buttonList['Throw_turn_value'] = ( T.Button( self, text=self.game.throwturn, command=None, bd=0, takefocus=0) )
        self.buttonList['Throw_turn_value'].grid(row=4, column=1)
        self.buttonList['Current_player_text'] = ( T.Button( self, text="Current\nplayer:", command=None, bd=0, takefocus=0) )
        self.buttonList['Current_player_text'].grid(row=5, column=0)    
        self.buttonList['Current_player_name'] = ( T.Button( self, text=self.game.currentPlayer.name, command=None, bd=0, takefocus=0) )
        self.buttonList['Current_player_name'].grid(row=5, column=1)        
        
    def updateStateValues(self):
        '''
        Read values indicating game state from the game and update the button text
        '''
        self.buttonList['Round_value'].config(text=self.game.gameround)
        self.buttonList['Turn_value'].config(text=self.game.gameturn)
        self.buttonList['Throw_turn_value'].config(text=self.game.throwturn)
        self.buttonList['Current_player_name'].config(text=self.game.currentPlayer.name)

    def goForward(self):
        '''
        Access to forward function of the game. As that function 
        can change the dice values, the dices need to be redrawn.
        
        If self.game.goForward() returns 0 no action has been
        done and nothing needs to be done.
        
        Returns the action# received from the game.
        '''
        action = self.game.goForward()
        if not action == 0: 
            self.updateStateValues()
            self.master.dices.createDices()
            self.keyBoardFocus()
        return action
        
    def keyBoardFocus(self):
        '''
        Give keyboard focus only to the scores of the current player
        and show the possible value that the combination produces
        '''
        for x in range(len(self.game.players)):
            for y in range(len(self.game.settings.combinations)):
                # Players numbered 1..no_of_players
                # No keyboard focus to used scores
                scoreButton = self.master.scores.scoreButton[x][y]
                if (x+1 == self.game.currentPlayer.index) and not scoreButton.score.locked:
                    textString = "<" + str(scoreButton.score.possible_value) + ">"
                    scoreButton.config(takefocus=1, text=textString)
                
                else:
                    scoreButton.config(takefocus=0)
                    if not scoreButton.score.locked:
                        scoreButton.config(text="")
