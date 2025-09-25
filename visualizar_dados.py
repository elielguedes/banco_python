#!/usr/bin/env python3
"""
Script para visualizar a modelagem de dados do sistema bancário
"""

import sqlite3
import os
from datetime import datetime

def visualizar_modelagem():
    print("📊 === MODELAGEM DE DADOS DO SISTEMA BANCÁRIO ===\n")
    
    if not os.path.exists("banco_teste.db"):
        print("❌ Banco de dados de teste não encontrado!")
        return
    
    conn = sqlite3.connect("banco_teste.db")
    cursor = conn.cursor()
    
    print("🗄️ === ESTRUTURA DAS TABELAS ===\n")
    
    # Obter schema das tabelas
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    schemas = cursor.fetchall()
    
    for schema in schemas:
        print(f"📋 {schema[0]}")
        print("-" * 80)
    
    print("\n📊 === DADOS ATUAIS ===\n")
    
    # Mostrar contas
    print("👥 TABELA: contas")
    cursor.execute("SELECT * FROM contas")
    contas = cursor.fetchall()
    
    if contas:
        print("ID | Titular        | Saldo     | Data Criação")
        print("-" * 50)
        for conta in contas:
            id_conta, titular, saldo, data = conta
            data_formatada = datetime.fromisoformat(data.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
            print(f"{id_conta:2} | {titular:14} | R$ {saldo:6.2f} | {data_formatada}")
    else:
        print("📭 Nenhuma conta encontrada")
    
    print(f"\n📈 Total de contas: {len(contas)}")
    
    # Mostrar transações
    print(f"\n💳 TABELA: transacoes")
    cursor.execute("""
        SELECT t.id, c.titular, t.tipo, t.valor, t.data_transacao, t.descricao
        FROM transacoes t 
        JOIN contas c ON t.conta_id = c.id
        ORDER BY t.data_transacao DESC
    """)
    transacoes = cursor.fetchall()
    
    if transacoes:
        print("ID | Titular        | Tipo      | Valor     | Data/Hora        | Descrição")
        print("-" * 80)
        for transacao in transacoes:
            id_trans, titular, tipo, valor, data, descricao = transacao
            data_formatada = datetime.fromisoformat(data.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
            print(f"{id_trans:2} | {titular:14} | {tipo:9} | R$ {valor:6.2f} | {data_formatada} | {descricao}")
    else:
        print("📭 Nenhuma transação encontrada")
    
    print(f"\n📊 Total de transações: {len(transacoes)}")
    
    # Estatísticas
    print(f"\n📈 === ESTATÍSTICAS ===")
    
    # Saldo total do banco
    cursor.execute("SELECT SUM(saldo) FROM contas")
    saldo_total = cursor.fetchone()[0] or 0
    print(f"💰 Saldo total no banco: R$ {saldo_total:.2f}")
    
    # Conta com maior saldo
    cursor.execute("SELECT titular, saldo FROM contas ORDER BY saldo DESC LIMIT 1")
    maior_saldo = cursor.fetchone()
    if maior_saldo:
        print(f"🏆 Maior saldo: {maior_saldo[0]} - R$ {maior_saldo[1]:.2f}")
    
    # Total de depósitos
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'DEPOSITO'")
    total_depositos = cursor.fetchone()[0] or 0
    print(f"📈 Total depositado: R$ {total_depositos:.2f}")
    
    # Total de saques
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'SAQUE'")
    total_saques = cursor.fetchone()[0] or 0
    print(f"📉 Total sacado: R$ {total_saques:.2f}")
    
    conn.close()
    
    print(f"\n🎯 === RELACIONAMENTOS ===")
    print("📋 contas (1) ←→ (N) transacoes")
    print("   • Cada conta pode ter múltiplas transações")
    print("   • Cada transação pertence a uma única conta")
    print("   • Chave estrangeira: transacoes.conta_id → contas.id")
    
    print(f"\n💾 === INFORMAÇÕES DO ARQUIVO ===")
    if os.path.exists("banco_teste.db"):
        size = os.path.getsize("banco_teste.db")
        print(f"📁 Arquivo: banco_teste.db")
        print(f"📊 Tamanho: {size} bytes ({size/1024:.1f} KB)")

if __name__ == "__main__":
    visualizar_modelagem()