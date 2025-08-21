import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

from routes.public import router as public_routes

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="SimpleBlog")
    session_secret = os.environ.get("SESSION_SECRET", "change-me-in-production")
    app.add_middleware(SessionMiddleware, secret_key=session_secret)
    if os.path.isdir("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(public_routes, tags=["Public"])

    @app.get("/health", tags=["Misc"])
    async def health() -> dict[str, str]:
        """A simple health check endpoint used for monitoring."""
        return {"status": "ok"}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)