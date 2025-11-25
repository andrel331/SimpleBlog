from datetime import datetime
from typing import Optional
from model.artigo_model import Artigo, StatusArtigo
from sql.artigo_sql import *
from util.db_util import get_connection


def _row_to_artigo(row) -> Artigo:
    """
    Converte uma linha do banco de dados em objeto Artigo.

    Args:
        row: Linha do cursor SQLite (sqlite3.Row)

    Returns:
        Objeto Artigo populado
    """
    return Artigo(
        id=row["id"],
        titulo=row["titulo"],
        conteudo=row["conteudo"],
        status=row["status"],
        artigo_id=row["artigo_id"],
        categoria_id=row["categoria_id"],
        qtde_visualizacoe=row["qtde_visualizacoe"],
        data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
        data_atualizacao=row["data_atualizacao"] if "data_atualizacao" in row.keys() else None,
        data_publicacao=row["data_publicacao"] if "data_publicacao" in row.keys() else None,
        data_pausa=row["data_pausa"] if "data_pausa" in row.keys() else None,
    )


def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(artigo: Artigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            artigo.titulo,
            artigo.conteudo,
            artigo.usuario_id,
            artigo.categoria_id
        ))
        artigo_id = cursor.lastrowid

        return artigo_id

def alterar(artigo: Artigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            artigo.titulo,
            artigo.conteudo,
            artigo.categoria_id,
            artigo.id
        ))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0

def obter_por_id(id: int) -> Optional[Artigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return _row_to_artigo(row)
        return None

def obter_todos() -> list[Artigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [_row_to_artigo(row) for row in rows]

def obter_quantidade() -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

