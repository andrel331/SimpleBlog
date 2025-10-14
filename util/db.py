import sqlite3
from pathlib import Path


def obter_conexao() -> sqlite3.Connection:
    """
    Retorna uma conexão com o banco de dados SQLite.

    O banco de dados 'dados.db' será criado na raiz do projeto
    se ainda não existir.

    Returns:
        sqlite3.Connection: Conexão ativa com o banco de dados
    """
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "dados.db"

    conexao = sqlite3.connect(str(db_path))
    conexao.row_factory = sqlite3.Row

    return conexao
