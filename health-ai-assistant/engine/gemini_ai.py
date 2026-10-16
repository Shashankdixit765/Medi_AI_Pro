"""
Gemini AI Medical Reasoning Integration with Resilient Local Fallback
Architected by Shashank Dixit
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def get_gemini_api_key(custom_key: Optional[str] = None) -> Optional[str]:
    """Retrieve API key from request, environment, or config file."""
    if custom_key and custom_key.strip():
        return custom_key.strip()
    return os.environ.get("GEMINI_API_KEY")

def generate_ai_diagnosis_insights(
    patient_data: Dict[str, Any],
    rule_results: Dict[str, Any],
    api_key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Calls the Gemini Generative AI model to provide enriched clinical reasoning.
    If no API key or network fails, returns None so caller uses the robust local rule engine.
    """
    key = get_gemini_api_key(api_key)
    if not key:
        return None

    prompt = f"""
You are an advanced AI Clinical Diagnostic Decision Support Assistant.
A patient has presented the following clinical profile and triage data:

PATIENT PROFILE:
- Age: {patient_data.get('age', 'Unknown')}
- Biological Sex: {patient_data.get('gender', 'Unknown')}
- Pre-existing Conditions: {', '.join(patient_data.get('history', [])) or 'None reported'}
- Current Medications: {patient_data.get('medications', 'None')}
- Allergies: {patient_data.get('allergies', 'None known')}
- Smoker: {patient_data.get('smoking', 'No')}
- Pregnant: {patient_data.get('pregnant', 'No')}

REPORTED SYMPTOMS & CHIEF COMPLAINT:
- Narrative Complaint: {patient_data.get('narrative', 'N/A')}
- Selected Specific Symptoms: {', '.join(patient_data.get('symptoms', []))}
- Symptom Duration: {patient_data.get('duration', 'N/A')}
- Symptom Severity (1-10): {patient_data.get('severity', 'N/A')}

VITAL SIGNS & BIOMETRICS:
- BP: {patient_data.get('vitals', {}).get('systolic_bp', 'N/A')}/{patient_data.get('vitals', {}).get('diastolic_bp', 'N/A')} mmHg
- Heart Rate: {patient_data.get('vitals', {}).get('heart_rate', 'N/A')} bpm
- SpO2: {patient_data.get('vitals', {}).get('spo2', 'N/A')}%
- Body Temp: {patient_data.get('vitals', {}).get('temperature', 'N/A')}
- Blood Sugar: {patient_data.get('vitals', {}).get('glucose', 'N/A')} mg/dL

RULE-BASED INFERENCE:
- Primary Working Diagnosis: {rule_results.get('primary_diagnosis', {}).get('name', 'N/A')}
- Triage Urgency: {rule_results.get('urgency', 'Routine')}

YOUR TASK:
Provide an expert, professional clinical synthesis in valid JSON format ONLY, without markdown wrapping or backticks.
JSON schema:
{{
    "clinical_summary": "Concise 2-3 sentence overview of patient status",
    "pathophysiological_insights": "Detailed explanation of why these symptoms correlate with the suspected diagnosis",
    "differential_diagnoses": [
        {{"name": "Condition Name", "probability": 85, "reasoning": "Why this matches"}},
        {{"name": "Alternative Condition", "probability": 60, "reasoning": "Why this is possible"}}
    ],
    "red_flag_concerns": ["Concern 1", "Concern 2"],
    "immediate_actions": ["Action 1", "Action 2"],
    "recommended_investigations": ["Lab/Test 1", "Imaging/Test 2"],
    "lifestyle_and_homecare": ["Care tip 1", "Care tip 2"]
}}
"""

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }

    try:
        url = f"{GEMINI_API_URL}?key={key}"
        response = requests.post(url, headers=headers, json=payload, timeout=12)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                text_content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                # Clean up if markdown fences present
                text_content = text_content.strip()
                if text_content.startswith("```json"):
                    text_content = text_content[7:]
                if text_content.startswith("```"):
                    text_content = text_content[3:]
                if text_content.endswith("```"):
                    text_content = text_content[:-3]
                parsed = json.loads(text_content.strip())
                return parsed
    except Exception as e:
        logger.warning(f"Gemini API invocation failed, falling back to local engine: {e}")

    return None

