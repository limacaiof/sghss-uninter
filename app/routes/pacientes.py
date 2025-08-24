from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_database
from app.schemas.paciente_schemas import PacienteCreate, PacienteUpdate, PacienteResponse
from app.services.paciente_service import PacienteService
from app.utils.dependencies import get_current_user, require_admin
from app.models.user import User, TipoUsuario

pacientes_router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

@pacientes_router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
async def criar_paciente(
    paciente_data: PacienteCreate,
    db: Session = Depends(get_database)
):
    """Criar novo paciente (endpoint público para auto-cadastro)"""
    paciente_service = PacienteService(db)
    paciente = paciente_service.create_paciente(paciente_data)
    
    return PacienteResponse(
        id=paciente.id,
        nome=paciente.user.nome,
        email=paciente.user.email,
        cpf=paciente.cpf,
        rg=paciente.rg,
        data_nascimento=paciente.data_nascimento,
        telefone=paciente.telefone,
        endereco=paciente.endereco,
        contato_emergencia=paciente.contato_emergencia,
        plano_saude=paciente.plano_saude,
        numero_carteirinha=paciente.numero_carteirinha,
        created_at=paciente.created_at
    )

@pacientes_router.get("/", response_model=List[PacienteResponse])
async def listar_pacientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_admin)
):
    """Listar todos os pacientes (apenas admin)"""
    paciente_service = PacienteService(db)
    pacientes = paciente_service.get_all_pacientes(skip, limit)
    
    return [
        PacienteResponse(
            id=p.id,
            nome=p.user.nome,
            email=p.user.email,
            cpf=p.cpf,
            rg=p.rg,
            data_nascimento=p.data_nascimento,
            telefone=p.telefone,
            endereco=p.endereco,
            contato_emergencia=p.contato_emergencia,
            plano_saude=p.plano_saude,
            numero_carteirinha=p.numero_carteirinha,
            created_at=p.created_at
        )
        for p in pacientes
    ]

@pacientes_router.get("/{paciente_id}", response_model=PacienteResponse)
async def obter_paciente(
    paciente_id: int,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Obter dados de um paciente específico"""
    # Verificar permissões
    if current_user.tipo_usuario == TipoUsuario.PACIENTE:
        # Paciente só pode ver seus próprios dados
        if current_user.paciente and current_user.paciente.id != paciente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
    
    paciente_service = PacienteService(db)
    paciente = paciente_service.get_paciente_by_id(paciente_id)
    
    return PacienteResponse(
        id=paciente.id,
        nome=paciente.user.nome,
        email=paciente.user.email,
        cpf=paciente.cpf,
        rg=paciente.rg,
        data_nascimento=paciente.data_nascimento,
        telefone=paciente.telefone,
        endereco=paciente.endereco,
        contato_emergencia=paciente.contato_emergencia,
        plano_saude=paciente.plano_saude,
        numero_carteirinha=paciente.numero_carteirinha,
        created_at=paciente.created_at
    )

@pacientes_router.put("/{paciente_id}", response_model=PacienteResponse)
async def atualizar_paciente(
    paciente_id: int,
    paciente_data: PacienteUpdate,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Atualizar dados do paciente"""
    # Verificar permissões
    if current_user.tipo_usuario == TipoUsuario.PACIENTE:
        # Paciente só pode atualizar seus próprios dados
        if current_user.paciente and current_user.paciente.id != paciente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
    
    paciente_service = PacienteService(db)
    paciente = paciente_service.update_paciente(paciente_id, paciente_data)
    
    return PacienteResponse(
        id=paciente.id,
        nome=paciente.user.nome,
        email=paciente.user.email,
        cpf=paciente.cpf,
        rg=paciente.rg,
        data_nascimento=paciente.data_nascimento,
        telefone=paciente.telefone,
        endereco=paciente.endereco,
        contato_emergencia=paciente.contato_emergencia,
        plano_saude=paciente.plano_saude,
        numero_carteirinha=paciente.numero_carteirinha,
        created_at=paciente.created_at
    )
