#!/usr/bin/env python3
"""
GUI do Sistema Bancário Seguro - VERSÃO CORRIGIDA
Interface gráfica moderna usando Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from banco_db import BancoDados
from main import ContaBancaria
import datetime

class BancoGUI:
    def __init__(self):
        """Inicializa a GUI do banco"""
        self.banco = BancoDados()
        self.conta_atual = None
        self.login_window = None
        
        # Janela principal
        self.root = tk.Tk()
        self.root.title("🏦 Banco Digital Seguro")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Centralizar janela
        self.centralizar_janela(self.root, 800, 600)
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Mostrar tela de login
        self.mostrar_login()

    def centralizar_janela(self, janela, largura, altura):
        """Centraliza a janela na tela"""
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x = (screen_width - largura) // 2
        y = (screen_height - altura) // 2
        janela.geometry(f'{largura}x{altura}+{x}+{y}')

    def configurar_estilos(self):
        """Configura os estilos da interface"""
        self.style = ttk.Style()
        
        # Tema moderno
        self.style.theme_use('clam')
        
        # Estilos personalizados
        self.style.configure('Titulo.TLabel', 
                           font=('Arial', 20, 'bold'),
                           foreground='#2E86AB',
                           background='#f0f0f0')
        
        self.style.configure('Subtitulo.TLabel',
                           font=('Arial', 12),
                           foreground='#666',
                           background='#f0f0f0')
        
        self.style.configure('Saldo.TLabel',
                           font=('Arial', 24, 'bold'),
                           foreground='#2E86AB',
                           background='#e8f4fd')
        
        self.style.configure('Operacao.TButton',
                           font=('Arial', 10, 'bold'),
                           padding=10)

    def limpar_tela(self):
        """Remove todos os widgets da tela"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        """Cria a tela de login inicial"""
        self.limpar_tela()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="🏦 BANCO DIGITAL SEGURO", style='Titulo.TLabel')
        titulo.pack(pady=20)
        
        # Subtitle
        subtitulo = ttk.Label(main_frame, text="🔐 Sistema com Criptografia e Autenticação", style='Subtitulo.TLabel')
        subtitulo.pack(pady=10)
        
        # Frame de login
        login_frame = ttk.LabelFrame(main_frame, text="Login", padding="20")
        login_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Nome de usuário
        ttk.Label(login_frame, text="👤 Nome completo:").pack(anchor=tk.W, pady=(0, 5))
        self.entry_nome = ttk.Entry(login_frame, width=30, font=('Arial', 10))
        self.entry_nome.pack(fill=tk.X, pady=(0, 10))
        
        # Senha
        ttk.Label(login_frame, text="🔐 Senha:").pack(anchor=tk.W, pady=(0, 5))
        self.entry_senha = ttk.Entry(login_frame, width=30, show="*", font=('Arial', 10))
        self.entry_senha.pack(fill=tk.X, pady=(0, 15))
        
        # Botões
        botoes_frame = ttk.Frame(login_frame)
        botoes_frame.pack(fill=tk.X, pady=10)
        
        # Botão Login
        btn_login = ttk.Button(botoes_frame, text="🔑 Entrar", command=self.fazer_login, style='Operacao.TButton')
        btn_login.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Botão Criar Conta
        btn_criar = ttk.Button(botoes_frame, text="➕ Criar Conta", command=self.criar_conta, style='Operacao.TButton')
        btn_criar.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Enter para login
        self.entry_senha.bind('<Return>', lambda e: self.fazer_login())
        
        # Foco no campo nome
        self.entry_nome.focus()

    def fazer_login(self):
        """Processa o login do usuário"""
        nome = self.entry_nome.get().strip()
        senha = self.entry_senha.get()
        
        if not nome or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
            return
        
        try:
            # Autenticar usuário
            conta_data, mensagem = self.banco.autenticar_usuario(nome, senha)
            
            if conta_data:
                # Login bem-sucedido
                self.conta_atual = ContaBancaria(conta_data, self.banco)
                messagebox.showinfo("Sucesso", f"Bem-vindo, {nome}!")
                self.mostrar_dashboard()
            else:
                messagebox.showerror("Erro de Login", mensagem)
                self.entry_senha.delete(0, tk.END)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro interno: {str(e)}")

    def criar_conta(self):
        """Dialog para criar nova conta"""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Criar Nova Conta")
        dialog.geometry("400x350")
        dialog.configure(bg='#f0f0f0')
        dialog.grab_set()  # Modal
        
        # Centralizar dialog
        self.centralizar_janela(dialog, 400, 350)
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Criar Nova Conta", style='Titulo.TLabel').pack(pady=(0, 20))
        
        # Nome completo
        ttk.Label(main_frame, text="👤 Nome completo:").pack(anchor=tk.W)
        entry_nome = ttk.Entry(main_frame, width=40, font=('Arial', 10))
        entry_nome.pack(fill=tk.X, pady=(5, 10))
        
        # Senha
        ttk.Label(main_frame, text="🔐 Senha (mín. 6 caracteres):").pack(anchor=tk.W)
        entry_senha = ttk.Entry(main_frame, width=40, show="*", font=('Arial', 10))
        entry_senha.pack(fill=tk.X, pady=(5, 10))
        
        # Confirmar senha
        ttk.Label(main_frame, text="🔐 Confirmar senha:").pack(anchor=tk.W)
        entry_confirmar = ttk.Entry(main_frame, width=40, show="*", font=('Arial', 10))
        entry_confirmar.pack(fill=tk.X, pady=(5, 10))
        
        # Depósito inicial
        ttk.Label(main_frame, text="💰 Depósito inicial (opcional):").pack(anchor=tk.W)
        entry_deposito = ttk.Entry(main_frame, width=40, font=('Arial', 10))
        entry_deposito.pack(fill=tk.X, pady=(5, 15))
        entry_deposito.insert(0, "0.00")
        
        def processar_criacao():
            nome = entry_nome.get().strip()
            senha = entry_senha.get()
            confirmar = entry_confirmar.get()
            
            try:
                deposito = float(entry_deposito.get().replace(',', '.'))
            except ValueError:
                deposito = 0.0
            
            # Validações
            if not nome or not senha:
                messagebox.showerror("Erro", "Nome e senha são obrigatórios!")
                return
            
            if len(senha) < 6:
                messagebox.showerror("Erro", "Senha deve ter pelo menos 6 caracteres!")
                return
                
            if senha != confirmar:
                messagebox.showerror("Erro", "Senhas não coincidem!")
                return
            
            if deposito < 0:
                messagebox.showerror("Erro", "Depósito não pode ser negativo!")
                return
            
            try:
                # Criar conta
                conta_id, resultado = self.banco.criar_conta(nome, senha, deposito)
                
                if conta_id:
                    messagebox.showinfo("Sucesso", f"Conta criada com sucesso!\nNúmero da conta: {resultado}")
                    dialog.destroy()
                    # Pré-preencher login
                    self.entry_nome.delete(0, tk.END)
                    self.entry_nome.insert(0, nome)
                    self.entry_senha.focus()
                else:
                    messagebox.showerror("Erro", resultado)
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar conta: {str(e)}")
        
        # Botões
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(botoes_frame, text="✅ Criar Conta", command=processar_criacao).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(botoes_frame, text="❌ Cancelar", command=dialog.destroy).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Foco no primeiro campo
        entry_nome.focus()

    def mostrar_dashboard(self):
        """Mostra o dashboard principal após login"""
        if not self.conta_atual:
            messagebox.showerror("Erro", "Nenhuma conta logada!")
            return
            
        self.limpar_tela()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Informações do usuário
        numero_mascarado = self.banco.seguranca.mascarar_dados_sensveis(self.conta_atual.numero_conta, "conta")
        ttk.Label(header_frame, text=f"👤 {self.conta_atual.titular}", style='Titulo.TLabel').pack(side=tk.LEFT)
        ttk.Label(header_frame, text=f"Conta: {numero_mascarado}", font=('Arial', 10)).pack(side=tk.LEFT, padx=(20, 0))
        
        # Botão logout
        ttk.Button(header_frame, text="🚪 Sair", command=self.logout).pack(side=tk.RIGHT)
        
        # Frame do saldo
        saldo_frame = ttk.LabelFrame(main_frame, text="💰 Saldo Atual", padding="20")
        saldo_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.label_saldo = ttk.Label(saldo_frame, text=f"R$ {self.conta_atual.saldo:.2f}",
                                   style='Saldo.TLabel')
        self.label_saldo.pack()
        
        # Frame das operações
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Operações (lado esquerdo)
        ops_frame = ttk.LabelFrame(content_frame, text="🔧 Operações", padding="15")
        ops_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Botões de operação
        ttk.Button(ops_frame, text="📥 Depositar", command=self.depositar, width=20).pack(pady=5, fill=tk.X)
        ttk.Button(ops_frame, text="📤 Sacar", command=self.sacar, width=20).pack(pady=5, fill=tk.X)
        ttk.Button(ops_frame, text="🔄 Atualizar Saldo", command=self.atualizar_saldo, width=20).pack(pady=5, fill=tk.X)
        ttk.Button(ops_frame, text="📊 Ver Histórico", command=self.mostrar_historico_completo, width=20).pack(pady=5, fill=tk.X)
        ttk.Button(ops_frame, text="👨‍💼 Admin", command=self.painel_admin, width=20).pack(pady=5, fill=tk.X)
        
        # Histórico recente (lado direito)
        historico_frame = ttk.LabelFrame(content_frame, text="📋 Últimas Transações", padding="10")
        historico_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Treeview para o histórico
        colunas = ('Data', 'Tipo', 'Valor')
        self.tree_historico = ttk.Treeview(historico_frame, columns=colunas, show='headings', height=8)
        
        # Configurar colunas
        self.tree_historico.heading('Data', text='Data/Hora')
        self.tree_historico.heading('Tipo', text='Tipo')
        self.tree_historico.heading('Valor', text='Valor')
        
        self.tree_historico.column('Data', width=120)
        self.tree_historico.column('Tipo', width=80)
        self.tree_historico.column('Valor', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(historico_frame, orient=tk.VERTICAL, command=self.tree_historico.yview)
        self.tree_historico.configure(yscrollcommand=scrollbar.set)
        
        self.tree_historico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Carregar histórico inicial
        self.atualizar_historico()

    def atualizar_saldo(self):
        """Atualiza o saldo na tela"""
        if not self.conta_atual:
            return
            
        try:
            self.conta_atual.atualizar_saldo_local()
            self.label_saldo.config(text=f"R$ {self.conta_atual.saldo:.2f}")
            messagebox.showinfo("Sucesso", "Saldo atualizado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar saldo: {str(e)}")

    def depositar(self):
        """Realiza um depósito"""
        if not self.conta_atual:
            return
            
        valor = simpledialog.askfloat("💰 Depósito", "Digite o valor do depósito:",
                                     minvalue=0.01, maxvalue=1000000.0)
        if valor:
            try:
                self.conta_atual.depositar(valor)
                self.atualizar_saldo()
                self.atualizar_historico()
                messagebox.showinfo("Sucesso", f"Depósito de R$ {valor:.2f} realizado!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro no depósito: {str(e)}")

    def sacar(self):
        """Realiza um saque"""
        if not self.conta_atual:
            return
            
        valor = simpledialog.askfloat("💸 Saque", f"Digite o valor do saque (Saldo: R$ {self.conta_atual.saldo:.2f}):",
                                     minvalue=0.01, maxvalue=self.conta_atual.saldo)
        if valor:
            if valor <= self.conta_atual.saldo:
                try:
                    self.conta_atual.sacar(valor)
                    self.atualizar_saldo()
                    self.atualizar_historico()
                    messagebox.showinfo("Sucesso", f"Saque de R$ {valor:.2f} realizado!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro no saque: {str(e)}")
            else:
                messagebox.showerror("Erro", "Saldo insuficiente!")

    def atualizar_historico(self):
        """Atualiza o histórico de transações na tela"""
        if not self.conta_atual:
            return
            
        try:
            # Limpar árvore
            for item in self.tree_historico.get_children():
                self.tree_historico.delete(item)
            
            # Obter transações (últimas 10)
            transacoes = self.banco.obter_historico(self.conta_atual.conta_id)
            
            for transacao in transacoes:
                tipo, valor, data, descricao = transacao
                
                # Formatar data
                try:
                    dt = datetime.datetime.fromisoformat(data.replace('Z', '+00:00'))
                    data_formatada = dt.strftime('%d/%m %H:%M')
                except:
                    data_formatada = data[:16]
                
                # Formatar valor
                valor_float = float(valor) if valor else 0.0
                valor_formatado = f"R$ {valor_float:.2f}"
                
                # Adicionar cor baseada no tipo
                tag = "deposito" if tipo == "DEPOSITO" else "saque"
                self.tree_historico.insert('', tk.END, values=(data_formatada, tipo, valor_formatado), tags=(tag,))
            
            # Configurar cores das tags
            self.tree_historico.tag_configure("deposito", foreground="green")
            self.tree_historico.tag_configure("saque", foreground="red")
            
        except Exception as e:
            print(f"Erro ao atualizar histórico: {e}")

    def mostrar_historico_completo(self):
        """Mostra o histórico completo em uma nova janela"""
        if not self.conta_atual:
            return
            
        # Nova janela
        hist_window = tk.Toplevel(self.root)
        hist_window.title("📊 Histórico Completo")
        hist_window.geometry("600x400")
        hist_window.configure(bg='#f0f0f0')
        
        # Centralizar
        self.centralizar_janela(hist_window, 600, 400)
        
        # Frame principal
        main_frame = ttk.Frame(hist_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="📊 Histórico Completo de Transações", 
                 style='Titulo.TLabel').pack(pady=(0, 10))
        
        # Treeview
        colunas = ('Data', 'Tipo', 'Valor', 'Descrição')
        tree = ttk.Treeview(main_frame, columns=colunas, show='headings')
        
        # Configurar colunas
        tree.heading('Data', text='Data/Hora')
        tree.heading('Tipo', text='Tipo')
        tree.heading('Valor', text='Valor')
        tree.heading('Descrição', text='Descrição')
        
        tree.column('Data', width=120)
        tree.column('Tipo', width=80)
        tree.column('Valor', width=100)
        tree.column('Descrição', width=200)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        h_scroll = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Pack da árvore e scrollbars
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Carregar dados
        try:
            transacoes = self.banco.obter_historico(self.conta_atual.conta_id)
            
            for transacao in transacoes:
                tipo, valor, data, descricao = transacao
                
                # Formatar data
                try:
                    dt = datetime.datetime.fromisoformat(data.replace('Z', '+00:00'))
                    data_formatada = dt.strftime('%d/%m/%Y %H:%M')
                except:
                    data_formatada = data
                
                # Formatar valor
                valor_float = float(valor) if valor else 0.0
                valor_formatado = f"R$ {valor_float:.2f}"
                
                # Inserir
                tag = "deposito" if tipo == "DEPOSITO" else "saque"
                tree.insert('', tk.END, values=(data_formatada, tipo, valor_formatado, descricao), tags=(tag,))
            
            # Cores
            tree.tag_configure("deposito", foreground="green")
            tree.tag_configure("saque", foreground="red")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar histórico: {str(e)}")

    def painel_admin(self):
        """Painel administrativo"""
        # Nova janela
        admin_window = tk.Toplevel(self.root)
        admin_window.title("👨‍💼 Painel Administrativo")
        admin_window.geometry("700x500")
        admin_window.configure(bg='#f0f0f0')
        
        # Centralizar
        self.centralizar_janela(admin_window, 700, 500)
        
        # Frame principal
        main_frame = ttk.Frame(admin_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="👨‍💼 Painel Administrativo", 
                 style='Titulo.TLabel').pack(pady=(0, 15))
        
        # Notebook (abas)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba Contas
        tab_contas = ttk.Frame(notebook)
        notebook.add(tab_contas, text="👥 Contas")
        
        # Lista de contas
        colunas_contas = ('ID', 'Número', 'Titular', 'Criação', 'Status')
        tree_contas = ttk.Treeview(tab_contas, columns=colunas_contas, show='headings')
        
        for col in colunas_contas:
            tree_contas.heading(col, text=col)
            tree_contas.column(col, width=120)
        
        tree_contas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar para contas
        scroll_contas = ttk.Scrollbar(tab_contas, orient=tk.VERTICAL, command=tree_contas.yview)
        tree_contas.configure(yscrollcommand=scroll_contas.set)
        scroll_contas.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Aba Logs
        tab_logs = ttk.Frame(notebook)
        notebook.add(tab_logs, text="📋 Logs")
        
        # Texto dos logs
        text_logs = tk.Text(tab_logs, wrap=tk.WORD)
        text_logs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar para logs
        scroll_logs = ttk.Scrollbar(tab_logs, orient=tk.VERTICAL, command=text_logs.yview)
        text_logs.configure(yscrollcommand=scroll_logs.set)
        scroll_logs.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Carregar dados
        try:
            # Carregar contas
            contas = self.banco.listar_contas_seguro()
            for conta in contas:
                tree_contas.insert('', tk.END, values=conta)
            
            # Carregar logs
            try:
                with open('logs_seguranca.txt', 'r', encoding='utf-8') as f:
                    logs = f.read()
                    text_logs.insert('1.0', logs)
            except FileNotFoundError:
                text_logs.insert('1.0', "Nenhum log encontrado.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados admin: {str(e)}")

    def logout(self):
        """Faz logout do usuário atual"""
        self.conta_atual = None
        messagebox.showinfo("Logout", "Logout realizado com sucesso!")
        self.mostrar_login()

    def executar(self):
        """Inicia a aplicação"""
        self.root.mainloop()

def main():
    """Função principal"""
    print("🏦 === INICIANDO GUI BANCÁRIA ===")
    print("🔐 Sistema com criptografia e autenticação")
    print("🎨 Interface gráfica moderna")
    
    try:
        app = BancoGUI()
        app.executar()
    except Exception as e:
        print(f"❌ Erro ao iniciar GUI: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()