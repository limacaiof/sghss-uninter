#!/usr/bin/env python3
"""
Script de seed para popular o banco de dados com usuários de cada tipo
"""

import sys
import os
from datetime import date, datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.config.database import SessionLocal, engine
from app.models import Base, User, Paciente, ProfissionalSaude, Admin
from app.models.user import TipoUsuario
from app.models.profissional_saude import EspecialidadeMedica
from app.utils.security import get_password_hash


def create_tables():
    """Criar tabelas se não existirem"""
    Base.metadata.create_all(bind=engine)


def seed_admin(db: Session):
    """Criar usuário admin"""

    existing_admin = db.query(User).filter(User.email == "admin1@admin.com").first()
    if existing_admin:
        return existing_admin

    admin_user = User(
        nome="Administrador Principal",
        email="admin1@admin.com",
        senha_hash=get_password_hash("admin"),
        tipo_usuario=TipoUsuario.ADMIN,
        ativo=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    admin_profile = Admin(
        user_id=admin_user.id,
        setor="TI",
        permissoes_especiais='["usuarios", "pacientes", "profissionais", "consultas", "prontuarios"]',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(admin_profile)
    db.commit()

    return admin_user


def seed_profissional(db: Session):
    existing_prof = (
        db.query(User).filter(User.email == "profissional1@saude.com").first()
    )
    if existing_prof:
        return existing_prof

    prof_user = User(
        nome="Dr. João Silva",
        email="profissional1@saude.com",
        senha_hash=get_password_hash("profissional"),
        tipo_usuario=TipoUsuario.PROFISSIONAL_SAUDE,
        ativo=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(prof_user)
    db.commit()
    db.refresh(prof_user)

    prof_profile = ProfissionalSaude(
        user_id=prof_user.id,
        crm="12345-SP",
        especialidade=EspecialidadeMedica.CLINICO_GERAL,
        telefone="(11) 99999-8888",
        horario_atendimento='{"segunda": "08:00-18:00", "terca": "08:00-18:00", "quarta": "08:00-18:00", "quinta": "08:00-18:00", "sexta": "08:00-18:00"}',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(prof_profile)
    db.commit()

    return prof_user


def seed_paciente(db: Session):
    """Criar usuário paciente"""

    existing_patient = (
        db.query(User).filter(User.email == "paciente1@email.com").first()
    )
    if existing_patient:
        return existing_patient

    patient_user = User(
        nome="Maria Santos",
        email="paciente1@email.com",
        senha_hash=get_password_hash("paciente"),
        tipo_usuario=TipoUsuario.PACIENTE,
        ativo=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(patient_user)
    db.commit()
    db.refresh(patient_user)

    patient_profile = Paciente(
        user_id=patient_user.id,
        cpf="123.456.789-00",
        rg="12.345.678-9",
        data_nascimento=date(1990, 5, 15),
        telefone="(11) 88888-7777",
        endereco="Rua das Flores, 123 - São Paulo/SP",
        contato_emergencia="João Santos - (11) 77777-6666",
        plano_saude="Unimed",
        numero_carteirinha="123456789",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(patient_profile)
    db.commit()

    return patient_user


def main():
    """Função principal"""

    create_tables()

    db = SessionLocal()

    try:
        seed_admin(db)
        seed_profissional(db)
        seed_paciente(db)

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
