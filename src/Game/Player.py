# -*- coding: utf-8 -*-
'''
Created on 31 Mar 2010

@author: pate
'''

import ScoreList as Tul

class Player(object):
    '''
    The Player class 

    '''


    def __init__(self, given_name, game, index):
        '''
        The players can be only created after the game settings
        have been loaded since a score list is created for every
        player when the player is initialized.
        '''
        self._name = None
        self.name = given_name
        self.index = index
        self._game = game
        self._score_list = Tul.ScoreList(self)
                
    def get_name(self):
        return self._name
    def set_name(self, new_name):
        self._name = new_name
    name = property(get_name, set_name)
    
    def get_score_list(self):
        return self._score_list
    score_list = property(get_score_list)    
        
    def get_game(self):
        return self._game
    game = property(get_game)
    