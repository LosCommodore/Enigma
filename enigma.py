import abc
import numpy as np
from collections import OrderedDict
from typing import Dict, List

alphabet = tuple(chr(ord('a') + i) for i in range(26))

class Scrambler():
    def __init__(self, name:str):
        self.name = name

    @abc.abstractmethod
    def route(self, character: int) -> int:
        """ relatives Routing vom character """
        return

    @abc.abstractmethod
    def inv_route(self, character) -> int:
        """ inverses relatives Routing vom character """
        return

class  Rotor(Scrambler):

    def __init__(self, name:str, wiring: str, notches=tuple(), isStatic=False):
        super().__init__(name);

        # Check if wiring is valid: is alphabet and unique items
        assert tuple(sorted(wiring)) == alphabet ,'Rotor falsch initialisiert, falsches Alphabet !'
        #//TODO: char is not allowed to map on itself ?

        # save wiring as Dict
        self.wiring     = {k:v for k,v in zip(alphabet,wiring)} 
        
        # relatives Mapping (bsp: d -> e => +1)
        self.mapping = [(ord(character)-ord(alpha)) for character,alpha in zip(wiring,alphabet)]

        # inverses relatives Mapping (bsp: e -> d => -1)
        numWiring = [ord(a) for a in wiring]
        self.inv_mapping = np.argsort(numWiring) - np.arange(len(alphabet))
        
        self.notches = tuple(ord(x)-ord('a') for x in notches)
        
        self.ringPos = 0
        self.isStatic = isStatic
        self.__rotation = 0 
    def route(self, character: int) -> int:

        rot = self.ringPos + self.rotation
        return (character + self.mapping[(character + rot) % len(alphabet)]) % len(alphabet)

    def inv_route(self, character):
        rot = self.ringPos + self.rotation
        return (character + self.inv_mapping[(character + rot) % len(alphabet)]) % len(alphabet)

    def doesStep(self):
        return any([self.rotation == n for n in self.notches])

    @property 
    def rotation(self):
        return self.__rotation

    @rotation.setter 
    def rotation(self,value):
        self.__rotation = value % len(alphabet)


class PlugBoard(Scrambler):
    def __init__(self,name):
        super().__init__(name);
        self.__cables = [] #List of Tuples, e.g: cables = [('a','b'), ('u','v'), ('r','x'), ('t','w')]
        self.mapping = [ord(x)-ord('a') for x in alphabet]

    @property 
    def cables(self): 
        return self.__cables
        
    @cables.setter
    def cables(self,cables):
        characters = [item for c in cables for item in c]
        assert len(characters) == len(set(characters)), 'Error in Plubboard! Characters are not unique' #check for unique characters
        self.__cables = cables.copy() #copy!
    
        plugMapping = list(alphabet)
        for cable in cables:
            i0 = plugMapping.index(cable[0])
            i1 = plugMapping.index(cable[1])
            plugMapping[i0] = cable[1]
            plugMapping[i1] = cable[0]

        self.mapping = [ord(x)-ord('a') for x in plugMapping]

    def route(self, character: int) -> int:
        return self.mapping[character]

    def inv_route(self, character):
        return self.mapping[character] #symmetrisches Mapping beim Plugboard: aus "c -> a" folgt "c <- a" 

    def print(self):
        for source,dest in zip(alphabet,self.mapping):
            print(f"{source} -> {chr(dest+ord('a'))}")

class Enigma:

    def __init__(self):
        self.scramblers=[]
        pass
    
    def pressKey(self,key):
        if isinstance(key,int):
            key=str(key)
        
        assert key in alphabet, 'ungültiger Schlüssel!'
        key = ord(key) - ord('a')

        #rotate
        self.rotate()

        #calc Wiring

        routing = [] # --> names
        char = [key] # --> [0, 1, 10, 11, 21, 22, 17, 6, 5, 5]
        for scram in self.scramblers:
            routing.append(scram.name)
            char.append(scram.route(char[-1]))

        for scram in self.scramblers[::-1][1:]: # reverse + exclude last element (ukw)
            routing.append(scram.name)
            char.append(scram.inv_route(char[-1]))

        return char, routing
    
    def rotate(self):
        rotors = [x for x in self.scramblers if isinstance(x,Rotor) and not x.isStatic]
        
        doRotate= [False] * len(rotors)
        doRotate[0] = True 
        for i,step in enumerate([s.doesStep() for s in rotors]):
            if step:
                doRotate[i] = True
                doRotate[i+1] = True

        for rotor,step in zip(rotors,doRotate):
            rotor.rotation += step
        
#%% main

#Create Enigma
riddle = Enigma()

#Create Plugboard
plugBoard = PlugBoard('Plugboard')
#plugBoard.cables =  [('a','b'), ('u','v'), ('r','x'), ('t','w')]
#plugBoard.print()

#Create Rotors
rot1 = Rotor('I','EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower(),('q',))
rot2 = Rotor('II','AJDKSIRUXBLHWTMCQGZNPYFVOE'.lower(),('e',))
rot3 = Rotor('III','BDFHJLCPRTXVZNYEIWGAKMUSQO'.lower(),('v',))
ukw_b = Rotor('ukw_b','YRUHQSLDPXNGOKMIEBFZCWVJAT'.lower(),isStatic=True) 
                      
#Wire Enigma:
riddle.scramblers.append(plugBoard)
riddle.scramblers += [rot1, rot2, rot3, ukw_b]

#Press Key:
text = 'aaa'

encoded=[]
for key in text:
    char,routing = riddle.pressKey(key) 
    print(char,routing)
    encoded.append(chr(char[-1]+ord('a')))

print("Encoded Text: " , encoded)

#charInv,routingInv = riddle.pressKey(lastChar)
#print(charInv,routingInv)

print("ende")

#%%
