from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ProntuarioBase(BaseModel):
    paciente_id: int
    consulta_id: Optional[int] = None
    queixa_principal: Optional[str] = None
    historia_doenca_atual: Optional[str] = None
    exame_fisico: Optional[str] = None
    diagnostico: Optional[str] = None
    prescricao: Optional[str] = None
    observacoes: Optional[str] = None

class ProntuarioCreate(ProntuarioBase):
    pass

class ProntuarioUpdate(BaseModel):
    queixa_principal: Optional[str] = None
    historia_doenca_atual: Optional[str] = None
    exame_fisico: Optional[str] = None
    diagnostico: Optional[str] = None
    prescricao: Optional[str] = None
    observacoes: Optional[str] = None
    anexos: Optional[Dict[str, Any]] = None

class ProntuarioResponse(ProntuarioBase):
    id: int
    profissional_id: int
    anexos: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    # Dados relacionados
    paciente_nome: Optional[str] = None
    profissional_nome: Optional[str] = None
    especialidade: Optional[str] = None
    
    class Config:
        from_attributes = True
