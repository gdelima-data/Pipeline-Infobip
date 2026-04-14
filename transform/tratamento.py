import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema

schema = DataFrameSchema(
    columns={
        "nome_dialogo": Column(str),
        "qtde_usuarios": Column("Int64", Check.greater_than_or_equal_to(0), coerce=True, nullable=True),
        "qtde_sessoes": Column("Int64", Check.greater_than_or_equal_to(0), coerce=True, nullable=True),
        "sessoes_expiradas": Column("Int64", Check.greater_than_or_equal_to(0), coerce=True, nullable=True),
        "qtde_ir_para_agente": Column("Int64", Check.greater_than_or_equal_to(0), coerce=True, nullable=True),
        "qtde_intervencao_humana": Column("Int64", Check.greater_than_or_equal_to(0), coerce=True, nullable=True),
        "qtde_encerrar_sessao": Column("Int64", Check.greater_than_or_equal_to(0), coerce=True, nullable=True),
        },
        strict=False,
        coerce=True
        )
        

def tratamento(df):
    """
    Padroniza colunas e remove duplicatas e nulos dos dados extraídos 
    do Infobip
    """
    mapping = {
        'Nome do diálogo': 'nome_dialogo',
        'Sessões': 'qtde_sessoes', 
        'Usuários': 'qtde_usuarios', 
        'Sessões expiradas': 'sessoes_expiradas', 
        'Ir para a ação do agente': 'qtde_ir_para_agente', 
        'Aquisição do agente': 'qtde_intervencao_humana', 
        'Fechar sessão': 'qtde_encerrar_sessao'
    }
   
    df_limpo = df.rename(columns=mapping).drop_duplicates().dropna(how='all')
    
    for col in schema.columns:
        if col not in df_limpo.columns:
            df_limpo[col] = 0
    
    df_limpo = df_limpo.fillna(0)
            
    return schema.validate(df_limpo)
