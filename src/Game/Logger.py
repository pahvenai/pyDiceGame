# -*- coding: utf-8 -*-
'''
Created on 19 Apr 2010
Last modified on 4 May 2010

@author: Patrik Ahvenainen
'''

import os
# Use python modules for logging
import logging
import logging.handlers

# GLOBAL VARIABLES FOR LOGGING
LOG_FILENAME = os.path.join("log", "gamelog.txt")
ERRORLOG_FILENAME = os.path.join("log", "game_error_log.txt")
# Format of log
FORMAT = "%(asctime)s - %(levelname)s(%(name)s): %(message)s"
# Maximum number of bytes in one logfile
MAXBYTES = 50000
# Number of different logfiles
BACKUPCOUNT = 0

class Logger(object):
    '''
    Create a logger for any module
    
    '''


    def __init__(self, logObject, name, loggeruse = True):
        '''
        Create a logger for general use. One logger writes all logging messages to file whereas 
        the second logger writes only the errors and criticals.
        '''
        
        self.unHandled = []
        self.Handled = []
        
        
        # Set up a specific logger with our desired output level
        logObject.logger = logging.getLogger(name)
        logObject.logger.setLevel(logging.DEBUG)
        
        
        self.loggeruse = loggeruse
        
        if not os.path.exists(LOG_FILENAME):
            f = open(LOG_FILENAME,'w')
            f.write('')
            f.close()
        try:
            game_log = logging.handlers.RotatingFileHandler(LOG_FILENAME, mode='w', maxBytes=MAXBYTES, backupCount=BACKUPCOUNT)
        except:
            self.loggeruse = False
            
            
        if not os.path.exists(ERRORLOG_FILENAME):
            f = open(ERRORLOG_FILENAME,'w')
            f.write('')
            f.close()
        try:        
            game_error_log = logging.handlers.RotatingFileHandler(ERRORLOG_FILENAME, mode='w', maxBytes=MAXBYTES, backupCount=BACKUPCOUNT)
        except:
            self.loggeruse = False
            
        # Format the logging styles
        formatter = logging.Formatter(FORMAT)
        game_log.setFormatter(formatter)
        game_error_log.setFormatter(formatter)
        
        # Set levels for the two handlers
        game_log.setLevel(logging.DEBUG)
        game_error_log.setLevel(logging.WARNING)
        
        # Remove old handlers if they exist
        for dummy in range(2):
            try: logObject.logger.removeHandler(logObject.logger.handlers[0])
            except IndexError: pass #No handlers found
        
        # Add handlers to the logger
        logObject.logger.addHandler(game_log)
        logObject.logger.addHandler(game_error_log)
    
    def addError(self, logger, ErrorList, errorString, critical = None):
        '''
        Add the 'errorString' to the list 'ErrorList' and log it using 'logger'.
        'errorString' is also printed using the standard output
        
        'critical = True' may be used to log the message as critical, 
        by default the message is logged as error.
        '''
        
        ErrorList.append(errorString)
        if self.loggeruse:
            if critical:
                logger.critical(errorString)
            else:
                logger.error(errorString)
#        print errorString
        