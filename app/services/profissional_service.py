from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.user import User, TipoUsuario
from app.models.profissional_saude import ProfissionalSaude
from app.schemas.profissional_schemas import ProfissionalSaudeCreate, ProfissionalSaudeUpdate
from app.services.user_service import UserService
from app.schemas.user_schemas import UserCreate

class ProfissionalSaudeService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
    
    def create_profissional(self, profissional_data: ProfissionalSaudeCreate) -> ProfissionalSaude:
        """Criar novo profissional de saúde"""
        # Verificar se CRM já existe
        existing_profissional = self.db.query(ProfissionalSaude).filter(
            ProfissionalSaude.crm == profissional_data.crm
        ).first()
        if existing_profissional:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CRM já cadastrado no sistema"
            )
        
        # Criar usuário
        user_data = UserCreate(
            nome=profissional_data.nome,
            email=profissional_data.email,
            senha=profissional_data.senha,
            tipo_usuario=TipoUsuario.PROFISSIONAL_SAUDE
        )
        user = self.user_service.create_user(user_data)
        
        # Criar profissional
        profissional = ProfissionalSaude(
            user_id=user.id,
            crm=profissional_data.crm,
            especialidade=profissional_data.especialidade,
            telefone=profissional_data.telefone,
            horario_atendimento=profissional_data.horario_atendimento
        )
        
        self.db.add(profissional)
        self.db.commit()
        self.db.refresh(profissional)
        
        return profissional
    
    def get_profissional_by_id(self, profissional_id: int) -> ProfissionalSaude:
        """Obter profissional por ID"""
        profissional = self.db.query(ProfissionalSaude).options(
            joinedload(ProfissionalSaude.user)
        ).filter(ProfissionalSaude.id == profissional_id).first()
        
        if not profissional:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profissional não encontrado"
            )
        
        return profissional
    
    def get_all_profissionais(self, skip: int = 0, limit: int = 100):
        """Listar todos os profissionais"""
        return self.db.query(ProfissionalSaude).options(
            joinedload(ProfissionalSaude.user)
        ).offset(skip).limit(limit).all()
    
    def update_profissional(self, profissional_id: int, profissional_data: ProfissionalSaudeUpdate) -> ProfissionalSaude:
        """Atualizar dados do profissional"""
        profissional = self.get_profissional_by_id(profissional_id)
        
        # Atualizar dados do profissional
        for field, value in profissional_data.model_dump(exclude_unset=True).items():
            if field == "nome":
                # Atualizar nome no usuário
                profissional.user.nome = value
            else:
                setattr(profissional, field, value)
        
        self.db.commit()
        self.db.refresh(profissional)
        
        return profissional
