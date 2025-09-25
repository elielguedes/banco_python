from banco_db import BancoDados
from datetime import datetime
import getpass  # Para ocultar senha na digitação

class ContaBancaria:
    def __init__(self, conta_data, banco_db):
        self.banco_db = banco_db
        self.conta_id = conta_data['id']
        self.numero_conta = conta_data['numero_conta']
        self.titular = conta_data['titular']
        self.saldo = conta_data['saldo']
    
    def atualizar_saldo_local(self):
        """Atualiza saldo local com dados do banco"""
        conta_data = self.banco_db.buscar_conta_por_id(self.conta_id)
        if conta_data:
            self.saldo = conta_data['saldo']
    
    
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.banco_db.atualizar_saldo(self.conta_id, self.saldo)
            self.banco_db.registrar_transacao(
                self.conta_id, "DEPOSITO", valor, f"Depósito de R$ {valor:.2f}"
            )
            print(f"✅ Depósito realizado com sucesso! R$ {valor:.2f}")
        else:
            print("❌ Valor de depósito inválido! Tente novamente.")
    
    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            self.banco_db.atualizar_saldo(self.conta_id, self.saldo)
            self.banco_db.registrar_transacao(
                self.conta_id, "SAQUE", valor, f"Saque de R$ {valor:.2f}"
            )
            print(f"✅ Saque realizado com sucesso! R$ {valor:.2f}")
        else:
            print("❌ Valor inválido ou saldo insuficiente!")
    
    def ver_saldo(self):
        # Atualizar saldo do banco
        self.atualizar_saldo_local()
        numero_mascarado = self.banco_db.seguranca.mascarar_dados_sensveis(self.numero_conta, "conta")
        print(f"💰 Conta: {numero_mascarado} | Titular: {self.titular} | Saldo: R$ {self.saldo:.2f}")
    
    def ver_historico(self):
        transacoes = self.banco_db.obter_historico(self.conta_id)
        
        if transacoes:
            print(f"\n📊 === Histórico de {self.titular} ===")
            print("-" * 60)
            for transacao in transacoes:
                tipo, valor, data, descricao = transacao
                try:
                    data_formatada = datetime.fromisoformat(data.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
                except:
                    data_formatada = data[:16]  # Fallback se data não estiver no formato esperado
                simbolo = "+" if tipo == "DEPOSITO" else "-"
                valor_float = float(valor) if valor else 0.0
                print(f"{data_formatada} | {tipo} | {simbolo}R$ {valor_float:.2f} | {descricao}")
            print("-" * 60)
            print(f"💰 Saldo atual: R$ {self.saldo:.2f}")
        else:
            print("📝 Nenhuma transação realizada ainda.")

def obter_senha_segura(prompt="Digite sua senha: "):
    """Obtém senha de forma segura (oculta na digitação)"""
    try:
        return getpass.getpass(prompt)
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada.")
        return None
    except Exception:
        # Fallback se getpass não funcionar
        return input(prompt + " (ATENÇÃO: senha visível) ")

def criar_nova_conta(banco):
    """Cria uma nova conta com autenticação"""
    print("\n🆕 === CRIAÇÃO DE NOVA CONTA ===")
    
    # Obter nome
    nome = input("Digite o nome completo do titular: ").strip()
    if not nome:
        print("❌ Nome não pode estar vazio!")
        return None
    
    # Obter senha
    print("⚠️  A senha deve ter pelo menos 6 caracteres")
    senha = obter_senha_segura("Crie uma senha: ")
    if not senha or len(senha) < 6:
        print("❌ Senha muito fraca! Deve ter pelo menos 6 caracteres.")
        return None
    
    # Confirmar senha
    senha_confirmacao = obter_senha_segura("Confirme a senha: ")
    if senha != senha_confirmacao:
        print("❌ Senhas não coincidem!")
        return None
    
    # Saldo inicial
    try:
        saldo_inicial = float(input("Saldo inicial (ou 0): R$ ") or "0")
        if saldo_inicial < 0:
            print("❌ Saldo inicial não pode ser negativo!")
            return None
    except ValueError:
        print("❌ Valor inválido!")
        return None
    
    # Criar conta
    resultado, mensagem = banco.criar_conta(nome, senha, saldo_inicial)
    
    if resultado:
        print(f"✅ Conta criada com sucesso!")
        print(f"📋 Número da conta: {mensagem}")
        print(f"👤 Titular: {nome}")
        print(f"💰 Saldo inicial: R$ {saldo_inicial:.2f}")
        return resultado
    else:
        print(f"❌ Erro: {mensagem}")
        return None

def fazer_login(banco):
    """Realiza login seguro"""
    print("\n🔐 === LOGIN ===")
    
    nome = input("Digite o nome do titular: ").strip()
    if not nome:
        print("❌ Nome não pode estar vazio!")
        return None
    
    senha = obter_senha_segura()
    if not senha:
        return None
    
    conta_data, mensagem = banco.autenticar_usuario(nome, senha)
    
    if conta_data:
        print(f"✅ {mensagem}")
        return ContaBancaria(conta_data, banco)
    else:
        print(f"❌ {mensagem}")
        return None

def main():
    # Inicializar banco de dados seguro
    banco = BancoDados()
    
    print("🏦 === SISTEMA BANCÁRIO SEGURO ===")
    print("🔐 Bem-vindo ao seu banco digital com criptografia!")
    print("⚠️  Todos os seus dados são protegidos e criptografados.\n")
    
    # Menu de opções iniciais
    while True:
        print("\n🔐 === ACESSO SEGURO ===")
        print("1 - Fazer login")
        print("2 - Criar nova conta")
        print("3 - Relatório administrativo")
        print("4 - Sair do sistema")
        
        try:
            opcao_inicial = int(input("Digite sua opção: "))
            
            if opcao_inicial == 1:
                # Login seguro
                conta = fazer_login(banco)
                if conta:
                    menu_operacoes(conta)
            
            elif opcao_inicial == 2:
                # Criar nova conta
                resultado = criar_nova_conta(banco)
                if resultado:
                    print("\n🎉 Agora você pode fazer login com suas credenciais!")
            
            elif opcao_inicial == 3:
                # Relatório administrativo (dados mascarados)
                print("🔐 Digite a senha de administrador:")
                senha_admin = obter_senha_segura()
                if senha_admin == "admin123":  # Senha simples para demo
                    mostrar_relatorio_administrativo(banco)
                else:
                    print("❌ Acesso negado!")
            
            elif opcao_inicial == 4:
                print("👋 Obrigado por usar nosso sistema seguro! Até logo!")
                break
            
            else:
                print("❌ Opção inválida! Tente novamente.")
                
        except ValueError:
            print("❌ Digite apenas números!")
        except KeyboardInterrupt:
            print("\n👋 Sistema encerrado. Até logo!")
            break

def mostrar_relatorio_administrativo(banco):
    """Mostra relatório com dados mascarados para administradores"""
    print("\n📊 === RELATÓRIO ADMINISTRATIVO ===")
    print("ℹ️  Dados sensíveis foram mascarados por segurança")
    
    contas = banco.listar_contas_seguro()
    if contas:
        print("\n📋 CONTAS CADASTRADAS:")
        print("-" * 70)
        print("ID | Número da Conta | Titular      | Data Criação    | Status")
        print("-" * 70)
        for conta_data in contas:
            id_conta, numero_mascarado, titular_mascarado, data_criacao, status = conta_data
            try:
                data_formatada = datetime.fromisoformat(data_criacao.replace('Z', '+00:00')).strftime('%d/%m/%Y')
            except:
                data_formatada = data_criacao[:10]
            print(f"{id_conta:2} | {numero_mascarado:15} | {titular_mascarado:12} | {data_formatada:15} | {status}")
        print("-" * 70)
        print(f"📈 Total de contas: {len(contas)}")
    else:
        print("📭 Nenhuma conta cadastrada ainda.")
    
    print("\n� Para visualizar logs de segurança, verifique o arquivo 'logs_seguranca.txt'")

def menu_operacoes(conta):
    """Menu de operações da conta com segurança"""
    while True:
        numero_mascarado = conta.banco_db.seguranca.mascarar_dados_sensveis(conta.numero_conta, "conta")
        print(f"\n💳 === CONTA {numero_mascarado} - {conta.titular.upper()} ===")
        print("1 - Depositar")
        print("2 - Sacar")
        print("3 - Ver saldo")
        print("4 - Ver histórico")
        print("5 - Logout")

        try:
            opcao = int(input("Digite o número da opção desejada: "))
            
            if opcao == 1:
                valor_str = input("Digite o valor do depósito R$ ")
                valido, valor_ou_erro = conta.banco_db.seguranca.validar_entrada_segura(valor_str, "valor")
                if valido:
                    valor = float(valor_ou_erro)
                    conta.depositar(valor)
                else:
                    print(f"❌ {valor_ou_erro}")
            
            elif opcao == 2:
                valor_str = input("Digite o valor do saque R$ ")
                valido, valor_ou_erro = conta.banco_db.seguranca.validar_entrada_segura(valor_str, "valor")
                if valido:
                    valor = float(valor_ou_erro)
                    conta.sacar(valor)
                else:
                    print(f"❌ {valor_ou_erro}")
            
            elif opcao == 3:
                conta.ver_saldo()
            
            elif opcao == 4:
                conta.ver_historico()
            
            elif opcao == 5:
                print("🔐 Logout realizado com segurança!")
                break
            
            else:
                print("❌ Opção inválida! Tente novamente.")
                
        except ValueError:
            print("❌ Valor inválido! Digite apenas números.")
        except KeyboardInterrupt:
            print("\n🔐 Sessão encerrada por segurança.")
            break

if __name__ == "__main__":
    main()

