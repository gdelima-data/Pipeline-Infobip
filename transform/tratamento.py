import pandas as pd

def tratamento(df):
    """
    Padroniza colunas e remove duplicatas e nulos dos dados extraídos 
    do Infobip
    """
    
    # Renomear colunas
    df = df.rename(columns={ 
        'Nome do diálogo': 'nome_dialogo',
        'Sessões': 'qtde_sessoes', 
        'Usuários': 'qtde_usuarios', 
        'Sessões expiradas': 'sessoes_expiradas', 
        'Ir para a ação do agente': 'qtde_ir_para_agente', 
        'Aquisição do agente': 'qtde_intervencao_humana', 
        'Fechar sessão': 'qtde_encerrar_sessao'
    })
    
    # Remover duplicatas
    if df.duplicated().sum() > 0:
        df = df.drop_duplicates()
    
    # Remover linhas totalmente nulas
    df = df.dropna(how='all')
    
    # Manter apenas colunas válidas para o banco
    colunas_validas = [
        "nome_dialogo",
        "qtde_sessoes",
        "sessoes_expiradas",
        "qtde_ir_para_agente",
        "qtde_intervencao_humana",
        "qtde_encerrar_sessao"
    ]
    # Se alguma coluna obrigatória ainda não existir, você pode criar vazia
    for col in colunas_validas:
        if col not in df.columns:
            df[col] = None
    
    df = df[colunas_validas]
    
    return df
