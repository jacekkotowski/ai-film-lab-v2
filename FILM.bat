@echo off
REM FILM -- stage 1: narrate, cut and caption a film (film\FILM.bat does the work).
REM   double-click: carry on with the last film    drag files on: a new film
REM   FILM.bat "<film name>": work on that film
call "%~dp0film\FILM.bat" %*
