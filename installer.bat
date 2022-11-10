@echo off
Title Package Installer
echo Installer requirements
python -m pip install -r requirements.txt --force-reinstall --no-cache

echo "MAKE SURE TO DOWNLOAD TESSERACT FROM https://sourceforge.net/projects/tesseract-ocr.mirror/"
PAUSE