@echo off
REM ============================================================
REM  SLIDES -- stage 0: animated slides for a film (slides\).
REM
REM    SLIDES.bat screening-95-percent-accurate check     rehearse every step against the script
REM    SLIDES.bat screening-95-percent-accurate publish   stills + script into the film's project
REM    SLIDES.bat screening-95-percent-accurate clips     after narrating + film go: the clips
REM    SLIDES.bat screening-95-percent-accurate look      every still, its notes, margins, timing
REM  Films: slides\films\*.txt, each named by its film's slug (film\projects\<Title>)
REM ============================================================
cd /d "%~dp0slides"
where uv >nul 2>nul
if errorlevel 1 (
  echo Cannot find 'uv'. In PowerShell: winget install --id astral-sh.uv -e
  pause
  exit /b 1
)
if "%~1"=="" (
  echo Films:
  dir /b films\*.txt | findstr /v ".script.txt"
  echo.
  echo Usage: SLIDES.bat ^<film^> check^|publish^|clips^|look
  pause
  exit /b 0
)
if /i "%~2"=="look" (
  uv run python -m aimanim.look film %1
) else (
  uv run python -m aimanim.film %1 %2
)
echo.
pause
