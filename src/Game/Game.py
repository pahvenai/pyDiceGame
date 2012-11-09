# -*- coding: utf-8 -*-
'''
Created on 31 Mar 2010
Last modified on 4 May 2010

@author: Patrik Ahvenainen
'''

import Logger

# Import Game-package Modules
import Player as PL
import Dice as Nop
import Throw as Hei
import Settings as Ase
import HighScores as HS

import random

class Game(object):
    '''
    game-luokka on gamen gamemoottorin tärkein luokka. Sen luomiskutsulla luodaan myös kaikki gamen käyttämät
    luokat, joita tarvitaan game käynnistyessä. game-luokka on oikeastaan lista gamein kuuluvista muilla luokista
    sekä sisältää tiedon gamekierroksesta ja gameturnsta.
    '''
    
    

    def __init__(self, players, settings_file, max_no_of_comb = 100, log = True):
        '''
        Luo listan pelaajista. Lataa tämän jälkeen settings_filesta listan
        gamessä käytettävistä yhdistelmistä ja luon niiden perusteella
        pelaajille tulostaulukot. Luo gamein settings_filessa määritellyn
        määrän noppia.
        '''

        self.log = log
        
        # Creates if self.log: self.logger which is a logging object
        self.logsetting = Logger.Logger(self, 'Game.Game')
        if self.log: self.logger.debug("Game started")
        
        #setting properties
        self._players = players
        self._player_list = []
        self._gameround = 0
        self._gameturn = 0
        self._throwturn = 0
        self._dicelist = []
        self._end = False
        self._max_no_of_comb = max_no_of_comb
        
        # List of errors the user has not seen
        self.unNotifiedErrors = []
        # List of errors the user has seen        
        self.NotifiedErrors = []
        
        # Add settings from file
        self._settings_file = settings_file    
        self._settings = Ase.Settings(self.settings_file, self)
        if self.log: self.logger.debug("Initial settings read from file")
        
        self.setPlayersDiceThrow(players)
        
    def settingUpdate(self, players=None):
        '''
        Invoke this method when settings are updated
        
        This method clears the player and dice lists
        and creates new lists using the method
        setPlayersDiceThrow
        
        The optional parameter 'players' can be used
        to change the number and names of the players
        The 'players' is a list of names (strings)
        '''
        if players:
            self._players = players
        self._player_list = []
        self._dicelist = []
        self.setPlayersDiceThrow(self.players)
        
    def setPlayersDiceThrow(self, players):
        '''
        Append players to self.player_list and add
        dices to the self.dicelist and update self.throw
        with the new self.dicelist.
        
        The score lists are also created when creating
        players.
        
        This method should be called whenever new settings
        are read from file or new game is created.
        '''
        
        # Add players, number players 1 trough N, N=number of players
        # The creation of players is required after every change of game settings
        for index, name in enumerate(players):
            self.player_list.append(PL.Player(name, self, index+1))
        if self.log: self.logger.debug("Players added to the game")

        
        # Add all the dice
        for dummy in range(self.settings.no_of_dice):
            self.dicelist.append(Nop.Dice(self.settings.max_value))
        if self.log: self.logger.debug("Dice added to the game")
        
        # Add throw-class object
        self._throw = Hei.Throw(self)
        self.throw.update_throw()
        # Add empty player as current player at the beginning of the game
        # This allows for a call [game].currentPlayer.name
        self._currentPlayer = PL.Player('-', self, 0)
        if self.log: self.logger.debug("Properties of current throw calculated")
        
        
    def goForward(self):
        '''
        Advance in the game if possible
        '''
        # Check that the game hasn't ended
        if not self.end:
            # go forward if first round
            if self.gameround == 0:
                self.next_gameround()
                self.next_gameturn()
                self.next_throwturn()
                self._currentPlayer = self.player_list[self._gameturn-1] 
                self.throwAllDices(unlock=True)
                return 1
            # If first throw turn, advance game and throw all the dice
            if self.throwturn == 0:
                if self.gameturn == 0:
                    self.next_gameturn()
                self.next_throwturn()
                # Make sure that all dice can be thrown
                self.throwAllDices(unlock=True)
                return 2
            # If there are throws remaining, throw again
            # Parameter throwturn starts with 0
            elif self.throwturn < self.settings.no_of_throws:
                self.next_throwturn()
                self.throwAllDices()
                return 3
        return 0
    
    def throwAllDices(self, unlock = False):
        '''
        Throw all dice in the game. Parameter 'unlock' can be used
        to indicate that all dice should be unlocked before throwing. 
        '''
        for dice in self.dicelist:
            if unlock: dice.unlock()
            dice.throw()
            self.throw.update_throw()      
            
    def SequentialChoice(self):
        '''
        Chooses next combination from the current player
        to mark the scores for.
        '''
        self.currentPlayer.score_list.value = self.gameround - 1
                            
    def randomChoice(self):
        '''
        Chooses randomly a combination from the current player
        to mark the scores for.
        '''
        values = range(0, len(self.settings.combinations))
        currentGameturn = self.gameturn
        if not self.end:
            while self.gameturn == currentGameturn:
                index = random.choice(values)
                self.currentPlayer.score_list.value = index
    
    def nextPlayer(self):
        '''
        This method is called when a player marks his score
        on his score sheet. It advances the game to the next
        player if possible.
        '''
        # Go to next player, if possible
        self._throwturn = 0
        self.next_gameturn()
        self.goForward()
        self._currentPlayer = self.player_list[self._gameturn-1] 
        
    def endGame(self):
        '''
        Check for high scores and mark mark the game 
        as ended
        '''
        self.high_scores = HS.HighScores(self)
        self.high_scores.appendScores()
        self._end = True
        if self.log: self.logger.info("Game has ended.")
        
    def newGame(self, players=None):
        '''
        Start a new game with the same settings and players
        
        The optional parameter 'players' can be used
        to change the number and names of the players
        The 'players' is a list of names (strings)
        '''
        self._gameround = 0
        self._gameturn = 0
        self._throwturn = 0
        self.settings.initializeToZero()
        self.settings.settings_from_file(self.settings.settings_file)
        self.settingUpdate(players)
        self._end = False
        if not players:
            if self.log: self.logger.info("Game restarted with the same settings")
        else:
            if self.log: self.logger.info("Game restarted with new players")

    #    -----------------------------------
    # 
    #    Properties which have an advancement
    #    function called next_<property_name>
    #    in addition to a simple getter.
    #    In alphabetical order.
    # 
    #    -----------------------------------

            
    def get_gameround(self):
        return self._gameround
    def next_gameround(self):
        self._gameround += 1
        if self._gameround > len(self.settings.combinations):
            self.endGame()
    gameround = property(get_gameround)
    
    def get_gameturn(self):
        return self._gameturn
    def next_gameturn(self):
        self._gameturn += 1
        if self._gameturn > len(self.player_list):
            # Go to first player
            self._gameturn = 0
            # Start new round
            self.next_gameround()
    gameturn = property(get_gameturn)
    
    def get_throwturn(self):
        return self._throwturn
    def next_throwturn(self):
        self._throwturn += 1
    throwturn = property(get_throwturn)
    
    #    -----------------------------------
    # 
    #    Properties with only getters.
    #    In alphabetical order
    # 
    #    -----------------------------------
    
    def get_currentPlayer(self):
        return self._currentPlayer
    currentPlayer = property(get_currentPlayer)

    def get_dicelist(self):
        return self._dicelist
    dicelist = property(get_dicelist)
    
    def get_end(self):
        return self._end
    end = property(get_end)
    
    def get_max_no_of_comb(self):
        return self._max_no_of_comb
    max_no_of_comb = property(get_max_no_of_comb)
    
    def get_player_list(self):
        return self._player_list
    player_list = property(get_player_list)
    
    def get_players(self):
        return self._players
    players = property(get_players)
    
    def get_settings(self):
        return self._settings
    settings = property(get_settings)
    
    def get_settings_file(self):
        return self._settings_file
    settings_file = property(get_settings_file)
    
    def get_throw(self):
        return self._throw
    throw = property(get_throw)
    
