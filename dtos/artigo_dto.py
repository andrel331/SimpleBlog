from pydantic import BaseModel, field_validator
from model.artigo_model import StatusArtigo
from dtos.validators import (
    validar_id_positivo,
    validar_texto_minimo_palavras,
    validar_tipo,
)


class CriarArtigoDTO(BaseModel):
    titulo: str
    conteudo: str
    status: str
    categoria_id: int

    _validar_titulo = field_validator("titulo")(validar_texto_minimo_palavras(3,256,"Título"))
    _validar_conteudo = field_validator("conteudo")(validar_texto_minimo_palavras(64,2048,"Conteúdo"))
    _validar_status = field_validator("status")(validar_tipo("Status", StatusArtigo))
    _validar_id_categoria = field_validator("categoria_id")(validar_id_positivo())


class AlterarArtigoDTO(BaseModel):
    id: int
    titulo: str
    conteudo: str
    status: str
    categoria_id: int

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_titulo = field_validator("titulo")(validar_texto_minimo_palavras(3,256,"Título"))
    _validar_conteudo = field_validator("conteudo")(validar_texto_minimo_palavras(64,2048,"Conteúdo"))
    _validar_status = field_validator("status")(validar_tipo("Status", StatusArtigo))
    _validar_id_categoria = field_validator("categoria_id")(validar_id_positivo())

