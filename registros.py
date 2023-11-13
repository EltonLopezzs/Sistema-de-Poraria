from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
DATABASE = 'portaria.db'


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "usuario TEXT NOT NULL, senha TEXT NOT NULL)")
    conn.commit()
    conn.close()


def insert_usuario(usuario, senha):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
    conn.commit()
    conn.close()


def validar_usuario(usuario, senha):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    result = cursor.fetchone()
    conn.close()
    return result is not None


@app.route('/')
def index():
    return render_template('login2.html')


@app.route('/login2', methods=['POST'])
def login2():
    usuario = request.form['usuario']
    senha = request.form['senha']
    
    if usuario == 'admin' and senha == 'u200809gx5':
        session['admin'] = True
        return redirect('/registro')
    else:
        return redirect('/erro')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'admin' in session:
        if request.method == 'GET':
            return render_template('registro.html')
        elif request.method == 'POST':
            usuario = request.form['usuario']
            senha = request.form['senha']
            
            if not validar_usuario(usuario, senha):
                insert_usuario(usuario, senha)
                return redirect('/sucesso')
            else:
                return redirect('/erro')
    else:
        return redirect('/')


@app.route('/sucesso')
def sucesso():
    if 'admin' in session:
        return "Registro bem-sucedido!"
    else:
        return redirect('/')


@app.route('/erro')
def erro():
    if 'admin' in session:
        return "Usuário já registrado!"
    else:
        return redirect('/')


if __name__ == '__main__':
    create_database()
    app.run(debug=True, host='192.168.1.67', port=5010)
