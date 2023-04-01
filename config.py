from flask_mysqldb import MySQL


mysql = MySQL()

# Configurações da aplicação
DEBUG = True

# Configurações do banco de dados
DATABASE = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'db': 'exemplo_flask_mysql'
}

# Configurar a aplicação para usar o MySQL
def init_app(app):
    app.config['MYSQL_HOST'] = DATABASE['host']
    app.config['MYSQL_USER'] = DATABASE['user']
    app.config['MYSQL_PASSWORD'] = DATABASE['password']
    app.config['MYSQL_DB'] = DATABASE['db']
    mysql.init_app(app)


from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)

