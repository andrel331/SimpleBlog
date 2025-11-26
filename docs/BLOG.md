# Tutorial: Criando um Blog Simples a partir do DefaultWebApp

Este tutorial guia você passo a passo na criação de um blog simplificado usando como base o repositório DefaultWebApp. Ao final, você terá um sistema de blog funcional com:

- **CRUD de Categorias** (Administrador)
- **CRUD de Artigos** (Autor)
- **Visualização de Artigos** (Leitor, Autor, Administrador)
- **Home Page com os últimos artigos**
- **Busca e filtros de artigos**

---

## Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Fork do Repositório](#2-fork-do-repositório)
3. [Clonando o Repositório](#3-clonando-o-repositório)
4. [Configurando o Ambiente](#4-configurando-o-ambiente)
5. [Estrutura do Projeto](#5-estrutura-do-projeto)
6. [Criando o Model de Artigo](#6-criando-o-model-de-artigo)
7. [Criando as Queries SQL](#7-criando-as-queries-sql)
8. [Criando o Repositório](#8-criando-o-repositório)
9. [Criando os DTOs](#9-criando-os-dtos)
10. [Criando as Rotas](#10-criando-as-rotas)
11. [Criando os Templates](#11-criando-os-templates)
12. [Integrando o Editor Markdown](#12-integrando-o-editor-markdown)
13. [Modificando a Home Page](#13-modificando-a-home-page)
14. [Atualizando o main.py](#14-atualizando-o-mainpy)
15. [Testando a Aplicação](#15-testando-a-aplicação)
16. [Conclusão](#16-conclusão)

---

## 1. Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.10+**
- **Git**
- **Conta no GitHub**
- **Editor de código** (VS Code recomendado)

---

## 2. Fork do Repositório

1. Acesse o repositório upstream: https://github.com/maroquio/DefaultWebApp
2. Clique no botão **Fork** no canto superior direito
3. Selecione sua conta como destino do fork
4. Opcionalmente, renomeie o repositório para "SimpleBlog" ou outro nome de sua preferência

---

## 3. Clonando o Repositório

Após criar o fork, clone-o para sua máquina:

```bash
# Substitua SEU_USUARIO pelo seu usuário do GitHub
git clone https://github.com/SEU_USUARIO/SimpleBlog.git
cd SimpleBlog

# Configure o upstream para receber atualizações futuras
git remote add upstream https://github.com/maroquio/DefaultWebApp.git
```

---

## 4. Configurando o Ambiente

### 4.1. Criando o ambiente virtual

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente (Linux/Mac)
source .venv/bin/activate

# Ativar o ambiente (Windows)
.venv\Scripts\activate
```

### 4.2. Instalando dependências

```bash
pip install -r requirements.txt
```

### 4.3. Configurando variáveis de ambiente

Copie o arquivo de exemplo e configure:

```bash
cp .env.example .env
```

Edite o arquivo `.env` conforme necessário.

### 4.4. Testando a instalação

```bash
python main.py
```

Acesse http://localhost:8000 para verificar se está funcionando.

---

## 5. Estrutura do Projeto

O DefaultWebApp segue a seguinte estrutura:

```
SimpleBlog/
├── dtos/               # Data Transfer Objects (validação)
├── model/              # Modelos de dados
├── repo/               # Repositórios (acesso ao banco)
├── routes/             # Rotas da aplicação
├── sql/                # Queries SQL
├── templates/          # Templates HTML (Jinja2)
├── static/             # Arquivos estáticos (CSS, JS, imagens)
├── util/               # Utilitários diversos
├── main.py             # Ponto de entrada da aplicação
└── requirements.txt    # Dependências
```

O projeto já possui um CRUD de Categorias implementado. Usaremos ele como modelo para criar o CRUD de Artigos.

---

## 6. Criando o Model de Artigo

Crie o arquivo `model/artigo_model.py`:

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class StatusArtigo(Enum):
    RASCUNHO = "Rascunho"
    FINALIZADO = "Finalizado"
    PUBLICADO = "Publicado"
    PAUSADO = "Pausado"


@dataclass
class Artigo:
    id: int
    titulo: str
    conteudo: str
    status: str
    usuario_id: int
    categoria_id: int
    resumo: Optional[str] = None
    qtde_visualizacoes: Optional[int] = 0
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    data_publicacao: Optional[datetime] = None
    data_pausa: Optional[datetime] = None
    # Campos do JOIN (para exibição)
    usuario_nome: Optional[str] = None
    usuario_email: Optional[str] = None
    categoria_nome: Optional[str] = None
```

### Explicação:

- **StatusArtigo**: Enum com os possíveis status de um artigo
- **Artigo**: Dataclass que representa um artigo no sistema
- Campos opcionais com `Optional` permitem valores `None`
- Campos de JOIN são preenchidos nas consultas com junção de tabelas

---

## 7. Criando as Queries SQL

Crie o arquivo `sql/artigo_sql.py`:

```python
# Queries SQL para operações com artigos

CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS artigo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT UNIQUE NOT NULL,
        resumo TEXT,
        conteudo TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Rascunho',
        usuario_id INTEGER NOT NULL,
        categoria_id INTEGER NOT NULL,
        qtde_visualizacoes INTEGER NOT NULL DEFAULT 0,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao TIMESTAMP,
        data_publicacao TIMESTAMP,
        data_pausa TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuario(id),
        FOREIGN KEY (categoria_id) REFERENCES categoria(id)
    )
"""

INSERIR = """
    INSERT INTO artigo (titulo, resumo, conteudo, status, usuario_id, categoria_id)
    VALUES (?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
    UPDATE artigo
    SET titulo=?, resumo=?, conteudo=?, status=?, categoria_id=?,
        data_atualizacao=CURRENT_TIMESTAMP
    WHERE id=?
"""

EXCLUIR = """
    DELETE FROM artigo WHERE id=?
"""

OBTER_TODOS = """
    SELECT a.id, a.titulo, a.resumo, a.conteudo, a.status, a.usuario_id, a.categoria_id,
           a.qtde_visualizacoes, a.data_cadastro, a.data_atualizacao,
           a.data_publicacao, a.data_pausa,
           u.nome as usuario_nome, u.email as usuario_email,
           c.nome as categoria_nome
    FROM artigo a
    LEFT JOIN usuario u ON a.usuario_id = u.id
    LEFT JOIN categoria c ON a.categoria_id = c.id
    ORDER BY a.data_cadastro DESC
"""

OBTER_POR_ID = """
    SELECT a.id, a.titulo, a.resumo, a.conteudo, a.status, a.usuario_id, a.categoria_id,
           a.qtde_visualizacoes, a.data_cadastro, a.data_atualizacao,
           a.data_publicacao, a.data_pausa,
           u.nome as usuario_nome, u.email as usuario_email,
           c.nome as categoria_nome
    FROM artigo a
    LEFT JOIN usuario u ON a.usuario_id = u.id
    LEFT JOIN categoria c ON a.categoria_id = c.id
    WHERE a.id = ?
"""

OBTER_POR_USUARIO = """
    SELECT a.id, a.titulo, a.resumo, a.conteudo, a.status, a.usuario_id, a.categoria_id,
           a.qtde_visualizacoes, a.data_cadastro, a.data_atualizacao,
           a.data_publicacao, a.data_pausa,
           u.nome as usuario_nome, u.email as usuario_email,
           c.nome as categoria_nome
    FROM artigo a
    LEFT JOIN usuario u ON a.usuario_id = u.id
    LEFT JOIN categoria c ON a.categoria_id = c.id
    WHERE a.usuario_id = ?
    ORDER BY a.data_cadastro DESC
"""

OBTER_PUBLICADOS = """
    SELECT a.id, a.titulo, a.resumo, a.conteudo, a.status, a.usuario_id, a.categoria_id,
           a.qtde_visualizacoes, a.data_cadastro, a.data_atualizacao,
           a.data_publicacao, a.data_pausa,
           u.nome as usuario_nome, u.email as usuario_email,
           c.nome as categoria_nome
    FROM artigo a
    LEFT JOIN usuario u ON a.usuario_id = u.id
    LEFT JOIN categoria c ON a.categoria_id = c.id
    WHERE a.status = 'Publicado'
    ORDER BY a.data_publicacao DESC
"""

OBTER_ULTIMOS_PUBLICADOS = """
    SELECT a.id, a.titulo, a.resumo, a.conteudo, a.status, a.usuario_id, a.categoria_id,
           a.qtde_visualizacoes, a.data_cadastro, a.data_atualizacao,
           a.data_publicacao, a.data_pausa,
           u.nome as usuario_nome, u.email as usuario_email,
           c.nome as categoria_nome
    FROM artigo a
    LEFT JOIN usuario u ON a.usuario_id = u.id
    LEFT JOIN categoria c ON a.categoria_id = c.id
    WHERE a.status = 'Publicado'
    ORDER BY a.data_publicacao DESC
    LIMIT ?
"""

BUSCAR_POR_TITULO = """
    SELECT a.id, a.titulo, a.resumo, a.conteudo, a.status, a.usuario_id, a.categoria_id,
           a.qtde_visualizacoes, a.data_cadastro, a.data_atualizacao,
           a.data_publicacao, a.data_pausa,
           u.nome as usuario_nome, u.email as usuario_email,
           c.nome as categoria_nome
    FROM artigo a
    LEFT JOIN usuario u ON a.usuario_id = u.id
    LEFT JOIN categoria c ON a.categoria_id = c.id
    WHERE a.status = 'Publicado' AND a.titulo LIKE ?
    ORDER BY a.data_publicacao DESC
"""

OBTER_POR_CATEGORIA = """
    SELECT a.id, a.titulo, a.resumo, a.conteudo, a.status, a.usuario_id, a.categoria_id,
           a.qtde_visualizacoes, a.data_cadastro, a.data_atualizacao,
           a.data_publicacao, a.data_pausa,
           u.nome as usuario_nome, u.email as usuario_email,
           c.nome as categoria_nome
    FROM artigo a
    LEFT JOIN usuario u ON a.usuario_id = u.id
    LEFT JOIN categoria c ON a.categoria_id = c.id
    WHERE a.status = 'Publicado' AND a.categoria_id = ?
    ORDER BY a.data_publicacao DESC
"""

INCREMENTAR_VISUALIZACOES = """
    UPDATE artigo SET qtde_visualizacoes = qtde_visualizacoes + 1 WHERE id = ?
"""

VERIFICAR_TITULO_EXISTE = """
    SELECT id FROM artigo WHERE titulo = ? AND id != ?
"""
```

---

## 8. Criando o Repositório

Crie o arquivo `repo/artigo_repo.py`:

```python
from typing import Optional
from model.artigo_model import Artigo
from sql.artigo_sql import *
from util.db_util import obter_conexao as get_connection


def _row_to_artigo(row) -> Artigo:
    """Converte uma linha do banco de dados em objeto Artigo."""
    return Artigo(
        id=row["id"],
        titulo=row["titulo"],
        resumo=row["resumo"] if "resumo" in row.keys() else None,
        conteudo=row["conteudo"],
        status=row["status"],
        usuario_id=row["usuario_id"],
        categoria_id=row["categoria_id"],
        qtde_visualizacoes=row["qtde_visualizacoes"] if "qtde_visualizacoes" in row.keys() else 0,
        data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
        data_atualizacao=row["data_atualizacao"] if "data_atualizacao" in row.keys() else None,
        data_publicacao=row["data_publicacao"] if "data_publicacao" in row.keys() else None,
        data_pausa=row["data_pausa"] if "data_pausa" in row.keys() else None,
        usuario_nome=row["usuario_nome"] if "usuario_nome" in row.keys() else None,
        usuario_email=row["usuario_email"] if "usuario_email" in row.keys() else None,
        categoria_nome=row["categoria_nome"] if "categoria_nome" in row.keys() else None,
    )


def criar_tabela() -> bool:
    """Cria a tabela de artigos se não existir."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela artigo: {e}")
        return False


def inserir(artigo: Artigo) -> Optional[int]:
    """Insere um novo artigo e retorna o ID gerado."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                artigo.titulo,
                artigo.resumo,
                artigo.conteudo,
                artigo.status,
                artigo.usuario_id,
                artigo.categoria_id
            ))
            return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir artigo: {e}")
        return None


def alterar(artigo: Artigo) -> bool:
    """Atualiza um artigo existente."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ALTERAR, (
                artigo.titulo,
                artigo.resumo,
                artigo.conteudo,
                artigo.status,
                artigo.categoria_id,
                artigo.id
            ))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao alterar artigo: {e}")
        return False


def excluir(id: int) -> bool:
    """Exclui um artigo pelo ID."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(EXCLUIR, (id,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir artigo: {e}")
        return False


def obter_por_id(id: int) -> Optional[Artigo]:
    """Busca um artigo pelo ID."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (id,))
            row = cursor.fetchone()
            if row:
                return _row_to_artigo(row)
            return None
    except Exception as e:
        print(f"Erro ao obter artigo por ID: {e}")
        return None


def obter_todos() -> list[Artigo]:
    """Retorna todos os artigos."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS)
            rows = cursor.fetchall()
            return [_row_to_artigo(row) for row in rows]
    except Exception as e:
        print(f"Erro ao obter todos os artigos: {e}")
        return []


def obter_por_usuario(usuario_id: int) -> list[Artigo]:
    """Retorna todos os artigos de um usuário específico."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_USUARIO, (usuario_id,))
            rows = cursor.fetchall()
            return [_row_to_artigo(row) for row in rows]
    except Exception as e:
        print(f"Erro ao obter artigos por usuário: {e}")
        return []


def obter_publicados() -> list[Artigo]:
    """Retorna todos os artigos publicados."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_PUBLICADOS)
            rows = cursor.fetchall()
            return [_row_to_artigo(row) for row in rows]
    except Exception as e:
        print(f"Erro ao obter artigos publicados: {e}")
        return []


def obter_ultimos_publicados(limite: int = 6) -> list[Artigo]:
    """Retorna os últimos N artigos publicados."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_ULTIMOS_PUBLICADOS, (limite,))
            rows = cursor.fetchall()
            return [_row_to_artigo(row) for row in rows]
    except Exception as e:
        print(f"Erro ao obter últimos artigos publicados: {e}")
        return []


def buscar_por_titulo(termo: str) -> list[Artigo]:
    """Busca artigos publicados pelo título."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(BUSCAR_POR_TITULO, (f"%{termo}%",))
            rows = cursor.fetchall()
            return [_row_to_artigo(row) for row in rows]
    except Exception as e:
        print(f"Erro ao buscar artigos por título: {e}")
        return []


def obter_por_categoria(categoria_id: int) -> list[Artigo]:
    """Retorna artigos publicados de uma categoria específica."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_CATEGORIA, (categoria_id,))
            rows = cursor.fetchall()
            return [_row_to_artigo(row) for row in rows]
    except Exception as e:
        print(f"Erro ao obter artigos por categoria: {e}")
        return []


def incrementar_visualizacoes(id: int) -> bool:
    """Incrementa o contador de visualizações de um artigo."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INCREMENTAR_VISUALIZACOES, (id,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao incrementar visualizações: {e}")
        return False


def titulo_existe(titulo: str, excluir_id: int = 0) -> bool:
    """Verifica se um título já existe (excluindo um ID específico)."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(VERIFICAR_TITULO_EXISTE, (titulo, excluir_id))
            row = cursor.fetchone()
            return row is not None
    except Exception as e:
        print(f"Erro ao verificar título: {e}")
        return False
```

---

## 9. Criando os DTOs

Crie ou atualize o arquivo `dtos/artigo_dto.py`:

```python
from pydantic import BaseModel, field_validator
from model.artigo_model import StatusArtigo
from dtos.validators import (
    validar_id_positivo,
    validar_string_obrigatoria,
    validar_comprimento,
    validar_tipo,
)


class CriarArtigoDTO(BaseModel):
    titulo: str
    resumo: str = ""
    conteudo: str
    status: str = "Rascunho"
    categoria_id: int

    _validar_titulo = field_validator("titulo")(
        validar_string_obrigatoria(
            nome_campo="Título",
            tamanho_minimo=5,
            tamanho_maximo=200
        )
    )
    _validar_resumo = field_validator("resumo")(
        validar_comprimento(tamanho_maximo=500)
    )
    _validar_conteudo = field_validator("conteudo")(
        validar_string_obrigatoria(
            nome_campo="Conteúdo",
            tamanho_minimo=50,
            tamanho_maximo=50000
        )
    )
    _validar_status = field_validator("status")(validar_tipo("Status", StatusArtigo))
    _validar_id_categoria = field_validator("categoria_id")(validar_id_positivo())


class AlterarArtigoDTO(BaseModel):
    id: int
    titulo: str
    resumo: str = ""
    conteudo: str
    status: str
    categoria_id: int

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_titulo = field_validator("titulo")(
        validar_string_obrigatoria(
            nome_campo="Título",
            tamanho_minimo=5,
            tamanho_maximo=200
        )
    )
    _validar_resumo = field_validator("resumo")(
        validar_comprimento(tamanho_maximo=500)
    )
    _validar_conteudo = field_validator("conteudo")(
        validar_string_obrigatoria(
            nome_campo="Conteúdo",
            tamanho_minimo=50,
            tamanho_maximo=50000
        )
    )
    _validar_status = field_validator("status")(validar_tipo("Status", StatusArtigo))
    _validar_id_categoria = field_validator("categoria_id")(validar_id_positivo())
```

---

## 10. Criando as Rotas

Crie o arquivo `routes/artigos_routes.py`. Este arquivo é extenso, então veja o código no repositório.

As rotas principais são:

- `GET /artigos/meus` - Lista artigos do autor logado
- `GET /artigos/cadastrar` - Formulário de cadastro
- `POST /artigos/cadastrar` - Processa cadastro
- `GET /artigos/editar/{id}` - Formulário de edição
- `POST /artigos/editar/{id}` - Processa edição
- `POST /artigos/excluir/{id}` - Exclui artigo
- `POST /artigos/publicar/{id}` - Publica artigo
- `GET /artigos` - Lista pública de artigos (com busca)
- `GET /artigos/ler/{id}` - Lê artigo completo (requer login)

### Controle de Acesso

O sistema usa decorators para controle de acesso:

```python
from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil

# Apenas autores e admins podem criar artigos
@router.get("/cadastrar")
@requer_autenticacao([Perfil.AUTOR.value, Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    ...

# Qualquer usuário autenticado pode ler
@router.get("/ler/{id}")
@requer_autenticacao()
async def ler_artigo(request: Request, id: int, usuario_logado: Optional[dict] = None):
    ...
```

---

## 11. Criando os Templates

Crie a pasta `templates/artigos/` e os seguintes arquivos:

### 11.1. listar.html

Template para listar os artigos do autor.

### 11.2. cadastrar.html

Template com formulário de cadastro e editor Markdown.

### 11.3. editar.html

Template com formulário de edição.

### 11.4. buscar.html

Template para busca pública de artigos.

### 11.5. ler.html

Template para visualização completa do artigo.

Veja os arquivos completos no repositório em `templates/artigos/`.

---

## 12. Integrando o Editor Markdown

Usamos o **EasyMDE**, um editor Markdown gratuito e popular.

### No template de cadastro/edição:

```html
{% block head %}
<!-- EasyMDE - Editor Markdown -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.css">
{% endblock %}

{% block content %}
...
<textarea name="conteudo" id="conteudo" required>{{ conteudo }}</textarea>
...
{% endblock %}

{% block scripts %}
<script src="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const easyMDE = new EasyMDE({
            element: document.getElementById('conteudo'),
            spellChecker: false,
            autosave: {
                enabled: true,
                uniqueId: 'artigo-novo',
                delay: 1000,
            },
            toolbar: [
                'bold', 'italic', 'heading', '|',
                'quote', 'unordered-list', 'ordered-list', '|',
                'link', 'image', '|',
                'preview', 'side-by-side', 'fullscreen', '|',
                'guide'
            ],
            minHeight: '300px',
        });
    });
</script>
{% endblock %}
```

### Na visualização (renderização):

```html
{% block scripts %}
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const conteudoEl = document.getElementById('conteudo-artigo');
        const conteudoOriginal = conteudoEl.textContent;
        conteudoEl.innerHTML = marked.parse(conteudoOriginal);
    });
</script>
{% endblock %}
```

---

## 13. Modificando a Home Page

### 13.1. Atualize `routes/public_routes.py`:

```python
from repo import artigo_repo, categoria_repo

@router.get("/")
async def home(request: Request):
    ultimos_artigos = artigo_repo.obter_ultimos_publicados(6)
    categorias = categoria_repo.obter_todos()
    usuario_logado = obter_usuario_logado(request)

    return templates_public.TemplateResponse(
        "index.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "ultimos_artigos": ultimos_artigos,
            "categorias": categorias,
        }
    )
```

### 13.2. Atualize `templates/index.html`:

Substitua o conteúdo por um layout de blog mostrando os últimos artigos.

### 13.3. Atualize a navbar em `templates/base_publica.html`:

Adicione link para a página de artigos:

```html
<li class="nav-item">
    <a class="nav-link" href="/artigos">
        <i class="bi bi-newspaper"></i> Artigos
    </a>
</li>
```

---

## 14. Atualizando o main.py

Adicione as importações e configurações necessárias:

```python
# Importar o repositório
from repo import artigo_repo

# Importar o router
from routes.artigos_routes import router as artigos_router

# Na função create_app(), adicionar criação da tabela:
artigo_repo.criar_tabela()

# Adicionar o router na lista:
routers = [
    ...
    artigos_router,
]
```

---

## 15. Testando a Aplicação

1. **Inicie a aplicação**:
   ```bash
   python main.py
   ```

2. **Crie um usuário administrador** (pelo cadastro ou seed)

3. **Crie categorias** em `/admin/categorias`

4. **Crie um usuário autor**

5. **Crie artigos** em `/artigos/meus`

6. **Publique artigos** e veja na home page

7. **Teste a busca** em `/artigos`

8. **Faça logout e veja** que precisa de login para ler artigos

---

## 16. Conclusão

Parabéns! Você criou um blog funcional com:

- Sistema de categorias para organização
- CRUD completo de artigos para autores
- Editor Markdown profissional
- Home page dinâmica com últimos artigos
- Sistema de busca e filtros
- Controle de acesso por perfis
- Contador de visualizações

### Próximos passos sugeridos:

1. Adicionar sistema de comentários
2. Implementar tags/palavras-chave
3. Adicionar imagem de capa aos artigos
4. Implementar feed RSS
5. Adicionar compartilhamento em redes sociais

---

## Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [EasyMDE Editor](https://github.com/Ionaru/easy-markdown-editor)
- [Marked.js](https://github.com/markedjs/marked)
- [Bootstrap 5](https://getbootstrap.com/)
