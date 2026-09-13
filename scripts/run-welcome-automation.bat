@echo off
cd /d "%USERPROFILE%\Documents\SunEnergyTechnology"
python scripts\solar-welcome-automation.py --send >> scripts\automation-log.txt 2>&1
echo --- Run complete: %DATE% %TIME% --- >> scripts\automation-log.txt
