import sqlite3

DB = "data/db/dialogos.db"

def registrar_carga(arquivo, status, erro=None):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO controle_carga (arquivo, status, erro)
    VALUES (?, ?, ?)
    """, (arquivo, status, erro))
    
    conn.commit()
    conn.close()