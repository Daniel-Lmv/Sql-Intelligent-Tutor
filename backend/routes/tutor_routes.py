# backend/routes/tutor_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.tutor_service import TutorService
from services.ia_service import ExplanationService
from typing import List, Dict

router = APIRouter(prefix="/tutor", tags=["Tutor Inteligente & Treino"])

# Modelos de dados para validação de requisições (Pydantic)
class StartLessonRequest(BaseModel):
    user_id: int
    conceito_id: int

class VerifyAnswerRequest(BaseModel):
    user_id: int
    questao_id: int
    resposta_aluno: str

class ChatMessage(BaseModel):
    role: str # "user" ou "assistant"
    content: str

class SocraticChatRequest(BaseModel):
    dados_questao: Dict[str, str] # enunciado, resposta_correta, resposta_aluno, conceito_nome
    historico_mensagens: List[ChatMessage]

@router.post("/lesson/start")
def iniciar_licao(data: StartLessonRequest):
    resultado = TutorService.gerar_licao(data.user_id, data.conceito_id)
    if resultado["status"] == "error":
        raise HTTPException(status_code=404, detail=resultado["message"])
    return resultado

@router.post("/lesson/verify")
def verificar_resposta(data: VerifyAnswerRequest):
    resultado = TutorService.verificar_resposta_treino(data.user_id, data.questao_id, data.resposta_aluno)
    if resultado["status"] == "error":
        raise HTTPException(status_code=404, detail=resultado["message"])
    return resultado

@router.post("/chat/socratic")
def conversar_tutor(data: SocraticChatRequest):
    # Transforma a lista de objetos Pydantic em uma lista de dicionários puros para o Ollama
    historico_convertido = [{"role": msg.role, "content": msg.content} for msg in data.historico_mensagens]
    
    resposta_ia = ExplanationService.conversar_tutor_socratico(data.dados_questao, historico_convertido)
    return {"status": "success", "response": resposta_ia}