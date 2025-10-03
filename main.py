import os
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

from routes.public import router as public_routes

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simpleblog.main")


def create_app() -> FastAPI:
    app = FastAPI(title="SimpleBlog")

    # SESSION_SECRET: defina em .env para produção
    session_secret = os.environ.get("SESSION_SECRET") or "change-me-in-production"
    if session_secret == "change-me-in-production":
        logger.warning(
            "SESSION_SECRET está usando o valor padrão. Defina SESSION_SECRET no .env para produção."
        )
    app.add_middleware(SessionMiddleware, secret_key=session_secret)

    # Monta static se a pasta existir
    static_dir = BASE_DIR / "static"
    if static_dir.is_dir():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        logger.info(f"Mounted static directory at: {static_dir}")
    else:
        logger.info("Pasta 'static' não encontrada — pulando montagem de arquivos estáticos.")

    # Inclui as rotas públicas
    app.include_router(public_routes, tags=["Public"])

    @app.get("/health", tags=["Misc"])
    async def health() -> dict[str, str]:
        """A simple health check endpoint used for monitoring."""
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    # Executa com reload em desenvolvimento
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
