from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde",
    description="API para gerenciamento das operações da clínica VidaPlus.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router)

@app.get("/", tags=["Root"])
def root():
    """Endpoint raiz da API"""
    return {
        "message": "Bem-vindo ao SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Verificação de saúde da API"""
    return {"status": "healthy", "timestamp": "2025-01-01T00:00:00Z"}
