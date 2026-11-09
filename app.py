import os
import sqlite3
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave-local-apenas-para-desenvolvimento')
DB_PATH = Path(os.environ.get('DATABASE_PATH', str(Path(__file__).parent / 'clientes.db')))


def conexao():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def iniciar_banco():
    with conexao() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            criado_em TEXT DEFAULT CURRENT_TIMESTAMP
        )''')


def validar_cliente(nome, email, telefone):
    if not nome.strip() or not email.strip() or not telefone.strip():
        return 'Preencha todos os campos.'
    if len(nome.strip()) > 100 or len(email.strip()) > 150 or len(telefone.strip()) > 30:
        return 'Um dos campos ultrapassou o tamanho permitido.'
    if '@' not in email or '.' not in email.split('@')[-1] or email.count('@') != 1:
        return 'Digite um e-mail válido.'
    return None


@app.get('/')
def inicio():
    with conexao() as db:
        total = db.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
        recentes = db.execute('SELECT * FROM clientes ORDER BY id DESC LIMIT 5').fetchall()
    return render_template('index.html', total=total, recentes=recentes)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        erro = validar_cliente(nome, email, telefone)
        if erro:
            flash(erro, 'erro')
            return render_template('cadastro.html', cliente={'nome': nome, 'email': email, 'telefone': telefone}), 400
        with conexao() as db:
            db.execute('INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)', (nome, email, telefone))
        flash('Cliente cadastrado com sucesso!', 'sucesso')
        return redirect(url_for('consulta'))
    return render_template('cadastro.html', cliente={})


@app.get('/clientes')
def consulta():
    busca = request.args.get('busca', '').strip()
    with conexao() as db:
        if busca:
            clientes = db.execute('SELECT * FROM clientes WHERE nome LIKE ? OR email LIKE ? ORDER BY id DESC', (f'%{busca}%', f'%{busca}%')).fetchall()
        else:
            clientes = db.execute('SELECT * FROM clientes ORDER BY id DESC').fetchall()
    return render_template('consulta.html', clientes=clientes, busca=busca)


@app.route('/clientes/<int:cliente_id>/editar', methods=['GET', 'POST'])
def editar(cliente_id):
    with conexao() as db:
        cliente = db.execute('SELECT * FROM clientes WHERE id=?', (cliente_id,)).fetchone()
    if cliente is None:
        flash('Cliente não encontrado.', 'erro')
        return redirect(url_for('consulta'))
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        erro = validar_cliente(nome, email, telefone)
        if erro:
            flash(erro, 'erro')
            return render_template('editar.html', cliente={'id': cliente_id, 'nome': nome, 'email': email, 'telefone': telefone}), 400
        with conexao() as db:
            db.execute('UPDATE clientes SET nome=?, email=?, telefone=? WHERE id=?', (nome, email, telefone, cliente_id))
        flash('Cliente atualizado com sucesso!', 'sucesso')
        return redirect(url_for('consulta'))
    return render_template('editar.html', cliente=cliente)


@app.post('/clientes/<int:cliente_id>/excluir')
def excluir(cliente_id):
    with conexao() as db:
        db.execute('DELETE FROM clientes WHERE id=?', (cliente_id,))
    flash('Cliente excluído com sucesso!', 'sucesso')
    return redirect(url_for('consulta'))


@app.get('/health')
def health():
    return {'status': 'ok'}


iniciar_banco()

if __name__ == '__main__':
    app.run(debug=True)
