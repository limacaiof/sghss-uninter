from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.user import User, TipoUsuario
from app.models.admin import Admin
from app.schemas.user_schemas import UserCreate
from app.services.user_service import UserService

class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
    
    def create_admin(self, admin_data: dict) -> Admin:
        """Criar novo administrador"""
        # Verificar se email já existe
        existing_user = self.db.query(User).filter(User.email == admin_data["email"]).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado no sistema"
            )
        
        # Criar usuário
        user_data = UserCreate(
            nome=admin_data["nome"],
            email=admin_data["email"],
            senha=admin_data["senha"],
            tipo_usuario=TipoUsuario.ADMIN
        )
        user = self.user_service.create_user(user_data)
        
        # Criar admin
        admin = Admin(
            user_id=user.id,
            setor=admin_data.get("setor"),
            permissoes_especiais=admin_data.get("permissoes_especiais")
        )
        
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        
        return admin
    
    def get_admin_by_id(self, admin_id: int) -> Admin:
        """Obter admin por ID"""
        admin = self.db.query(Admin).options(
            joinedload(Admin.user)
        ).filter(Admin.id == admin_id).first()
        
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado"
            )
        
        return admin
    
    def get_all_admins(self, skip: int = 0, limit: int = 100):
        """Listar todos os administradores"""
        return self.db.query(Admin).options(
            joinedload(Admin.user)
        ).offset(skip).limit(limit).all()
