@echo off
Title Package Installer
echo Installer requirements
python -m pip install -r requirements.txt --force-reinstall --no-cache
python AutoRain.py
PAUSE