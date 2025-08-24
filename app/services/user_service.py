from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user_schemas import UserCreate
from app.utils.security import get_password_hash, verify_password, create_access_token

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        """Criar novo usuário"""
        # Verificar se email já existe
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado no sistema"
            )
        
        # Criar usuário
        hashed_password = get_password_hash(user_data.senha)
        user = User(
            nome=user_data.nome,
            email=user_data.email,
            senha_hash=hashed_password,
            tipo_usuario=user_data.tipo_usuario
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def authenticate_user(self, email: str, senha: str) -> User:
        """Autenticar usuário"""
        user = self.db.query(User).filter(
            User.email == email, 
            User.ativo == True
        ).first()
        
        if not user or not verify_password(senha, user.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        return user
    
    def generate_token(self, user: User) -> str:
        """Gerar token para usuário"""
        access_token = create_access_token(data={"sub": str(user.id)})
        return access_token
