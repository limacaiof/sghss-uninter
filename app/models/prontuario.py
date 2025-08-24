from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Prontuario(BaseModel):
    __tablename__ = "prontuarios"
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("profissionais_saude.id"), nullable=False)
    consulta_id = Column(Integer, ForeignKey("consultas.id"))
    queixa_principal = Column(Text)
    historia_doenca_atual = Column(Text)
    exame_fisico = Column(Text)
    diagnostico = Column(Text)
    prescricao = Column(Text)
    observacoes = Column(Text)
    anexos = Column(JSON)  # Para armazenar caminhos de arquivos/exames
    
    # Relacionamentos
    paciente = relationship("Paciente", back_populates="prontuarios")
    profissional = relationship("ProfissionalSaude", back_populates="prontuarios_criados")
