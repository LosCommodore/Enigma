import numpy as np
from collections import OrderedDict

class  Rotor():
    alphabet = [chr(ord('a') + i) for i in range(26)]

    def __init__(self,wiring: str):
        self.rotation = 0 #position of rotor
        
        # Check if wiring is valid: is alphabet and unique items
        assert sorted(wiring) == self.alphabet ,'Rotor falsch initialisiert, falsches Alphabet !'
        
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


#%% Test
rot = Rotor('DMTWSILRUYQNKFEJCAZBPGXOHV'.lower())
rot.rotation = 12

newPos = rot.route(7)
orgPos = rot.inv_route(newPos)
print("ende")

#%%
