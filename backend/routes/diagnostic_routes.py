# backend/routes/diagnostic_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.diagnostic_service import DiagnosticService
from typing import Dict

router = APIRouter(prefix="/diagnostic", tags=["Diagnóstico Inicial"])

# Modelo para receber o dicionário de respostas (ex: {"1": "A", "2": "C"})
class SubmitDiagnosticRequest(BaseModel):
    user_id: int
    answers: Dict[str, str]

@router.get("/questions")
def obter_questoes():
    questoes = DiagnosticService.obter_questoes_diagnostico()
    if not questoes:
        raise HTTPException(status_code=404, detail="Nenhuma questão de diagnóstico encontrada.")
    return questoes

@router.post("/submit")
def submeter_diagnostico(data: SubmitDiagnosticRequest):
    resultado = DiagnosticService.processar_respostas_diagnostico(data.user_id, data.answers)
    return resultado