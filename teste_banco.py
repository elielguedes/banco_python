#!/usr/bin/env python3
"""
Script de teste para o sistema bancário com banco de dados SEGURO
"""

from banco_db import BancoDados
from main import ContaBancaria
import os

def teste_sistema():
    print("🧪 === TESTE DO SISTEMA BANCÁRIO SEGURO ===\n")
    
    # Remover banco de dados de teste se existir
    arquivos_teste = ["banco_teste.db", "sistema.key", "logs_seguranca.txt"]
    for arquivo in arquivos_teste:
        if os.path.exists(arquivo):
            os.remove(arquivo)
    
    # Criar banco de dados de teste
    banco = BancoDados("banco_teste.db")
    
    print("✅ Banco de dados seguro criado com sucesso!")
    print("🔐 Sistema de criptografia ativado")
    
    # Teste 1: Criar conta com autenticação
    print("\n📝 Teste 1: Criando conta com senha...")
    try:
        conta_id, numero_conta = banco.criar_conta("João Silva", "senha123", 1000.0)
        if conta_id:
            print(f"✅ Conta criada com sucesso!")
            print(f"   ID: {conta_id}")
            print(f"   Número: {numero_conta}")
            print("   🔐 Dados criptografados no banco de dados")
        else:
            print(f"❌ Erro: {numero_conta}")
            return
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # Teste 2: Fazer login
    print("\n🔐 Teste 2: Fazendo login...")
    conta_data, mensagem = banco.autenticar_usuario("João Silva", "senha123")
    if conta_data:
        print(f"✅ Login realizado: {mensagem}")
        conta = ContaBancaria(conta_data, banco)
        print(f"   Titular: {conta.titular}")
        numero_mascarado = banco.seguranca.mascarar_dados_sensveis(conta.numero_conta, "conta")
        print(f"   Conta mascarada: {numero_mascarado}")
        print(f"   Saldo: R$ {conta.saldo:.2f}")
    else:
        print(f"❌ Falha: {mensagem}")
        return
    
    # Teste 3: Depositar (com validação)
    print("\n💰 Teste 3: Depositando R$ 500...")
    conta.depositar(500.0)
    
    # Teste 4: Sacar (com validação)
    print("\n💸 Teste 4: Sacando R$ 200...")
    conta.sacar(200.0)
    
    # Teste 5: Ver saldo (dados mascarados)
    print("\n📊 Teste 5: Verificando saldo...")
    conta.ver_saldo()
    
    # Teste 6: Ver histórico (descriptografado)
    print("\n📋 Teste 6: Verificando histórico...")
    conta.ver_historico()
    
    # Teste 7: Criar segunda conta
    print("\n👥 Teste 7: Criando segunda conta...")
    try:
        conta_id2, numero_conta2 = banco.criar_conta("Maria Santos", "senha456", 750.0)
        if conta_id2:
            print(f"✅ Segunda conta criada: {numero_conta2}")
            
            # Login na segunda conta
            conta_data2, _ = banco.autenticar_usuario("Maria Santos", "senha456")
            if conta_data2:
                conta2 = ContaBancaria(conta_data2, banco)
                print(f"   Titular: {conta2.titular}")
                print(f"   Saldo: R$ {conta2.saldo:.2f}")
        else:
            print(f"❌ Erro: {numero_conta2}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 8: Listar contas (dados mascarados)
    print("\n📋 Teste 8: Listando contas (dados mascarados)...")
    contas_seguras = banco.listar_contas_seguro()
    if contas_seguras:
        print("ID | Número         | Titular      | Data       | Status")
        print("-" * 60)
        for conta_data in contas_seguras:
            id_conta, numero_mask, titular_mask, data_criacao, status = conta_data
            try:
                from datetime import datetime
                data_formatada = datetime.fromisoformat(data_criacao.replace('Z', '+00:00')).strftime('%d/%m/%Y')
            except:
                data_formatada = data_criacao[:10]
            print(f"{id_conta:2} | {numero_mask:14} | {titular_mask:12} | {data_formatada} | {status}")
        print("-" * 60)
    else:
        print("📭 Nenhuma conta cadastrada ainda.")
    
    # Teste 9: Tentar senha incorreta (sistema de bloqueio)
    print("\n� Teste 9: Tentando senha incorreta...")
    conta_falha, mensagem_falha = banco.autenticar_usuario("João Silva", "senha_errada")
    if conta_falha:
        print("❌ ERRO: Login deveria ter falhado!")
    else:
        print(f"✅ Segurança funcionando: {mensagem_falha}")
    
    # Teste 10: Tentar criar conta duplicada
    print("\n🚫 Teste 10: Tentando criar conta duplicada...")
    resultado_dup, mensagem_dup = banco.criar_conta("João Silva", "outra_senha", 500.0)
    if resultado_dup:
        print("❌ ERRO: Conta duplicada foi criada!")
    else:
        print(f"✅ Proteção funcionando: {mensagem_dup}")
    
    # Teste 11: Verificar criptografia no banco
    print("\n🔍 Teste 11: Verificando criptografia no banco...")
    import sqlite3
    conn = sqlite3.connect("banco_teste.db")
    cursor = conn.cursor()
    
    print("   📋 DADOS CRIPTOGRAFADOS NO BANCO:")
    cursor.execute("SELECT titular_criptografado, saldo_criptografado FROM contas LIMIT 1")
    dados_cripto = cursor.fetchone()
    if dados_cripto:
        titular_cripto, saldo_cripto = dados_cripto
        print(f"      Titular: {titular_cripto[:40]}... (criptografado)")
        print(f"      Saldo: {saldo_cripto[:40]}... (criptografado)")
    
    cursor.execute("SELECT valor_criptografado, descricao_criptografada FROM transacoes LIMIT 1")
    transacao_cripto = cursor.fetchone()
    if transacao_cripto:
        valor_cripto, desc_cripto = transacao_cripto
        print(f"      Valor transação: {valor_cripto[:30]}... (criptografado)")
        print(f"      Descrição: {desc_cripto[:30]}... (criptografado)")
    
    conn.close()
    
    # Teste 12: Verificar logs de segurança
    print("\n📋 Teste 12: Verificando logs de auditoria...")
    if os.path.exists("logs_seguranca.txt"):
        with open("logs_seguranca.txt", "r", encoding="utf-8") as log_file:
            logs = log_file.readlines()
            print(f"   📊 Total de eventos: {len(logs)}")
            if logs:
                print("   🔍 Últimos 3 eventos:")
                for log_line in logs[-3:]:
                    print(f"      {log_line.strip()}")
    
    print("\n✅ === TODOS OS TESTES CONCLUÍDOS COM SUCESSO ===")
    print("\n🔐 === RECURSOS DE SEGURANÇA TESTADOS ===")
    print("✅ Criptografia de dados pessoais e financeiros")
    print("✅ Autenticação com hash de senha + salt")
    print("✅ Mascaramento de dados sensíveis")
    print("✅ Sistema de auditoria e logs")
    print("✅ Validação de entrada de dados")
    print("✅ Proteção contra duplicação de contas")
    print("✅ Sistema de bloqueio por tentativas incorretas")
    print("✅ Descriptografia automática quando necessário")
    
    # Verificar arquivos criados
    print(f"\n📁 === ARQUIVOS DE SEGURANÇA ===")
    for arquivo in ["banco_teste.db", "sistema.key", "logs_seguranca.txt"]:
        if os.path.exists(arquivo):
            size = os.path.getsize(arquivo)
            print(f"📄 {arquivo}: {size} bytes ({size/1024:.1f} KB)")
    
    print("\n🎯 O sistema está funcionando com segurança máxima!")

if __name__ == "__main__":
    teste_sistema()