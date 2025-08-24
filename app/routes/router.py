from fastapi import APIRouter

from app.routes.auth import auth_router
from app.routes.admin import admin_router
from app.routes.pacientes import pacientes_router
from app.routes.profissionais import profissionais_router
from app.routes.consultas import consultas_router

router = APIRouter(prefix="/api")


router.include_router(auth_router)
router.include_router(admin_router)
router.include_router(pacientes_router)
router.include_router(profissionais_router)
router.include_router(consultas_router)




