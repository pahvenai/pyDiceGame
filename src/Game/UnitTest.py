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


VALUE_TEST_LIST = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 'string', {'dict': 'value'}]
#VALUE_TEST_LIST = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1000, 'string', {'dict': 'value'}]

SETTINGS_FILE = "TestSettings.dat"
WRITETOFILE = "unit_test_2"
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
        
        self.game = Game.Game(PLAYERS, SETTINGS_FILE)
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
            b = open(WRITETOFILE, 'a')
            b.write( "Game settings are: n= " + str(VALUE_TEST_LIST[self.index1])  + "-->" + str(self.game.settings.no_of_dice) + \
                  ", s=" + str(VALUE_TEST_LIST[self.index2])  + "-->" + str(self.game.settings.max_value) + \
                  ", h=" + str(VALUE_TEST_LIST[self.index3])  + "-->" + str(self.game.settings.no_of_throws) + \
                  ", no of combinations=" + str(len(self.game.settings.combinations)) )
            b.close()
        self.assertTrue(self.game.end, "Game end was not reached")

    def tearDown(self):
        logging.shutdown()

class TestNoSettingsFunctions(unittest.TestCase):

    def setUp(self):
        self.game = Game.Game(PLAYERS, SETTINGS_FILE)

    def test_set_max_value(self):
        f.write( "\nTESTING 'MAX VALUE OF DICE' ASSIGNMENT\n" )
        f.write( "ACCEPTABLE VALUES ARE BETWEEN " + str(Settings.SMIN) + \
              " AND " + str(Settings.SMAX)+ "\n" )
        for testItem in VALUE_TEST_LIST:
            self.game.settings.max_value = testItem
            f.write( "Trying to set value '" + str(testItem) + \
                  "'. New value is = " + str(self.game.settings.max_value)+ "\n" )
            logging.shutdown()
        self.assertTrue(Settings.SMIN <= self.game.settings.max_value <= Settings.SMAX)

    def test_set_no_of_dice(self):
        f.write( "\nTESTING 'NUMBER OF DICE' ASSIGNMENT\n" )
        f.write( "ACCEPTABLE VALUES ARE BETWEEN " + str(Settings.NMIN) + \
              " AND " + str(Settings.NMAX)+ "\n" )
        for testItem in VALUE_TEST_LIST:
            self.game.settings.no_of_dice = testItem
            f.write( "Trying to set value '" + str(testItem) + \
                  "'. New value is = " + str(self.game.settings.no_of_dice) + "\n")
            logging.shutdown()
        self.assertTrue(Settings.NMIN <= self.game.settings.no_of_dice <= Settings.NMAX)

    def test_set_no_of_throws(self):
        f.write( "\nTESTING 'MAXIMUM NUMBER OF THROWS' ASSIGNMENT\n" )
        f.write( "ACCEPTABLE VALUES ARE BETWEEN " + str(Settings.HMIN) + \
              " AND " + str(Settings.HMAX) + "\n")
        for testItem in VALUE_TEST_LIST:
            self.game.settings.no_of_throws = testItem
            f.write( "Trying to set value '" + str(testItem) + \
                  "'. New value is = " + str(self.game.settings.no_of_throws) + "\n")
            logging.shutdown()
        self.assertTrue(Settings.HMIN <= self.game.settings.no_of_throws <= Settings.HMAX)

    def tearDown(self):
        logging.shutdown()

if __name__ == '__main__':
#    unittest.main()'
    no_of_total_errors = 0

    f = open(WRITETOFILE, 'w')
    f.write("Starting unit tests\n\n")
    
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
    f.write( "\nErrors: " + str(testresults.errors) + "\n")
    if testresults.wasSuccessful():
        f.write( "SUCCESS in " + str(took) + "s !" + "\n" )
    print "Parameter setting test completed in %5.3fs" % took
    
#    myObj = WriteStringClass()
                
    f.write( "\nTESTING 'GAME COMPLETION' ASSIGNMENT USING RANDOM SELECTION OF SCORES TO MARK, " )
    f.write( "TEST SETTINGS FILE '" + str(SETTINGS_FILE) + "'\n" )
    timeri = time.clock()
    test_suite = unittest.TestSuite()  
    test_complete_game = TestGameCompletion('test_complete_game')
    testresults = unittest.TestResult()
    for index, item1 in enumerate(VALUE_TEST_LIST):
        for item2 in VALUE_TEST_LIST:
            for item3 in VALUE_TEST_LIST:
                test_suite = unittest.TestSuite()
                test_suite.addTest(test_complete_game)
                f.close()
                test_suite.run(testresults)
                f = open(WRITETOFILE, 'a')
                if len(testresults.errors) > 0:
                    no_of_total_errors += 1
                if len(testresults.errors) > 0:
                    f.write(  ", Errors: " + str(testresults.errors) + "\n" )
                if testresults.wasSuccessful():
                    f.write(  ", SUCCESS \n" ) 
        print "Game completion test %4.2f completed in %3.1fs" % ((index+1)/float(len(VALUE_TEST_LIST)), time.clock() - totaltime)
    
    f.write( "\nIn total the test took " + str(time.clock() - totaltime) + "s." + "\n" )
    f.write( "There were " + str(no_of_total_errors) + " errors in total" + "\n" )
    f.close()
