@echo off
echo =======================================================
echo   Antigravity Automacios Bongeszo Inditasa (Avast)
echo =======================================================
echo.
echo Profil mentesi helye: H:\avast-automation-profile
echo Debug port: 9222
echo.
echo Megnyitom a Google Ads Keyword Plannert...
echo.

start "" "C:\Program Files\Avast Software\Browser\Application\AvastBrowser.exe" ^
  --user-data-dir="H:\avast-automation-profile" ^
  --remote-debugging-port=9222 ^
  --remote-allow-origins=* ^
  "https://ads.google.com/aw/keywordplanner/home"

echo A bongeszo elindult a 9222-es porton!
echo Miutan a bongeszo megjelent, az AI azonnal atveheti az iranyitast!
pause
