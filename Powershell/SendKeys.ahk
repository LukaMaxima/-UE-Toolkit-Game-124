SetTitleMatchMode, RegEx  ; Enable regex match mode

; Wait for the window with a regex pattern that matches titles like "UE - Analyse... - JupyterLab"
WinWaitActive, UE - Analyse.*JupyterLab

; Activate the window
WinActivate
Sleep, 2000  ; Wait for 500 milliseconds

; Send Ctrl+A to select all text
Send, ^a
Sleep, 2000  ; Wait for 500 milliseconds
Send, +{Enter}