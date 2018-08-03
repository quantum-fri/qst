;--------In SPC GUI------
;file: 14, 32
;   save data: 30, 82
;   save: 1300, 636
;start/stop: 134, 356
#WinActivateForce
;Hotkey: Q + S + T
#if GetKeyState("s") && GetKeyState("t")
d::

;Settings
CoordMode, Mouse, Screen
DetectHiddenWindows, On
SetTitleMatchMode, 2

;Allow for customizable folder name to store data
FormatTime, month,, MMMM
FormatTime, day,, d
InputBox, newFolder, Name Data Set, `Enter a valid folder name to store the data,,,, 726, 465,,, %day%-

;Create the file
FileCreateDir, C:\Users\quantum\Desktop\QST experiments\%month%\%newFolder%

;Store the path so we can enter it when prompted
thePath = C:\Users\quantum\Desktop\QST experiments\%month%\%newFolder%

;Names to loop over
files := ["d", "a", "r", "l","h","v"]

;Make sure both of our lab equiment interfaces are ready for the script
IfWinExist, Thorlabs `Single Photon Counter `GUI 
{
    WinActivate
    WinMaximize
} else {
    Run C:\Program Files (x86)\Thorlabs\SPCM\SinglePhotonCounterGUI.exe
    WinMaximize
}

IfWinExist, Kinesis 
{
    WinActivate
    WinMaximize
} else {
    Run C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.Kinesis.exe
    WinMaximize
}

;The tomography program that generates the random povm (a tetrahedron) and eventually runs the tomography calculation
;Run, C:\ProgramData\Anaconda3\python.exe Tomography.py %thePath%, C:\Users\quantum\Desktop\QST experiments\Programs
WinActivate Anaconda Prompt
Send, python stdTomo.py "%thePath%"{Enter}


SleepCalculator(q, qPrev, h, hPrev) {
    theta := Max(Mod(q - qPrev, 180), Mod(h - hPrev, 180)) ; determines the largest angle of rotation for either of the rotators
    if (theta > 20) { ;Handles acceleration and max velocity
        return 1500 * ((theta - 20)/20.0 + 2)
    } else { ;1500 is to hopefuly account for the time it takes for the rotator to decelerate/make corrections
        return 1500 * (Sqrt(theta / 5.0))
    }
}


WinActivate, Kinesis
Sleep 1000
Click, 1597, 641
Sleep 100
Click, 278, 205
Click, 873, 220

Sleep 38000 ; max homing time (hopefuly)

;Read angle data from python program. Set it after the big homing sleep to give it time make calculations
anglesQuarter := []
anglesHalf := []
SetWorkingDir, C:\Users\quantum\Desktop\QST experiments\Programs

Loop, Read, runData.txt
{
    Loop, parse, A_LoopReadLine, %A_Space%
    {
        if (A_Index = 1) {
            anglesQuarter.push(A_LoopField)
        } else {
            anglesHalf.push(A_LoopField)
        }
    }
}

qPrev := 0 ;Used to properly calculate sleep times for rotators
hPrev := 0

For i, fileName in files {

    q := Mod(334 + anglesQuarter[i], 360) ;Calculate the proper angle to input into rotators 
    h := Mod(305 + anglesHalf[i], 360)  

   
    WinActivate, Kinesis,, Thorlabs Single Photon Counter GUI
    ;WinWaitActive here somehow prevents Kinesis from being Active so just leave it out

    Click, 947, 149 ;Move
    Sleep, 1100 ;make sure program has time to catch up
    Send, %q%{Enter} ; input angle for the rotator with the quarter waveplate
    Click, 336, 146
    Sleep, 1100
    Send, %h%{Enter}
    
    sleepVal := SleepCalculator(q, qPrev, h, hPrev) ;Sleeps long enough to allow both motors reach their intended positions
    qPrev := q ;set up for next loop
    hPrev := h
    Sleep, sleepVal


    WinActivate, Thorlabs Single Photon Counter GUI,, Kinesis ;Return to SPC interface to collect data
    WinWaitActive, Thorlabs Single Photon Counter GUI,, Kinesis
    
    Click, 134, 356 ;Start collecting data
    Sleep 10000
    Click, 134, 356 ;Stop collecting data
    Click, 14, 32 ;File
    Click, 30, 82 ;Sava data
    Click 1026, 563 ;Handles a pop up box that likely won't appear when the SPD is actually connected.
    if (i = 1) { ;Following code specifies the new folder to save data. Only needs to run the first time.
        Click, right, 1162, 183 ;select edit path
        Click, 1180, 238 ;click edit path
        Send, %thePath%{Enter} ;enter path
    }
    Click, 695, 562 ; select filename entry
    Sleep 50
    ;FIXME: filenames are not written correctly
    Send, %fileName%{Enter} ; enter filename
    Sleep 100 ;the last two sleeps help the program do everything in proper sequence.
}

Return