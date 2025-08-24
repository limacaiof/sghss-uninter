from fastapi import APIRouter

pacientes_router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

@pacientes_router.get("")
def index():
    return {"message": "Pacientes"}
