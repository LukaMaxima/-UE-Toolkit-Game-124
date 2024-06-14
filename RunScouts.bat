start Powershell.exe -executionpolicy remotesigned -File "Powershell\Run Scouts Analysis.ps1"
timeout /t 12 /nobreak >nul  // Give some time for the script to open the window
start Powershell\SendKeys.ahk