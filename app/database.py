import sqlite3
from config import DB_FILE

def conectar():
    return sqlite3.connect(DB_FILE)


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        residencia TEXT,
        tipo TEXT,
        favorecido TEXT,
        referencia TEXT,
        valor REAL,
        vencimento TEXT,
        codigo_barras TEXT,
        pix_payload TEXT,
        descricao TEXT,
        status TEXT DEFAULT 'pendente',
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def inserir_conta(dados):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO contas (
        residencia,
        tipo,
        favorecido,
        referencia,
        valor,
        vencimento,
        codigo_barras,
        pix_payload,
        descricao
    ) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados.get("residencia"),
        dados.get("tipo"),
        dados.get("favorecido"),
        dados.get("referencia"),
        float(dados.get("valor", "0").replace(",", ".")) if dados.get("valor") else None,
        dados.get("vencimento"),
        dados.get("codigo_pagamento"),
        dados.get("pix_payload"),
        dados.get("descricao"),
    ))

    conn.commit()
    conn.close()

