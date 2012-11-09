# -*- coding: utf-8 -*-

'''
Created on 26 Apr 2010
Last modified on 4 May 2010

@author: Patrik Ahvenainen
'''

import os

import Logger
import pickle
from datetime import datetime

SCORE_FOLDER_NAME = "Scores"

class HighScores(object):
    '''
    This class is used to create top 10 scores from the game.
    It reads current top scores from file using the pickle
    module. The scores are also written in file using the
    pickle module as a python dict object. The scores are
    saved in a folder called 'Scores' under a folder that
    is named after the game settings file by removing the 
    extension. High Score file name is 'NNSSHH.sco', where 
    NN is a zero-padded number of dice
    SS is a zero-padded maximum value of dice and
    HH is a zero-padded maximum number of throws
    
    The score are the keys in this dictionary. The values are
    lists of dictionaries with the following keys:
    'total', 'name', 'time', 'date' and 'datetime'.
    
    Exemplary HighScores dictionary with three items:
    {
        125: [   {  'total': 125, 
                    'name': Matti, 
                    'time': '12:53:07',
                    'date':  'Tuesday May 04, 2010',
                    'datetime': 'Tue May  4 12:53:07 2010'},
                 {  'total': 125, 
                    'name': Ville, 
                    'time': '00:31:40',
                    'date':  'Tuesday April 27, 2010',
                    'datetime': 'Tue Apr 27 00:31:40 2010'}                    
             ],
        120: [   {  'total': 120, 
                    'name': Matti, 
                    'time': '23:18:09',
                    'date':  'Monday April 26, 2010',
                    'datetime': 'Mon Apr 26 23:18:09 2010'}
            ]
    }
    
    Attributes:
    game, settingsfile, logsetting, high_scores, scores_directory,
    max_score, winner
    
    Functions:
    appendScores(self)
    readScores(self)
    get_high_scores(self)
    get_max_score(self)
    get_winner(self)
    '''


    def __init__(self, game):
        '''
        All necessary information can be accessed from the game-class
        When created the HighScores instance reads current high scores
        from file with the pickle module if they exist or returns an 
        empty dictionary.  
        '''
        self.game = game
        self.settingsfile = os.path.splitext(self.game.settings.settings_file)[0]
        # Creates self.logger which is a logging object
        self.logsetting = Logger.Logger(self, 'Game.HighScores')
        
        self._high_scores = {}
        self.readScores()
        self._max_score = None
        self._winner = None
        
    def appendScores(self):
        '''
        Append scores to the high score list. Only ten highest scores
        are added. More than ten player can be on the list only if there
        are more than one player with the same number of points at the
        last position.
        '''
        self._max_score = 0
        self._winner = None
        for player in self.game.player_list:
            if player.score_list.total > self.max_score:
                self._max_score = player.score_list.total
                self._winner = player
        self.currentscore = {}
        self.currentscore['total'] = self.max_score
        self.currentscore['name'] = self.winner.name
        self.currentscore['time'] = datetime.now().strftime("%H:%M:%S")
        self.currentscore['date'] = datetime.now().strftime("%A %B %d, %Y")
        self.currentscore['datetime'] = datetime.now().ctime()  
        
        # Log winning player score and name
        infoString = "Winner is " + self.winner.name + " with " + str(self.max_score) + " points."
        if self.game.log: self.logger.info(infoString)

        
        # Add the current high score to the list
        if not self.max_score in self.high_scores:
            self.high_scores[self.max_score] = [self.currentscore]
        else:
            self.high_scores[self.max_score].append(self.currentscore)
            
               
        # Check that there are no more than ten items in the list
        
        # Calculate number of items
        length_before = 0
        for item in self.high_scores:
            length_before += len(self.high_scores[item])
        
        # If there are more than ten items on the list, remove 
        # the lowest valued key and check how many scores remain
        # If ten or more items remain, proceed the removal, else
        # don't remove the lowest key from the list
        if length_before > 10:
            minValue = min(self.high_scores.keys())
            helpDict = self.high_scores.copy()
            helpDict.pop(minValue)
            length_hd = 0
            for item in helpDict:
                length_hd += len(helpDict[item])            
            if length_hd >= 10:
                self._high_scores = helpDict
        
        # Write to file the new high score list
        output = open(self.score_file, 'wb')
        pickle.dump(self.high_scores, output)
        output.close()
                
    def readScores(self):
        '''
        Read high scores from file. If the correct path does not exist,
        try to create it. 
        '''
        self.scores_directory = os.path.join(SCORE_FOLDER_NAME, self.settingsfile)
        
        # Check does the directory exist and that it is a directory
        if os.path.exists(self.scores_directory):
            if not os.path.isdir(self.scores_directory):
                self.logger.critical('Cannot create a High scores file because file %s exists and is not a directory!', self.scores_directory)
                return
        else:
            try:
                os.makedirs(self.scores_directory)
            except:
                pass
                
        myString = "%02d%02d%02d.sco" % ( self.game.settings.no_of_dice, \
                                       self.game.settings.max_value, \
                                       self.game.settings.no_of_throws )
        self.score_file = os.path.join(self.scores_directory, myString)
        # Check does the file exist and that it is a file
        if os.path.exists(self.score_file):
            if not os.path.isfile(self.score_file):
                self.logger.critical('Cannot create a High scores file because file %s exists and is not a file!', self.score_file)
                return
            else:
                pkl_file = open(self.score_file, 'rb')
                self._high_scores = pickle.load(pkl_file)
                pkl_file.close()
        else:
            self._high_scores = {}    
        
    def get_high_scores(self):
        return self._high_scores
    high_scores = property(get_high_scores)
    
    def get_max_score(self):
        return self._max_score
    max_score = property(get_max_score)  
        
    def get_winner(self):
        return self._winner
    winner = property(get_winner)    
