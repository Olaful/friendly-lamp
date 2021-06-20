@echo off

echo Starting ie...
start "browser" "C:\Program Files\Internet Explorer\iexplore.exe" & ping 127.0.0.1 -n 2 > nul
pause