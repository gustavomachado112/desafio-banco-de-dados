from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'chave_secreta_simples'

# Lista para simular banco de dados (em memória)
usuarios = []

@app.route('/')
def index():
    return render_template('index.html', usuarios=usuarios)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Obter dados do formulário
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        idade = request.form.get('idade', '').strip()
        
        # Validação simples
        if not nome or not email:
            flash('❌ Nome e Email são obrigatórios!', 'error')
            return render_template('cadastro.html')
        
        # Verificar se email já existe
        for usuario in usuarios:
            if usuario['email'] == email:
                flash('❌ Este email já está cadastrado!', 'error')
                return render_template('cadastro.html')
        
        # Criar novo usuário
        novo_usuario = {
            'id': len(usuarios) + 1,
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'idade': idade,
            'data_cadastro': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        # Adicionar à lista
        usuarios.append(novo_usuario)
        flash('✅ Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('lista'))
    
    return render_template('cadastro.html')

@app.route('/lista')
def lista():
    return render_template('lista.html', usuarios=usuarios)

@app.route('/excluir/<int:usuario_id>')
def excluir(usuario_id):
    global usuarios
    
    # Encontrar e remover usuário
    for i, usuario in enumerate(usuarios):
        if usuario['id'] == usuario_id:
            usuarios.pop(i)
            flash('✅ Usuário excluído com sucesso!', 'success')
            break
    else:
        flash('❌ Usuário não encontrado!', 'error')
    
    return redirect(url_for('lista'))

@app.route('/limpar_tudo')
def limpar_tudo():
    global usuarios
    usuarios.clear()
    flash('🗑️ Todos os cadastros foram removidos!', 'success')
    return redirect(url_for('lista'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)