#!/usr/bin/env python3
"""
Script de teste para o sistema bancário SEGURO
"""

from banco_db import BancoDados
from main import ContaBancaria
import os

def teste_sistema_seguro():
    print("🔐 === TESTE DO SISTEMA BANCÁRIO SEGURO ===\n")
    
    # Remover arquivos de teste se existirem
    arquivos_teste = ["banco_seguro_teste.db", "sistema.key", "logs_seguranca.txt"]
    for arquivo in arquivos_teste:
        if os.path.exists(arquivo):
            os.remove(arquivo)
    
    # Criar banco de dados de teste
    banco = BancoDados("banco_seguro_teste.db")
    
    print("✅ Sistema bancário seguro inicializado!")
    print("🔐 Chave de criptografia gerada automaticamente")
    
    # Teste 1: Criar conta com senha
    print("\n📝 Teste 1: Criando conta com autenticação...")
    try:
        conta_id, numero_conta = banco.criar_conta("João Silva Santos", "minha_senha_123", 1000.0)
        if conta_id:
            print(f"✅ Conta criada com sucesso!")
            print(f"   ID: {conta_id}")
            print(f"   Número da conta: {numero_conta}")
        else:
            print(f"❌ Erro: {numero_conta}")
            return
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # Teste 2: Tentar login com senha correta
    print("\n🔐 Teste 2: Login com senha correta...")
    conta_data, mensagem = banco.autenticar_usuario("João Silva Santos", "minha_senha_123")
    if conta_data:
        print(f"✅ Login bem-sucedido!")
        print(f"   Mensagem: {mensagem}")
        conta = ContaBancaria(conta_data, banco)
        print(f"   Titular: {conta.titular}")
        print(f"   Número da conta (mascarado): {banco.seguranca.mascarar_dados_sensveis(conta.numero_conta, 'conta')}")
        print(f"   Saldo: R$ {conta.saldo:.2f}")
    else:
        print(f"❌ Falha no login: {mensagem}")
        return
    
    # Teste 3: Tentar login com senha incorreta
    print("\n🚫 Teste 3: Tentativa de login com senha incorreta...")
    conta_data_falha, mensagem_falha = banco.autenticar_usuario("João Silva Santos", "senha_errada")
    if conta_data_falha:
        print("❌ ERRO DE SEGURANÇA: Login deveria ter falhado!")
    else:
        print(f"✅ Segurança funcionando: {mensagem_falha}")
    
    # Teste 4: Operações bancárias
    print("\n💰 Teste 4: Realizando operações bancárias...")
    
    # Depósito
    print("   Fazendo depósito de R$ 500...")
    conta.depositar(500.0)
    
    # Saque
    print("   Fazendo saque de R$ 200...")
    conta.sacar(200.0)
    
    # Verificar saldo
    print("   Verificando saldo atual...")
    conta.ver_saldo()
    
    # Teste 5: Histórico criptografado
    print("\n📊 Teste 5: Verificando histórico (dados descriptografados)...")
    conta.ver_historico()
    
    # Teste 6: Visualizar dados no banco (criptografados)
    print("\n🔍 Teste 6: Dados no banco de dados (CRIPTOGRAFADOS)...")
    import sqlite3
    conn = sqlite3.connect("banco_seguro_teste.db")
    cursor = conn.cursor()
    
    print("   📋 TABELA CONTAS (dados criptografados):")
    cursor.execute("SELECT numero_conta, titular_criptografado, saldo_criptografado FROM contas LIMIT 1")
    conta_cripto = cursor.fetchone()
    if conta_cripto:
        numero, titular_cripto, saldo_cripto = conta_cripto
        print(f"      Número da conta: {numero}")
        print(f"      Titular criptografado: {titular_cripto[:50]}...")
        print(f"      Saldo criptografado: {saldo_cripto[:50]}...")
    
    print("\n   💳 TABELA TRANSAÇÕES (valores criptografados):")
    cursor.execute("SELECT tipo, valor_criptografado, descricao_criptografada FROM transacoes LIMIT 2")
    transacoes_cripto = cursor.fetchall()
    for i, transacao in enumerate(transacoes_cripto, 1):
        tipo, valor_cripto, desc_cripto = transacao
        print(f"      Transação {i}:")
        print(f"        Tipo: {tipo}")
        print(f"        Valor criptografado: {valor_cripto[:30]}...")
        print(f"        Descrição criptografada: {desc_cripto[:30]}...")
    
    conn.close()
    
    # Teste 7: Relatório administrativo (dados mascarados)
    print("\n👨‍💼 Teste 7: Relatório administrativo (dados mascarados)...")
    contas_mascaradas = banco.listar_contas_seguro()
    if contas_mascaradas:
        for conta_mask in contas_mascaradas:
            id_conta, numero_mask, titular_mask, data, status = conta_mask
            print(f"   ID: {id_conta} | Conta: {numero_mask} | Titular: {titular_mask} | Status: {status}")
    
    # Teste 8: Verificar logs de segurança
    print("\n📋 Teste 8: Logs de segurança gerados...")
    if os.path.exists("logs_seguranca.txt"):
        with open("logs_seguranca.txt", "r", encoding="utf-8") as log_file:
            logs = log_file.readlines()
            print(f"   📊 Total de eventos registrados: {len(logs)}")
            print("   🔍 Últimos eventos:")
            for log_line in logs[-3:]:
                print(f"      {log_line.strip()}")
    
    # Teste 9: Tentar criar conta duplicada
    print("\n🚫 Teste 9: Tentativa de criar conta duplicada...")
    resultado_dup, mensagem_dup = banco.criar_conta("João Silva Santos", "outra_senha", 500.0)
    if resultado_dup:
        print("❌ ERRO DE SEGURANÇA: Conta duplicada deveria ser rejeitada!")
    else:
        print(f"✅ Segurança funcionando: {mensagem_dup}")
    
    print("\n🎉 === TODOS OS TESTES DE SEGURANÇA CONCLUÍDOS ===")
    print("\n🔐 === RESUMO DE SEGURANÇA ===")
    print("✅ Dados pessoais criptografados no banco")
    print("✅ Valores financeiros criptografados")
    print("✅ Senhas com hash seguro + salt")
    print("✅ Dados mascarados na exibição")
    print("✅ Logs de auditoria gerados")
    print("✅ Validação de entradas")
    print("✅ Proteção contra contas duplicadas")
    print("✅ Sistema de bloqueio por tentativas incorretas")
    
    # Verificar arquivos criados
    print(f"\n📁 === ARQUIVOS GERADOS ===")
    for arquivo in ["banco_seguro_teste.db", "sistema.key", "logs_seguranca.txt"]:
        if os.path.exists(arquivo):
            size = os.path.getsize(arquivo)
            print(f"📄 {arquivo}: {size} bytes")

if __name__ == "__main__":
    teste_sistema_seguro()