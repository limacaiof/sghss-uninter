from fastapi import APIRouter

profissionais_router = APIRouter(prefix="/profissionais", tags=["Profissionais"])

@profissionais_router.get("")
def index():
    return {"message": "Profissionais"}
