# -*- coding: utf-8 -*-
'''
Created on 1 May 2010

@author: pate
'''

class SimpleCallback(object):
    """
    Create a callback shim. Based on code by Scott David Daniels
    (which also handles keyword arguments). This function is used
    to deliver parameters to Tkinter Button commands that are
    called when the button is clicked. 
    """
    def __init__(self, callback, *firstArgs):
        self.__callback = callback
        self.__firstArgs = firstArgs
    
    def __call__(self, *args):
        return self.__callback (*(self.__firstArgs + args))
        