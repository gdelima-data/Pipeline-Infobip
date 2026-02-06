# ETL Infobip Dialogs

Pipeline ETL em Python para ingestão, tratamento e carga de dados
extraídos manualmente do Infobip.

## Fluxo
1. CSV cai em `data/entrada`
2. Pipeline trata e valida os dados
3. CSV tratado é salvo em `data/processado`
4. Dados são carregados em SQLite
5. Controle de carga é registrado
6. Dados são consumidos no Power BI e heurística posterior

## Execução
```bash
python main.py
```

## Tecnologias
Python  
Pandas  
SQLite  
Task Scheduler (Windows)  



