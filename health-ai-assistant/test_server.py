"""
Verification Test Suite for MediAI Pro
Architected by Shashank Dixit
"""

import sys
import json

def run_tests():
    print("=== Testing MediAI Pro Modules ===")

    # 1. Test Config & Knowledge Base
    import config
    from engine.knowledge_base import DISEASES_DB, SYMPTOM_DICTIONARY, BODY_SYSTEMS
    assert len(DISEASES_DB) > 10, "Knowledge base diseases check failed"
    assert len(SYMPTOM_DICTIONARY) > 20, "Symptom dictionary check failed"
    assert len(BODY_SYSTEMS) > 5, "Body systems check failed"
    print("[PASS] Knowledge base & Config verified.")

    # 2. Test Emergency Triage & Vitals
    from engine.emergency_triage import assess_vitals
    vitals_sample = {
        "systolic_bp": 160,
        "diastolic_bp": 98,
        "heart_rate": 105,
        "spo2": 93,
        "temperature": 38.8,
        "glucose": 210,
        "height_cm": 175,
        "weight_kg": 72
    }
    vital_res = assess_vitals(vitals_sample)
    assert vital_res["news2_score"] > 0, "NEWS2 score calculation failed"
    assert vital_res["bmi"] == 23.5, f"BMI calculation incorrect: {vital_res['bmi']}"
    assert vital_res["bmi_category"] == "Normal Weight", "BMI category incorrect"
    print(f"[PASS] Vitals & NEWS2 verified (Score: {vital_res['news2_score']}, Triage: {vital_res['vital_triage']}, BMI: {vital_res['bmi']}).")

    # 3. Test Diagnosis Engine
    from engine.diagnosis_engine import diagnose_patient
    cardiac_case = {
        "age": 58,
        "gender": "Male",
        "narrative": "Severe retrosternal chest pain radiating to left arm with cold sweats and breathlessness",
        "symptoms": ["chest_pain", "chest_tightness", "radiating_arm_pain", "diaphoresis", "shortness_of_breath"],
        "body_system": "Cardiovascular",
        "history": ["hypertension", "smoking"],
        "vitals": {"systolic_bp": 155, "heart_rate": 102, "spo2": 94}
    }
    diag_res = diagnose_patient(cardiac_case)
    assert diag_res["primary_diagnosis"]["id"] == "acute_coronary_syndrome", "Diagnosis mismatch for cardiac case"
    assert diag_res["overall_urgency"] == "Emergency", "Cardiac urgency should be Emergency"
    print(f"[PASS] Diagnostic Engine verified (Primary: {diag_res['primary_diagnosis']['name']}, Confidence: {diag_res['primary_diagnosis']['probability']}%, Urgency: {diag_res['overall_urgency']}).")

    # 4. Test Lab Analyzer
    from engine.lab_analyzer import analyze_lab_report
    sample_labs = {
        "fasting_glucose": 190.0,
        "hba1c": 8.5,
        "creatinine": 1.1,
        "total_cholesterol": 240.0,
        "ldl": 160.0,
        "hemoglobin": 14.5
    }
    lab_res = analyze_lab_report(sample_labs)
    assert lab_res["abnormal_count"] >= 3, "Abnormal lab counts not properly detected"
    print(f"[PASS] Lab Analyzer verified (Total: {lab_res['total_analyzed']}, Abnormal: {lab_res['abnormal_count']}, Severity: {lab_res['overall_severity']}).")

    # 5. Test Chatbot Local Fallback
    from engine.gemini_ai import chat_with_medical_ai
    chat_reply = chat_with_medical_ai([], "Who created MediAI?")
    assert "Shashank Dixit" in chat_reply, "Author attribution in chat failed"
    print("[PASS] Chatbot local conversational engine verified (Attribution to Shashank Dixit confirmed).")

    # 6. Test FastAPI App initialization
    from app import app
    assert app.title == config.APP_TITLE, "FastAPI app title mismatch"
    print("[PASS] FastAPI Server initialized successfully.")

    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY! 100% HEALTHY.")

if __name__ == "__main__":
    run_tests()
