#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

~LButton::
KeyWait, LButton, T0.2  ; Wait for 200ms to see if it's a hold
if (ErrorLevel)  ; If LButton was held for 200ms or more
{
    KeyWait, LButton, D  ; Wait for LButton to be released
    SetTimer, CheckRButton, 10
}
return

CheckRButton:
if (!GetKeyState("LButton", "P"))  ; If LButton is no longer pressed
{
    SetTimer, CheckRButton, Off
    return
}
if (GetKeyState("RButton", "P"))  ; If RButton is pressed
{
    Send, {Delete}  ; This sends the Delete key press
    SetTimer, CheckRButton, Off
}
return
