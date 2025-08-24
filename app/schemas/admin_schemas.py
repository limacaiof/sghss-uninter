from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdminCreate(BaseModel):
    nome: str
    email: str
    senha: str
    setor: Optional[str] = None
    permissoes_especiais: Optional[str] = None

class AdminUpdate(BaseModel):
    nome: Optional[str] = None
    setor: Optional[str] = None
    permissoes_especiais: Optional[str] = None

class AdminResponse(BaseModel):
    id: int
    nome: str
    email: str
    setor: Optional[str] = None
    permissoes_especiais: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
