import mysql.connector
from config import DATABASE

# Cria a conexão com o banco de dados
conn = mysql.connector.connect(
    host=DATABASE['host'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    database=DATABASE['db']
)

# Cria o cursor para executar comandos no banco de dados
cursor = conn.cursor()

# Cria a tabela "usuarios" no banco de dados
cursor.execute("""CREATE TABLE usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        senha VARCHAR(50) NOT NULL,
        nivelAcesso INT NOT NULL
);""")

# Insere registros na tabela "usuarios"
insert_query = """INSERT INTO `usuarios` (`id`, `nome`, `email`, `senha`, `nivelAcesso`) 
VALUES (NULL, 'Administrador', 'administrador@teste.com', '123456', '1'), 
       (NULL, 'Usuario Comum', 'user@teste.com', '123456', '2');"""
cursor.execute(insert_query)

# Salva as mudanças no banco de dados
conn.commit()

# Fecha o cursor e a conexão com o banco de dados
cursor.close()
conn.close()
