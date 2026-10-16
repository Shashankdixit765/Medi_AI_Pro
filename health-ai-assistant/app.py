"""
FastAPI Server Entrypoint
AI Healthcare Diagnosis Assistant
Architected by Shashank Dixit
"""

import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

import config
from engine.knowledge_base import SYMPTOM_DICTIONARY, BODY_SYSTEMS
from engine.emergency_triage import assess_vitals
from engine.lab_analyzer import analyze_lab_report, LAB_TEST_RANGES
from engine.diagnosis_engine import diagnose_patient
from engine.gemini_ai import chat_with_medical_ai

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title=config.APP_TITLE,
    description="Interactive, secure, and clinical-grade AI Healthcare Diagnosis and Triage Assistant created by Shashank Dixit.",
    version=config.APP_VERSION
)

# CORS setup for flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# --- Pydantic Data Models ---
class VitalsModel(BaseModel):
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    heart_rate: Optional[float] = None
    respiratory_rate: Optional[float] = None
    spo2: Optional[float] = None
    temperature: Optional[float] = None
    glucose: Optional[float] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None

class DiagnosisRequest(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=125)
    gender: Optional[str] = "Unspecified"
    narrative: Optional[str] = ""
    symptoms: List[str] = []
    body_system: Optional[str] = "All"
    history: List[str] = []
    medications: Optional[str] = ""
    allergies: Optional[str] = ""
    smoking: Optional[bool] = False
    pregnant: Optional[bool] = False
    vitals: Optional[VitalsModel] = None
    api_key: Optional[str] = None

class LabAnalysisRequest(BaseModel):
    values: Dict[str, Any]
    patient_id: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []
    api_key: Optional[str] = None

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Renders the comprehensive Medical Diagnosis Portal UI."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": config.APP_TITLE,
            "subtitle": config.APP_SUBTITLE,
            "author": config.AUTHOR_NAME,
            "author_title": config.AUTHOR_TITLE,
            "version": config.APP_VERSION,
            "symptoms": SYMPTOM_DICTIONARY,
            "body_systems": BODY_SYSTEMS,
            "hotlines": config.EMERGENCY_HOTLINES,
            "lab_tests": LAB_TEST_RANGES
        }
    )

@app.get("/api/health")
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "app": config.APP_TITLE,
        "author": config.AUTHOR_NAME,
        "version": config.APP_VERSION,
        "engine": "Active & Operational"
    }

@app.get("/api/symptoms")
async def get_symptom_catalog():
    """Returns the full dictionary of symptoms and body systems."""
    return {
        "symptoms": SYMPTOM_DICTIONARY,
        "body_systems": BODY_SYSTEMS
    }

@app.get("/api/hotlines")
async def get_emergency_hotlines():
    """Returns emergency hotlines directory."""
    return {"hotlines": config.EMERGENCY_HOTLINES}

@app.post("/api/diagnose")
async def perform_diagnosis(req: DiagnosisRequest):
    """
    Executes clinical evaluation and differential diagnostic scoring.
    """
    try:
        payload = req.model_dump()
        result = diagnose_patient(payload, api_key=req.api_key)
        return {
            "success": True,
            "data": result,
            "author": config.AUTHOR_NAME
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnostic calculation error: {str(e)}")

@app.post("/api/analyze-vitals")
async def evaluate_vitals(vitals: VitalsModel):
    """
    Evaluates vital signs against clinical safety boundaries and generates NEWS2 score.
    """
    try:
        assessment = assess_vitals(vitals.model_dump())
        return {
            "success": True,
            "assessment": assessment,
            "author": config.AUTHOR_NAME
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vital assessment error: {str(e)}")

@app.post("/api/analyze-labs")
async def evaluate_labs(req: LabAnalysisRequest):
    """
    Analyzes entered laboratory biomarkers against standard reference ranges.
    """
    try:
        report = analyze_lab_report(req.values)
        return {
            "success": True,
            "report": report,
            "author": config.AUTHOR_NAME
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lab analysis error: {str(e)}")

@app.post("/api/chat")
async def medical_chat(req: ChatRequest):
    """
    MediBot conversational healthcare assistant with Gemini AI or local clinical fallback.
    """
    try:
        if not req.message.strip():
            return {"reply": "Please enter a health or medical question so I can assist you."}
        
        reply = chat_with_medical_ai(
            conversation_history=req.history or [],
            user_message=req.message,
            api_key=req.api_key
        )
        return {
            "success": True,
            "reply": reply,
            "author": config.AUTHOR_NAME
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host=config.HOST, port=config.PORT, reload=True)
