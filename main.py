from ingest.watcher import verificar_novos_arquivos
from transform.tratamento import tratamento
from load.carga import salvar_csv
from load.carga import carregar_sqlite
from control.controle import registrar_carga
import pandas as pd

def pipeline():
    arquivos = verificar_novos_arquivos()

    for arquivo in arquivos:
        try:
            df_raw = pd.read_csv(arquivo)
            
            df = tratamento(df_raw)

            # 1️⃣ Persistir resultado do T
            salvar_csv(df)

            # 2️⃣ Carregar no banco
            carregar_sqlite(df)

            registrar_carga(str(arquivo), "SUCESSO")

        except Exception as e:
            registrar_carga(str(arquivo), "ERRO", str(e))

if __name__ == "__main__":
    pipeline()