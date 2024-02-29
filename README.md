# termsrv-multiuser-patcher
Patch Windows 10/11's termsrv.dll to enable concurrent multi-user sessions

## Run
1. Have Python 3.6+ installed
2. **Right-click termsrv_patch.py and select "Run as Administrator", then the script will do all the work for you**

The automated steps are:
- Check if termsrv.dll is patchable
- Patch the bytes (39 81 3C 06 00 00 0F ?? ?? ?? ?? ?? -> B8 00 01 00 00 89 81 38 06 00 00 90)
- Stop Remote Desktop Services
- Take ownership and grant permissions to termsrv.dll
- Rename termsrv.dll to termsrv.dll.old
- Write patched termsrv.dll to system32 folder
- Start Remote Desktop Services

*Note: It's (almost) safe to configure the script to run at startup, so it automatically patches the file after a Windows Update. If the file is already patched, it will just exit.*

## Reference
[How to Allow Multiple RDP Sessions on Windows 10 and 11 | Windows OS Hub](https://woshub.com/how-to-allow-multiple-rdp-sessions-in-windows-10/#h2_4)
