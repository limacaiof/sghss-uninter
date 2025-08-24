from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class EspecialidadeMedica(enum.Enum):
    CLINICO_GERAL = "clinico_geral"
    CARDIOLOGIA = "cardiologia"
    DERMATOLOGIA = "dermatologia"
    PEDIATRIA = "pediatria"
    GINECOLOGIA = "ginecologia"
    ORTOPEDIA = "ortopedia"
    PSIQUIATRIA = "psiquiatria"
    NEUROLOGIA = "neurologia"

class ProfissionalSaude(BaseModel):
    __tablename__ = "profissionais_saude"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    crm = Column(String(20), unique=True, nullable=False)
    especialidade = Column(Enum(EspecialidadeMedica), nullable=False)
    telefone = Column(String(20))
    horario_atendimento = Column(String(255))  # JSON string com horários
    
    # Relacionamentos
    user = relationship("User", back_populates="profissional_saude")
    consultas_medico = relationship("Consulta", foreign_keys="Consulta.profissional_id", back_populates="profissional")
    prontuarios_criados = relationship("Prontuario", back_populates="profissional")
