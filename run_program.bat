@echo off
:start
Title Package Installer
echo Installer requirements
python AutoRain.py
python -m pip install -r requirements.txt --force-reinstall --no-cache
python AutoRain.py
goto start
PAUSE