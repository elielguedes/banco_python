#!/usr/bin/env python3
"""
Script para recriar o banco de dados com schema correto
"""

import sqlite3
import os

def recriar_banco():
    """Recria o banco com schema correto"""
    # Remover banco antigo se existir
    if os.path.exists("banco.db"):
        os.remove("banco.db")
        print("✅ Banco antigo removido")
    
    # Criar novo banco
    from banco_db import BancoDados
    banco = BancoDados()
    print("✅ Novo banco criado com schema correto")
    
    # Verificar tabelas
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    print(f"📊 Tabelas criadas: {[t[0] for t in tabelas]}")
    
    # Verificar colunas da tabela contas
    cursor.execute("PRAGMA table_info(contas);")
    colunas = cursor.fetchall()
    print(f"📋 Colunas da tabela 'contas': {[c[1] for c in colunas]}")
    
    conn.close()
    print("✅ Banco recriado com sucesso!")

if __name__ == "__main__":
    recriar_banco()