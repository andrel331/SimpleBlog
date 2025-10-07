from dataclasses import dataclass
from enum import Enum

class TipoUsuario(Enum):
    ADMIN = "ADMIN"
    AUTOR = "AUTOR"

@dataclass
class Usuario:
    id: int
    nome: str
    cpf: str
    data_nascimento: str
    email: str
    telefone: str
    senha: str
    perfil: TipoUsuario