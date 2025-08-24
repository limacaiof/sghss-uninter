# SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde

Sistema completo de gestão hospitalar desenvolvido em FastAPI com padrão MVC, focado na clínica VidaPlus.

## Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados
- **JWT** - Autenticação segura
- **MariaDB/MySQL** - Banco de dados
- **Alembic** - Migrações de banco
- **Uvicorn** - Servidor ASGI

## Pré-requisitos

- Python 3.8+
- MariaDB/MySQL
- pip

## Como rodar o projeto

### Manual

1. **Instale as dependências**
```bash
pip install -r requirements.txt
```

2. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
```

3. **Configure o banco de dados**
```bash
mysql -u root -p
CREATE DATABASE sghss_db;
```

4. **Execute as migrações**
```bash
alembic upgrade head
```

5. **(Opcional) Execute o seed do banco**
```bash
python seed_database.py
```

6. **Execute a aplicação**
```bash
uvicorn main:app --reload
```

## Documentação da API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
