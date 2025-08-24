from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Paciente(BaseModel):
    __tablename__ = "pacientes"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    cpf = Column(String(14), unique=True, nullable=False)
    rg = Column(String(20))
    data_nascimento = Column(Date)
    telefone = Column(String(20))
    endereco = Column(String(500))
    contato_emergencia = Column(String(255))
    plano_saude = Column(String(100))
    numero_carteirinha = Column(String(50))
    
    # Relacionamentos
    user = relationship("User", back_populates="paciente")
    consultas_paciente = relationship("Consulta", foreign_keys="Consulta.paciente_id", back_populates="paciente")
    prontuarios = relationship("Prontuario", back_populates="paciente")
