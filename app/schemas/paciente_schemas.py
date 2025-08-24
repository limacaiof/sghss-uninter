from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class PacienteBase(BaseModel):
    cpf: str
    rg: Optional[str] = None
    data_nascimento: Optional[date] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    contato_emergencia: Optional[str] = None
    plano_saude: Optional[str] = None
    numero_carteirinha: Optional[str] = None

class PacienteCreate(PacienteBase):
    # Dados do usuário
    nome: str
    email: str
    senha: str

class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    contato_emergencia: Optional[str] = None
    plano_saude: Optional[str] = None
    numero_carteirinha: Optional[str] = None

class PacienteResponse(PacienteBase):
    id: int
    nome: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True
