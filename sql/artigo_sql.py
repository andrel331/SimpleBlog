# Queries SQL para operações com artigos

# Cria a tabela artigo se ela não existir
CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS artigo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT UNIQUE NOT NULL,
        conteudo TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT "Rascunho",
        usuario_id INTEGER NOT NULL,
        categoria_id INTEGER NOT NULL,
        qtde_visualizacoes INTEGER NOT NULL DEFAULT 0,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao TIMESTAMP,
        data_publicacao TIMESTAMP,
        data_pausa TIMESTAMP
    )
"""

# Insere uma nova artigo
INSERIR = """
    INSERT INTO artigo (titulo, conteudo, usuario_id, categoria_id)
    VALUES (?, ?, ?, ?)
"""

# Atualiza uma artigo existente
ALTERAR = """
    UPDATE artigo
    SET titulo=?, conteudo=?, categoria_id=?, data_atualizacao=CURRENT_TIMESTAMP
    WHERE id=?
"""

# Exclui uma artigo
EXCLUIR = """
    DELETE FROM artigo WHERE id=?
"""

# Busca todas as artigos ordenadas por titulo
OBTER_TODOS = """
    SELECT id, titulo, data_publicacao
    FROM artigo
    ORDER BY titulo
"""

# Busca uma artigo por ID
OBTER_POR_ID = """
    SELECT id, titulo, conteudo, data_publicacao
    FROM artigo
    WHERE id=?
"""

OBTER_QUANTIDADE = """
    SELECT COUNT(*)
    FROM artigo
"""