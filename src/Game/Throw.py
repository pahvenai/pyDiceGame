# -*- coding: utf-8 -*-

'''
Created on 31 Mar 2010
Last modified on 4 May 2010


@author: Patrik Ahvenainen
'''

class Throw(object):
    '''
    Yhdessä kaikkien noppien silmäluvut muodostavat throwvuoro-tiedon kanssa heiton. throw-luokan ilmentymä luodaan kun
    ensimmäinen player on heittänyt noppia. throw-luokka tarjoaa Yhdistelmät-luokalle jotain hyödyllisiä
    tietoja noppien silmäluvuista, kuten kirjaston (dict) noppien silmäluvuista, m:n nopan suorista sekä n:stä
    kappaleesta noppia, joilla on sama silmäluku (n samaa). Lisäksi throw-luokasta saadaan kaikkien noppien
    silmälukujen summa (sattuma).
    '''


    def __init__(self, game):
        '''
        throwvuoro luodaan gamen ensimmäisen playern heittäessä noppaa
        '''
        self._game = game
        self.nullify_throw()
        
    def update_throw(self):
        self.nullify_throw()
        
        # Calculate chance
        for dice in self.game.dicelist:
            self._chance += int(dice.value)
        
        # Build dict of dice sides
        for index, dice in enumerate(self.game.dicelist):
            self._silmaluvut[index+1] = int(dice.value)
        
        # Build dict of nn of a kinds
        CurValues = sorted(self.silmaluvut.values())
        for index in range(1, self.game.settings.max_value+1):
            if CurValues.count(index) > 0:
                if not CurValues.count(index) in self.nn_of_a_kind:
                    self._nn_of_a_kind[CurValues.count(index)] = [index]
                else:
                    self._nn_of_a_kind[CurValues.count(index)].append(index)
                
        # Copy the current values of nn_of_a_kind to _nn_of_a_kind_absolute
        # This list includes each value only ones in a dictionary format
        # [3, 5, 5, 5, 2, 5, 5] --> {1: [2, 3], 4:[5]} 
        for index in self.nn_of_a_kind:
            self._nn_of_a_kind_absolute[index] = []
            for inner in self.nn_of_a_kind[index]:
                self._nn_of_a_kind_absolute[index].append(inner)

        # Create a dictionary for which each value is marked under each key 
        # that is smaller than equal to the number of occurences of that value
        # [3, 5, 5, 5, 2, 5, 5] --> {1: [2, 3, 5], 2:[5], 3:[5]  4:[5]}         
        list_of_keys = self._nn_of_a_kind.keys()
        # Go through all the keys and add all occurences where
        # for every number index < key1 
        for key1 in list_of_keys:
            # Go from key-1 to 1 in descending order
            for index in range(int(key1)-1, 0, -1):
                if not index in self.nn_of_a_kind:
                    self._nn_of_a_kind[index] = self.nn_of_a_kind[key1]
                else:
                    for number in self._nn_of_a_kind[key1]:
                        self._nn_of_a_kind[index].append(number)
                        
        # Build dict of straights of mm
        # Go through all possible starting numbers of the straights
        for index in range(1,self.game.settings.max_value+1):
            # Skip all values that do no appear in value list
            if index in CurValues:
                # If not initialised, initialise the dict list of lists for key==1
                if not (1 in self._straight_of_mm):
                    self._straight_of_mm[1] = [[index]]
                # If dict initialised for key==1 add the value (list) to the list for key==1
                else:
                    self._straight_of_mm[1].append([index])
                # Go trough all possible straights for which value=index..maximumValue
                for additional in range (index+1, self.game.settings.max_value+1):
                    # Initialise straightlist with the value of index
                    straightlist = [index]
                    # Add all numbers from index+1..additional to straightlist
                    for integernumber in range(1,additional-index+1):
                        # Add only values that are in value list
                        if ((index + integernumber) in CurValues):
                            straightlist.append(index + integernumber)
                        # If value is not in value list break the current for loop
                        else:
                            break
                    # Do not add single values
                    if len(straightlist) > 1:
                        # If dict is not initialised for a straight of the length
                        # of straightlist, initialise
                        if not (len(straightlist) in self._straight_of_mm):
                            self._straight_of_mm[len(straightlist)] = [straightlist]
                        else:
                            # Skip straights that have already been added
                            if self._straight_of_mm[len(straightlist)].count(straightlist) == 0:
                                # Add additional straight of the length of straightlist to
                                # the list of straights
                                self._straight_of_mm[len(straightlist)].append(straightlist)
                    
        
        
    def nullify_throw(self):
        self._silmaluvut = {}
        self._chance = 0
        self._nn_of_a_kind = {}
        self._straight_of_mm = {}
        self._nn_of_a_kind_absolute = {}
        
    #    -----------------------------------
    # 
    #    Properties with only getters.
    #    In alphabetical order
    # 
    #    -----------------------------------
    def get_chance(self):
        return self._chance
    chance = property(get_chance)
             
    def get_game(self):
        return self._game
    game = property(get_game)
    
    def get_nn_of_a_kind(self):
        return self._nn_of_a_kind
    nn_of_a_kind = property(get_nn_of_a_kind)      

    def get_nn_of_a_kind_absolute(self):
        return self._nn_of_a_kind_absolute
    nn_of_a_kind_absolute = property(get_nn_of_a_kind_absolute)   
       
    def get_silmaluvut(self):
        return self._silmaluvut
    silmaluvut = property(get_silmaluvut)
    
    def get_straight_of_mm(self):
        return self._straight_of_mm
    straight_of_mm = property(get_straight_of_mm)       