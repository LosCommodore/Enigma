import numpy as np
from collections import OrderedDict
from typing import Dict, List

class  Scrambler():
    alphabet = tuple(chr(ord('a') + i) for i in range(26))

    def __init__(self, name:str, wiring: str):
        self.name = name
        self.rotation = 0 #position of rotor
        
        # Check if wiring is valid: is alphabet and unique items
        assert tuple(sorted(wiring)) == self.alphabet ,'Rotor falsch initialisiert, falsches Alphabet !'
        
        # save wiring as Dict
        self.wiring     = {k:v for k,v in zip(self.alphabet,wiring)} 
        
        # relatives Mapping (bsp: d -> e => +1)
        self.mapping = [(ord(character)-ord(alpha)) for character,alpha in zip(wiring,self.alphabet)]

        # inverses relatives Mapping (bsp: e -> d => -1)
        numWiring = [ord(a) for a in wiring]
        self.inv_mapping = np.argsort(numWiring) - np.arange(len(self.alphabet))
        
    def route(self, character: int) -> int:
        return (character + self.mapping[(character + self.rotation) % len(self.alphabet)]) % len(self.alphabet)

    def inv_route(self, character):
        return (character + self.inv_mapping[(character + self.rotation) % len(self.alphabet)]) % len(self.alphabet)


#%% main

#Plugboard
plugMapping = list(Scrambler.alphabet)


cables = [('a','b'), ('u','v'), ('r','x'), ('t','w')]

characters = [item for c in cables for item in c]
assert len(characters) == len(set(characters)), 'Error in Plubboard! Characters are not unique' #check for unique characters

for cable in cables:
    i0 = plugMapping.index(cable[0])
    i1 = plugMapping.index(cable[1])
    plugMapping[i0] = cable[1]
    plugMapping[i1] = cable[0]

plugBoard = Scrambler('plug',plugMapping)

rot1 = Scrambler('rot1','EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower())
rot2 = Scrambler('rot2','AJDKSIRUXBLHWTMCQGZNPYFVOE'.lower())
rot3 = Scrambler('rot3','BDFHJLCPRTXVZNYEIWGAKMUSQO'.lower())
ukw_b = Scrambler('ukw_b','YRUHQSLDPXNGOKMIEBFZCWVJAT'.lower()) 
#Append to Scrambler-List
Scramblers = []
Scramblers += [plugBoard, rot1, rot2 , rot3, ukw_b]

#char = [ord('a')-ord('a')] #-> 5 -> F
char = [0]
#char = [5] # --> [5, 5, 6, 17, 22, 21, 11, 10, 1, 0]
routing = [] # --> [0, 1, 10, 11, 21, 22, 17, 6, 5, 5]
for scram in Scramblers:
    routing.append(scram.name)
    char.append(scram.route(char[-1]))

for scram in Scramblers[::-1][1:]: # reverse + exclude last element (ukw)
    routing.append(scram.name)
    char.append(scram.inv_route(char[-1]))

print("ende")

#%%
