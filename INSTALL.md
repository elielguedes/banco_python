# 🚀 Instalação Ultra-Rápida

## 🎯 **1 MINUTO PARA COMEÇAR**

### **Clone & Execute**
```bash
git clone https://github.com/elielguedes/banco_python.git
cd banco_python
pip install -r requirements.txt
python gui_banco_corrigida.py
```

## 🎨 **ESCOLHA SUA INTERFACE**

### **🖥️ Interface Gráfica (Recomendada)**
```bash
python gui_banco_corrigida.py
```
- ✅ **Mais fácil de usar**
- ✅ **Visual moderno**  
- ✅ **Zero configuração**

### **🌐 API + Cliente Web**
```bash
# Terminal 1: API
python api_banco.py

# Terminal 2: Cliente Web
start cliente_web.html  # Windows
open cliente_web.html   # Mac/Linux
```
- ✅ **Interface web moderna**
- ✅ **API REST completa**
- ✅ **JWT Authentication**

### **🖥️ Console Tradicional**  
```bash
python main.py
```
- ✅ **Interface clássica**
- ✅ **Zero dependências visuais**
- ✅ **Perfeita para servidores**

## 🔐 **CRIAR SUA PRIMEIRA CONTA**

### **GUI (Clique e Use)**
1. Execute `python gui_banco_corrigida.py`
2. Clique "➕ Criar Conta"
3. Preencha: Nome, Senha, Depósito
4. Clique "Criar" ✅

### **API (Programática)**
```bash
curl -X POST http://localhost:5000/api/cadastro \
  -H "Content-Type: application/json" \
  -d '{"nome": "Seu Nome", "senha": "senha123", "saldo_inicial": 1000.0}'
```

### **Console (Tradicional)**
1. Execute `python main.py`
2. Digite `2` (Criar conta)
3. Siga as instruções ✅

## 💰 **OPERAÇÕES RÁPIDAS**

| Operação | GUI | API Endpoint | Console |
|----------|-----|--------------|---------|
| **Depositar** | 📥 Botão "Depositar" | `POST /api/deposito` | Opção `3` |
| **Sacar** | 📤 Botão "Sacar" | `POST /api/saque` | Opção `4` |
| **Ver Saldo** | 💰 Atualização automática | `GET /api/saldo` | Opção `5` |
| **Histórico** | 📊 Botão "Histórico" | `GET /api/historico` | Opção `6` |

## ⚡ **TESTE RÁPIDO**

### **Conta de Demonstração**
```bash
# 1. Execute o teste
python teste_criar_conta.py

# 2. Use a conta criada
# Nome: João da Silva
# Senha: senha123
# Saldo: R$ 1000.00
```

## 🛡️ **SEGURANÇA GARANTIDA**

- 🔐 **AES-128 Encryption** para todos os dados
- 🔑 **SHA-256 + Salt** para senhas  
- 🎭 **Mascaramento automático** de dados sensíveis
- 📋 **Logs de auditoria** de todas as operações
- 🚫 **Zero vulnerabilidades** conhecidas

## 📦 **ARQUIVOS PRINCIPAIS**

```
banco_python/
├── gui_banco_corrigida.py   ← 🎨 Interface gráfica (START HERE)
├── api_banco.py             ← 🌐 API REST com docs
├── cliente_web.html         ← 💻 Cliente web moderno  
├── main.py                  ← 🖥️ Console tradicional
├── banco_db.py              ← 💾 Database criptografado
├── seguranca.py             ← 🛡️ Módulo de segurança
└── teste_*.py               ← 🧪 Testes automatizados
```

## 🆘 **AJUDA RÁPIDA**

### **Problemas Comuns**

**❌ Erro: "Módulo não encontrado"**
```bash
pip install -r requirements.txt
```

**❌ Erro: "Permissão negada"**
```bash
# Windows
python -m pip install -r requirements.txt

# Linux/Mac  
pip3 install -r requirements.txt
```

**❌ GUI não abre**
```bash
# Instale tkinter (se necessário)
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install tkinter
```

### **Links Úteis**
- 📖 **Documentação**: [README.md](README.md)
- 🐛 **Reportar Bug**: [GitHub Issues](https://github.com/elielguedes/banco_python/issues)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/elielguedes/banco_python/discussions)

## 🎉 **PRONTO!**

**Você tem um sistema bancário profissional rodando em menos de 1 minuto!** 🚀

---

**✨ Desenvolvido com ❤️ por [Eliel Guedes](https://github.com/elielguedes)**