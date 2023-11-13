import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Coindex6igurações do banco de dados
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


def criar_tabela_acucar1():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS acucar1 (
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
        print(f"Ocorreu um erro ao criar a tabela de acucar1: {str(e)}")


def obter_acucar1(data=None):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        if data:
            cursor.execute("SELECT * FROM acucar1 WHERE data = ?", (data,))
        else:
            cursor.execute("SELECT * FROM acucar1")

        acucar1 = cursor.fetchall()
        conn.close()
        return acucar1
    except Exception as e:
        print(f"Ocorreu um erro ao obter os acucar1: {str(e)}")
        return None


def adicionar_acucar1(data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                       horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO acucar1 (data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino, horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                        horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar o acucar1: {str(e)}")
        return False


def atualizar_acucar1(acucar1_id, data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                      horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''UPDATE acucar1 SET data=?, horario=?, nome_motorista=?, cpf=?, placa=?, nota_fiscal=?, itens=?, fornecedor=?, destino=?, horario_entrada=?, horario_saida=?, porteiro=?, entrada_saida=?, natureza_operacao=?
                          WHERE id=?''',
                       (data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                        horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao, acucar1_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o acucar1: {str(e)}")
        return False


def excluir_acucar1(acucar1_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM acucar1 WHERE id=?", (acucar1_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ocorreu um erro ao excluir o acucar1: {str(e)}")
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index6'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verificar_credenciais(username, password):
            session['username'] = username
            return redirect(url_for('index6'))
        else:
            return 'Usuário ou senha incorretos.'
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def index6():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.form['filtro_data']
        acucar1 = obter_acucar1(data)
        return render_template('index6.html', acucar1=acucar1)
    else:
        acucar1 = obter_acucar1()
        return render_template('index6.html', acucar1=acucar1)


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

    if adicionar_acucar1(data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                          horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
        return redirect(url_for('index6'))
    else:
        return 'Ocorreu um erro ao adicionar o acucar1.'


@app.route('/editar6/<int:acucar1_id>', methods=['GET', 'POST'])
def editar6(acucar1_id):
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

        if atualizar_acucar1(acucar1_id, data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                              horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
            return redirect(url_for('index6'))
        else:
            return 'Ocorreu um erro ao atualizar o acucar1.'
    else:
        acucar1 = obter_acucar1()[acucar1_id - 1]
        return render_template('editar6.html', registro=acucar1)


@app.route('/excluir/<int:acucar1_id>')
def excluir(acucar1_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if excluir_acucar1(acucar1_id):
        return redirect(url_for('index6'))
    else:
        return 'Ocorreu um erro ao excluir o acucar1.'
    

if __name__ == '__main__':
    criar_tabela_usuarios()
    criar_tabela_acucar1()

    app.run(debug=True, host='192.168.1.145', port=5013)
