from time import sleep

dllpath = 'c:/windows/system32/termsrv.dll'
findbytes = bytes.fromhex('39 81 3C 06 00 00 0F')
patchbytes = bytes.fromhex('B8 00 01 00 00 89 81 38 06 00 00 90')

with open(dllpath, mode='rb') as f:
    srcdll = f.read()

a = srcdll.find(findbytes)
if a == -1:
    print('file not supported')
    sleep(2)
    exit()

newdll = srcdll[:a] + patchbytes + srcdll[a + len(patchbytes):]

f = open('./termsrv.dll', mode='wb')
f.write(newdll)
f.close()

print('patch success')
sleep(2)