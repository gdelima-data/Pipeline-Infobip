@echo off

echo [%date% %time%] Iniciando pipeline >> logs\task_scheduler.log

cd /d C:\Users\gabriel.lima_incenti\Documents\Scraping\ETL

python main.py >> logs\task_scheduler.log 2>&1

echo [%date% %time%] Pipeline finalizado >> logs\task_scheduler.log
