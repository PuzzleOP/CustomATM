@echo off
title CustomATM - Update Pack
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0Update-Pack.ps1" %*
echo.
if errorlevel 1 (echo Update did not complete. Read the message above before playing.) else (echo You can now launch this profile in CurseForge.)
pause

