from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_database
from app.schemas.admin_schemas import AdminCreate, AdminUpdate, AdminResponse
from app.services.admin_service import AdminService
from app.utils.dependencies import get_current_user, require_admin
from app.models.user import User

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
async def criar_admin(
    admin_data: AdminCreate,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_admin)
):
    """Criar novo administrador (apenas admin existente)"""
    admin_service = AdminService(db)
    admin = admin_service.create_admin(admin_data.dict())
    
    return AdminResponse(
        id=admin.id,
        nome=admin.user.nome,
        email=admin.user.email,
        setor=admin.setor,
        permissoes_especiais=admin.permissoes_especiais,
        created_at=admin.created_at
    )

@admin_router.get("/", response_model=List[AdminResponse])
async def listar_admins(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_admin)
):
    """Listar todos os administradores (apenas admin)"""
    admin_service = AdminService(db)
    admins = admin_service.get_all_admins(skip, limit)
    
    return [
        AdminResponse(
            id=a.id,
            nome=a.user.nome,
            email=a.user.email,
            setor=a.setor,
            permissoes_especiais=a.permissoes_especiais,
            created_at=a.created_at
        )
        for a in admins
    ]

@admin_router.get("/{admin_id}", response_model=AdminResponse)
async def obter_admin(
    admin_id: int,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_admin)
):
    """Obter dados de um administrador específico (apenas admin)"""
    admin_service = AdminService(db)
    admin = admin_service.get_admin_by_id(admin_id)
    
    return AdminResponse(
        id=admin.id,
        nome=admin.user.nome,
        email=admin.user.email,
        setor=admin.setor,
        permissoes_especiais=admin.permissoes_especiais,
        created_at=admin.created_at
    )

@admin_router.get("/dashboard")
async def dashboard_admin(
    db: Session = Depends(get_database),
    current_user: User = Depends(require_admin)
):
    """Dashboard administrativo (apenas admin)"""
    return {
        "message": "Dashboard Administrativo",
        "usuario": current_user.nome,
        "tipo": current_user.tipo_usuario.value,
        "funcionalidades": [
            "Gestão de Usuários",
            "Gestão de Pacientes", 
            "Gestão de Profissionais",
            "Relatórios e Estatísticas"
        ]
    }
