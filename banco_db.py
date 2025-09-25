import sqlite3
from datetime import datetime
import os
from seguranca import Seguranca

class BancoDados:
    def __init__(self, nome_db="banco.db"):
        self.nome_db = nome_db
        self.seguranca = Seguranca()
        self.criar_tabelas()
    
    def conectar(self):
        """Conecta ao banco de dados SQLite"""
        return sqlite3.connect(self.nome_db)
    
    def criar_tabelas(self):
        """Cria as tabelas necessárias se não existirem"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        # Tabela de contas com segurança
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_conta TEXT UNIQUE NOT NULL,
                titular_criptografado TEXT NOT NULL,
                hash_senha TEXT NOT NULL,
                salt_senha TEXT NOT NULL,
                saldo_criptografado TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tentativas_login INTEGER DEFAULT 0,
                bloqueada BOOLEAN DEFAULT 0
            )
        ''')
        
        # Tabela de transações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conta_id INTEGER,
                tipo TEXT NOT NULL,
                valor_criptografado TEXT NOT NULL,
                data_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                descricao_criptografada TEXT,
                FOREIGN KEY (conta_id) REFERENCES contas (id)
            )
        ''')
        
        # Tabela de auditoria de acessos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_conta TEXT,
                acao TEXT NOT NULL,
                sucesso BOOLEAN NOT NULL,
                ip_tentativa TEXT,
                data_tentativa TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def criar_conta(self, titular, senha, saldo_inicial=0.0):
        """Cria uma nova conta bancária com autenticação"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            # Validar entrada
            valido, titular_limpo = self.seguranca.validar_entrada_segura(titular, "nome")
            if not valido:
                return None, titular_limpo  # Retorna erro
            
            # Verificar se conta já existe - buscar todas e descriptografar
            cursor.execute("SELECT titular_criptografado FROM contas")
            contas_existentes = cursor.fetchall()
            
            for conta_cripto in contas_existentes:
                titular_existente = self.seguranca.descriptografar_dados(conta_cripto[0])
                if titular_existente and titular_existente.lower().strip() == titular_limpo.lower().strip():
                    return None, "Conta já existe para este titular"
            
            # Gerar dados seguros
            numero_conta = self.seguranca.gerar_numero_conta_seguro()
            hash_senha, salt_senha = self.seguranca.hash_senha(senha)
            titular_criptografado = self.seguranca.criptografar_dados(titular_limpo)
            saldo_criptografado = self.seguranca.criptografar_dados(str(saldo_inicial))
            
            # Inserir conta
            cursor.execute("""
                INSERT INTO contas (numero_conta, titular_criptografado, hash_senha, salt_senha, saldo_criptografado) 
                VALUES (?, ?, ?, ?, ?)
            """, (numero_conta, titular_criptografado, hash_senha, salt_senha, saldo_criptografado))
            
            conta_id = cursor.lastrowid
            
            # Registrar transação inicial se houver saldo
            if saldo_inicial > 0:
                valor_criptografado = self.seguranca.criptografar_dados(str(saldo_inicial))
                descricao_criptografada = self.seguranca.criptografar_dados("Saldo inicial")
                cursor.execute("""
                    INSERT INTO transacoes (conta_id, tipo, valor_criptografado, descricao_criptografada) 
                    VALUES (?, ?, ?, ?)
                """, (conta_id, "DEPOSITO", valor_criptografado, descricao_criptografada))
            
            conn.commit()
            
            # Log de auditoria
            self.registrar_auditoria(numero_conta, "CRIACAO_CONTA", True)
            self.seguranca.log_acesso(titular_limpo, "CONTA_CRIADA", True)
            
            return conta_id, numero_conta
            
        except Exception as e:
            conn.rollback()
            self.seguranca.log_acesso(titular if 'titular' in locals() else "DESCONHECIDO", "ERRO_CRIACAO", False)
            return None, f"Erro ao criar conta: {str(e)}"
        finally:
            conn.close()
    
    def autenticar_usuario(self, titular, senha):
        """Autentica usuário com senha"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            # Validar entrada
            valido, titular_limpo = self.seguranca.validar_entrada_segura(titular, "nome")
            if not valido:
                self.seguranca.log_acesso(titular, "LOGIN_INVALIDO", False)
                return None, titular_limpo
            
            # Buscar todas as contas e descriptografar para comparação
            cursor.execute("""
                SELECT id, numero_conta, titular_criptografado, hash_senha, salt_senha, saldo_criptografado, tentativas_login, bloqueada 
                FROM contas
            """)
            
            todas_contas = cursor.fetchall()
            conta_encontrada = None
            
            # Procurar conta descriptografando os titulares
            for conta_data in todas_contas:
                id_conta, numero_conta, titular_criptografado, hash_senha, salt_senha, saldo_criptografado, tentativas, bloqueada = conta_data
                titular_descriptografado = self.seguranca.descriptografar_dados(titular_criptografado)
                
                if titular_descriptografado and titular_descriptografado.lower().strip() == titular_limpo.lower().strip():
                    conta_encontrada = conta_data
                    break
            
            if not conta_encontrada:
                self.seguranca.log_acesso(titular_limpo, "LOGIN_CONTA_INEXISTENTE", False)
                return None, "Conta não encontrada"
            
            id_conta, numero_conta, titular_criptografado, hash_armazenado, salt_armazenado, saldo_criptografado, tentativas, bloqueada = conta_encontrada
            
            # Verificar se conta está bloqueada
            if bloqueada or tentativas >= 5:
                self.registrar_auditoria(numero_conta, "LOGIN_CONTA_BLOQUEADA", False)
                self.seguranca.log_acesso(titular_limpo, "LOGIN_BLOQUEADO", False)
                return None, "Conta bloqueada por excesso de tentativas"
            
            # Verificar senha
            if self.seguranca.verificar_senha(senha, hash_armazenado, salt_armazenado):
                # Login bem-sucedido - resetar tentativas
                cursor.execute("UPDATE contas SET tentativas_login = 0 WHERE id = ?", (id_conta,))
                conn.commit()
                
                # Descriptografar saldo
                saldo_descriptografado = self.seguranca.descriptografar_dados(saldo_criptografado)
                saldo = float(saldo_descriptografado) if saldo_descriptografado else 0.0
                
                # Log de sucesso
                self.registrar_auditoria(numero_conta, "LOGIN_SUCESSO", True)
                self.seguranca.log_acesso(titular_limpo, "LOGIN_SUCESSO", True)
                
                return {
                    'id': id_conta,
                    'numero_conta': numero_conta,
                    'titular': titular_limpo,
                    'saldo': saldo
                }, "Login realizado com sucesso"
            else:
                # Senha incorreta - incrementar tentativas
                tentativas += 1
                bloqueada_agora = tentativas >= 5
                
                cursor.execute("""
                    UPDATE contas SET tentativas_login = ?, bloqueada = ? WHERE id = ?
                """, (tentativas, bloqueada_agora, id_conta))
                conn.commit()
                
                # Log de falha
                self.registrar_auditoria(numero_conta, "LOGIN_SENHA_INCORRETA", False)
                self.seguranca.log_acesso(titular_limpo, "LOGIN_SENHA_INCORRETA", False)
                
                if bloqueada_agora:
                    return None, "Muitas tentativas incorretas. Conta bloqueada."
                else:
                    return None, f"Senha incorreta. Restam {5-tentativas} tentativas."
        
        except Exception as e:
            self.seguranca.log_acesso(titular if 'titular' in locals() else "DESCONHECIDO", "ERRO_LOGIN", False)
            return None, f"Erro na autenticação: {str(e)}"
        finally:
            conn.close()
    
    def registrar_auditoria(self, numero_conta, acao, sucesso):
        """Registra evento de auditoria"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO auditoria (numero_conta, acao, sucesso) 
                VALUES (?, ?, ?)
            """, (numero_conta, acao, sucesso))
            conn.commit()
        except Exception:
            pass  # Não interrompe o sistema se auditoria falhar
        finally:
            conn.close()
    
    
    def atualizar_saldo(self, conta_id, novo_saldo):
        """Atualiza o saldo de uma conta de forma segura"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            saldo_criptografado = self.seguranca.criptografar_dados(str(novo_saldo))
            cursor.execute("UPDATE contas SET saldo_criptografado = ? WHERE id = ?", (saldo_criptografado, conta_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def registrar_transacao(self, conta_id, tipo, valor, descricao=""):
        """Registra uma transação no banco de forma segura"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            valor_criptografado = self.seguranca.criptografar_dados(str(valor))
            descricao_criptografada = self.seguranca.criptografar_dados(descricao)
            
            cursor.execute("""
                INSERT INTO transacoes (conta_id, tipo, valor_criptografado, descricao_criptografada) 
                VALUES (?, ?, ?, ?)
            """, (conta_id, tipo, valor_criptografado, descricao_criptografada))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def obter_historico(self, conta_id):
        """Obtém o histórico de transações descriptografado"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT tipo, valor_criptografado, data_transacao, descricao_criptografada 
                FROM transacoes 
                WHERE conta_id = ? 
                ORDER BY data_transacao DESC
            """, (conta_id,))
            
            transacoes_criptografadas = cursor.fetchall()
            transacoes_descriptografadas = []
            
            for transacao in transacoes_criptografadas:
                tipo, valor_criptografado, data_transacao, descricao_criptografada = transacao
                
                # Descriptografar dados
                valor = self.seguranca.descriptografar_dados(valor_criptografado)
                descricao = self.seguranca.descriptografar_dados(descricao_criptografada)
                
                transacoes_descriptografadas.append((tipo, valor, data_transacao, descricao))
            
            return transacoes_descriptografadas
        except Exception as e:
            return []
        finally:
            conn.close()
    
    def listar_contas_seguro(self):
        """Lista contas com dados mascarados para administradores"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id, numero_conta, titular_criptografado, data_criacao, bloqueada FROM contas ORDER BY data_criacao")
            contas_criptografadas = cursor.fetchall()
            contas_mascaradas = []
            
            for conta in contas_criptografadas:
                id_conta, numero_conta, titular_criptografado, data_criacao, bloqueada = conta
                
                # Descriptografar e mascarar dados
                titular = self.seguranca.descriptografar_dados(titular_criptografado)
                titular_mascarado = self.seguranca.mascarar_dados_sensveis(titular, "nome")
                numero_mascarado = self.seguranca.mascarar_dados_sensveis(numero_conta, "conta")
                status = "BLOQUEADA" if bloqueada else "ATIVA"
                
                contas_mascaradas.append((id_conta, numero_mascarado, titular_mascarado, data_criacao, status))
            
            return contas_mascaradas
        except Exception as e:
            return []
        finally:
            conn.close()
    
    def buscar_conta_por_id(self, conta_id):
        """Busca conta por ID para operações internas"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, numero_conta, titular_criptografado, saldo_criptografado, bloqueada 
                FROM contas WHERE id = ?
            """, (conta_id,))
            
            resultado = cursor.fetchone()
            if resultado:
                id_conta, numero_conta, titular_criptografado, saldo_criptografado, bloqueada = resultado
                
                # Descriptografar dados
                titular = self.seguranca.descriptografar_dados(titular_criptografado)
                saldo_str = self.seguranca.descriptografar_dados(saldo_criptografado)
                saldo = float(saldo_str) if saldo_str else 0.0
                
                return {
                    'id': id_conta,
                    'numero_conta': numero_conta,
                    'titular': titular,
                    'saldo': saldo,
                    'bloqueada': bool(bloqueada)
                }
            return None
        except Exception:
            return None
        finally:
            conn.close()