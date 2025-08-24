from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_database
from app.schemas.consulta_schemas import ConsultaCreate, ConsultaUpdate, ConsultaResponse
from app.services.consulta_service import ConsultaService
from app.utils.dependencies import get_current_user, require_profissional_or_admin
from app.models.user import User, TipoUsuario

consultas_router = APIRouter(prefix="/consultas", tags=["Consultas"])

@consultas_router.post("/", response_model=ConsultaResponse, status_code=status.HTTP_201_CREATED)
async def criar_consulta(
    consulta_data: ConsultaCreate,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_profissional_or_admin)
):
    """Criar nova consulta (apenas profissionais de saúde ou admin)"""
    consulta_service = ConsultaService(db)
    consulta = consulta_service.create_consulta(consulta_data)
    
    return ConsultaResponse(
        id=consulta.id,
        paciente_id=consulta.paciente_id,
        profissional_id=consulta.profissional_id,
        data_hora=consulta.data_hora,
        tipo_consulta=consulta.tipo_consulta,
        status=consulta.status,
        observacoes=consulta.observacoes,
        link_telemedicina=consulta.link_telemedicina,
        created_at=consulta.created_at,
        paciente_nome=consulta.paciente.user.nome,
        profissional_nome=consulta.profissional.user.nome,
        especialidade=consulta.profissional.especialidade.value
    )

@consultas_router.get("/", response_model=List[ConsultaResponse])
async def listar_consultas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Listar consultas baseado no tipo de usuário"""
    consulta_service = ConsultaService(db)
    
    if current_user.tipo_usuario == TipoUsuario.PACIENTE:
        # Paciente vê apenas suas próprias consultas
        if not current_user.paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente não encontrado"
            )
        consultas = consulta_service.get_consultas_by_paciente(
            current_user.paciente.id, skip, limit
        )
    elif current_user.tipo_usuario == TipoUsuario.PROFISSIONAL_SAUDE:
        # Profissional vê apenas suas consultas
        if not current_user.profissional_saude:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profissional não encontrado"
            )
        consultas = consulta_service.get_consultas_by_profissional(
            current_user.profissional_saude.id, skip, limit
        )
    else:
        # Admin vê todas as consultas
        consultas = consulta_service.get_all_consultas(skip, limit)
    
    return [
        ConsultaResponse(
            id=c.id,
            paciente_id=c.paciente_id,
            profissional_id=c.profissional_id,
            data_hora=c.data_hora,
            tipo_consulta=c.tipo_consulta,
            status=c.status,
            observacoes=c.observacoes,
            link_telemedicina=c.link_telemedicina,
            created_at=c.created_at,
            paciente_nome=c.paciente.user.nome,
            profissional_nome=c.profissional.user.nome,
            especialidade=c.profissional.especialidade.value
        )
        for c in consultas
    ]

@consultas_router.get("/{consulta_id}", response_model=ConsultaResponse)
async def obter_consulta(
    consulta_id: int,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Obter dados de uma consulta específica"""
    consulta_service = ConsultaService(db)
    consulta = consulta_service.get_consulta_by_id(consulta_id)
    
    # Verificar permissões
    if current_user.tipo_usuario == TipoUsuario.PACIENTE:
        if not current_user.paciente or current_user.paciente.id != consulta.paciente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
    elif current_user.tipo_usuario == TipoUsuario.PROFISSIONAL_SAUDE:
        if not current_user.profissional_saude or current_user.profissional_saude.id != consulta.profissional_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
    # Admin pode ver qualquer consulta
    
    return ConsultaResponse(
        id=consulta.id,
        paciente_id=consulta.paciente_id,
        profissional_id=consulta.profissional_id,
        data_hora=consulta.data_hora,
        tipo_consulta=consulta.tipo_consulta,
        status=consulta.status,
        observacoes=consulta.observacoes,
        link_telemedicina=consulta.link_telemedicina,
        created_at=consulta.created_at,
        paciente_nome=consulta.paciente.user.nome,
        profissional_nome=consulta.profissional.user.nome,
        especialidade=consulta.profissional.especialidade.value
    )

@consultas_router.put("/{consulta_id}", response_model=ConsultaResponse)
async def atualizar_consulta(
    consulta_id: int,
    consulta_data: ConsultaUpdate,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_profissional_or_admin)
):
    """Atualizar consulta (apenas profissionais de saúde ou admin)"""
    consulta_service = ConsultaService(db)
    consulta = consulta_service.update_consulta(consulta_id, consulta_data)
    
    return ConsultaResponse(
        id=consulta.id,
        paciente_id=consulta.paciente_id,
        profissional_id=consulta.profissional_id,
        data_hora=consulta.data_hora,
        tipo_consulta=consulta.tipo_consulta,
        status=consulta.status,
        observacoes=consulta.observacoes,
        link_telemedicina=consulta.link_telemedicina,
        created_at=consulta.created_at,
        paciente_nome=consulta.paciente.user.nome,
        profissional_nome=consulta.profissional.user.nome,
        especialidade=consulta.profissional.especialidade.value
    )

@consultas_router.get("/historico/paciente/{paciente_id}", response_model=List[ConsultaResponse])
async def historico_consultas_paciente(
    paciente_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Obter histórico de consultas de um paciente específico"""
    consulta_service = ConsultaService(db)
    
    # Verificar permissões
    if current_user.tipo_usuario == TipoUsuario.PACIENTE:
        if not current_user.paciente or current_user.paciente.id != paciente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
    elif current_user.tipo_usuario == TipoUsuario.PROFISSIONAL_SAUDE:
        # Profissional pode ver histórico de seus pacientes
        pass
    # Admin pode ver qualquer histórico
    
    consultas = consulta_service.get_consultas_by_paciente(paciente_id, skip, limit)
    
    return [
        ConsultaResponse(
            id=c.id,
            paciente_id=c.paciente_id,
            profissional_id=c.profissional_id,
            data_hora=c.data_hora,
            tipo_consulta=c.tipo_consulta,
            status=c.status,
            observacoes=c.observacoes,
            link_telemedicina=c.link_telemedicina,
            created_at=c.created_at,
            paciente_nome=c.paciente.user.nome,
            profissional_nome=c.profissional.user.nome,
            especialidade=c.profissional.especialidade.value
        )
        for c in consultas
    ]

@consultas_router.get("/historico/profissional/{profissional_id}", response_model=List[ConsultaResponse])
async def historico_consultas_profissional(
    profissional_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    """Obter histórico de consultas de um profissional específico"""
    consulta_service = ConsultaService(db)
    
    # Verificar permissões
    if current_user.tipo_usuario == TipoUsuario.PROFISSIONAL_SAUDE:
        if not current_user.profissional_saude or current_user.profissional_saude.id != profissional_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
    # Admin pode ver qualquer histórico
    
    consultas = consulta_service.get_consultas_by_profissional(profissional_id, skip, limit)
    
    return [
        ConsultaResponse(
            id=c.id,
            paciente_id=c.paciente_id,
            profissional_id=c.profissional_id,
            data_hora=c.data_hora,
            tipo_consulta=c.tipo_consulta,
            status=c.status,
            observacoes=c.observacoes,
            link_telemedicina=c.link_telemedicina,
            created_at=c.created_at,
            paciente_nome=c.paciente.user.nome,
            profissional_nome=c.profissional.user.nome,
            especialidade=c.profissional.especialidade.value
        )
        for c in consultas
    ]
