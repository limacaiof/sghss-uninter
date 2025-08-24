from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_database
from app.schemas.user_schemas import UserLogin, Token, UserResponse
from app.services.user_service import UserService

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])


@auth_router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_database)):
    user_service = UserService(db)

    user = user_service.authenticate_user(
        user_credentials.email, user_credentials.senha
    )

    access_token = user_service.generate_token(user)

    return Token(
        access_token=access_token,
        token_type="bearer",
        user_data=UserResponse(
            id=user.id,
            nome=user.nome,
            email=user.email,
            tipo_usuario=user.tipo_usuario,
            ativo=user.ativo,
            created_at=user.created_at,
        ),
    )


@auth_router.get("/logout")
def logout():
    """Endpoint para logout (implementar invalidação de token se necessário)"""
    return {"message": "Logout realizado com sucesso"}
