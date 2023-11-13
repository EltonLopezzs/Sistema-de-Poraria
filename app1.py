import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Coindexigurações do banco de dados
DATABASE = 'portaria.db'

app.secret_key = 'sua_chave_secreta'


def criar_tabela_usuarios():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT
                        )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela de usuários: {str(e)}")


def verificar_credenciais(username, password):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Ocorreu um erro ao verificar as credenciais do usuário: {str(e)}")
        return False


def criar_tabela_alcool():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS alcool (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            data TEXT,
                            horario TEXT,
                            nome_motorista TEXT,
                            cpf TEXT,
                            placa TEXT,
                            nota_fiscal TEXT,
                            itens TEXT,
                            fornecedor TEXT,
                            destino TEXT,
                            horario_entrada TEXT,
                            horario_saida TEXT,
                            porteiro TEXT,
                            entrada_saida TEXT,
                            natureza_operacao TEXT
                        )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela de alcool: {str(e)}")


def obter_alcool(data=None):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        if data:
            cursor.execute("SELECT * FROM alcool WHERE data = ?", (data,))
        else:
            cursor.execute("SELECT * FROM alcool")

        alcool = cursor.fetchall()
        conn.close()
        return alcool
    except Exception as e:
        print(f"Ocorreu um erro ao obter os alcool: {str(e)}")
        return None


def adicionar_alcool(data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                       horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO alcool (data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino, horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                        horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar o alcool: {str(e)}")
        return False


def atualizar_alcool(alcool_id, data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                      horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''UPDATE alcool SET data=?, horario=?, nome_motorista=?, cpf=?, placa=?, nota_fiscal=?, itens=?, fornecedor=?, destino=?, horario_entrada=?, horario_saida=?, porteiro=?, entrada_saida=?, natureza_operacao=?
                          WHERE id=?''',
                       (data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                        horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao, alcool_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o alcool: {str(e)}")
        return False


def excluir_alcool(alcool_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alcool WHERE id=?", (alcool_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ocorreu um erro ao excluir o alcool: {str(e)}")
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verificar_credenciais(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Usuário ou senha incorretos.'
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.form['filtro_data']
        alcool = obter_alcool(data)
        return render_template('index.html', alcool=alcool)
    else:
        alcool = obter_alcool()
        return render_template('index.html', alcool=alcool)


@app.route('/adicionar', methods=['POST'])
def adicionar():
    data = request.form['data']
    horario = request.form['horario']
    nome_motorista = request.form['nome_motorista']
    cpf = request.form['cpf']
    placa = request.form['placa']
    nota_fiscal = request.form['nota_fiscal']
    itens = request.form['itens']
    fornecedor = request.form['fornecedor']
    destino = request.form['destino']
    horario_entrada = request.form['horario_entrada']
    horario_saida = request.form['horario_saida']
    porteiro = request.form['porteiro']
    entrada_saida = request.form['entrada_saida']
    natureza_operacao = request.form['natureza_operacao']

    if adicionar_alcool(data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                          horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
        return redirect(url_for('index'))
    else:
        return 'Ocorreu um erro ao adicionar o alcool.'


@app.route('/editar2/<int:alcool_id>', methods=['GET', 'POST'])
def editar2(alcool_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.form['data']
        horario = request.form['horario']
        nome_motorista = request.form['nome_motorista']
        cpf = request.form['cpf']
        placa = request.form['placa']
        nota_fiscal = request.form['nota_fiscal']
        itens = request.form['itens']
        fornecedor = request.form['fornecedor']
        destino = request.form['destino']
        horario_entrada = request.form['horario_entrada']
        horario_saida = request.form['horario_saida']
        porteiro = request.form['porteiro']
        entrada_saida = request.form['entrada_saida']
        natureza_operacao = request.form['natureza_operacao']

        if atualizar_alcool(alcool_id, data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                              horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
            return redirect(url_for('index'))
        else:
            return 'Ocorreu um erro ao atualizar o alcool.'
    else:
        alcool = obter_alcool()[alcool_id - 1]
        return render_template('editar2.html', registro=alcool)


@app.route('/excluir/<int:alcool_id>')
def excluir(alcool_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if excluir_alcool(alcool_id):
        return redirect(url_for('index'))
    else:
        return 'Ocorreu um erro ao excluir o alcool.'
    

if __name__ == '__main__':
    criar_tabela_usuarios()
    criar_tabela_alcool()

    app.run(debug=True, host='192.168.1.67', port=5001)