def chat_with_medical_ai(
    conversation_history: list,
    user_message: str,
    api_key: Optional[str] = None
) -> str:
    """
    Conversational MediBot chat assistant with Gemini AI or intelligent medical conversational fallback.
    """
    key = get_gemini_api_key(api_key)
    if key:
        try:
            # Build Gemini messages format
            contents = [
                {
                    "role": "user",
                    "parts": [{
                        "text": "You are MediBot, an empathetic, highly knowledgeable AI Medical Assistant created by Shashank Dixit. You provide reliable, evidence-based medical information, explain lab tests, suggest lifestyle and first-aid steps, and always clarify that you do not replace an in-person licensed doctor. Keep answers structured, friendly, clear, and easy to read with bullet points."
                    }]
                },
                {
                    "role": "model",
                    "parts": [{
                        "text": "Hello! I am MediBot, your AI Medical Assistant created by Shashank Dixit. I am here to help answer your health questions, explain symptoms and lab reports, and guide you on wellness. How can I assist your health journey today?"
                    }]
                }
            ]

            # Add recent history (up to last 6 messages)
            for msg in conversation_history[-6:]:
                role = "user" if msg.get("sender") == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg.get("text", "")}]
                })

            contents.append({
                "role": "user",
                "parts": [{"text": user_message}]
            })

            url = f"{GEMINI_API_URL}?key={key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": contents,
                "generationConfig": {"temperature": 0.4, "maxOutputTokens": 800}
            }

            res = requests.post(url, headers=headers, json=payload, timeout=12)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except Exception as e:
            logger.warning(f"Gemini Chat API call error: {e}")

    # Fallback to local intelligent medical response generator
    return generate_local_medibot_response(user_message)

