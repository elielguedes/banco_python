# 🤝 Guia de Contribuição

Obrigado por considerar contribuir para o **Sistema Bancário Digital Ultra-Seguro**! 

Este documento fornece diretrizes e informações sobre como contribuir efetivamente para o projeto.

## 📋 Sumário

- [🚀 Como Começar](#-como-começar)
- [🔄 Processo de Contribuição](#-processo-de-contribuição)
- [📝 Padrões de Código](#-padrões-de-código)
- [🧪 Testes](#-testes)
- [📖 Documentação](#-documentação)
- [🐛 Reportando Bugs](#-reportando-bugs)
- [💡 Sugerindo Melhorias](#-sugerindo-melhorias)
- [🛡️ Segurança](#️-segurança)
- [❓ Dúvidas](#-dúvidas)

## 🚀 Como Começar

### Pré-requisitos
- **Python 3.12+**
- **Git**
- **Conhecimento básico** de Python e Flask
- **Ambiente virtual** (recomendado)

### Setup do Ambiente
```bash
# 1. Fork do repositório
git clone https://github.com/SEU_USUARIO/banco_python.git
cd banco_python

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar testes
python teste_banco.py
python teste_seguranca.py

# 5. Testar interfaces
python gui_banco_corrigida.py  # GUI
python api_banco.py           # API
```

## 🔄 Processo de Contribuição

### 1. **Preparação**
```bash
# Criar branch para sua contribuição
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/nome-do-bug
# ou
git checkout -b docs/melhoria-documentacao
```

### 2. **Desenvolvimento**
- 🔍 **Analise** o código existente
- 📝 **Escreva** código limpo e documentado
- ✅ **Adicione** testes para novas funcionalidades
- 🧪 **Execute** todos os testes
- 📖 **Atualize** a documentação se necessário

### 3. **Commit**
```bash
# Use Conventional Commits
git add .
git commit -m "feat: adicionar autenticação 2FA"
# ou
git commit -m "fix: corrigir bug no saque"
# ou
git commit -m "docs: atualizar README com novos endpoints"
```

### 4. **Pull Request**
- 📤 **Push** sua branch
- 🔄 **Abra** um Pull Request
- 📝 **Descreva** as mudanças claramente
- 🔗 **Referencie** issues relacionadas
- ⏳ **Aguarde** a revisão

## 📝 Padrões de Código

### **Python Style Guide**
Seguimos a [PEP 8](https://pep8.org/) com algumas adaptações:

```python
# ✅ Bom
def criar_conta(nome: str, senha: str, saldo_inicial: float = 0.0) -> bool:
    """
    Cria uma nova conta bancária.
    
    Args:
        nome: Nome completo do titular
        senha: Senha segura (mínimo 6 caracteres)
        saldo_inicial: Depósito inicial (padrão: 0.0)
        
    Returns:
        bool: True se conta criada com sucesso
        
    Raises:
        ValueError: Se dados inválidos
    """
    if len(senha) < 6:
        raise ValueError("Senha deve ter pelo menos 6 caracteres")
    
    # Implementação...
    return True

# ❌ Ruim
def criar_conta(n,s,si=0):
    if len(s)<6:
        return False
    # sem documentação...
```

### **Estrutura de Arquivos**
```python
# Imports organizados
import os
import sys
from datetime import datetime

# Third-party
import flask
from cryptography.fernet import Fernet

# Local
from banco_db import BancoDados
from seguranca import CriptografiaSegura
```

### **Nomenclatura**
- **Variáveis/Funções**: `snake_case`
- **Classes**: `PascalCase`
- **Constantes**: `UPPER_CASE`
- **Arquivos**: `snake_case.py`

```python
# ✅ Bom
class ContaBancaria:
    TAXA_SAQUE = 0.02
    
    def __init__(self, titular: str):
        self.titular = titular
        self.saldo_atual = 0.0
        
    def fazer_deposito(self, valor: float) -> bool:
        # Implementação...

# ❌ Ruim
class contaBancaria:
    taxaSaque = 0.02
    
    def __init__(self, Titular):
        self.Titular = Titular
        self.SaldoAtual = 0.0
```

## 🧪 Testes

### **Estrutura de Testes**
```python
import unittest
from main import ContaBancaria
from banco_db import BancoDados

class TestContaBancaria(unittest.TestCase):
    def setUp(self):
        """Configuração antes de cada teste."""
        self.banco = BancoDados()
        self.conta = ContaBancaria("João Silva")
    
    def tearDown(self):
        """Limpeza após cada teste."""
        # Limpar dados de teste
    
    def test_criar_conta_sucesso(self):
        """Testa criação de conta com dados válidos."""
        resultado = self.banco.criar_conta("Maria Silva", "senha123", 1000.0)
        self.assertTrue(resultado)
        
    def test_criar_conta_senha_fraca(self):
        """Testa criação de conta com senha fraca."""
        with self.assertRaises(ValueError):
            self.banco.criar_conta("João", "123", 0.0)
```

### **Executar Testes**
```bash
# Todos os testes
python -m unittest discover

# Teste específico
python teste_banco.py
python teste_seguranca.py

# Com coverage
pip install coverage
coverage run -m unittest discover
coverage report -m
```

### **Novos Testes Obrigatórios**
Para **novas funcionalidades**, adicione:
- ✅ **Teste de sucesso** (caminho feliz)
- ✅ **Teste de erro** (entrada inválida)
- ✅ **Teste de segurança** (se aplicável)
- ✅ **Teste de performance** (operações críticas)

## 📖 Documentação

### **Docstrings**
Use [Google Style](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings):

```python
def calcular_juros(principal: float, taxa: float, tempo: int) -> float:
    """
    Calcula juros compostos.
    
    Args:
        principal: Valor principal do investimento
        taxa: Taxa de juros (decimal, ex: 0.05 para 5%)
        tempo: Período em anos
        
    Returns:
        Valor final com juros compostos
        
    Example:
        >>> calcular_juros(1000.0, 0.05, 2)
        1102.5
        
    Note:
        Usa a fórmula: P(1 + r)^t
    """
    return principal * ((1 + taxa) ** tempo)
```

### **README Updates**
Se sua contribuição afeta o uso do sistema:
- 📝 Atualize seções relevantes do `README.md`
- ➕ Adicione exemplos de uso
- 🔄 Atualize comandos de instalação/execução

## 🐛 Reportando Bugs

### **Template de Bug Report**
```markdown
## 🐛 Descrição do Bug
Breve descrição do que está acontecendo.

## 🔄 Passos para Reproduzir
1. Acesse '...'
2. Clique em '...'
3. Digite '...'
4. Veja o erro

## ✅ Comportamento Esperado
O que deveria acontecer.

## ❌ Comportamento Atual
O que está acontecendo.

## 🖥️ Ambiente
- **SO**: Windows 10 / Ubuntu 20.04 / macOS Big Sur
- **Python**: 3.12.0
- **Dependências**: lista das versões relevantes

## 📋 Logs/Screenshots
Cole logs de erro ou screenshots se aplicável.

## 🔄 Informações Adicionais
Qualquer contexto adicional sobre o problema.
```

### **Checklist antes de reportar**
- [ ] ✅ Procurei por issues similares
- [ ] 🔄 Tentei reproduzir o bug
- [ ] 📝 Incluí todas as informações necessárias
- [ ] 🏷️ Adicionei labels apropriadas

## 💡 Sugerindo Melhorias

### **Template de Feature Request**
```markdown
## 🌟 Feature Request

### 📋 Resumo
Breve descrição da funcionalidade desejada.

### 💡 Motivação
Por que esta funcionalidade seria útil?

### 🎯 Solução Proposta
Como você imagina que isso funcionaria?

### 🔄 Alternativas Consideradas
Outras abordagens que você considerou?

### 📊 Impacto
- **Usuários afetados**: Todos / Administradores / Desenvolvedores
- **Complexidade**: Baixa / Média / Alta
- **Prioridade**: Baixa / Média / Alta / Crítica
```

## 🛡️ Segurança

### **Princípios de Segurança**
1. 🔐 **Nunca** commite chaves, senhas ou tokens
2. 🔒 **Sempre** valide entrada do usuário
3. 🎭 **Use** mascaramento para dados sensíveis
4. 📋 **Registre** operações sensíveis em logs
5. 🔑 **Implemente** autenticação robusta

### **Checklist de Segurança**
Antes de submeter código com aspectos de segurança:

- [ ] 🔐 **Dados sensíveis** criptografados
- [ ] 🔑 **Senhas** com hash + salt
- [ ] 🛡️ **Validação** de entrada implementada
- [ ] 📋 **Auditoria** de operações críticas
- [ ] 🧪 **Testes de segurança** incluídos
- [ ] 🔍 **Review de código** para vulnerabilidades

### **Reportando Vulnerabilidades**
🔐 Para **vulnerabilidades de segurança**, **NÃO** abra issues públicas.

Envie email para: `security@elielguedes.dev`

Inclua:
- 📝 Descrição detalhada
- 🔄 Passos para reproduzir
- 💥 Impacto potencial
- 🛠️ Sugestão de correção (se tiver)

## 💬 Código de Conduta

### **Nossa Promessa**
Nos comprometemos a tornar a participação uma experiência livre de assédio para todos.

### **Comportamento Esperado**
- 🤝 **Seja respeitoso** e inclusivo
- 💬 **Comunique-se** de forma construtiva
- 🎯 **Foque** no que é melhor para a comunidade
- 🧠 **Seja** aberto a diferentes pontos de vista

### **Comportamento Inaceitável**
- ❌ Linguagem ofensiva ou discriminatória
- ❌ Ataques pessoais ou trolling
- ❌ Assédio público ou privado
- ❌ Compartilhar informações privadas sem permissão

## 🏷️ Labels e Issues

### **Labels de Tipo**
- `bug` 🐛 - Problema no código
- `enhancement` ✨ - Nova funcionalidade
- `documentation` 📖 - Melhorias na documentação
- `security` 🛡️ - Questões de segurança
- `performance` ⚡ - Otimizações
- `refactor` 🔄 - Refatoração de código

### **Labels de Prioridade**
- `priority/low` 🟢 - Baixa prioridade
- `priority/medium` 🟡 - Média prioridade
- `priority/high` 🟠 - Alta prioridade
- `priority/critical` 🔴 - Crítica

### **Labels de Status**
- `status/needs-review` 👀 - Precisa de revisão
- `status/work-in-progress` 🚧 - Em desenvolvimento
- `status/blocked` ⛔ - Bloqueado
- `status/ready` ✅ - Pronto para merge

## ❓ Dúvidas

### **Onde Buscar Ajuda**
1. 📖 **Documentação**: Leia o README e Wiki primeiro
2. 🔍 **Issues**: Procure por issues similares
3. 💬 **Discussions**: Use GitHub Discussions para perguntas gerais
4. 📧 **Email**: `dev@elielguedes.dev` para dúvidas específicas

### **Discord da Comunidade**
Junte-se ao nosso Discord: [Banco Python Community](https://discord.gg/banco-python)

Canais disponíveis:
- `#geral` - Discussões gerais
- `#desenvolvimento` - Dúvidas técnicas  
- `#bugs` - Reportar problemas
- `#features` - Sugestões de melhorias

## 🎉 Primeiras Contribuições

### **Good First Issues**
Procure por issues marcadas com `good first issue` - são ideais para começar!

### **Ideias para Contribuir**
- 📝 **Documentação**: Melhorar exemplos, corrigir typos
- 🧪 **Testes**: Adicionar casos de teste
- 🐛 **Bugs**: Corrigir problemas pequenos
- ✨ **Features**: Implementar funcionalidades simples
- 🎨 **UI/UX**: Melhorar interfaces

### **Mentorship**
Primeira vez contribuindo? Procure mentores marcados com `mentor available`!

---

## 🏆 Reconhecimento

Todos os contribuidores são reconhecidos no projeto:

- 📜 **Contributors.md**: Lista de todos os contribuidores
- 🎖️ **Releases**: Créditos nas notas de versão  
- 🌟 **README**: Seção de reconhecimentos
- 🐦 **Social**: Posts celebrando contribuições

---

## 📞 Contato

### **Mantenedor Principal**
- 👤 **Eliel Guedes**
- 📧 **Email**: eliel.guedes@dev.com
- 🐦 **Twitter**: [@elielguedes](https://twitter.com/elielguedes)
- 💼 **LinkedIn**: [Eliel Guedes](https://linkedin.com/in/elielguedes)

### **Time de Revisão**
- 🔍 **Code Review**: @elielguedes
- 🛡️ **Security**: @security-team
- 📖 **Documentation**: @docs-team

---

**✨ Obrigado por contribuir para tornar este projeto ainda melhor! ✨**

Cada contribuição, por menor que seja, faz diferença. Juntos estamos construindo um sistema bancário digital de nível mundial! 🚀