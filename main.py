# ------------------------------------------------------------
# main.py – Aplicação FastAPI
# ------------------------------------------------------------

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path

# ------------------------------------------------------------
# Configurações
# ------------------------------------------------------------
from util.config import (
    APP_NAME,
    SECRET_KEY,
    HOST,
    PORT,
    RELOAD,
    VERSION,
)

# ------------------------------------------------------------
# Logger
# ------------------------------------------------------------
from util.logger_config import logger

# ------------------------------------------------------------
# Exception Handlers
# ------------------------------------------------------------
from util.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
    form_validation_exception_handler,
)
from util.exceptions import FormValidationError

# ------------------------------------------------------------
# Repositórios
# ------------------------------------------------------------
from repo import (
    usuario_repo,
    artigo_repo,
    comentario_repo,
    configuracao_repo,
    tarefa_repo,
    chamado_repo,
    chamado_interacao_repo,
    indices_repo,
    chat_sala_repo,
    chat_participante_repo,
    chat_mensagem_repo,
)

# ------------------------------------------------------------
# Routers
# ------------------------------------------------------------
from routes.auth_routes import router as auth_router
from routes.tarefas_routes import router as tarefas_router
from routes.chamados_routes import router as chamados_router
from routes.admin_usuarios_routes import router as admin_usuarios_router
from routes.admin_configuracoes_routes import router as admin_config_router
from routes.admin_backups_routes import router as admin_backups_router
from routes.admin_chamados_routes import router as admin_chamados_router
from routes.admin_artigos_routes import router as admin_artigos_router
from routes.admin_categorias_routes import router as admin_categorias_router  # ✅ Novo import
from routes.usuario_routes import router as usuario_router
from routes.chat_routes import router as chat_router
from routes.public_routes import router as public_router
from routes.examples_routes import router as examples_router

# ------------------------------------------------------------
# Seeds
# ------------------------------------------------------------
from util.seed_data import inicializar_dados

# ------------------------------------------------------------
# Inicialização da aplicação
# ------------------------------------------------------------
app = FastAPI(title=APP_NAME, version=VERSION)

# ------------------------------------------------------------
# Middlewares
# ------------------------------------------------------------
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# CSRF Protection Middleware
from util.csrf_protection import CSRFProtectionMiddleware

app.add_middleware(CSRFProtectionMiddleware)
logger.info("CSRF Protection habilitado")

# ------------------------------------------------------------
# Exception Handlers
# ------------------------------------------------------------
app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(FormValidationError, form_validation_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, generic_exception_handler)
logger.info("Exception handlers registrados")

# ------------------------------------------------------------
# Arquivos estáticos
# ------------------------------------------------------------
static_path = Path("static")
if static_path.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("Arquivos estáticos montados em /static")
else:
    logger.warning("Diretório 'static' não encontrado – rotas estáticas não foram montadas")

# ------------------------------------------------------------
# Banco de dados – Criação de tabelas e índices
# ------------------------------------------------------------
logger.info("Criando tabelas do banco de dados...")
try:
    usuario_repo.criar_tabela()
    configuracao_repo.criar_tabela()
    tarefa_repo.criar_tabela()
    chamado_repo.criar_tabela()
    chamado_interacao_repo.criar_tabela()
    chat_sala_repo.criar_tabela()
    chat_participante_repo.criar_tabela()
    chat_mensagem_repo.criar_tabela()
    indices_repo.criar_indices()
    logger.info("Tabelas e índices verificados com sucesso")
except Exception as e:
    logger.error(f"Erro ao criar tabelas: {e}", exc_info=True)
    raise

# ------------------------------------------------------------
# Dados iniciais (seeds)
# ------------------------------------------------------------
try:
    inicializar_dados()
    logger.info("Dados iniciais carregados com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar dados seed: {e}", exc_info=True)

# ------------------------------------------------------------
# Inclusão de routers
# ------------------------------------------------------------
app.include_router(auth_router, tags=["Autenticação"])
logger.info("Router de autenticação incluído")

app.include_router(tarefas_router, tags=["Tarefas"])
logger.info("Router de tarefas incluído")

app.include_router(chamados_router, tags=["Chamados"])
logger.info("Router de chamados incluído")

app.include_router(admin_artigos_router, tags=["Admin - Artigos"])
logger.info("Router admin de artigos incluído")

app.include_router(admin_usuarios_router, tags=["Admin - Usuários"])
logger.info("Router admin de usuários incluído")

app.include_router(admin_categorias_router, tags=["Admin - Categorias"])
logger.info("Router admin de categorias incluído")

app.include_router(admin_config_router, tags=["Admin - Configurações"])
logger.info("Router admin de configurações incluído")

app.include_router(admin_backups_router, tags=["Admin - Backups"])
logger.info("Router admin de backups incluído")

app.include_router(admin_chamados_router, tags=["Admin - Chamados"])
logger.info("Router admin de chamados incluído")

app.include_router(usuario_router, tags=["Usuário"])
logger.info("Router de usuário incluído")

app.include_router(chat_router, tags=["Chat"])
logger.info("Router de chat incluído")

# Rotas públicas (devem ser incluídas por último)
app.include_router(public_router, tags=["Público"])
logger.info("Router público incluído")

# Rotas de exemplo (também por último)
app.include_router(examples_router, tags=["Exemplos"])
logger.info("Router de exemplos incluído")

# ------------------------------------------------------------
# Health Check
# ------------------------------------------------------------
@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde do servidor."""
    return {"status": "healthy"}

# ------------------------------------------------------------
# Execução
# ------------------------------------------------------------
if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info(f"Iniciando {APP_NAME} v{VERSION}")
    logger.info("=" * 60)
    logger.info(f"Servidor rodando em http://{HOST}:{PORT}")
    logger.info(f"Hot reload: {'Ativado' if RELOAD else 'Desativado'}")
    logger.info(f"Documentação API: http://{HOST}:{PORT}/docs")
    logger.info("=" * 60)

    try:
        uvicorn.run(
            "main:app",
            host=HOST,
            port=PORT,
            reload=RELOAD,
            log_level="info",
        )
    except KeyboardInterrupt:
        logger.info("Servidor encerrado pelo usuário")
    except Exception as e:
        logger.error(f"Erro ao iniciar servidor: {e}", exc_info=True)
        raise