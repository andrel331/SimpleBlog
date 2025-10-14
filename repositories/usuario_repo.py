from typing import Optional
from sqlite3 import Connection

from models.usuario import Usuario, TipoUsuario
from sql import usuario_sql
from util.db import obter_conexao


class UsuarioRepo:
    """Repositório para manipulação de usuários no banco de dados."""

    @staticmethod
    def criar_tabela():
        """
        Cria a tabela de usuários no banco de dados se ela não existir.
        """
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(usuario_sql.CRIAR_TABELA)
            conn.commit()

    @staticmethod
    def inserir(usuario: Usuario) -> Optional[int]:
        """
        Insere um novo usuário no banco de dados.

        Args:
            usuario: Objeto Usuario a ser inserido

        Returns:
            O ID do usuário inserido ou None em caso de erro
        """
        try:
            with obter_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    usuario_sql.INSERIR,
                    (
                        usuario.nome,
                        usuario.cpf,
                        usuario.data_nascimento,
                        usuario.email,
                        usuario.telefone,
                        usuario.senha,
                        usuario.perfil.value,
                    ),
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao inserir usuário: {e}")
            return None

    @staticmethod
    def obter_por_id(id: int) -> Optional[Usuario]:
        """
        Obtém um usuário pelo ID.

        Args:
            id: ID do usuário

        Returns:
            Objeto Usuario ou None se não encontrado
        """
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(usuario_sql.OBTER_POR_ID, (id,))
            row = cursor.fetchone()

            if row:
                return Usuario(
                    id=row["id"],
                    nome=row["nome"],
                    cpf=row["cpf"],
                    data_nascimento=row["data_nascimento"],
                    email=row["email"],
                    telefone=row["telefone"],
                    senha=row["senha"],
                    perfil=TipoUsuario(row["perfil"]),
                )
            return None

    @staticmethod
    def obter_por_pagina(
        tamanho_pagina: int = 10, pagina: int = 1
    ) -> list[Usuario]:
        """
        Obtém usuários paginados.

        Args:
            tamanho_pagina: Quantidade de registros por página
            pagina: Número da página (começa em 1)

        Returns:
            Lista de objetos Usuario
        """
        offset = (pagina - 1) * tamanho_pagina

        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(usuario_sql.OBTER_POR_PAGINA, (tamanho_pagina, offset))
            rows = cursor.fetchall()

            usuarios = []
            for row in rows:
                usuarios.append(
                    Usuario(
                        id=row["id"],
                        nome=row["nome"],
                        cpf=row["cpf"],
                        data_nascimento=row["data_nascimento"],
                        email=row["email"],
                        telefone=row["telefone"],
                        senha=row["senha"],
                        perfil=TipoUsuario(row["perfil"]),
                    )
                )
            return usuarios

    @staticmethod
    def alterar(usuario: Usuario) -> bool:
        """
        Altera os dados de um usuário existente (exceto senha).

        Args:
            usuario: Objeto Usuario com os dados atualizados

        Returns:
            True se alterado com sucesso, False caso contrário
        """
        try:
            with obter_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    usuario_sql.ALTERAR,
                    (
                        usuario.nome,
                        usuario.cpf,
                        usuario.data_nascimento,
                        usuario.email,
                        usuario.telefone,
                        usuario.id,
                    ),
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao alterar usuário: {e}")
            return False

    @staticmethod
    def alterar_senha(id: int, nova_senha: str) -> bool:
        """
        Altera a senha de um usuário.

        Args:
            id: ID do usuário
            nova_senha: Nova senha (deve estar hasheada)

        Returns:
            True se alterado com sucesso, False caso contrário
        """
        try:
            with obter_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(usuario_sql.ALTERAR_SENHA, (nova_senha, id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao alterar senha: {e}")
            return False

    @staticmethod
    def excluir(id: int) -> bool:
        """
        Exclui um usuário do banco de dados.

        Args:
            id: ID do usuário a ser excluído

        Returns:
            True se excluído com sucesso, False caso contrário
        """
        try:
            with obter_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(usuario_sql.EXCLUIR, (id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            return False
