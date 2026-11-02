@echo off
echo =======================================================
echo   Antigravity Automacios Bongeszo Inditasa (Chrome)
echo =======================================================
echo.
echo Profil mentesi helye: H:\chrome-automation-profile
echo Debug port: 9222
echo.
echo Megnyitom a Google Ads Keyword Plannert...
echo.

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --user-data-dir="H:\chrome-automation-profile" ^
  --remote-debugging-port=9222 ^
  --remote-allow-origins=* ^
  "https://ads.google.com/aw/keywordplanner/home"

echo A Chrome elindult a 9222-es porton!
pause
