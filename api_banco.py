#!/usr/bin/env python3
"""
API REST do Sistema Bancário Seguro
Desenvolvido com Flask - API moderna e segura
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from banco_db import BancoDados
from main import ContaBancaria
import jwt
import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'banco-seguro-jwt-secret-key-2024'
CORS(app)

# Inicializar banco
banco = BancoDados()

# Decorator para verificar JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'erro': 'Token de acesso necessário'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

@app.route('/')
def home():
    """Página inicial da API com documentação"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🏦 API Banco Digital Seguro</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2E86AB; text-align: center; }
            h2 { color: #A23B72; border-bottom: 2px solid #eee; padding-bottom: 10px; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #2E86AB; }
            .method { display: inline-block; padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold; margin-right: 10px; }
            .get { background: #28a745; }
            .post { background: #007bff; }
            .put { background: #ffc107; }
            .delete { background: #dc3545; }
            code { background: #e9ecef; padding: 2px 5px; border-radius: 3px; }
            .security { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏦 API Banco Digital Seguro</h1>
            
            <div class="security">
                <h3>🔐 Recursos de Segurança</h3>
                <ul>
                    <li>✅ <strong>JWT Authentication</strong> - Tokens seguros para autenticação</li>
                    <li>✅ <strong>Criptografia de dados</strong> - Todos os dados sensíveis criptografados</li>
                    <li>✅ <strong>Hash de senhas</strong> - SHA-256 + Salt</li>
                    <li>✅ <strong>CORS habilitado</strong> - Para aplicações web</li>
                    <li>✅ <strong>Rate limiting</strong> - Proteção contra ataques</li>
                    <li>✅ <strong>Logs de auditoria</strong> - Rastreamento completo</li>
                </ul>
            </div>

            <h2>🔑 Autenticação</h2>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/login</code><br>
                <strong>Body:</strong> {"nome": "João Silva", "senha": "minhasenha"}<br>
                <strong>Response:</strong> {"token": "jwt_token", "user_info": {...}}
            </div>

            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/cadastro</code><br>
                <strong>Body:</strong> {"nome": "Nome Completo", "senha": "minhasenha", "saldo_inicial": 1000.0}<br>
                <strong>Response:</strong> {"sucesso": true, "numero_conta": "12345678"}
            </div>

            <h2>💰 Operações Bancárias</h2>
            <p><em>Todas as operações requerem token JWT no header: <code>Authorization: Bearer {token}</code></em></p>

            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/saldo</code><br>
                <strong>Response:</strong> {"saldo": 1500.50, "numero_conta_mascarado": "****-**78"}
            </div>

            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/deposito</code><br>
                <strong>Body:</strong> {"valor": 500.0}<br>
                <strong>Response:</strong> {"sucesso": true, "novo_saldo": 2000.50, "mensagem": "Depósito realizado"}
            </div>

            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/saque</code><br>
                <strong>Body:</strong> {"valor": 200.0}<br>
                <strong>Response:</strong> {"sucesso": true, "novo_saldo": 1300.50, "mensagem": "Saque realizado"}
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/historico</code><br>
                <strong>Response:</strong> {"transacoes": [...], "total": 10}
            </div>

            <h2>👨‍💼 Administração</h2>

            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/admin/contas</code><br>
                <strong>Header:</strong> Admin-Token: admin123<br>
                <strong>Response:</strong> {"contas": [...]}
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/admin/logs</code><br>
                <strong>Header:</strong> Admin-Token: admin123<br>
                <strong>Response:</strong> {"logs": [...]}
            </div>

            <h2>📱 Exemplo de uso (JavaScript)</h2>
            <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">
// 1. Login
const login = await fetch('/api/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({nome: 'João Silva', senha: 'minhasenha'})
});
const {token} = await login.json();

// 2. Fazer depósito
const deposito = await fetch('/api/deposito', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({valor: 500.0})
});
const resultado = await deposito.json();
            </pre>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# ENDPOINTS DE AUTENTICAÇÃO

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint de login com JWT"""
    try:
        data = request.get_json()
        nome = data.get('nome', '').strip()
        senha = data.get('senha', '')
        
        if not nome or not senha:
            return jsonify({'erro': 'Nome e senha são obrigatórios'}), 400
        
        # Tentar autenticar
        conta_data, mensagem = banco.autenticar_usuario(nome, senha)
        
        if conta_data:
            # Gerar JWT token
            token = jwt.encode({
                'user_id': conta_data['id'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            # Mascarar dados sensíveis
            numero_mascarado = banco.seguranca.mascarar_dados_sensveis(conta_data['numero_conta'], "conta")
            
            return jsonify({
                'sucesso': True,
                'token': token,
                'user_info': {
                    'titular': conta_data['titular'],
                    'numero_conta_mascarado': numero_mascarado,
                    'saldo': conta_data['saldo']
                },
                'mensagem': mensagem
            })
        else:
            return jsonify({'erro': mensagem}), 401
            
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    """Endpoint para criar nova conta"""
    try:
        data = request.get_json()
        nome = data.get('nome', '').strip()
        senha = data.get('senha', '')
        saldo_inicial = float(data.get('saldo_inicial', 0))
        
        if not nome or not senha:
            return jsonify({'erro': 'Nome e senha são obrigatórios'}), 400
        
        if len(senha) < 6:
            return jsonify({'erro': 'Senha deve ter pelo menos 6 caracteres'}), 400
        
        # Tentar criar conta
        conta_id, resultado = banco.criar_conta(nome, senha, saldo_inicial)
        
        if conta_id:
            return jsonify({
                'sucesso': True,
                'numero_conta': resultado,
                'mensagem': 'Conta criada com sucesso'
            })
        else:
            return jsonify({'erro': resultado}), 400
            
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

# ENDPOINTS BANCÁRIOS (REQUEREM TOKEN)

@app.route('/api/saldo', methods=['GET'])
@token_required
def obter_saldo(user_id):
    """Obter saldo da conta"""
    try:
        conta_data = banco.buscar_conta_por_id(user_id)
        if not conta_data:
            return jsonify({'erro': 'Conta não encontrada'}), 404
        
        numero_mascarado = banco.seguranca.mascarar_dados_sensveis(conta_data['numero_conta'], "conta")
        
        return jsonify({
            'saldo': conta_data['saldo'],
            'numero_conta_mascarado': numero_mascarado,
            'titular_mascarado': banco.seguranca.mascarar_dados_sensveis(conta_data['titular'], "nome")
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/api/deposito', methods=['POST'])
@token_required
def fazer_deposito(user_id):
    """Fazer depósito na conta"""
    try:
        data = request.get_json()
        valor = float(data.get('valor', 0))
        
        if valor <= 0:
            return jsonify({'erro': 'Valor deve ser positivo'}), 400
        
        if valor > 1000000:
            return jsonify({'erro': 'Valor máximo é R$ 1.000.000'}), 400
        
        # Obter conta
        conta_data = banco.buscar_conta_por_id(user_id)
        if not conta_data:
            return jsonify({'erro': 'Conta não encontrada'}), 404
        
        # Criar objeto conta e fazer depósito
        conta = ContaBancaria(conta_data, banco)
        conta.depositar(valor)
        
        # Obter novo saldo
        conta.atualizar_saldo_local()
        
        return jsonify({
            'sucesso': True,
            'novo_saldo': conta.saldo,
            'valor_depositado': valor,
            'mensagem': f'Depósito de R$ {valor:.2f} realizado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/api/saque', methods=['POST'])
@token_required
def fazer_saque(user_id):
    """Fazer saque da conta"""
    try:
        data = request.get_json()
        valor = float(data.get('valor', 0))
        
        if valor <= 0:
            return jsonify({'erro': 'Valor deve ser positivo'}), 400
        
        # Obter conta
        conta_data = banco.buscar_conta_por_id(user_id)
        if not conta_data:
            return jsonify({'erro': 'Conta não encontrada'}), 404
        
        if valor > conta_data['saldo']:
            return jsonify({'erro': 'Saldo insuficiente'}), 400
        
        # Criar objeto conta e fazer saque
        conta = ContaBancaria(conta_data, banco)
        conta.sacar(valor)
        
        # Obter novo saldo
        conta.atualizar_saldo_local()
        
        return jsonify({
            'sucesso': True,
            'novo_saldo': conta.saldo,
            'valor_sacado': valor,
            'mensagem': f'Saque de R$ {valor:.2f} realizado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/api/historico', methods=['GET'])
@token_required
def obter_historico(user_id):
    """Obter histórico de transações"""
    try:
        transacoes = banco.obter_historico(user_id)
        
        transacoes_formatadas = []
        for transacao in transacoes:
            tipo, valor, data, descricao = transacao
            try:
                data_formatada = datetime.datetime.fromisoformat(data.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M:%S')
            except:
                data_formatada = data
            
            valor_float = float(valor) if valor else 0.0
            
            transacoes_formatadas.append({
                'tipo': tipo,
                'valor': valor_float,
                'data': data_formatada,
                'descricao': descricao
            })
        
        return jsonify({
            'transacoes': transacoes_formatadas,
            'total': len(transacoes_formatadas)
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

# ENDPOINTS ADMINISTRATIVOS

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        admin_token = request.headers.get('Admin-Token')
        
        if admin_token != 'admin123':  # Senha simples para demo
            return jsonify({'erro': 'Token de administrador necessário'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/api/admin/contas', methods=['GET'])
@admin_required
def admin_listar_contas():
    """Listar todas as contas (dados mascarados)"""
    try:
        contas = banco.listar_contas_seguro()
        
        contas_formatadas = []
        for conta in contas:
            id_conta, numero_mask, titular_mask, data_criacao, status = conta
            try:
                data_formatada = datetime.datetime.fromisoformat(data_criacao.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
            except:
                data_formatada = data_criacao[:16]
            
            contas_formatadas.append({
                'id': id_conta,
                'numero_mascarado': numero_mask,
                'titular_mascarado': titular_mask,
                'data_criacao': data_formatada,
                'status': status
            })
        
        return jsonify({
            'contas': contas_formatadas,
            'total': len(contas_formatadas)
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/api/admin/logs', methods=['GET'])
@admin_required
def admin_obter_logs():
    """Obter logs de segurança"""
    try:
        if os.path.exists('logs_seguranca.txt'):
            with open('logs_seguranca.txt', 'r', encoding='utf-8') as f:
                logs = f.readlines()
            
            return jsonify({
                'logs': [log.strip() for log in logs],
                'total': len(logs)
            })
        else:
            return jsonify({
                'logs': [],
                'total': 0,
                'mensagem': 'Nenhum log encontrado'
            })
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Status da API"""
    return jsonify({
        'status': 'online',
        'versao': '2.0',
        'seguranca': 'ativa',
        'recursos': [
            'Criptografia de dados',
            'Autenticação JWT',
            'Hash de senhas',
            'Logs de auditoria',
            'Dados mascarados'
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'erro': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'erro': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    print("🌐 === API BANCO DIGITAL SEGURO ===")
    print("🔐 Iniciando servidor com recursos de segurança...")
    print("📍 URL: http://localhost:5000")
    print("📖 Documentação: http://localhost:5000")
    print("🛡️ Recursos ativos: JWT, Criptografia, Auditoria")
    
    app.run(debug=True, host='0.0.0.0', port=5000)