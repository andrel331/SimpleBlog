CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        data_nascimento TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        telefone TEXT,
        senha TEXT NOT NULL,
        perfil TEXT NOT NULL
    )
"""

INSERIR = """
    INSERT INTO usuario
    (nome, cpf, data_nascimento, email, telefone, senha, perfil)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""

OBTER_POR_ID = """
    SELECT id, nome, cpf, data_nascimento, email, telefone, senha, perfil
    FROM usuario
    WHERE id = ?
"""

OBTER_POR_PAGINA = """
    SELECT id, nome, cpf, data_nascimento, email, telefone, senha, perfil
    FROM usuario
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

ALTERAR = """
    UPDATE usuario
    SET nome = ?, cpf = ?, data_nascimento = ?, email = ?, telefone = ?
    WHERE id = ?
"""

ALTERAR_SENHA = """
    UPDATE usuario
    SET senha = ?
    WHERE id = ?
"""

EXCLUIR = """
    DELETE FROM usuario
    WHERE id = ?
"""
