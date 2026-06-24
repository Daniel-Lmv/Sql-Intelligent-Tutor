from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Autenticação"])

class LoginRequest(BaseModel):
    email: EmailStr

@router.post("/login")
def login(data: LoginRequest):
    resultado = UserService.login_simplificado(data.email)
    
    if resultado["status"] == "error":
        raise HTTPException(status_code=404, detail=resultado["message"])
        
    return resultado

@router.get("/progresso/{user_id}")
def obter_progresso(user_id: int):
    return UserService.obter_status_progresso(user_id)