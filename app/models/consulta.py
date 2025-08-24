from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class StatusConsulta(enum.Enum):
    AGENDADA = "agendada"
    CONFIRMADA = "confirmada"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"

class TipoConsulta(enum.Enum):
    PRESENCIAL = "presencial"
    TELEMEDICINA = "telemedicina"

class Consulta(BaseModel):
    __tablename__ = "consultas"
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("profissionais_saude.id"), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    tipo_consulta = Column(Enum(TipoConsulta), default=TipoConsulta.PRESENCIAL)
    status = Column(Enum(StatusConsulta), default=StatusConsulta.AGENDADA)
    observacoes = Column(Text)
    link_telemedicina = Column(String(255))  # Para consultas online
    
    # Relacionamentos
    paciente = relationship("Paciente", foreign_keys=[paciente_id], back_populates="consultas_paciente")
    profissional = relationship("ProfissionalSaude", foreign_keys=[profissional_id], back_populates="consultas_medico")
