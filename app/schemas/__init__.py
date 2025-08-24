from .user_schemas import UserBase, UserCreate, UserResponse, UserLogin, Token
from .paciente_schemas import PacienteBase, PacienteCreate, PacienteUpdate, PacienteResponse
from .profissional_schemas import ProfissionalSaudeBase, ProfissionalSaudeCreate, ProfissionalSaudeUpdate, ProfissionalSaudeResponse
from .admin_schemas import AdminCreate, AdminUpdate, AdminResponse
from .consulta_schemas import ConsultaBase, ConsultaCreate, ConsultaUpdate, ConsultaResponse
from .prontuario_schemas import ProntuarioBase, ProntuarioCreate, ProntuarioUpdate, ProntuarioResponse

__all__ = [
    "UserBase", "UserCreate", "UserResponse", "UserLogin", "Token",
    "PacienteBase", "PacienteCreate", "PacienteUpdate", "PacienteResponse",
    "ProfissionalSaudeBase", "ProfissionalSaudeCreate", "ProfissionalSaudeUpdate", "ProfissionalSaudeResponse",
    "AdminCreate", "AdminUpdate", "AdminResponse",
    "ConsultaBase", "ConsultaCreate", "ConsultaUpdate", "ConsultaResponse",
    "ProntuarioBase", "ProntuarioCreate", "ProntuarioUpdate", "ProntuarioResponse"
]
