from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.config.database import get_database
from app.models.user import User, TipoUsuario
from app.utils.security import verify_token

security = HTTPBearer()

def get_current_user(token: str = Depends(security), db: Session = Depends(get_database)) -> User:
    """Obter usuário atual baseado no token"""
    payload = verify_token(token.credentials)
    user_id: int = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    user = db.query(User).filter(User.id == user_id, User.ativo == True).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )
    
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Requer que o usuário seja admin"""
    if current_user.tipo_usuario != TipoUsuario.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores podem acessar este recurso."
        )
    return current_user

def require_profissional_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """Requer que o usuário seja profissional de saúde ou admin"""
    if current_user.tipo_usuario not in [TipoUsuario.PROFISSIONAL_SAUDE, TipoUsuario.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas profissionais de saúde ou administradores podem acessar este recurso."
        )
    return current_user
