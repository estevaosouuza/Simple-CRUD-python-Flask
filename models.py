from app import app
from flask_mysqldb import MySQL

mysql = MySQL(app)

class Usuario:
    def __init__(self, id, nome, email, senha, nivel_acesso):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.nivel_acesso = nivel_acesso

    @staticmethod
    def criar(usuario):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nome, email, senha, nivel_acesso) VALUES (%s, %s, %s, %s)",
                    (usuario.nome, usuario.email, usuario.senha, usuario.nivel_acesso))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def atualizar(usuario):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET nome=%s, email=%s, senha=%s, nivel_acesso=%s WHERE id=%s",
                    (usuario.nome, usuario.email, usuario.senha, usuario.nivel_acesso, usuario.id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def remover(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def obter(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
        data = cur.fetchone()
        cur.close()

        if data is None:
            return None

        usuario = Usuario(data[0], data[1], data[2], data[3], data[4])
        return usuario

    @staticmethod
    def listar():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios")
        data = cur.fetchall()
        cur.close()

        usuarios = []
        for row in data:
            usuario = Usuario(row[0], row[1], row[2], row[3], row[4])
            usuarios.append(usuario)

        return usuarios
