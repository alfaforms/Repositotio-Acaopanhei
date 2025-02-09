import sqlite3

# Variável que conecta ao banco de dados
conn = sqlite3.connect('banco_de_dados.sqlite')

# Cria um objeto cursor para usar na conexão
cur = conn.cursor()

# Declarações do banco de dados corrigidas
sql_statements = [
    """
    CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        login VARCHAR(44) NOT NULL,
        password VARCHAR(255) 
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Responsaveis(
        id_responsavel INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome_responsavel VARCHAR(100) NOT NULL,
        ddd VARCHAR(2) NOT NULL,
        celular VARCHAR(10) NOT NULL,
        id_usuario INT NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES Usuarios (id_usuario)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Pets(
        id_pet INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome_pet VARCHAR(100) NOT NULL,
        raca_pet VARCHAR(100) NOT NULL,
        sexo_pet CHAR(1) NOT NULL,
        id_responsavel INT NOT NULL,
        FOREIGN KEY (id_responsavel) REFERENCES Responsaveis (id_responsavel)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Observacoes(
        id_observacoes INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        id_pet INT NOT NULL,
        observacao VARCHAR(255),
        FOREIGN KEY (id_pet) REFERENCES Pets (id_pet)
    );
    """
]

# Executa cada declaração do banco de dados para criar as tabelas
for sql in sql_statements:
    try:
        cur.execute(sql)
    except sqlite3.OperationalError as e:
        print("Ocorreu um erro:", e)
