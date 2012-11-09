# -*- coding: utf-8 -*-

'''
Created on 31 Mar 2010
Last modified on 3 May 2010


@author: Patrik Ahvenainen
'''

import random

class Dice(object):
    '''
    Noppagamessä tärkeitä tekijöitä ovat tietenkin nopat. gamen toteutuksessa nopalla ei itse asiassa ole
    montaa metodia ja attribuuttia. Nopalla on tieto vain neljästä asiasta: maksimisilmäluvustaan, silmä-
    luvustaan, edellisestä silmäluvustaan, sekä lockmisstatuksestaan. Edellinen silmäluku-tieto nopalla on
    siksi, että se mahdollistaa edellisen siirron perumiseen, jos gamein halutaan toteuttaa "Peru"-toiminto.
    Tämän harjoitustyön toteutuksessa sitä toimintoa ei toteuteta.
    '''


    def __init__(self, max_value):
        '''
        gamen luomisen yhteydessä luodaan gameasetuksista luettu määrä
        noppia. Nopat luodaan myös muutettaessa noppien maksimisilmälukua
        tai noppien lukumäärää.
        '''
        self.max_value = max_value
        
        self._value = 0
        self._prev_value = 0
        self._locked = False
        
        self.throw()       
        
    
    def throw(self):
        '''
        Käyttää value-ominaisuuden (property) setteriä, joka
        määrää, että nopan silmälukua voi vaihtaa vain heittämällä
        noppaa, eli valitsemalla satunnaisen silmäluvun yhden ja 
        nopan maksimisilmäluvun väliltä
        
        esim. noppa.value = 3 --> noppa.value = (1..maksimi)
        
        Lukitun nopan heittäminen ei aiheuta mitään toimintoja.
        '''
        self._prev_value = self._value
        if not self.locked:
            self._value = random.randint(1, self.max_value)
        
    def lock(self):
        '''
        Changes the locked attribute to True
        '''
        self._locked = True
        
    def unlock(self):
        '''
        Changes the locked attribute to False
        '''
        self._locked = False
        
    def toggle_locked(self):
        '''
        Changes the locked attribute to True
        if it was previously False.
        Changes the locked attribute to False
        if it was previously True.
        
        In other words this function toggles
        the attribute locked between
        True and False.
        '''
        if self.locked: self.unlock()
        else: self.lock()
        
    #    -----------------------------------
    # 
    #    Properties with only getters.
    #    In alphabetical order
    # 
    #    -----------------------------------
        
    def get_locked(self):
        return self._locked
    locked = property(get_locked)
    
    def get_prev_value(self):
        return self._prev_value
    prev_value = property(get_prev_value)
            
    def get_value(self):
        return self._value
    value = property(get_value)