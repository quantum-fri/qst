;--------In SPC GUI------
;file: 14, 32
;   save data: 30, 82
;   save: 1300, 636
;start/stop: 134, 356
#if GetKeyState("q") && GetKeyState("s")
t::
CoordMode, Mouse, Screen
FormatTime, month,, MMMM
FormatTime, day,, d
InputBox, newFolder, Name Data Set, `Enter a valid folder name to store the data,,,, 726, 465,,, %day%-

FileCreateDir, C:\Users\quantum\Desktop\QST experiments\%month%\%newFolder%
thePath = C:\Users\quantum\Desktop\QST experiments\%month%\%newFolder%
files := ["d1", "d2", "a1", "a2", "r1", "r2", "l1", "l2", "h1", "h2", "v1", "v2"]
uniqueNum := WinExist("Thorlabs Single Photon Counter GUI")
IfWinExist, Thorlabs `Single Photon Counter `GUI
    WinActivate
else {
    Run C:\Program Files (x86)\Thorlabs\SPCM\SinglePhotonCounterGUI.exe
    ;WinWait Thorlabs `Single Photon Counter `GUI
}


for fileName in files
{
    ;MsgBox, %fileNameqs%
    Click, 134, 356
    Sleep 10000
    Click, 134, 356
    Click, 14, 32
    Click, 30, 82
    Click 1026, 563
    Click, right, 1162, 183
    Click, 1180, 238
    Send, %thePath%{Enter}
    Click, 695, 562
    Send, %fileName%{Enter}
}
return
