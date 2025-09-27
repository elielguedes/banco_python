#!/usr/bin/env python3
"""
Teste simples para identificar erro na criação de conta
"""

from banco_db import BancoDados

def teste_criar_conta():
    """Testa a criação de conta"""
    banco = BancoDados()
    
    print("🏦 === TESTE DE CRIAÇÃO DE CONTA ===")
    
    # Dados de teste
    nome = "João da Silva"
    senha = "123456"
    deposito = 1000.0
    
    print(f"📝 Criando conta para: {nome}")
    print(f"💰 Depósito inicial: R$ {deposito:.2f}")
    
    try:
        # Tentar criar conta
        conta_id, resultado = banco.criar_conta(nome, senha, deposito)
        
        if conta_id:
            print(f"✅ Conta criada com sucesso!")
            print(f"🆔 ID: {conta_id}")
            print(f"📋 Número: {resultado}")
            
            # Testar login
            print(f"\n🔐 Testando login...")
            conta_data, mensagem = banco.autenticar_usuario(nome, senha)
            
            if conta_data:
                print(f"✅ Login bem-sucedido!")
                print(f"📊 Dados da conta: {conta_data}")
                
                # Testar criação de objeto ContaBancaria
                from main import ContaBancaria
                print(f"\n🏗️ Testando criação de objeto ContaBancaria...")
                conta_obj = ContaBancaria(conta_data, banco)
                print(f"✅ Objeto criado com sucesso!")
                print(f"👤 Titular: {conta_obj.titular}")
                print(f"💰 Saldo: R$ {conta_obj.saldo:.2f}")
                
            else:
                print(f"❌ Erro no login: {mensagem}")
        else:
            print(f"❌ Erro ao criar conta: {resultado}")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    teste_criar_conta()