start Powershell.exe -executionpolicy remotesigned -File "Powershell\Run Team Analysis.ps1"
timeout /t 12 /nobreak >nul  // Give some time for the script to open the window
start Powershell\SendKeys.ahk