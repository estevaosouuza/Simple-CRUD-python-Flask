from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from config import mysql, init_app
import mysql.connector
from config import DATABASE
import hashlib

connect = mysql.connector.connect(
    host=DATABASE['host'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    database=DATABASE['db']
)


app = Flask(__name__)
app.secret_key = 'asfdwqewrawrEFF23eea'
init_app(app)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if session.get('logged') == True:
        return render_template('home.html')
    else:
        email = request.form['email']
        senha = hash_password(request.form['password'])

        conn = connect
        conn.reconnect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s",
                       (email,))
        usuario = cursor.fetchall()
        if usuario:
            if senha == usuario[0][3] and email == usuario[0][2]:
                session['logged'] = True
                session['username'] = usuario[0][1]
                session['email'] = usuario[0][2]
                session['nivel'] = usuario[0][4]

                # Fechar a conexão com o banco de dados

                cursor.execute("SELECT id, nome, email, senha, nivelAcesso FROM usuarios")
                usuarios = cursor.fetchall()


                cursor.close()
                conn.close()

                # Redirecionar para a página principal
                return render_template('home.html', usuarios=usuarios, nivel=session['nivel'], nome=session['username'], email=session['email'])
            else:
                flash('wrong password!')
                return render_template('index.html', mensagem="Usuário ou senha incorretos!")   
        else:
                flash('wrong password!')
                return render_template('index.html', mensagem="Usuário ou senha incorretos!")     
    

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('logged', False)
   session.pop('username', None)
   session.pop('email', None)
   session.pop('nivel', None)
   return render_template('index.html')


# Rota para adicionar um usuário
@app.route('/home')
def home():
    if session.get('logged') == True:
        # Conectar ao banco de dados
        conn = connect
        conn.reconnect()
        cursor = conn.cursor()

        # Obter todos os usuários
        cursor.execute("SELECT id, nome, email, senha, nivelAcesso FROM usuarios")
        usuarios = cursor.fetchall()

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Renderizar o template HTML com a lista de usuários
        return render_template('home.html', usuarios=usuarios, nivel=session['nivel'], nome=session['username'], email=session['email'])
    else:
        return render_template('index.html')

# Rota para adicionar um usuário

@app.route('/adicionar')
def adicionar():
    if session.get('logged') == True:
        return render_template('adicionar.html')
    else:
        return render_template('index.html')

@app.route('/cadastrar')
def cadastrar():
    if session.get('logged') == True:
        return render_template('home.html')
    else:
        return render_template('cadastrar.html')


@app.route('/cad/', methods=['POST'])
def cad():
    if session.get('logged') != True:
        conn = connect
        conn.reconnect()
        cursor = conn.cursor()

        if request.method == 'POST':
            # Obter os dados do formulário
            nome = request.form['nome']
            email = request.form['email']
            senha = hash_password(request.form['senha'])
            nivelAcesso = 2

            # Conectar ao banco de dados

            # Inserir o usuário na tabela de usuários
            cursor.execute("INSERT INTO usuarios (nome, email, senha, nivelAcesso) VALUES (%s, %s, %s, %s)",
                    (nome, email, senha, nivelAcesso))
            conn.commit()

            # Obter todos os usuários
        cursor.execute("SELECT id, nome, email, senha, nivelAcesso FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()   
        # Fechar a conexão com o banco de dados
    return render_template('index.html', mensagem="Usuário cadastrado")


@app.route('/add/', methods=['POST'])
def add():
    if session.get('logged') == True:
        conn = connect
        conn.reconnect()
        cursor = conn.cursor()

        if request.method == 'POST':
            # Obter os dados do formulário
            nome = request.form['nome']
            email = request.form['email']
            senha = hash_password(request.form['senha'])
            nivelAcesso = request.form['nivelAcesso']

            # Conectar ao banco de dados

            # Inserir o usuário na tabela de usuários
            cursor.execute("INSERT INTO usuarios (nome, email, senha, nivelAcesso) VALUES (%s, %s, %s, %s)",
                    (nome, email, senha, nivelAcesso))
            conn.commit()

            # Obter todos os usuários
        cursor.execute("SELECT id, nome, email, senha, nivelAcesso FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()   

        return render_template('home.html', usuarios=usuarios, nivel=session['nivel'], nome=session['username'], email=session['email'])
        # Fechar a conexão com o banco de dados
    else:
        return render_template('index.html')

    

    # Redirecionar para a página principal
    

# Rota para editar um usuário


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    if session.get('logged') == True:
        # Conectar ao banco de dados
        conn = connect
        conn.reconnect()
        cursor = conn.cursor()

        if request.method == 'POST':
            # Obter os dados do formulário
            nome = request.form['nome']
            email = request.form['email']
            senha = hash_password(request.form['senha'])
            nivelAcesso = request.form['nivelAcesso']

            # Atualizar o usuário na tabela de usuários
            cursor.execute("UPDATE usuarios SET nome = %s, email = %s, senha = %s, nivelAcesso = %s WHERE id = %s",
                        (nome, email, senha, nivelAcesso, id))
            conn.commit()
            

            # Obter todos os usuários
            cursor.execute("SELECT id, nome, email, senha, nivelAcesso FROM usuarios")
            usuarios = cursor.fetchall()
            # Fechar a conexão com o banco de dados
            cursor.close()
            conn.close()

            # Redirecionar para a página principal
            return render_template('home.html', usuarios=usuarios, nivel=session['nivel'], nome=session['username'], email=session['email'])
        else:
            # Obter o usuário pelo ID
            conn.reconnect()
            cursor.execute(
                "SELECT id, nome, email, senha, nivelAcesso FROM usuarios WHERE id = %s", (id,))
            
        usuario = cursor.fetchone()
        print(cursor.fetchone())

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Renderizar o template HTML com o formulário de edição do usuário
        return render_template('edit.html', usuario=usuario)
    else:
        return render_template('index.html')


@app.route('/delete', methods=['POST'])
def delete():
    if session.get('logged') == True:
        # Conectar ao banco de dados
        conn = connect
        conn.reconnect()
        cursor = conn.cursor()
        idUser = request.form['idUser']
        # Deletar o usuário da tabela de usuários
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (idUser,))
        conn.commit()

        # Fechar a conexão com o banco de dados
        cursor.execute("SELECT id, nome, email, senha, nivelAcesso FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()   

        return render_template('home.html', usuarios=usuarios, nivel=session['nivel'], nome=session['username'], email=session['email'])
    else:
        return render_template('index.html')
    
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)