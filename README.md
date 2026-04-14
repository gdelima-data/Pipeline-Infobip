# ETL Infobip Dialogs

Pipeline ETL orquestrado para ingestão, validação e carga incremental de dados de BI,
com foco em confiabilidade, rastreabilidade e escalabilidade.

## Arquitetura do Pipeline

- **Ingestão**: Monitoramento de arquivos CSV em diretório local
- **Orquestração**: Prefect (flows, tasks, retries e logging)
- **Transformação**: Pandas
- **Validação**: Pandera (contratos de dados)
- **Persistência intermediária**: CSV tratado
- **Carga**: SQLite
- **Controle**: Registro de cargas e status de execução
- **Consumo**: Power BI

## Fluxo
1. Arquivos CSV são disponibilizados manualmente em `data/entrada`
2. O Prefect orquestra a execução do pipeline
3. Os dados são ingeridos e transformados com Pandas
4. Validações de schema e qualidade são aplicadas com Pandera
5. O dataset tratado é persistido em `data/processado`
6. Os dados são carregados em SQLite
7. O controle de cargas é registrado para rastreabilidade
8. Os dados são consumidos no Power BI para análise e geração de insights

## Tecnologias
Python  
Pandas  
SQLite  
SQLAlchemy
Prefect
Pandera



