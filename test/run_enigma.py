from enigmatic import Enigma
from rich.console import Console
import rich.traceback
import yaml
from pathlib import Path

rich.traceback.install(show_locals=True)

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)
print = console.print

THIS_DIR = Path(__file__).parent

with open(THIS_DIR / r"test_messages\msg_0.yaml", "r") as stream:
    x = yaml.safe_load(stream)

enigma = Enigma(**x['enigma'])

enigma = Enigma(['ukw_caesar', 'beta', 'V', 'VI', 'VIII'])
enigma.plugboard.cables = "AE BF CM DQ HU JN LX PR SZ VW"
enigma.wheel_positions = "*SCHL"
enigma.ring_positions = "*AAEL"

cypher_text = """TAWZZYNZGGMICVLSADLQFDFKHDGZLSEEMDFFBQLYISEIWKDONDWJWETKZOWWYLTYII
OWSMCFTGNLKOZCAAWHBHFJDRWLDHFHEWUBPWVDEZFPBOCVKECVFXWZGSVBDPHLTVOJCFLSQNSODYFMBQFQU
LTHDISGOQURABEHHIBNXNAAKLEJMXQHJWXAVDLVTPTSTDCPWPYXCUVWAFJTTSFUSPTHOSTHXADWRQWZJCTU
KWCWHYFYQTRTPKPPJGPMDZQDAXAIZLWCADYZUTLXJJUDQGMFWZRWZXBQRHNCRUFUZZ.LALDHHOIBWYPKTSR
NQUHMUPTFWUHWBIKMASACVPRELBRRMRKLZWLVSFGUQFFXTAVQIHXDXRKQVGARLMZDBMDGRYNWIYSHWCNHIW
XYFBFGXXQNPTSEROCVYTOJTKKLQRALUDQMUFAKRHKOJCMWPSZHNAVVSEWFFPGRJTVNOLSGRERKXSCYWBOQT
PXOXJLQXSPYTMEOXOURSHIBYBNWQEFPTGGMCVXNGCDFQIYLCMPDLWOOAALODSWCDAWOZOMBGDZOQKZWQKFR
MRWCHGWFUERWPJAQFDRBVOAEYYAIYNPCLJDXOCBAZOHQOKVUFGLQNXQYDUZJIFXRVJDQ.OOOGXIGNONPEQL
KQBTVJ.DANIXQ.FDYXRDTQTFP.ZEHEOMXPPPFGGLTVFODHBSQPAQMDDWXMMGAJZVURSIYGAAXDZDV""".replace(".", "")

output_text = enigma.write(cypher_text)
console.print(output_text)
