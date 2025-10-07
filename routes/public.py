from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()

templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("public/index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("public/login.html", {"request": request})


@router.get("/cadastro", response_class=HTMLResponse)
async def cadastro(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("public/cadastro.html", {"request": request})


@router.get("/sobre", response_class=HTMLResponse)
async def sobre(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("public/sobre.html", {"request": request})


@router.get("/artigos", response_class=HTMLResponse)
async def artigos(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("public/artigos.html", {"request": request})


@router.get("/artigo/{id}", response_class=HTMLResponse)
async def artigo(request: Request, id: int) -> HTMLResponse:
    return templates.TemplateResponse("public/artigo.html", {"request": request})
