import subprocess
import os
import ctypes
from time import sleep


def printTxt(txt):
    print(f'\n{'=' * (len(txt) + 2)}\n {txt} \n{'=' * (len(txt) + 2)}')


if not ctypes.windll.shell32.IsUserAnAdmin():
    printTxt('Please run this file as Administrator')
    input()
    exit()


dllpath = R'c:\windows\system32\termsrv.dll'
find_bytes = bytes.fromhex('39 81 3C 06 00 00 0F')
patch_bytes = bytes.fromhex('B8 00 01 00 00 89 81 38 06 00 00 90')


with open(dllpath, mode='rb') as f:
    srcdll = f.read()

patch_offset = srcdll.find(find_bytes)

if patch_offset == -1:
    if srcdll.find(patch_bytes) > 0:
        printTxt('File already patched')
    else:
        printTxt('File not supported')
    for i in range(5, 0, -1):
        print('.' * i + ' ' * (5 - i), end='\r')
        sleep(1)
    exit()
else:
    printTxt(f'Found target bytes at 0x{patch_offset:0X}')

newdll = srcdll[:patch_offset] + patch_bytes + srcdll[patch_offset + len(patch_bytes):]


printTxt('Stopping termservice...')
subprocess.call('net stop termservice /y', shell=True)

printTxt('Taking ownership of termsrv.dll')
subprocess.call(f'takeown /f {dllpath} /a')

printTxt('Granting permissions for Administrators to termsrv.dll')
subprocess.call(f'icacls {dllpath} /grant administrators:f')

try:
    suffix = 0
    while os.path.isfile(f'{dllpath}.old{'' if suffix == 0 else suffix}'):
        suffix += 1
    printTxt(f'Renaming termsrv.dll to termsrv.dll.old{'' if suffix == 0 else suffix}')
    if subprocess.call(f'ren {dllpath} termsrv.dll.old{'' if suffix == 0 else suffix}', shell=True) != 0:
        raise Exception('Failed to rename termsrv.dll')

    printTxt('Writing patched file')
    with open(dllpath, mode='wb') as f:
        f.write(newdll)

    printTxt('Starting termservice...')
    if subprocess.call('net start termservice', shell=True) != 0:
        raise Exception('Failed to start service')

    printTxt('Patch success')
except Exception as e:
    print(f'\n!!! {e} !!!')

input('\nPress enter to exit')
