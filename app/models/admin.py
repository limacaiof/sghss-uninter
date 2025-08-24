from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Admin(BaseModel):
    __tablename__ = "admins"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    setor = Column(String(100))
    permissoes_especiais = Column(String(500))  # JSON string com permissões
    
    # Relacionamentos
    user = relationship("User", back_populates="admin")
