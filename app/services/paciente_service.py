from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.user import User, TipoUsuario
from app.models.paciente import Paciente
from app.schemas.paciente_schemas import PacienteCreate, PacienteUpdate
from app.services.user_service import UserService
from app.schemas.user_schemas import UserCreate

class PacienteService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
    
    def create_paciente(self, paciente_data: PacienteCreate) -> Paciente:
        """Criar novo paciente"""
        # Verificar se CPF já existe
        existing_paciente = self.db.query(Paciente).filter(
            Paciente.cpf == paciente_data.cpf
        ).first()
        if existing_paciente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado no sistema"
            )
        
        # Criar usuário
        user_data = UserCreate(
            nome=paciente_data.nome,
            email=paciente_data.email,
            senha=paciente_data.senha,
            tipo_usuario=TipoUsuario.PACIENTE
        )
        user = self.user_service.create_user(user_data)
        
        # Criar paciente
        paciente = Paciente(
            user_id=user.id,
            cpf=paciente_data.cpf,
            rg=paciente_data.rg,
            data_nascimento=paciente_data.data_nascimento,
            telefone=paciente_data.telefone,
            endereco=paciente_data.endereco,
            contato_emergencia=paciente_data.contato_emergencia,
            plano_saude=paciente_data.plano_saude,
            numero_carteirinha=paciente_data.numero_carteirinha
        )
        
        self.db.add(paciente)
        self.db.commit()
        self.db.refresh(paciente)
        
        return paciente
    
    def get_paciente_by_id(self, paciente_id: int) -> Paciente:
        """Obter paciente por ID"""
        paciente = self.db.query(Paciente).options(
            joinedload(Paciente.user)
        ).filter(Paciente.id == paciente_id).first()
        
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente não encontrado"
            )
        
        return paciente
    
    def get_all_pacientes(self, skip: int = 0, limit: int = 100):
        """Listar todos os pacientes"""
        return self.db.query(Paciente).options(
            joinedload(Paciente.user)
        ).offset(skip).limit(limit).all()
    
    def update_paciente(self, paciente_id: int, paciente_data: PacienteUpdate) -> Paciente:
        """Atualizar dados do paciente"""
        paciente = self.get_paciente_by_id(paciente_id)
        
        # Atualizar dados do paciente
        for field, value in paciente_data.model_dump(exclude_unset=True).items():
            if field == "nome":
                # Atualizar nome no usuário
                paciente.user.nome = value
            else:
                setattr(paciente, field, value)
        
        self.db.commit()
        self.db.refresh(paciente)
        
        return paciente
