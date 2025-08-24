from fastapi import APIRouter

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("")
def index():
    return {"message": "Admin"}
