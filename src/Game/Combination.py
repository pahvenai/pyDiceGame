# -*- coding: utf-8 -*-

'''
Created on 2 Apr 2010
Last modified on 3 May 2010

@author: Patrik Ahvenainen
'''

import Logger

class Combination(object):
    '''
    Combinations are the heart and soul of the dice game. They tell
    how many points a combination of dice values can produce. 
    
    Some combinations have indices that separate combinations with 
    same code. For example:
    
    Combination    Code        Index    Name                Type
    
    4's            '000100'    4        's                  'ENUMERATE': 'MAX_VALUE'
    5's            '000100'    5        's                  'ENUMERATE': 'MAX_VALUE'
    straight of 3  '000200'    3        'mm, straight of'   'ENUMERATE': 'MAX_VALUE_AND_NO_OF_DICE'
    straight of 4  '000200'    4        'mm, straight of'   'ENUMERATE': 'MAX_VALUE_AND_NO_OF_DICE'
    Chance         '000000'    0        'Chance'            'SINGLE': 'ALL'
    
    In type the key 'SINGLE' tells that only one combination of 
    this code should be used in the game. The possible values after 
    that key are 'ALL', 'ODD', 'EVEN' which tell, respectively, that
    the combination applied to all games, the combination is applied
    only to games with odd number of dice and that the combination is 
    applied only to games with even number of dice.   
    
    In the type the key 'ENUMERATE' tells that more than one combination
    of the same code can appear in the game. The values for this key are
    'MAX_VALUE', 'MAX_VALUE_AND_NO_OF_DICE' and 'NO_OF_DICE'. To see how
    they effect on how many combinations are created when reading new
    rules from a file see Settings-class documentation.
    
    Possible combination for which there are rules are:
    
    Code        Name                Type
    
    '000000'    'Chance'            'SINGLE': 'ALL'
    '000100'    '\'s'               'ENUMERATE': 'MAX_VALUE'
    '000200'    ', straight of'     'ENUMERATE': 'MAX_VALUE_AND_NO_OF_DICE'
    '000300'    ' of a kind'        'ENUMERATE': 'NO_OF_DICE'
    '000400'    'Two pairs'         'SINGLE': 'ALL'
    '000500'    ', divisible by'    'ENUMERATE': 'MAX_VALUE'
    '000600'    ', undivisible by'  'ENUMERATE': 'MAX_VALUE'
    '000700'    'Yahtzee'           'SINGLE': 'ALL'
    '000800'    'Fair division'     'SINGLE': 'EVEN'
    '000900'    'Unfair division'   'SINGLE': 'ODD'
    '001000'    'Full House'        'SINGLE': 'ALL'
        
    '''

    CodeList = {
                '000000': {
                         'name': 'Chance',
                         'type': {'SINGLE': 'ALL'}, # Single combination
                         },   
                '000100': {
                         'name': '\'s',
                         'type': {'ENUMERATE': 'MAX_VALUE'}, # enumerate: 1..maximum value
                         },
                '000200': {
                         'name': ', straight of',
                         'type': {'ENUMERATE': 'MAX_VALUE_AND_NO_OF_DICE'}, # enumerate: min(number of dice, maximum value)
                         }, 
                '000300': {
                         'name': ' of a kind',
                         'type': {'ENUMERATE': 'NO_OF_DICE'}, # enumerate: 1..number of dice
                         },
                '000400': {
                         'name': 'Two pairs',
                         'type': {'SINGLE': 'ALL'}, # Single combination
                         },
                '000500': {
                         'name': ', divisible by',
                         'type': {'ENUMERATE': 'MAX_VALUE'}, # Enumerate: 1..maximum value
                         },
                '000600': {
                         'name': ', undivisible by',
                         'type':{'ENUMERATE': 'MAX_VALUE'}, # Enumerate: 1..maximum value
                         },
                '000700': {
                         'name': 'Yahtzee',
                         'type': {'SINGLE': 'ALL'}, # Single combination
                         },
                '000800': {
                         'name': 'Fair division',
                         'type': {'SINGLE': 'EVEN'}, # Single combination: even number of dice
                         },
                '000900': {
                         'name': 'Unfair division',
                         'type': {'SINGLE': 'ODD'}, # Single combination: odd number of dice
                         },                        
                '001000': {
                         'name': 'Full House',
                         'type': {'SINGLE': 'ALL'}, # Single combination
                         },                                                                  
                }

    def __init__(self, code, game, index=0):
        '''
        The combination are created when the game is loaded and are added
        to the combination list of the game. Combination can be locked
        which means that the combination can not be used in the game again.
        The combination instances should thus be instantiated for each
        player.
        
        '''
        self._game = game
        self._locked = False
        self._code = code
        self._name = Combination.CodeList[str(self._code)]['name']
        self._type = Combination.CodeList[str(self._code)]['type']             
        self._index = index
        self._value = 0
        self._possible_value = 0
                 
        # Creates self.logger which is a logging object
        if self.game.log: self.logsetting = Logger.Logger(self, 'Game.Combination')
    
    def value_by_code(self):
        '''
        Calculate the values of the default combinations by their code
        
        self.index is an integer between 1 and max_value and it is 
        used to index enumerated combinations such as
        1 of a kind, 2 of a kind, 3 of a kind, etc. 
        
        If the specific condition for the combination is filled,
        non-zero value is returned. If the condition is not met, zero is
        returned
        '''
        
        # Introduce some shorter variable name for readability
        chance = self.game.throw.chance
        values = self.game.throw.silmaluvut.values()
        throw = self.game.throw
                
        if self.code == '000000': # 'Chance'
            return ( chance )
        if self.code == '000100': # '\'s'
            if self.index in values:
                return ( self.index * values.count(self.index) )
            else: return 0
        if self.code == '000200': # 'mm, straight of'
            if self.index in self.game.throw.straight_of_mm:
                # Find out what is the maximum length of the straights
                max_straight = min(self.game.settings.max_value, self.game.settings.no_of_dice)
                # Value returned is 30 * (index/max_straight)^2
                # If the straight is the longest possible 30 points is rewarded
                # and less for each 
                return ( int(40 * (float(self.index) / float(max_straight))**2 ) )
            else: return 0
        if self.code == '000300': # 'nn of a kind'
            if self.index in throw.nn_of_a_kind:
                return ( self.index * max(throw.nn_of_a_kind[self.index])  )
            else: return 0        
        if self.code == '000400': # 'two pairs'
            if 2 in throw.nn_of_a_kind:
                pair_list_length = len(throw.nn_of_a_kind[2])
                # Make sure that there are two of something
                if 2 in throw.nn_of_a_kind:
                    # Make sure that there are more than one pair
                    if pair_list_length > 1:
                        # return the values of the two pairs
                        return ( (throw.nn_of_a_kind[2][pair_list_length-2] + \
                                  throw.nn_of_a_kind[2][pair_list_length-1])  *2 )
                    else: return 0                 
                else: return 0
            # Two pairs can be replaced with one four of a kind
            elif 4 in throw.nn_of_a_kind:
                return ( max(throw.nn_of_a_kind) * 4 )
            else: return 0        
        if self.code == '000500': # 'kk, divisible by'
            sum = 0
            for dice_value in values:
                sum += dice_value % self.index
            if sum == 0:
                return ( chance  )
            else: return 0        
        if self.code == '000600': # ', undivisible by'
            product = 1
            for dice_value in values:
                product *= (dice_value % self.index)*2
            if product > 1:
                return ( chance  )
            else: return 0        
        if self.code == '000700': # 'Yahtzee'
            # 
            if self.game.settings.no_of_dice in throw.nn_of_a_kind:
                return ( 50 )
            else: return 0        
        if self.code == '000800': # 'Fair division'
            for index in throw.nn_of_a_kind_absolute:
                # If there are any odd indices return zero
                if (index % 2) > 0:
                    return 0
            # Only even indices have been found, return chance
            return ( chance )    
        if self.code == '000900': # 'Unfair division'
            sum = 0
            for index in throw.nn_of_a_kind_absolute:
                # Check for odd indices
                if (index % 2) > 0:
                    # Count the number of odd indices == sum
                    sum += len(throw.nn_of_a_kind_absolute[index])
            # if exactly one odd index has been found return chance
            if sum == 1:
                return ( chance )
            else: return 0        
        if self.code == '001000': # 'Full House'
            # requirement: at least one times 3(+) of a kind
            if 3 in throw.nn_of_a_kind:
                # requirement: at least two pairs
                if 2 in throw.nn_of_a_kind_absolute:
                    maxThree = max(throw.nn_of_a_kind[3])
                    maxTwo = 0
                    for item in throw.nn_of_a_kind[2]:
                        if item != maxThree:
                            if item > maxTwo: 
                                maxTwo = int(item)
                    return ( maxTwo * 2 + maxThree * 3 )
            # possible to replace pair + 3 of a kind
            # with one five of a kind
            if 5 in throw.nn_of_a_kind:
                return ( max(throw.nn_of_a_kind[5]) )
            else: return 0
        errorstring = "No code Found for code %s! Zero is returned." % self.code
        if self.game.log: self.logsetting.addError(self.logger, self.game.unNotifiedErrors, errorstring)

        return 0
    
    
    def get_possible_value(self):
        '''
        Return the value this combination can make with the
        dice in the current throw
        '''
        return self.value_by_code()
    def set_possible_value(self):
        self._possible_value = self.value_by_code()
    possible_value = property(get_possible_value)
        
    def get_value(self):
        '''
        If not locked, return value by combination code
        else return 0
        '''
        if self.locked: return self._value
        else: return 0
    def set_value(self, value):
        '''
        If not locked, return possible value and lock dice
        else pass
        '''
        if not self.locked:
            self._value = self.possible_value
            self._locked = True
    value = property(get_value, set_value)

    #    -----------------------------------
    # 
    #    Properties with only getters.
    #    In alphabetical order
    # 
    #    -----------------------------------
    
    def get_code(self):
        return self._code
    code = property(get_code)   
    
    def get_game(self):
        return self._game
    game = property(get_game)
    
    def get_index(self):
        return self._index
    index = property(get_index)
    
    def get_locked(self):
        return self._locked
    locked = property(get_locked)      
    
    def get_type(self):
        return self._type
    type = property(get_type)     
