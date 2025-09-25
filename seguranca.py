import hashlib
import secrets
import os
from cryptography.fernet import Fernet
import base64

class Seguranca:
    """Classe responsável pela segurança do sistema bancário"""
    
    def __init__(self):
        self.chave_arquivo = "sistema.key"
        self.garantir_chave_existe()
    
    def garantir_chave_existe(self):
        """Garante que existe uma chave de criptografia"""
        if not os.path.exists(self.chave_arquivo):
            self.gerar_chave_criptografia()
    
    def gerar_chave_criptografia(self):
        """Gera uma nova chave de criptografia"""
        chave = Fernet.generate_key()
        with open(self.chave_arquivo, 'wb') as arquivo:
            arquivo.write(chave)
        return chave
    
    def obter_chave_criptografia(self):
        """Obtém a chave de criptografia existente"""
        try:
            with open(self.chave_arquivo, 'rb') as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            return self.gerar_chave_criptografia()
    
    def criptografar_dados(self, dados):
        """Criptografa dados sensíveis"""
        if dados is None:
            return None
        
        chave = self.obter_chave_criptografia()
        fernet = Fernet(chave)
        dados_bytes = str(dados).encode('utf-8')
        dados_criptografados = fernet.encrypt(dados_bytes)
        return base64.b64encode(dados_criptografados).decode('utf-8')
    
    def descriptografar_dados(self, dados_criptografados):
        """Descriptografa dados sensíveis"""
        if dados_criptografados is None:
            return None
        
        try:
            chave = self.obter_chave_criptografia()
            fernet = Fernet(chave)
            dados_base64 = base64.b64decode(dados_criptografados.encode('utf-8'))
            dados_descriptografados = fernet.decrypt(dados_base64)
            return dados_descriptografados.decode('utf-8')
        except Exception:
            return dados_criptografados  # Retorna original se falhar
    
    def gerar_salt(self):
        """Gera um salt aleatório para hash de senha"""
        return secrets.token_hex(32)
    
    def hash_senha(self, senha, salt=None):
        """Cria hash seguro da senha com salt"""
        if salt is None:
            salt = self.gerar_salt()
        
        # Combina senha + salt e faz hash com SHA-256
        senha_salt = f"{senha}{salt}".encode('utf-8')
        hash_obj = hashlib.sha256()
        hash_obj.update(senha_salt)
        hash_senha = hash_obj.hexdigest()
        
        return hash_senha, salt
    
    def verificar_senha(self, senha, hash_armazenado, salt_armazenado):
        """Verifica se a senha está correta"""
        hash_tentativa, _ = self.hash_senha(senha, salt_armazenado)
        return hash_tentativa == hash_armazenado
    
    def mascarar_dados_sensveis(self, dados, tipo="padrao"):
        """Mascara dados sensíveis para exibição"""
        if not dados:
            return dados
        
        if tipo == "cpf":
            # CPF: 123.***.***-**
            if len(dados) >= 11:
                return f"{dados[:3]}.***.**{dados[-2:]}"
        elif tipo == "conta":
            # Número da conta: ****-**12
            if len(dados) >= 4:
                return f"****-**{dados[-2:]}"
        elif tipo == "nome":
            # Nome: João S****
            partes = dados.split()
            if len(partes) > 1:
                return f"{partes[0]} {partes[1][0]}****"
            else:
                return f"{dados[:2]}****"
        else:
            # Padrão: mostra só os primeiros 2 e últimos 2 caracteres
            if len(dados) > 4:
                return f"{dados[:2]}***{dados[-2:]}"
        
        return dados
    
    def validar_entrada_segura(self, entrada, tipo="texto"):
        """Valida e sanitiza entradas do usuário"""
        if not entrada:
            return False, "Entrada não pode estar vazia"
        
        # Remove caracteres perigosos
        caracteres_perigosos = ['<', '>', '"', "'", '&', ';', '--', '/*', '*/', 'DROP', 'DELETE', 'UPDATE']
        entrada_upper = entrada.upper()
        
        for char in caracteres_perigosos:
            if char in entrada_upper:
                return False, f"Caractere/comando não permitido: {char}"
        
        if tipo == "nome":
            # Nome: apenas letras, espaços e acentos
            if not all(c.isalpha() or c.isspace() or c in 'áàâãéêíóôõúçñü' for c in entrada.lower()):
                return False, "Nome deve conter apenas letras"
            if len(entrada) > 100:
                return False, "Nome muito longo"
        
        elif tipo == "valor":
            # Valor: apenas números e ponto decimal
            try:
                valor = float(entrada)
                if valor < 0:
                    return False, "Valor não pode ser negativo"
                if valor > 1000000:  # Limite de 1 milhão
                    return False, "Valor muito alto"
            except ValueError:
                return False, "Valor deve ser numérico"
        
        return True, entrada.strip()
    
    def gerar_numero_conta_seguro(self):
        """Gera um número de conta único e seguro"""
        # Gera 8 dígitos aleatórios
        numero = secrets.randbelow(99999999)
        return f"{numero:08d}"
    
    def log_acesso(self, titular, acao, sucesso=True):
        """Registra tentativas de acesso para auditoria"""
        try:
            with open("logs_seguranca.txt", "a", encoding="utf-8") as log:
                from datetime import datetime
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                status = "SUCESSO" if sucesso else "FALHA"
                titular_mascarado = self.mascarar_dados_sensveis(titular, "nome")
                log.write(f"[{timestamp}] {status} - {titular_mascarado} - {acao}\n")
        except Exception:
            pass  # Não interrompe o sistema se log falhar