# Contents

[TOC]

# Introduction

<img src=".\pictures\Enigma_(crittografia)_-_Museo_scienza_e_tecnologia_Milano.jpg" alt="img" style="zoom:50%;" />

## Movies

### Die Enigma in "das Boot"

Aus https://de.wikipedia.org/wiki/Das_Boot_(Film):

> In mehreren Szenen ist eine [Enigma-Schlüsselmaschine](https://de.wikipedia.org/wiki/Enigma_(Maschine)) (Bild) zu sehen, die zur [Entschlüsselung](https://de.wikipedia.org/wiki/Entschlüsselung) empfangener [Funksprüche](https://de.wikipedia.org/wiki/Funkspruch) benutzt wird. Beim ersten Auftritt der Enigma (in der 282-Minuten-Langversion nach 53 Minuten) schaut der Kriegsberichterstatter Leutnant Werner dem II. WO (Zweiter Wachoffizier) über die Schulter, während dieser einen Funkspruch mittels einer [Enigma-M4](https://de.wikipedia.org/wiki/Enigma-M4) entschlüsselt. Dabei hört man als Kommentar die Stimme von Herbert Grönemeyer: „Erst durch die Schlüsselmaschine ergibt sich aus wirren Buchstabenfolgen ganz langsam ein Sinn.“ Historisch nicht ganz korrekt an dieser Szene ist die Verwendung einer M4 (mit vier Walzen), da sie erst am 1. Februar 1942 in Dienst gestellt wurde, während *Das Boot* in Roman und Film seine Feindfahrt im Herbst und frühen Winter des Jahres 1941 durchführt. Somit hätte korrekterweise eine [M3](https://de.wikipedia.org/wiki/Enigma-M#Enigma-M3) (mit drei Walzen) gezeigt werden müssen.

## Imitation game

https://www.imdb.com/title/tt2084970/

# Sources

## Books
- https://simonsingh.net/books/the-code-book/

## Internet
- [wikipedia: Enigma machine](https://en.wikipedia.org/wiki/Enigma_machine)
- [wikipedia: rotor details](https://en.wikipedia.org/wiki/Enigma_rotor_details)
- [wikipedia: Turing-Bombe](https://de.wikipedia.org/wiki/Turing-Bombe)

## YouTube
- [Simon Sign ](https://www.youtube.com/watch?v=ASfAPOiq_eQ&t=309s)
- [Enigma Machine Mechanism 'Double Step'](https://www.youtube.com/watch?v=hcVhQeZ5gI4)

- [Wie ein Mathegenie Hitler knackte ARTE Doku](https://www.youtube.com/watch?v=ttRDu4wuVTA)
# Notes

## Rotor
- If the first letter of a rotor is E, this means that the A is wired to the E. This does not mean that E is wired to A. This looped wiring is only the case with the reflectors.
## Rotor offset
- Notice that every letter is encoded into another.
- With the rotors I, II and III (from left to right), wide B-reflector, all ring settings in A-position, and start position AAA, typing AAAAA will produce the encoded sequence BDZGO.
## Ring setting
- In early models, the alphabet ring was fixed to the rotor disc. A later improvement was the ability to adjust the alphabet ring relative to the rotor disc. The position of the ring was known as the Ringstellung("ring setting"), and was a part of the initial setting prior to an operating session. In modern terms it was a part of the initialization vector.
- They do not change the notch or the alphabet ring on the exterior. Those are fixed to the rotor. Changing the ring setting will therefore change the positions of the wiring, relative to the turnover-point and start position.
## Stepping
-  To avoid merely implementing a simple (and easily solvable) substitution cipher, every key press caused one or more rotors to step by one twenty-sixth of a full rotation, before the electrical connections were made.
- The stepping mechanism varied slightly from model to model.
- The advancement of a rotor other than the left-hand one was called a turnover by the British
- The design also included a feature known as double-stepping 
## Notch
- The first five rotors to be introduced (I–V) contained one notch each, while the additional naval rotors VI, VII and VIII each had two notches
- The position of the notch on each rotor was determined by the letter ring which could be adjusted in relation to the core containing the interconnections
- Each rotor contained a notch (or more than one) that controlled rotor stepping. In the military variants, the notches are located on the alphabet ring.
## Entry wheel
- The current entry wheel (Eintrittswalze in German), or entry stator, connects the plugboard to the rotor assembly. If the plugboard is not present, the entry wheel instead connects the keyboard and lampboard to the rotor assembly. While the exact wiring used is of comparatively little importance to security, it proved an obstacle to Rejewski's progress during his study of the rotor wirings. The commercial Enigma connects the keys in the order of their sequence on a QWERTZ keyboard: Q→A, W→B, E→C and so on. The military Enigma connects them in straight alphabetical order: A→A, B→B, C→C, and so on. It took inspired guesswork for Rejewski to penetrate the modification.
## Reflector
- In Model 'C', the reflector could be inserted in one of two different positions. In Model 'D', the reflector could be set in 26 possible positions, although it did not move during encryption. In the Abwehr Enigma, the reflector stepped during encryption in a manner similar to the other wheels.
- In the German Army and Air Force Enigma, the reflector was fixed and did not rotate; there were four versions. The original version was marked 'A', and was replaced by Umkehrwalze B on 1 November 1937. A third version, Umkehrwalze C was used briefly in 1940, possibly by mistake, and was solved by Hut 6.[15]The fourth version, first observed on 2 January 1944, had a rewireable reflector, called Umkehrwalze D, nick-named Uncle Dick by the British, allowing the Enigma operator to alter the connections as part of the key settings.
	
