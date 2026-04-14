import pandas as pd
from prefect import flow, task, get_run_logger
from prefect.client.schemas.schedules import CronSchedule
from ingest.watcher import verificar_novos_arquivos
from transform.tratamento import tratamento
from load.carga import carregar_sqlite
from control.controle import registrar_carga
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PASTA_PROCESSADOS = BASE_DIR / "data" / "processado"
PASTA_PROCESSADOS.mkdir(parents=True, exist_ok=True)

@task(retries=2, retry_delay_seconds=5)
def ingest() -> list[Path]:
    return verificar_novos_arquivos()
    
@task
def transform(arquivo):
    df = pd.read_csv(arquivo)
    return tratamento(df)
    
@task
def mover_arquivo(arquivo):
    destino = PASTA_PROCESSADOS / arquivo.name
    shutil.move(str(arquivo), destino)

@task(retries=3, retry_delay_seconds=10)
def carregar_banco(df):
    return carregar_sqlite(df)
        
@task
def registrar_sucesso(arquivo):
    registrar_carga(str(arquivo), "SUCESSO")
    
@task
def registrar_erro(arquivo, erro):
    registrar_carga(str(arquivo), "ERRO", str(erro))
    
@flow(name="ETL Dialogos Infobip")
def etl_pipeline():
    
    logger = get_run_logger()
    logger.info("Iniciando pipeline")
    
    # Ingestão
    arquivos = ingest()
    
    if not arquivos:
        logger.warning('Nenhum arquivo encontrado')
        return
    
    logger.info(f'{len(arquivos)} arquivo encontrado')
    
    for arquivo in arquivos:
        try:
            # Transformação
            df_tratado = transform(arquivo)
            
            # Carga
            carregar_banco(df_tratado)
            
            # Registro
            mover_arquivo(arquivo)
            registrar_sucesso(arquivo)
            
        except Exception as e:
            registrar_erro(arquivo, str(e))
            continue
    
    logger.info('Pipeline finalizado')
    
if __name__ == "__main__":
    etl_pipeline.serve(
    name="deployment",
    schedule=CronSchedule(
    cron="0 10 * * *",
    timezone="America/Sao_Paulo",
    ),
    tags=["local", "infobip"]
    )