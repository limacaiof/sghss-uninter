from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class TipoUsuario(enum.Enum):
    PACIENTE = "paciente"
    PROFISSIONAL_SAUDE = "profissional_saude"
    ADMIN = "admin"

class User(BaseModel):
    __tablename__ = "users"
    
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo_usuario = Column(Enum(TipoUsuario), nullable=False)
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    paciente = relationship("Paciente", back_populates="user", uselist=False)
    profissional_saude = relationship("ProfissionalSaude", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