def generate_local_medibot_response(message: str) -> str:
    """
    High-quality conversational fallback when running offline or without an API key.
    """
    msg = message.lower()

    if any(k in msg for k in ["creator", "who made", "who created", "who built", "developer", "author", "shashank"]):
        return (
            "✨ **MediAI Healthcare Diagnosis Assistant** was proudly designed and architected by **Shashank Dixit**! "
            "It combines clinical decision support, modified NEWS2 early warning triage, vital signs assessment, and laboratory analytics "
            "into a modern, responsive, and secure healthcare platform."
        )

    if any(k in msg for k in ["chest pain", "heart attack", "crushing", "arm pain", "jaw pain"]):
        return (
            "⚠️ **URGENT EMERGENCY ALERT:**\n"
            "Chest pain, pressure, or tightness radiating to the arm, neck, or jaw is a medical emergency that could indicate Acute Coronary Syndrome (Heart Attack).\n\n"
            "**Immediate Steps:**\n"
            "• **Call Emergency Medical Services (112 / 108 / 911) immediately.**\n"
            "• Chew 300mg of Aspirin if not allergic and no history of internal bleeding.\n"
            "• Sit or lie down in a comfortable position, loosen tight clothing, and remain calm.\n"
            "• Do NOT attempt to drive yourself to the hospital."
        )

    if any(k in msg for k in ["stroke", "face droop", "slurred speech", "weakness in arm", "fast"]):
        return (
            "🚨 **CRITICAL STROKE WARNING (F.A.S.T.):**\n"
            "• **F - Face:** Ask the person to smile. Does one side of the face droop?\n"
            "• **A - Arms:** Ask them to raise both arms. Does one arm drift downward?\n"
            "• **S - Speech:** Ask them to repeat a simple phrase. Is their speech slurred or strange?\n"
            "• **T - Time:** If you observe ANY of these signs, call emergency services immediately! Note the exact time symptoms began."
        )

    if any(k in msg for k in ["fever", "temperature", "high temp", "pyrexia"]):
        return (
            "🌡️ **Fever Management & Guidance:**\n"
            "A fever (temperature >= 38.0°C / 100.4°F) is your immune system's physiological response to an infection.\n\n"
            "**Recommended Home Care:**\n"
            "• **Hydration:** Drink plenty of fluids (water, electrolyte solutions, herbal teas, broth).\n"
            "• **Rest:** Avoid strenuous exertion.\n"
            "• **Antipyretics:** Paracetamol / Acetaminophen (500mg-650mg every 4-6 hours, max 3000mg/day) can help reduce discomfort.\n"
            "• **Red Flags:** Seek immediate medical care if fever exceeds 39.5°C (103°F), lasts > 3 days, or is accompanied by stiff neck, shortness of breath, confusion, or rash."
        )

    if any(k in msg for k in ["blood pressure", "bp", "hypertension", "systolic"]):
        return (
            "💓 **Blood Pressure Classification Guide:**\n"
            "• **Normal:** Less than 120 / 80 mmHg\n"
            "• **Elevated / Prehypertension:** 120-129 / <80 mmHg\n"
            "• **Stage 1 Hypertension:** 130-139 / 80-89 mmHg\n"
            "• **Stage 2 Hypertension:** >= 140 / >= 90 mmHg\n"
            "• **Hypertensive Crisis:** > 180 / > 120 mmHg (Requires immediate medical evaluation!)\n\n"
            "**Lifestyle Recommendations:** Adopt the DASH diet (rich in fruits, vegetables, low-fat dairy), limit sodium intake (< 2000mg/day), engage in regular aerobic exercise, and monitor BP regularly."
        )

    if any(k in msg for k in ["diabetes", "sugar", "glucose", "hba1c"]):
        return (
            "🩸 **Blood Glucose & Diabetes Insights:**\n"
            "• **Normal Fasting Glucose:** 70 - 99 mg/dL\n"
            "• **Prediabetes:** 100 - 125 mg/dL (or HbA1c 5.7% - 6.4%)\n"
            "• **Diabetes Threshold:** Fasting >= 126 mg/dL or HbA1c >= 6.5%\n\n"
            "**Key Tips:** Maintain a low glycemic index diet, perform 150 minutes of weekly moderate exercise, stay hydrated, and track post-meal glucose spikes."
        )

    if any(k in msg for k in ["headache", "migraine"]):
        return (
            "🧠 **Headache Evaluation & Relief:**\n"
            "Headaches range from tension headaches and migraines to secondary causes.\n\n"
            "**Self-Care Tips for Migraines:**\n"
            "• Rest in a dark, quiet, temperature-regulated room.\n"
            "• Apply a cold or warm compress to forehead or neck.\n"
            "• Maintain steady hydration and avoid trigger foods (caffeine, aged cheese, chocolate, nitrates).\n"
            "• Over-the-counter NSAIDs (Naproxen, Ibuprofen) or Triptans as prescribed.\n\n"
            "⚠️ **Red Flag:** If you experience a sudden, severe 'thunderclap' headache (worst headache of your life), seek emergency care immediately!"
        )

    # General supportive answer
    return (
        f"Thank you for reaching out. Based on your question regarding '{message[:50]}...', "
        "here are primary clinical considerations:\n\n"
        "• **Symptom Monitoring:** Track when symptoms started, their triggers, and whether they are progressing.\n"
        "• **Vitals Assessment:** Use the **Symptom Checker & Triage tab** to run a complete evaluation with your vitals.\n"
        "• **Lab Diagnostics:** If you have recent blood work, test it in the **Lab Analyzer tab** for instant reference-range breakdown.\n"
        "• **Professional Evaluation:** Always consult a qualified healthcare physician for formal diagnostic testing, physical examination, and prescription medications.\n\n"
        "Feel free to ask about specific symptoms, vital signs, or first-aid protocols!"
    )
