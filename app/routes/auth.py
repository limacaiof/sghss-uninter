from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/login")
def index():
    return {"message": "Login"}


@auth_router.get("/logout")
def index():
    return {"message": "Logout"}
