from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde",
    description="API para gerenciamento das operações da clínica VidaPlus.",
    version="1.0.0",
)

app.include_router(router)
