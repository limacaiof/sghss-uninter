from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.profissional_saude import EspecialidadeMedica

class ProfissionalSaudeBase(BaseModel):
    crm: str
    especialidade: EspecialidadeMedica
    telefone: Optional[str] = None
    horario_atendimento: Optional[str] = None

class ProfissionalSaudeCreate(ProfissionalSaudeBase):
    # Dados do usuário
    nome: str
    email: str
    senha: str

class ProfissionalSaudeUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    horario_atendimento: Optional[str] = None

class ProfissionalSaudeResponse(ProfissionalSaudeBase):
    id: int
    nome: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True
