from enigmatic import Enigma
from rich.console import Console
import rich.traceback

rich.traceback.install(show_locals=True)

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)

enigma = Enigma(['ukw_caesar', 'beta', 'V', 'VI', 'VIII'])
enigma.plugboard.cables = "AE BF CM DQ HU JN LX PR SZ VW"
enigma.wheel_rotations = "*NAEM"
enigma.ring_positions = "*EPEL"

msg_key = enigma.write("QEOB")
print(f"msg_key: {msg_key}")

enigma.wheel_rotations = "*" + msg_key

cypher_text = """LANO TCTO UARB BFPM HPHG CZXT DYGA HGUF XGEW KBLK GJWL QXXT
   GPJJ AVTO CKZF SLPP QIHZ FXOE BWII EKFZ LCLO AQJU LJOY HSSM BBGW HZAN
   VOII PYRB RTDJ QDJJ OQKC XWDN BBTY VXLY TAPG VEAT XSON PNYN QFUD BBHH
   VWEP YEYD OHNL XKZD NWRH DUWU JUMW WVII WZXI VIUQ DRHY MNCY EFUA PNHO
   TKHK GDNP SAKN UAGH JZSM JBMH VTRE QEDG XHLZ WIFU SKDQ VELN MIMI THBH
   DBWV HDFY HJOQ IHOR TDJD BWXE MEAY XGYQ XOHF DMYU XXNO JAZR SGHP LWML
   RECW WUTL RTTV LBHY OORG LGOW UXNX HMHY FAAC QEKT HSJW"""


output_text = enigma.write(cypher_text)
console.print(output_text)
