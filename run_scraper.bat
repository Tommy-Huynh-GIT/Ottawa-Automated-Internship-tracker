@echo off
cd /d "%~dp0"

if not exist logs mkdir logs

echo [%date% %time%] Starting scraper >> logs\scraper.log
python main.py >> logs\scraper.log 2>&1
echo [%date% %time%] Scraper finished with exit code %ERRORLEVEL% >> logs\scraper.log
