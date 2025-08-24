from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.consulta import StatusConsulta, TipoConsulta

class ConsultaBase(BaseModel):
    paciente_id: int
    profissional_id: int
    data_hora: datetime
    tipo_consulta: TipoConsulta = TipoConsulta.PRESENCIAL
    observacoes: Optional[str] = None

class ConsultaCreate(ConsultaBase):
    pass

class ConsultaUpdate(BaseModel):
    data_hora: Optional[datetime] = None
    status: Optional[StatusConsulta] = None
    observacoes: Optional[str] = None
    link_telemedicina: Optional[str] = None

class ConsultaResponse(ConsultaBase):
    id: int
    status: StatusConsulta
    link_telemedicina: Optional[str] = None
    created_at: datetime
    
    # Dados relacionados
    paciente_nome: Optional[str] = None
    profissional_nome: Optional[str] = None
    especialidade: Optional[str] = None
    
    class Config:
        from_attributes = True
