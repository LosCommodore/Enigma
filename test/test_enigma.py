import time
import pytest
import enigmatic
from enigmatic import Enigma
import random
from rich.console import Console

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)


def test_plug_board():
    cables = ('BZ', 'FG')
    p = enigmatic.PlugBoard(cables)

    # scheck for symmetry
    for x in enigmatic._letters2num(enigmatic.ALPHABET):
        assert x == p.inv_route(p.route(x))

    for cable in cables:
        i, o = enigmatic._letters2num(cable)
        assert p.route(i) == o
        assert p.route(o) == i


def test_wheel_spec_constructor():
    ok_spec = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"

    # check ok
    enigmatic.WheelSpec("test", ok_spec)

    # check conversion to upper
    w = enigmatic.WheelSpec("test", ok_spec.lower())
    assert w.wiring.isupper()

    # check wrong letter
    err_spec = list(ok_spec)
    err_spec[4] = "^"
    err_spec = str(err_spec)
    with pytest.raises(ValueError):
        enigmatic.WheelSpec("testRotor", err_spec)

    # wrong length
    with pytest.raises(ValueError):
        enigmatic.WheelSpec("testRotor", ok_spec[:-1])


def test_rotor_symmetry():
    wiring = list(enigmatic.ALPHABET)
    random.shuffle(wiring)
    wiring = "".join(str(x) for x in wiring)
    spec = enigmatic.WheelSpec("r1", wiring)
    r = enigmatic.Wheel(spec)

    for i, _ in enumerate(enigmatic.ALPHABET):
        letter_out = r.inv_route(r.route(i))
        assert i == letter_out


def test_double_step():
    """ Test the double step feature
    „Royal Flags Wave Kings Above“
    https://de.wikipedia.org/wiki/Enigma_(Maschine)#Anomalie
    """

    enigma = Enigma(['ukw_b', 'I', 'II', 'III'])
    enigma.wheel_rotations = "*ADU"

    enigma.write("x")
    assert enigma.wheel_rotations == "AADV"

    enigma.write("x")
    assert enigma.wheel_rotations == "AAEW"

    enigma.write("x")
    assert enigma.wheel_rotations == "ABFX"


def test_enigma_period():
    """
    https://de.wikipedia.org/wiki/Enigma_(Maschine)#Schl%C3%BCsselraum
    Period = 26*25*26 = 16.900 Walzenstellungen
    """

    enigma = Enigma(['ukw_b', 'I', 'II', 'III'])

    t = time.perf_counter()
    text = enigma.write("x" * 3 * 16900)
    dt = time.perf_counter() - t

    print(f"elapsed time: {dt}")

    assert text[:16900] == text[16900:2*16900] == text[2*16900:]


def test_enigma_typing():
    enigma = Enigma(['ukw_b', 'III', 'II', 'I'])

    assert enigma.write("hallodiesisteintest") == "MTNCZEVKHZUDSOACOEF"
    console.print(enigma)
    console.print(enigma.memory)


def test_M3_wiki_message():
    """
    messsage described in:
    https://de.wikipedia.org/wiki/Enigma_(Maschine)
    """

    message = """LJPQH SVDWC LYXZQ FXHIU VWDJO BJNZX RCWEO TVNJC IONTF
QNSXW ISXKH JDAGD JVAKU KVMJA JHSZQ QJHZO IAVZO WMSCK ASRDN
XKKSR FHCXC MPJGX YIJCC KISYY SHETX VVOVD QLZYT NJXNU WKZRX
UJFXM BDIBR VMJKR HTCUJ QPTEE IYNYN JBEAQ JCLMU ODFWM ARQCF
OBWN""".replace(' ', '').replace('\n', '')

    translation = """dasoberkommandoderwehrmaqtgibtbekanntxaachenxaache
nxistgerettetxdurqgebuendelteneinsatzderhilfskraef
tekonntediebedrohungabgewendetunddierettungderstad
tgegenxeinsxaqtxnullxnullxuhrsiqergestelltwerdenx"""

    # Tagesschlüssel:
    # Tag UKW Walzenlage Ringstellung ---- Steckerverbindungen ----    Kenngruppen
    #  31  B  I   IV III   16 26 08   AD CN ET FL GI JV KZ PU QY WX  dmr now wxy bev
    #
    # Die Kenngruppe hat keine kryptologische Bedeutung,[49] sie dient dem Empfänger der Nachricht nur dazu, zu erkennen, dass die Nachricht wirklich für ihn bestimmt ist und auch befugt entschlüsselt werden kann.

    enigma = Enigma(['ukw_b', 'I', 'IV', 'III'])
    enigma.plugboard.cables = "AD CN ET FL GI JV KZ PU QY WX"
    enigma.wheel_rotations = "*QWE"
    enigma.ring_positions = [1, 16, 26, 8]

    message_key = 'RTZ'
    assert enigma.write(message_key) == 'EWG'

    # Spruchkopf wird offen übertragen
    # Uhrzeit - Anzahl zeichen - Zufällige Wahl + Ergebnis
    # Kopf: 2220 – 204 – QWE EWG -

    enigma.wheel_rotations = "*" + message_key
    assert enigma.write(translation) == message


def test_M4_message():
    """ https://www.cryptomuseum.com/crypto/enigma/msg/p1030681.htm """

    enigma = Enigma(['ukw_caesar', 'beta', 'V', 'VI', 'VIII'])
    enigma.plugboard.cables = "AE BF CM DQ HU JN LX PR SZ VW"
    enigma.wheel_rotations = "*NAEM"
    enigma.ring_positions = "*EPEL"

    msg_key = enigma.write("QEOB")
    print(f"msg_key: {msg_key}")

    assert msg_key == "CDSZ"

    enigma.wheel_rotations = "*" + msg_key

    cypher_text = """LANO TCTO UARB BFPM HPHG CZXT DYGA HGUF XGEW KBLK GJWL QXXT
       GPJJ AVTO CKZF SLPP QIHZ FXOE BWII EKFZ LCLO AQJU LJOY HSSM BBGW HZAN
       VOII PYRB RTDJ QDJJ OQKC XWDN BBTY VXLY TAPG VEAT XSON PNYN QFUD BBHH
       VWEP YEYD OHNL XKZD NWRH DUWU JUMW WVII WZXI VIUQ DRHY MNCY EFUA PNHO
       TKHK GDNP SAKN UAGH JZSM JBMH VTRE QEDG XHLZ WIFU SKDQ VELN MIMI THBH
       DBWV HDFY HJOQ IHOR TDJD BWXE MEAY XGYQ XOHF DMYU XXNO JAZR SGHP LWML
       RECW WUTL RTTV LBHY OORG LGOW UXNX HMHY FAAC QEKT HSJW"""

    plain_text = """KRKRALLEXXFOLGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBEBEFEHLERH
   ALTENXXJANSTERLEDESBISHERIGXNREICHSMARSCHALLSJGOERINGJSETZTDERFUEHRER
   SIEYHVRRGRZSSADMIRALYALSSEINENNACHFOLGEREINXSCHRIFTLSCHEVOLLMACHTUNTE
   RWEGSXABSOFORTSOLLENSIESAEMTLICHEMASSNAHMENVERFUEGENYDIESICHAUSDERGEG
   ENWAERTIGENLAGEERGEBENXGEZXREICHSLEITEIKKTULPEKKJBORMANNJXXOBXDXMMMDU
   RNHFKSTXKOMXADMXUUUBOOIEXKP""".replace(' ', '').replace('\n', '')

    output_text = enigma.write(cypher_text)
    console.print(output_text)

    assert output_text == plain_text
