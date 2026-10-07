@echo off
REM ============================================================
REM  FLY  --  turn an ai-film-lab film into its 3D flight.
REM
REM    drag a film ONTO it    its final.timeline.json, final.mp4,
REM                           out\ folder or project folder:
REM                           makes a new project and its stills,
REM                           then asks: draft, video or quit
REM    FLY.bat what-is-love --draft    a project you have (the film's slug)
REM    FLY.bat what-is-love --video
REM
REM  Works offline. Needs Python, Blender and ffmpeg (see README).
REM ============================================================
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 goto :nopython

if "%~1"=="" (
  python library\rigs\fly.py
) else (
  python library\rigs\fly.py %*
)

echo.
pause
exit /b 0

:nopython
echo.
echo   Cannot find 'python'. Open PowerShell and paste:
echo.
echo     winget install Python.Python.3.12
echo.
echo   Then close every terminal window and run this again.
echo.
pause
exit /b 1
