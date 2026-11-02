@echo off
echo ========================================================
echo Launching Avast Secure Browser with Remote Debugging
echo ========================================================
echo Closing current Avast instances to release profile lock...
taskkill /F /IM AvastBrowser.exe 2>nul
timeout /t 2 /nobreak >nul
echo Starting Avast with CDP port 9222...
start "" "C:\Program Files\Avast Software\Browser\Application\AvastBrowser.exe" --remote-debugging-port=9222 --remote-allow-origins=*
echo.
echo Avast Secure Browser is running with remote automation enabled!
