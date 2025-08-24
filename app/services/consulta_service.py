from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.consulta import Consulta, StatusConsulta
from app.models.paciente import Paciente
from app.models.profissional_saude import ProfissionalSaude
from app.schemas.consulta_schemas import ConsultaCreate, ConsultaUpdate
from typing import List, Optional

class ConsultaService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_consulta(self, consulta_data: ConsultaCreate) -> Consulta:
        """Criar nova consulta"""
        # Verificar se paciente existe
        paciente = self.db.query(Paciente).filter(Paciente.id == consulta_data.paciente_id).first()
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente não encontrado"
            )
        
        # Verificar se profissional existe
        profissional = self.db.query(ProfissionalSaude).filter(
            ProfissionalSaude.id == consulta_data.profissional_id
        ).first()
        if not profissional:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profissional não encontrado"
            )
        
        # Criar consulta
        consulta = Consulta(
            paciente_id=consulta_data.paciente_id,
            profissional_id=consulta_data.profissional_id,
            data_hora=consulta_data.data_hora,
            tipo_consulta=consulta_data.tipo_consulta,
            observacoes=consulta_data.observacoes
        )
        
        self.db.add(consulta)
        self.db.commit()
        self.db.refresh(consulta)
        
        return consulta
    
    def get_consulta_by_id(self, consulta_id: int) -> Consulta:
        """Obter consulta por ID"""
        consulta = self.db.query(Consulta).options(
            joinedload(Consulta.paciente).joinedload(Paciente.user),
            joinedload(Consulta.profissional).joinedload(ProfissionalSaude.user)
        ).filter(Consulta.id == consulta_id).first()
        
        if not consulta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consulta não encontrada"
            )
        
        return consulta
    
    def get_consultas_by_paciente(self, paciente_id: int, skip: int = 0, limit: int = 100):
        """Obter consultas de um paciente específico"""
        return self.db.query(Consulta).options(
            joinedload(Consulta.paciente).joinedload(Paciente.user),
            joinedload(Consulta.profissional).joinedload(ProfissionalSaude.user)
        ).filter(Consulta.paciente_id == paciente_id).offset(skip).limit(limit).all()
    
    def get_consultas_by_profissional(self, profissional_id: int, skip: int = 0, limit: int = 100):
        """Obter consultas de um profissional específico"""
        return self.db.query(Consulta).options(
            joinedload(Consulta.paciente).joinedload(Paciente.user),
            joinedload(Consulta.profissional).joinedload(ProfissionalSaude.user)
        ).filter(Consulta.profissional_id == profissional_id).offset(skip).limit(limit).all()
    
    def get_all_consultas(self, skip: int = 0, limit: int = 100):
        """Obter todas as consultas"""
        return self.db.query(Consulta).options(
            joinedload(Consulta.paciente).joinedload(Paciente.user),
            joinedload(Consulta.profissional).joinedload(ProfissionalSaude.user)
        ).offset(skip).limit(limit).all()
    
    def update_consulta(self, consulta_id: int, consulta_data: ConsultaUpdate) -> Consulta:
        """Atualizar consulta"""
        consulta = self.get_consulta_by_id(consulta_id)
        
        # Atualizar dados da consulta
        for field, value in consulta_data.model_dump(exclude_unset=True).items():
            setattr(consulta, field, value)
        
        self.db.commit()
        self.db.refresh(consulta)
        
        return consulta
    
    def update_status_consulta(self, consulta_id: int, novo_status: StatusConsulta) -> Consulta:
        """Atualizar status de uma consulta"""
        consulta = self.get_consulta_by_id(consulta_id)
        consulta.status = novo_status
        
        self.db.commit()
        self.db.refresh(consulta)
        
        return consulta
