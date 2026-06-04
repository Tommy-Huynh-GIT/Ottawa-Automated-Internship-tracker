@echo off
cd /d "C:\Users\tommy\OneDrive\Desktop\Projects\SeleniumStuff"

if not exist logs mkdir logs

echo [%date% %time%] Starting scraper >> logs\scraper.log
"C:\Python314\python.exe" main.py >> logs\scraper.log 2>&1
echo [%date% %time%] Scraper finished with exit code %ERRORLEVEL% >> logs\scraper.log
