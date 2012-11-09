# -*- coding: utf-8 -*-

'''
Created on 4 Apr 2010

@author: pate
'''

import Combination as Yhd

class ScoreList(object):
    '''
     score_liston kerätään pelaajien pisteet. Tulostaulocked ei ole mitään tietoa siitä, mistä
    yhdistelmästä mikäkin pistemäärä tulee. Kokonaissaldo päivitetään aina muuttaessa yhtä valuea.

    '''


    def __init__(self, player):
        '''
        score_list playerlle luodaan aina uuden gamen aloittamisen
        yhteydessä sekä asetuksia muuttaessa.
        '''
        self._player = player
        self._combinations = []
        co = self.player.game.settings.combinations
        for index, y in enumerate(self.player.game.settings.combinations):
            self._combinations.append(Yhd.Combination(co[index].code, co[index].game, co[index].index))
            self._value = 0
        self._total = 0
        
        
    def updateTotal(self):
        '''
        Update the total score of the player by calculating the score
        from every combination score.
        '''
        self._total = 0
        for combi in self.combinations:
            self._total += combi.value
    
    def get_combinations(self):
        return self._combinations
    combinations = property(get_combinations)

    def get_total(self):
        self.updateTotal()
        return self._total
    total = property(get_total)    
        
    def get_value(self, index):
        return self.combinations[index].value
    def set_value(self, index):
        if self.player.game.gameturn == self.player.index:
            self.combinations[index].value = "Check value"
            self.updateTotal()
            self.player.game.nextPlayer()
    value = property(get_value, set_value)

    def get_player(self):
        return self._player
    player = property(get_player)
         
    
        