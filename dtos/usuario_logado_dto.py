from dataclasses import dataclass


@dataclass
class UsuarioLogado:
    id: int
    nome: str
    email: str
    perfil: str
