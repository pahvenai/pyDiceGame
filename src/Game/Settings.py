# -*- coding: utf-8 -*-

'''
Created on 1 Apr 2010
Last modified on 4 May 2010

@author: Patrik Ahvenainen
'''

NMIN = 1
NMAX = 9
DEFAULT_N = 5
SMIN = 2
SMAX = 9
DEFAULT_S = 6
HMIN = 1
HMAX = 10
DEFAULT_H = 3

COMB_PARAMETER_LIST = ['nmin', 'nmax','smin', 'smax', 'hmin', 'hmax', 'indexmin', 'indexmax']

DEFAULT_SETTINGS = "Basic Yahtzee.dat"

import Combination as Yhd
import Logger


class Settings(object):
    '''
     game-luokan jälkeen toiseksi tärkein luokka on varmaankin settings-luokka. Tässä luokassa määritellään
    gamesäännöt. gamesettings luodaan lukemalla tiedostosta gamesettings. gameasetuksiin luetaan eri
    yhdistelmien lisäksi oletusarvot seuraaville muuttujille: roundten lukumäärä, noppien maksimisilmäluku ja
    throwvuorojen lukumäärä yhdellä gamevuorolla. Näiden kolmen muuttujien arvoja voidaan muuttaa ennen
    gamen alkua (gameround 0).
    '''


    def __init__(self, tiedoston_nimi, game):
        '''
        Luo asetuksiin tarvittavat muuttujat. Muuttujien arvot luetaan game-
        asetuksista kutsumalla metodia set_Yhdistelmalista_tiedostosta(...)
        '''
        
        self._game = game
        # Creates if self.game.log: self.logger which is a logging object
        if self.game.log: self.logsetting = Logger.Logger(self, 'Game.Settings')
        self._settings_file = tiedoston_nimi
        self._no_of_dice = 0
        self._max_value = 0
        self._no_of_throws = 0
        
        self.initializeToZero()
        self.settings_from_file(tiedoston_nimi)
        
    def initializeToZero(self):
        self._combinations = {}
        self._combinations_raw = {}
        self._combinationcodelist = []
        
        self.AsDic = {}
        
    def settings_from_file(self, tiedoston_nimi):
        '''
        Lukee gamesettings-tiedostosta käytettävät yhdistelmät sekä
        roundten lukumäärän, noppien maksimisilmäluvun ja throwvuorojen
        lukumäärän yhdellä gamevuorolla.
        '''
        self._settings_file = tiedoston_nimi
        filtsu = open(tiedoston_nimi, 'r')
        
        newAsetus =  {'n': 0, 's': 0, 'h': 0}
        repeatcount, comb_repeat_count, combinationcount = 0, 0, 0
        # list of possible combinations
        self._combinations_raw = {}
        # list of combination codes already read and listed
        self._combinationcodelist = []
        
        for line in filtsu:
            wordlist = line.split()    
            for index, word in enumerate(wordlist):
                # Read possible values for number of dice
                if word.lower() == "#n#":
                    # Check that this is not end of line
                    if index + 1 < len(wordlist): 
                        # Don't overwrite 
                        if newAsetus['n'] == 0:
                            newAsetus['n'] = wordlist[index+1]
                        else:
                            repeatcount += 1
                if word.lower() == "#s#":
                    if index + 1 < len(wordlist):
                        if newAsetus['s'] == 0:
                            newAsetus['s'] = wordlist[index+1]
                        else:
                            repeatcount += 1
                if word.lower() == "#h#":
                    if index + 1 < len(wordlist):
                        if newAsetus['h'] == 0:
                            newAsetus['h'] = wordlist[index+1]
                        else:
                            repeatcount += 1
                        
                
                if word.lower() == "#y#":
                    # Check that a code exists for the combination
                    if index + 1 < len(wordlist):
                        # Check that the combination is not already added to the list of possible combinations
                        if (wordlist[index+1] not in self._combinationcodelist):
                            # Only add combination whose code is defined in 'Yhd.Combination.CodeList'
                            if wordlist[index+1] in Yhd.Combination.CodeList:
                                self._combinations_raw[combinationcount] = {'code': wordlist[index+1]}
                                # Add the code of the combination to a list of combination codes
                                self._combinationcodelist.append(wordlist[index+1])
                                # Check to see if there are any parameter associated to this combination
                                # Loop over the rest of the line in which this combination occured
                                for combIndex in range(index, len(wordlist)-1):
                                    # Loop over possible parameters listed in 'Comb_parameter_list'
                                    for parameter in COMB_PARAMETER_LIST:
                                        if wordlist[combIndex].lower() == parameter:
                                            if combIndex+1 < len(wordlist):
                                                try:
                                                    self._combinations_raw[combinationcount][parameter] = int(wordlist[combIndex+1])
                                                except ValueError:
                                                    warningstring = "The value '" + str(wordlist[combIndex+1]) + \
                                                                  "' of parameter '" + str(parameter) + \
                                                                  "' cannot be converted to integer and the parameter is ignored "
                                                    if self.game.log: self.logger.warning(warningstring)           
                                combinationcount += 1
                            else:
                                comb_repeat_count += 1

        #
        #    BEGIN CHECK FOR ERRORS AND WARNINGS
        #

        if combinationcount == 0:
            criticalstring = "No dice combinations found from file '" + str(self.settings_file) + "'! " + \
                             "Loading default settings '" + str(DEFAULT_SETTINGS) + "'."
            if self.game.log: self.logsetting.addError(self.logger, self.game.unNotifiedErrors, criticalstring, critical=True)
            self.new_settings(DEFAULT_SETTINGS)
            return

        if (repeatcount > 0):
            warningstring = "\n\tThere were " + str(repeatcount)  + " repeats of some of the parameters n, s and h.\n" + \
                            "\tOnly the first ocurrences were used, the rest were ignored"
            if self.game.log: self.logger.warning(warningstring)
            print warningstring

        if (comb_repeat_count > 0):
            warningstring = "\n\tThere were " + str(comb_repeat_count)  + " repeats of some of the combination entries.\n" + \
                            "\tOnly the first ocurrences were used, the rest were ignored"
            if self.game.log: self.logger.warning(warningstring)
            print warningstring

        # Check that the given parameters 'n', 's', 'h' can be converted to integers
        defaults = DEFAULT_N, DEFAULT_S, DEFAULT_H
        ParameterStrings = "number of dice", "maximum value for dice", "number of throws per turn"
        for index, code in enumerate(('n', 's', 'h')):
            try: 
                newAsetus[code] = int(newAsetus[code])
            except ValueError:
                errorstring = "\nGiven parameter for the " + str(ParameterStrings[index]) + " (" + str(newAsetus[code]) + ") is not a valid integer." +\
                              "\nDefault value of " + str(defaults[index]) + " is used instead."
                if self.game.log: self.logsetting.addError(self.logger, self.game.unNotifiedErrors, errorstring)
                newAsetus[code] = defaults[index]
        
        # Check that the given integer parameters 'n', 's', 'h' are in the correct integer range
        mins = NMIN, SMIN, HMIN
        maxs = NMAX, SMAX, HMAX
        # Loop over indices 'n', 's', 'h'
        for i, code in enumerate(('n', 's', 'h')):
            if ( mins[i] <= int(newAsetus[code]) <= maxs[i] ):
                if self.game.log: self.logger.debug("Succesfully read from file %d as the %s", int(newAsetus[code]), ParameterStrings[i])
            else:
                if self.game.log: self.logger.warning("The value for for %s (%d) was not in the current range of %d-%d", ParameterStrings[i], str(newAsetus[code]), mins[i], maxs[i])
                newAsetus[code] = defaults[i]

        #
        #    END CHECK FOR ERRORS AND WARNINGS
        #

        # Update only if the old value is unset == 0
        if self.no_of_dice == 0:
            self._no_of_dice = newAsetus['n']
            if self.game.log: self.logger.info('Updating the value of %s', ParameterStrings[0])
        else: 
            if self.game.log: self.logger.debug('%s was not changed and the current value is %d', ParameterStrings[0], self.no_of_dice)
        if self.max_value == 0:
            self._max_value = newAsetus['s']
            if self.game.log: self.logger.info('Updating the value of %s', ParameterStrings[1])
        else: 
            if self.game.log: self.logger.debug('%s was not changed and the current value is %d', ParameterStrings[1], self.max_value)
        if self.no_of_throws == 0:
            self._no_of_throws = newAsetus['h']
            if self.game.log: self.logger.info('Updating the value of %s', ParameterStrings[2])
        else: 
            if self.game.log: self.logger.debug('%s was not changed and the current value is %d', ParameterStrings[2], self.no_of_throws)

        
        # read in the combinations
        real_combination_count = 0
        if combinationcount > 0:
            for index in self._combinations_raw:
                if self.combination_parameter_check(index):
                    code = self._combinations_raw[index]['code']
                    type = Yhd.Combination.CodeList[code]['type']
                    # Add combinations that have no index,
                    # "Special" combinations
                    if 'SINGLE' in type:
                        if type['SINGLE'] == 'ALL' or \
                        (type['SINGLE'] == 'EVEN' and self.no_of_dice % 2 == 0) or \
                        (type['SINGLE'] == 'ODD' and self.no_of_dice % 2 == 1):
                            if real_combination_count == self.game.max_no_of_comb:
                                warningString = "Maximum number of combinations reached (" + \
                                                str(self.game.max_no_of_comb) + "). Some " + \
                                                "combinations will not be used."
                                if self.game.log: self.logger.warning(warningString) 
                                break
                            self._combinations[real_combination_count] = \
                                Yhd.Combination(self._combinations_raw[index]['code'], self.game)
                            real_combination_count += 1
                    # Add combinations that have an index,
                    # and add combinations with all applicable indices
                    if 'ENUMERATE' in type:
                        if type['ENUMERATE'] == 'MAX_VALUE':
                            # Check lower limit
                            if 'indexmin' in self._combinations_raw[index]:
                                lower_limit = max(1, self._combinations_raw[index]['indexmin'])
                            else: lower_limit = 1
                            # Check upper limit
                            if 'indexmax' in self._combinations_raw[index]:
                                upper_limit = min(self.no_of_dice, self._combinations_raw[index]['indexmax'])
                            else: upper_limit = self.max_value
                        if type['ENUMERATE'] == 'NO_OF_DICE':
                            # Check lower limit
                            if 'indexmin' in self._combinations_raw[index]:
                                lower_limit = max(1, self._combinations_raw[index]['indexmin'])
                            else: lower_limit = 1
                            # Check upper limit
                            if 'indexmax' in self._combinations_raw[index]:
                                upper_limit = min(self.no_of_dice, self._combinations_raw[index]['indexmax'])
                            else: upper_limit = self.no_of_dice                 
                        if type['ENUMERATE'] == 'MAX_VALUE_AND_NO_OF_DICE':
                            # Check lower limit
                            if 'indexmin' in self._combinations_raw[index]:
                                lower_limit = max(1, self._combinations_raw[index]['indexmin'])
                            else:
                                lower_limit = 1
                            if 'indexmax' in self._combinations_raw[index]:
                                upper_limit = min(self.no_of_dice, self.max_value, self._combinations_raw[index]['indexmax'])
                            else: upper_limit = min(self.no_of_dice, self.max_value)
                        # Loop over lower and upper limits to add all the combinations                                                          
                        for index2 in range(lower_limit, upper_limit + 1):
                            if real_combination_count == self.game.max_no_of_comb: 
                                warningString = "Maximum number of combinations reached (" + \
                                                str(self.game.max_no_of_comb) + "). Some " + \
                                                "combinations will not be used."
                                if self.game.log: self.logger.warning(warningString)
                            self._combinations[real_combination_count] = \
                                Yhd.Combination(self._combinations_raw[index]['code'], self.game, index2)
                            real_combination_count += 1
        
        if real_combination_count == 0:
            criticalstring = "In the setting file '" + str(self.settings_file) + "' there were no combinations " + \
                             "that could be used with current settings. Loading default settings '" + str(DEFAULT_SETTINGS) + "'."
            if self.game.log: self.logsetting.addError(self.logger, self.game.unNotifiedErrors, criticalstring, critical = True)
            self.new_settings(DEFAULT_SETTINGS)
            return
    
            
    def new_settings(self, filename):
        '''
        Open a new settings file
        '''
        self.initializeToZero()
        self.settings_from_file(filename)
        self.game.settingUpdate()
            
    def combination_parameter_check(self, index):
        '''
        Check that parameters for the maximum and 
        minimum values of the possible combinations
        are not bigger and smaller, respectively, 
        than the current values in the game.
        
        The following parameter values are checked:
        - No of dice
        - Maximum value of the dice
        - Maximum number of throws per game turn
        '''
        if 'nmin' in self._combinations_raw[index]:
            if self._combinations_raw[index]['nmin'] > self.no_of_dice:
                return False
        if 'nmax' in self._combinations_raw[index]:
            if self._combinations_raw[index]['nmax'] < self.no_of_dice:
                return False      
        if 'smin' in self._combinations_raw[index]:
            if self._combinations_raw[index]['smin'] > self.max_value:
                return False
        if 'smax' in self._combinations_raw[index]:
            if self._combinations_raw[index]['smax'] < self.max_value:
                return False                                  
        if 'hmin' in self._combinations_raw[index]:
            if self._combinations_raw[index]['hmin'] > self.no_of_throws:
                return False
        if 'hmax' in self._combinations_raw[index]:
            if self._combinations_raw[index]['hmax'] < self.no_of_throws:
                return False
        # All checks cleared, return True
        return True

    def get_max_value(self):
        return self._max_value
    def set_max_value(self, new_max_value):
        if self.game.gameround == 0:
            if SMIN <= new_max_value <= SMAX:
                self._max_value = new_max_value
                self.initializeToZero()
                self.settings_from_file(self.settings_file)
                self.game.settingUpdate()
            else:
                warningStrin = "Attempted to pass inproper maximum value of dice" + \
                               str(new_max_value)
                if self.game.log: self.logger.warning(warningStrin)
    max_value = property(get_max_value, set_max_value)

    def get_no_of_dice(self):
        return self._no_of_dice
    def set_no_of_dice(self, new_no_of_dice):
        if self.game.gameround == 0:
            if NMIN <= new_no_of_dice <= NMAX:
                self._no_of_dice = new_no_of_dice
                self.initializeToZero()
                self.settings_from_file(self.settings_file)
                self.game.settingUpdate()
            else:
                warningStrin = "Attempted to pass inproper no of dice" + \
                               str(new_no_of_dice)
                if self.game.log: self.logger.warning(warningStrin)
    no_of_dice = property(get_no_of_dice, set_no_of_dice)
    
    
    def get_no_of_throws(self):
        return self._no_of_throws
    def set_no_of_throws(self, new_no_of_throws):
        if self.game.gameround == 0:
            if HMIN <= new_no_of_throws <= HMAX:
                self._no_of_throws = new_no_of_throws
                self.initializeToZero()
                self.settings_from_file(self.settings_file)
                self.game.settingUpdate()
            else:
                warningStrin = "Attempted to pass inproper maximum no of throws" + \
                               str(new_no_of_throws)
                if self.game.log: self.logger.warning(warningStrin)
    no_of_throws = property(get_no_of_throws, set_no_of_throws)

    #    -----------------------------------
    # 
    #    Properties with only getters.
    #    In alphabetical order
    # 
    #    -----------------------------------

    def get_combinations(self):
        return self._combinations
    combinations = property(get_combinations)

    def get_game(self):
        return self._game
    game = property(get_game)

    def get_settings_file(self):
        return self._settings_file
    settings_file = property(get_settings_file)
    