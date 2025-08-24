from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import TipoUsuario

class UserBase(BaseModel):
    nome: str
    email: EmailStr
    tipo_usuario: TipoUsuario

class UserCreate(UserBase):
    senha: str

class UserResponse(UserBase):
    id: int
    ativo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_data: UserResponse
