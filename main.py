class ContaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo
        self.historico = []
    
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.append(f"Depósito: +R$ {valor:.2f}")
            print(f"Depósito realizado com sucesso! R$ {valor:.2f}")
        else:
            print("Valor de depósito inválido! Tente novamente.")
    
    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            self.historico.append(f"Saque: -R$ {valor:.2f}")
            print(f"Saque realizado com sucesso! R$ {valor:.2f}")
        else:
            print("Valor inválido ou saldo insuficiente!")
    
    def ver_saldo(self):
        print(f"Titular: {self.titular} | Saldo atual: R$ {self.saldo:.2f}")
    
    def ver_historico(self):
        if self.historico:
            print(f"\n=== Histórico de {self.titular} ===")
            for transacao in self.historico:
                print(transacao)
            print(f"Saldo atual: R$ {self.saldo:.2f}")
        else:
            print("Nenhuma transação realizada ainda.")

nome = input("Digite o nome do titular: ")
conta = ContaBancaria(nome)

while True:
    print("\n=== CAIXA ELETRÔNICO ===")
    print("1 - Depositar")
    print("2 - Sacar")
    print("3 - Ver saldo")
    print("4 - Ver histórico")
    print("5 - Sair")

    try:
        opcao = int(input("Digite o número da opção desejada: "))
        
        if opcao == 1:
            valor = float(input("Digite o valor do depósito R$ "))
            conta.depositar(valor)
        elif opcao == 2:
            valor = float(input("Digite o valor do saque R$ "))
            conta.sacar(valor)
        elif opcao == 3:
            conta.ver_saldo()
        elif opcao == 4:
            conta.ver_historico()
        elif opcao == 5:
            print("Saindo... Volte sempre!")
            break
        else:
            print("Opção inválida! Tente novamente.")
    except ValueError:
        print("Valor inválido! Digite apenas números.")
