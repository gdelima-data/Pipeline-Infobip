import os
import sqlite3
import pandas as pd
from datetime import datetime
from load.schema import SCHEMA_VERSION

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processado")
DB_PATH = os.path.join(BASE_DIR, "data", "db", "dialogos.db")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def salvar_csv(df: pd.DataFrame, prefixo="dialogos"):
    data = datetime.now().strftime("%Y%m%d")
    arquivo = f"{prefixo}_{data}.csv"
    path = os.path.join(PROCESSED_DIR, arquivo)
    
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"CSV salvo em: {path}")
    
    return path

def validar_df_para_carga(df):
    assert not df.empty, "DataFrame vazio"

def carregar_sqlite(df: pd.DataFrame, tabela="dialogos"):
    validar_df_para_carga(df)
    
    colunas = [
        "nome_dialogo",
        "qtde_sessoes",
        "sessoes_expiradas",
        "qtde_ir_para_agente",
        "qtde_intervencao_humana",
        "qtde_encerrar_sessao"
    ]
    
    set_clause = ", ".join([f"{col} = excluded.{col}" for col in colunas[1:]])
    
    placeholders = ", ".join(["?"] * len(colunas))
    
    query = f"""
        INSERT INTO {tabela} ({", ".join(colunas)})
        VALUES ({placeholders})
        ON CONFLICT(nome_dialogo) DO UPDATE SET
        {set_clause}
    """

    with sqlite3.connect(DB_PATH) as conn:
        dados = df[colunas].to_records(index=False).tolist()
        conn.executemany(query, dados)

    print(f"Dados atualizados (sobrescritos) na tabela '{tabela}'")


    