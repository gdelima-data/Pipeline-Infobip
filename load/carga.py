import os
import sqlite3
import pandas as pd
import pandera as pa
from transform.tratamento import schema
from sqlalchemy import create_engine, text
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processado")
DB_PATH = os.path.join(BASE_DIR, "data", "db", "dialogos.db")

# Cria diretórios caso não existam
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(f'sqlite:///{DB_PATH}')

def validar_df_para_carga(df: pd.DataFrame):
    try:
        schema.validate(df, lazy=True)
    except pa.errors.SchemaErros as err:
        print('Erro de validação nos dados antes da carga:')
        print(err.failure_cases)
        raise

def carregar_sqlite(df: pd.DataFrame, tabela="dialogos"):
    # Validação
    validar_df_para_carga(df)
    
    colunas = [
        "nome_dialogo",
        "qtde_usuarios",
        "qtde_sessoes",
        "sessoes_expiradas",
        "qtde_ir_para_agente",
        "qtde_intervencao_humana",
        "qtde_encerrar_sessao"
    ]

    df_upload = df[colunas].copy()
    
    with engine.begin() as conn:
        df_upload.to_sql('stg_dialogos', conn, if_exists='replace', index=False)
        
        delete_query = f"""
            DELETE FROM {tabela} 
            WHERE nome_dialogo IN (SELECT nome_dialogo FROM stg_dialogos);
        """
        conn.execute(text(delete_query))
      
        insert_query = f"""
            INSERT INTO {tabela} ({', '.join(colunas)})
            SELECT {', '.join(colunas)} FROM stg_dialogos;
        """
        result = conn.execute(text(insert_query))
        
        conn.execute(text('DROP TABLE stg_dialogos'))
        
        print(f'Carga Finalizada. Linhas atualizadas: {result.rowcount}')