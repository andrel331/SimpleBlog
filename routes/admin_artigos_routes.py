# ------------------------------------------------------------
# routes/admin_artigos_routes.py
# ------------------------------------------------------------
from typing import Optional

from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette import status

# Imports auxiliares com fallback claro (evita crash na importação)
try:
    from util.auth_utils import verificar_sessao_admin # pyright: ignore[reportMissingImports]
except Exception:  # pragma: no cover
    # Fallback: dependency que levanta 401 (use apenas em dev)
    def verificar_sessao_admin():
        raise HTTPException(status_code=401, detail="Dependência verificar_sessao_admin não disponível")

try:
    # Espera-se que `util.templates` exponha `templates` (Jinja2Templates)
    from util.templates import templates # pyright: ignore[reportMissingImports]
except Exception:  # pragma: no cover
    # Fallback: cria um objeto Jinja2Templates mínimo para evitar crash
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")

try:
    from repo import artigo_repo
except Exception:  # pragma: no cover
    # Fallback: repositório mínimo em memória (só para dev rápido)
    class _DummyRepo:
        _data = []
        _next = 1

        def listar_todos(self):
            return list(self._data)

        def inserir(self, titulo, conteudo, categoria_id):
            item = {
                "id": self._next,
                "titulo": titulo,
                "conteudo": conteudo,
                "categoria_id": categoria_id,
            }
            self._data.append(item)
            self._next += 1
            return item

        def obter_por_id(self, id):
            for a in self._data:
                if a["id"] == id:
                    return a
            return None

        def atualizar(self, id, titulo, conteudo, categoria_id):
            art = self.obter_por_id(id)
            if not art:
                raise ValueError("Artigo não encontrado")
            art.update({"titulo": titulo, "conteudo": conteudo, "categoria_id": categoria_id})
            return art

        def excluir(self, id):
            art = self.obter_por_id(id)
            if not art:
                raise ValueError("Artigo não encontrado")
            self._data.remove(art)
            return True

    artigo_repo = _DummyRepo()

# Logger (fallback silencioso caso o util não exista)
try:
    from util.logger_config import logger
except Exception:  # pragma: no cover
    import logging
    logger = logging.getLogger("admin_artigos_routes")
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/admin/artigos", tags=["Admin - Artigos"])

# ------------------------------------------------------------
# LISTAR ARTIGOS
# ------------------------------------------------------------
@router.get("/listar", response_class=HTMLResponse)
async def listar_artigos(request: Request, usuario=Depends(verificar_sessao_admin)):
    """Exibe a lista de artigos cadastrados."""
    try:
        artigos = artigo_repo.listar_todos()
        return templates.TemplateResponse(
            "admin/artigos_listar.html",
            {"request": request, "artigos": artigos}
        )
    except Exception as e:
        logger.error(f"Erro ao listar artigos: {e}", exc_info=True)
        return templates.TemplateResponse(
            "erro.html",
            {"request": request, "mensagem": "Erro ao carregar artigos."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# ------------------------------------------------------------
# CADASTRAR ARTIGO
# ------------------------------------------------------------
@router.get("/cadastrar", response_class=HTMLResponse)
async def form_cadastrar_artigo(request: Request, usuario=Depends(verificar_sessao_admin)):
    """Exibe o formulário de novo artigo."""
    return templates.TemplateResponse(
        "admin/artigos_form.html",
        {"request": request, "acao": "cadastrar", "titulo_pagina": "Novo Artigo"}
    )

@router.post("/cadastrar")
async def cadastrar_artigo(
    request: Request,
    titulo: str = Form(...),
    conteudo: str = Form(...),
    categoria_id: int = Form(...),
    usuario=Depends(verificar_sessao_admin)
):
    """Processa o cadastro de um novo artigo."""
    try:
        artigo_repo.inserir(titulo=titulo, conteudo=conteudo, categoria_id=categoria_id)
        logger.info(f"Artigo '{titulo}' cadastrado com sucesso.")
        return RedirectResponse(
            "/admin/artigos/listar",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except Exception as e:
        logger.error(f"Erro ao cadastrar artigo: {e}", exc_info=True)
        return templates.TemplateResponse(
            "admin/artigos_form.html",
            {"request": request, "erro": "Erro ao cadastrar o artigo.", "titulo": titulo, "conteudo": conteudo},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

# ------------------------------------------------------------
# EDITAR ARTIGO
# ------------------------------------------------------------
@router.get("/editar/{id}", response_class=HTMLResponse)
async def form_editar_artigo(request: Request, id: int, usuario=Depends(verificar_sessao_admin)):
    """Exibe o formulário para edição de um artigo."""
    try:
        artigo = artigo_repo.obter_por_id(id)
        if not artigo:
            # Redireciona para a listagem se não encontrar
            return RedirectResponse(
                "/admin/artigos/listar",
                status_code=status.HTTP_303_SEE_OTHER
            )
        return templates.TemplateResponse(
            "admin/artigos_form.html",
            {"request": request, "artigo": artigo, "acao": "editar", "titulo_pagina": "Editar Artigo"}
        )
    except Exception as e:
        logger.error(f"Erro ao carregar artigo: {e}", exc_info=True)
        return templates.TemplateResponse(
            "erro.html",
            {"request": request, "mensagem": "Erro ao carregar o artigo."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.post("/editar/{id}")
async def editar_artigo(
    request: Request,
    id: int,
    titulo: str = Form(...),
    conteudo: str = Form(...),
    categoria_id: int = Form(...),
    usuario=Depends(verificar_sessao_admin)
):
    """Atualiza os dados de um artigo existente."""
    try:
        artigo_repo.atualizar(id, titulo=titulo, conteudo=conteudo, categoria_id=categoria_id)
        logger.info(f"Artigo {id} atualizado com sucesso.")
        return RedirectResponse(
            "/admin/artigos/listar",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except Exception as e:
        logger.error(f"Erro ao atualizar artigo: {e}", exc_info=True)
        # Reexibe o formulário com mensagem de erro e dados preenchidos
        artigo = {"id": id, "titulo": titulo, "conteudo": conteudo, "categoria_id": categoria_id}
        return templates.TemplateResponse(
            "admin/artigos_form.html",
            {"request": request, "erro": "Erro ao atualizar o artigo.", "artigo": artigo, "acao": "editar"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

# ------------------------------------------------------------
# EXCLUIR ARTIGO
# ------------------------------------------------------------
@router.post("/excluir/{id}")
async def excluir_artigo(id: int, usuario=Depends(verificar_sessao_admin)):
    """Exclui um artigo existente."""
    try:
        artigo_repo.excluir(id)
        logger.info(f"Artigo {id} excluído com sucesso.")
        return RedirectResponse(
            "/admin/artigos/listar",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except Exception as e:
        logger.error(f"Erro ao excluir artigo: {e}", exc_info=True)
        # Mesmo em erro, redireciona para a listagem (poderia exibir mensagem)
        return RedirectResponse(
            "/admin/artigos/listar",
            status_code=status.HTTP_303_SEE_OTHER,
        )
