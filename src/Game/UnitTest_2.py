'''
Created on 2 May 2010
Last modified on 4 May 2010

@author: Patrik Ahvenainen
'''

import unittest
import Game
import Settings
import logging
import time
import sys


VALUE_TEST_LIST = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 'string', {'dict': 'value'}]
#VALUE_TEST_LIST = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1000, 'string', {'dict': 'value'}]

SETTINGS_FILE = "Basic Yahtzee.dat"
WRITETOFILE = "unit_test_2.txt"
PLAYERS = "Player 1" , "Player 2"#, "Player 3", "Player 4"

WRITESTRING = ""

#class WriteStringClass(object):
#    def __init__(self):
#        self.WRITESTRING = ""
        
    

class TestGameCompletion(unittest.TestCase):

    def setUp(self):
        try: self.index1 == 0
        except: self.index1 = -1
        try: self.index2 == 0
        except: self.index2 = 0
        try: self.index3 == 0
        except: self.index3 = 0
        self.index1 += 1
        if self.index1 == len(VALUE_TEST_LIST):
            self.index2 += 1
            self.index1 = 0
        if self.index2 == len(VALUE_TEST_LIST):
            self.index3 += 1
            self.index2 = 0
        
        self.game = Game.Game(PLAYERS, SETTINGS_FILE, log=False)
        self.game.settings.max_value = VALUE_TEST_LIST[self.index1]
        self.game.settings.no_of_dice = VALUE_TEST_LIST[self.index2]
        self.game.settings.no_of_throws = VALUE_TEST_LIST[self.index3]
        self.game.goForward()

    def test_complete_game(self):
        self.assertFalse(self.game.end, "Game end was reached before the game started")
        for no_of_players in range(len(self.game.player_list)):
            for i in range(0, len(self.game.settings.combinations)):
                self.game.SequentialChoice()
        if self.game.end:
            print "Game settings are: n= " + str(VALUE_TEST_LIST[self.index1])  + "-->" + str(self.game.settings.no_of_dice) + \
                  ", s=" + str(VALUE_TEST_LIST[self.index2])  + "-->" + str(self.game.settings.max_value) + \
                  ", h=" + str(VALUE_TEST_LIST[self.index3])  + "-->" + str(self.game.settings.no_of_throws) + \
                  ", no of combinations=" + str(len(self.game.settings.combinations)) 
        self.assertTrue(self.game.end, "Game end was not reached")

    def tearDown(self):
        logging.shutdown()

class TestNoSettingsFunctions(unittest.TestCase):

    def setUp(self):
        self.game = Game.Game(PLAYERS, SETTINGS_FILE, log=False)

    def test_set_max_value(self):
        print "\nTESTING 'MAX VALUE OF DICE' ASSIGNMENT"
        print "ACCEPTABLE VALUES ARE BETWEEN " + str(Settings.SMIN) + \
              " AND " + str(Settings.SMAX)
        for testItem in VALUE_TEST_LIST:
            self.game.settings.max_value = testItem
            print "Trying to set value '" + str(testItem) + \
                  "'. New value is = " + str(self.game.settings.max_value)
            logging.shutdown()
        self.assertTrue(Settings.SMIN <= self.game.settings.max_value <= Settings.SMAX)

    def test_set_no_of_dice(self):
        print "\nTESTING 'NUMBER OF DICE' ASSIGNMENT"
        print "ACCEPTABLE VALUES ARE BETWEEN " + str(Settings.NMIN) + \
              " AND " + str(Settings.NMAX)
        for testItem in VALUE_TEST_LIST:
            self.game.settings.no_of_dice = testItem
            print "Trying to set value '" + str(testItem) + \
                  "'. New value is = " + str(self.game.settings.no_of_dice)
            logging.shutdown()
        self.assertTrue(Settings.NMIN <= self.game.settings.no_of_dice <= Settings.NMAX)

    def test_set_no_of_throws(self):
        print "\nTESTING 'MAXIMUM NUMBER OF THROWS' ASSIGNMENT" 
        print "ACCEPTABLE VALUES ARE BETWEEN " + str(Settings.HMIN) + \
              " AND " + str(Settings.HMAX) 
        for testItem in VALUE_TEST_LIST:
            self.game.settings.no_of_throws = testItem
            print "Trying to set value '" + str(testItem) + \
                  "'. New value is = " + str(self.game.settings.no_of_throws) 
            logging.shutdown()
        self.assertTrue(Settings.HMIN <= self.game.settings.no_of_throws <= Settings.HMAX)

    def tearDown(self):
        logging.shutdown()

if __name__ == '__main__':
#    unittest.main()'
    no_of_total_errors = 0

    sys.stdout = open(WRITETOFILE, 'w')
    print ("Starting unit tests\n")
    
    totaltime = time.clock()
    
    test_suite = unittest.TestSuite()
    test_set_max_value_ = TestNoSettingsFunctions('test_set_max_value')
    test_set_no_of_dice_ = TestNoSettingsFunctions('test_set_no_of_dice')
    test_set_no_of_throws_ = TestNoSettingsFunctions('test_set_no_of_throws')
    test_suite.addTest(test_set_max_value_)
    test_suite.addTest(test_set_no_of_dice_)
    test_suite.addTest(test_set_no_of_throws_)
    testresults = unittest.TestResult()
    timeri = time.clock()
    test_suite.run(testresults)
    took = time.clock() - timeri
    if len(testresults.errors) > 0:
        no_of_total_errors += 1
    print ( "\nErrors: " + str(testresults.errors))
    if testresults.wasSuccessful():
        print ( "SUCCESS in " + str(took) + "s !" )
    
#    myObj = WriteStringClass()
                
    print "\nTESTING 'GAME COMPLETION' ASSIGNMENT USING RANDOM SELECTION OF SCORES TO MARK, "
    print "TEST SETTINGS FILE '" + str(SETTINGS_FILE)
    timeri = time.clock()
    test_suite = unittest.TestSuite()  
    test_complete_game = TestGameCompletion('test_complete_game')
    testresults = unittest.TestResult()
    for index, item1 in enumerate(VALUE_TEST_LIST):
        for item2 in VALUE_TEST_LIST:
            for item3 in VALUE_TEST_LIST:
                test_suite = unittest.TestSuite()
                test_suite.addTest(test_complete_game)
                test_suite.run(testresults)
                if len(testresults.errors) > 0:
                    no_of_total_errors += 1
                if len(testresults.errors) > 0:
                    print  ", Errors: " + str(testresults.errors)
                if testresults.wasSuccessful():
                    print  ", SUCCESS"
#        print "Game completion test %4.2f completed in %3.1fs" % ((index+1)/float(len(VALUE_TEST_LIST)), time.clock() - totaltime)
    
    print "\nIn total the test took " + str(time.clock() - totaltime) + "s." 
    print "There were " + str(no_of_total_errors) + " errors in total"
    
    sys.stdout = sys.__stdout__
