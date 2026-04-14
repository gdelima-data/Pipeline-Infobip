from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # raiz do projeto
PASTA_ENTRADA = BASE_DIR / "data" / "entrada"
PASTA_PROCESSADOS = BASE_DIR / "data" / "processado"

def verificar_novos_arquivos():
    arquivos = []

    for arquivo in PASTA_ENTRADA.glob("*.csv"):
        destino = PASTA_PROCESSADOS / arquivo.name
        if not destino.exists():
            arquivos.append(arquivo)
    
    return arquivos
    
verificar_novos_arquivos()