from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_database
from app.schemas.profissional_schemas import ProfissionalSaudeCreate, ProfissionalSaudeUpdate, ProfissionalSaudeResponse
from app.services.profissional_service import ProfissionalSaudeService
from app.utils.dependencies import get_current_user, require_admin
from app.models.user import User

profissionais_router = APIRouter(prefix="/profissionais", tags=["Profissionais"])

@profissionais_router.post("/", response_model=ProfissionalSaudeResponse, status_code=status.HTTP_201_CREATED)
async def criar_profissional(
    profissional_data: ProfissionalSaudeCreate,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_admin)
):
    """Criar novo profissional de saúde (apenas admin)"""
    profissional_service = ProfissionalSaudeService(db)
    profissional = profissional_service.create_profissional(profissional_data)
    
    return ProfissionalSaudeResponse(
        id=profissional.id,
        nome=profissional.user.nome,
        email=profissional.user.email,
        crm=profissional.crm,
        especialidade=profissional.especialidade,
        telefone=profissional.telefone,
        horario_atendimento=profissional.horario_atendimento,
        created_at=profissional.created_at
    )

@profissionais_router.get("/", response_model=List[ProfissionalSaudeResponse])
async def listar_profissionais(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Listar todos os profissionais (acesso para todos os usuários autenticados)"""
    profissional_service = ProfissionalSaudeService(db)
    profissionais = profissional_service.get_all_profissionais(skip, limit)
    
    return [
        ProfissionalSaudeResponse(
            id=p.id,
            nome=p.user.nome,
            email=p.user.email,
            crm=p.crm,
            especialidade=p.especialidade,
            telefone=p.telefone,
            horario_atendimento=p.horario_atendimento,
            created_at=p.created_at
        )
        for p in profissionais
    ]

@profissionais_router.get("/{profissional_id}", response_model=ProfissionalSaudeResponse)
async def obter_profissional(
    profissional_id: int,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Obter dados de um profissional específico"""
    profissional_service = ProfissionalSaudeService(db)
    profissional = profissional_service.get_profissional_by_id(profissional_id)
    
    return ProfissionalSaudeResponse(
        id=profissional.id,
        nome=profissional.user.nome,
        email=profissional.user.email,
        crm=profissional.crm,
        especialidade=profissional.especialidade,
        telefone=profissional.telefone,
        horario_atendimento=profissional.horario_atendimento,
        created_at=profissional.created_at
    )

@profissionais_router.put("/{profissional_id}", response_model=ProfissionalSaudeResponse)
async def atualizar_profissional(
    profissional_id: int,
    profissional_data: ProfissionalSaudeUpdate,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_admin)
):
    """Atualizar dados do profissional (apenas admin)"""
    profissional_service = ProfissionalSaudeService(db)
    profissional = profissional_service.update_profissional(profissional_id, profissional_data)
    
    return ProfissionalSaudeResponse(
        id=profissional.id,
        nome=profissional.user.nome,
        email=profissional.user.email,
        crm=profissional.crm,
        especialidade=profissional.especialidade,
        telefone=profissional.telefone,
        horario_atendimento=profissional.horario_atendimento,
        created_at=profissional.created_at
    )
