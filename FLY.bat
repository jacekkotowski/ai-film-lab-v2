@echo off
REM FLY -- stage 2: a finished film becomes its 3D flight (fly\FLY.bat does the work).
REM   drag a film's out\ folder or final.mp4 on it, or: FLY.bat <project> --draft
call "%~dp0fly\FLY.bat" %*
