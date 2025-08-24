# Importações dos modelos
from .base import Base
from .user import User, TipoUsuario
from .paciente import Paciente
from .profissional_saude import ProfissionalSaude, EspecialidadeMedica
from .admin import Admin
from .consulta import Consulta, StatusConsulta, TipoConsulta
from .prontuario import Prontuario

__all__ = [
    "Base",
    "User", 
    "TipoUsuario",
    "Paciente",
    "ProfissionalSaude",
    "EspecialidadeMedica", 
    "Admin",
    "Consulta",
    "StatusConsulta",
    "TipoConsulta",
    "Prontuario"
]
