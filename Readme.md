# PythonAESObfuscate
Pythonic way to load shellcode. Builds an EXE for you too!

### Usage
* Place a `payload.bin` raw shellcode file in the same directory. Default Architecture is x86
* run `python obfuscate.py`
* Default output is `out.py`

#### Requirements
* Windows
* Python 2.7
* Pyinstaller
* PyCrypto (PyCryptodome didn't seem to work)