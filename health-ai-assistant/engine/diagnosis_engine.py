"""
Clinical Diagnosis and Probabilistic Triage Engine
Multi-factor reasoning matching narrative, explicit symptoms, patient profile, and vitals.
Architected by Shashank Dixit
"""

import re
from typing import Dict, Any, List, Optional
from .knowledge_base import DISEASES_DB, SYMPTOM_DICTIONARY
from .emergency_triage import assess_vitals
from .gemini_ai import generate_ai_diagnosis_insights

KEYWORD_TO_SYMPTOM = {
    r"\b(chest\s*pain|chest\s*pressure|heavy\s*chest|heart\s*pain)\b": "chest_pain",
    r"\b(tightness\s*in\s*chest|chest\s*tight)\b": "chest_tightness",
    r"\b(arm\s*pain|left\s*arm|radiating\s*arm)\b": "radiating_arm_pain",
    r"\b(jaw\s*pain|radiating\s*jaw|neck\s*pain)\b": "radiating_jaw_pain",
    r"\b(breathless|short\s*of\s*breath|dyspnea|hard\s*to\s*breathe|breathing\s*problem)\b": "shortness_of_breath",
    r"\b(cold\s*sweat|sweating|perspiration|diaphoresis)\b": "diaphoresis",
    r"\b(face\s*droop|facial\s*droop|crooked\s*smile)\b": "facial_droop",
    r"\b(weak\s*arm|arm\s*drift|weakness\s*in\s*leg|arm\s*weakness)\b": "arm_weakness",
    r"\b(slurred\s*speech|speech\s*problem|hard\s*to\s*talk|aphasia)\b": "speech_difficulty",
    r"\b(numbness|numb\s*side|loss\s*of\s*feeling)\b": "sudden_numbness",
    r"\b(blurred\s*vision|double\s*vision|cant\s*see|vision\s*loss)\b": "vision_loss",
    r"\b(unstable|loss\s*of\s*balance|dizzy|ataxia|clumsy)\b": "ataxia",
    r"\b(cough\s*with\s*phlegm|wet\s*cough|sputum|productive\s*cough)\b": "productive_cough",
    r"\b(fever|high\s*temp|temperature|burning\s*up)\b": "fever",
    r"\b(chills|shivering|rigors)\b": "chills",
    r"\b(sharp\s*chest|pleuritic|pain\s*on\s*breathing)\b": "pleuritic_chest_pain",
    r"\b(stomach\s*pain|belly\s*pain|abdominal\s*pain|tummy\s*ache)\b": "abdominal_pain",
    r"\b(right\s*lower|right\s*side\s*pain|rlq|appendix)\b": "right_lower_quadrant_pain",
    r"\b(navel\s*pain|belly\s*button|periumbilical)\b": "periumbilical_pain",
    r"\b(no\s*appetite|loss\s*of\s*appetite|anorexia)\b": "anorexia",
    r"\b(nausea|queasy|feel\s*sick)\b": "nausea",
    r"\b(vomiting|threw\s*up|vomit|emesis)\b": "vomiting",
    r"\b(excessive\s*urination|pee\s*a\s*lot|polyuria|frequent\s*pee)\b": "polyuria",
    r"\b(thirsty|excessive\s*thirst|polydipsia)\b": "polydipsia",
    r"\b(weight\s*loss|lost\s*weight)\b": "unexplained_weight_loss",
    r"\b(high\s*bp|hypertension|blood\s*pressure)\b": "elevated_bp",
    r"\b(wheezing|whistling\s*breath|wheeze)\b": "wheezing",
    r"\b(heartburn|acid|burning\s*in\s*chest|reflux)\b": "heartburn",
    r"\b(acid\s*taste|regurgitation|sour\s*fluid)\b": "acid_regurgitation",
    r"\b(burning\s*urine|pain\s*peeing|dysuria|sting\s*urine)\b": "dysuria",
    r"\b(frequent\s*urination|urinary\s*frequency)\b": "urinary_frequency",
    r"\b(urgent\s*urine|cant\s*hold\s*urine|urinary\s*urgency)\b": "urinary_urgency",
    r"\b(throbbing\s*headache|pulsing\s*headache|migraine)\b": "throbbing_headache",
    r"\b(light\s*sensitive|photophobia|bright\s*light\s*hurts)\b": "photophobia",
    r"\b(sound\s*sensitive|loud\s*noise\s*hurts|phonophobia)\b": "phonophobia",
    r"\b(joint\s*pain|knee\s*pain|hip\s*pain|arthritis)\b": "joint_pain",
    r"\b(stiff\s*joints|morning\s*stiffness)\b": "joint_stiffness",
    r"\b(diarrhea|loose\s*motion|loose\s*stools)\b": "watery_diarrhea",
    r"\b(lost\s*smell|lost\s*taste|no\s*smell|anosmia)\b": "loss_of_taste_smell",
    r"\b(sneezing|sneeze)\b": "sneezing",
    r"\b(stuffy\s*nose|runny\s*nose|nasal\s*congestion|blocked\s*nose)\b": "nasal_congestion"
}

def extract_symptoms_from_narrative(text: str) -> List[str]:
    """Detects symptom tokens from natural language narrative."""
    detected = set()
    if not text:
        return list(detected)
    
    clean = text.lower()
    for pattern, sym_id in KEYWORD_TO_SYMPTOM.items():
        if re.search(pattern, clean):
            detected.add(sym_id)
    return list(detected)

def diagnose_patient(payload: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Main Clinical Diagnosis Orchestrator.
    Combines:
    - Narrative free text
    - Explicitly selected symptoms
    - Patient risk factors & demographics
    - Vital signs & biometrics
    - Generative AI enrichment (if key provided)
    """
    narrative = payload.get("narrative") or ""
    explicit_symptoms = payload.get("symptoms") or []
    system_filter = payload.get("body_system") or "All"
    
    # Extract symptoms from narrative and merge
    narrative_symptoms = extract_symptoms_from_narrative(narrative)
    combined_symptoms = list(set(explicit_symptoms + narrative_symptoms))
    
    # Assess vitals
    vitals = payload.get("vitals") or {}
    vital_assessment = assess_vitals(vitals)
    
    # Patient profile risk factors
    age = 0
    try:
        age = int(payload.get("age", 0) or 0)
    except (ValueError, TypeError):
        pass
    
    gender = payload.get("gender") or "Unspecified"
    history = [h.lower() for h in (payload.get("history") or [])]
    is_smoker = payload.get("smoking") in (True, "true", "yes", "Yes")
    is_pregnant = payload.get("pregnant") in (True, "true", "yes", "Yes")

    # Score each condition in knowledge base
    scored_conditions = []
    
    for disease in DISEASES_DB:
        # If user filtered by body system and it does not match, penalize or filter
        if system_filter and system_filter != "All" and disease["system"] != system_filter:
            system_bonus = 0
        else:
            system_bonus = 10

        primary_matches = [s for s in disease["primary_symptoms"] if s in combined_symptoms]
        secondary_matches = [s for s in disease["secondary_symptoms"] if s in combined_symptoms]

        # Base score from symptom matches
        primary_score = len(primary_matches) * 25.0
        secondary_score = len(secondary_matches) * 12.0
        base_score = primary_score + secondary_score

        if base_score == 0 and len(combined_symptoms) > 0:
            continue

        # Clinical Risk Factors
        risk_modifier = 0
        if disease["id"] in ("acute_coronary_syndrome", "ischemic_stroke"):
            if age >= 50:
                risk_modifier += 15
            if is_smoker:
                risk_modifier += 12
            if any("hypertension" in h for h in history):
                risk_modifier += 15
            if any("diabetes" in h for h in history):
                risk_modifier += 12
        elif disease["id"] == "type2_diabetes_hyperglycemia":
            if any("diabetes" in h for h in history):
                risk_modifier += 30
            if age >= 45:
                risk_modifier += 10
        elif disease["id"] == "bronchial_asthma_exacerbation":
            if any("asthma" in h or "copd" in h for h in history):
                risk_modifier += 30
            if is_smoker:
                risk_modifier += 10
        elif disease["id"] == "osteoarthritis_knee_hip":
            if age >= 55:
                risk_modifier += 20

        # Vital sign correlations
        if disease["id"] == "acute_coronary_syndrome":
            if vitals.get("systolic_bp") and float(vitals.get("systolic_bp", 0)) > 150:
                risk_modifier += 10
            if vitals.get("heart_rate") and float(vitals.get("heart_rate", 0)) > 100:
                risk_modifier += 10
        elif disease["id"] == "pneumonia_community" or disease["id"] == "covid19_viral_respiratory_infection":
            if vitals.get("spo2") and float(vitals.get("spo2", 100)) < 94:
                risk_modifier += 20
            if vitals.get("temperature") and float(vitals.get("temperature", 0)) > 38.0:
                risk_modifier += 15

        # Normalization
        max_possible_symptom_score = (len(disease["primary_symptoms"]) * 25.0) + (len(disease["secondary_symptoms"]) * 12.0)
        if max_possible_symptom_score == 0:
            max_possible_symptom_score = 1.0

        match_ratio = (base_score / max_possible_symptom_score) * 70.0
        final_probability = match_ratio + risk_modifier + (system_bonus * 0.5)

        # Cap between 5% and 96% (clinical certainty shouldn't claim 100%)
        final_probability = max(5.0, min(96.0, final_probability))

        scored_conditions.append({
            "disease": disease,
            "probability": round(final_probability, 1),
            "primary_matches": [SYMPTOM_DICTIONARY.get(s, s) for s in primary_matches],
            "secondary_matches": [SYMPTOM_DICTIONARY.get(s, s) for s in secondary_matches],
        })

    # Sort descending by probability
    scored_conditions.sort(key=lambda x: x["probability"], reverse=True)

    # If no conditions matched or empty symptoms provided
    if not scored_conditions:
        # Default fallback for general wellness/unclassified
        primary = {
            "name": "Nonspecific Constitutional Symptoms / General Consultation",
            "icd10": "R68.89",
            "system": "General",
            "urgency": "Routine",
            "probability": 45.0,
            "description": "The reported symptoms do not uniquely match a single acute syndrome. Clinical evaluation by a physician is recommended for definitive history and physical examination.",
            "recommended_tests": ["Complete Blood Count (CBC)", "Comprehensive Metabolic Panel (CMP)", "Vital signs check"],
            "clinical_management": ["Maintain adequate hydration and rest.", "Monitor symptoms for changes or worsening.", "Consult an outpatient physician."],
            "red_flags": ["Severe chest pain", "Shortness of breath", "Sudden weakness", "High fever"]
        }
        differentials = []
    else:
        top_match = scored_conditions[0]
        top_disease = top_match["disease"]
        primary = {
            "id": top_disease["id"],
            "name": top_disease["name"],
            "icd10": top_disease["icd10"],
            "system": top_disease["system"],
            "urgency": top_disease["urgency"],
            "probability": top_match["probability"],
            "description": top_disease["description"],
            "recommended_tests": top_disease["recommended_tests"],
            "clinical_management": top_disease["clinical_management"],
            "red_flags": top_disease["red_flags"],
            "matched_primary_symptoms": top_match["primary_matches"],
            "matched_secondary_symptoms": top_match["secondary_matches"]
        }

        # Differentials are the next 2-4 matches
        differentials = []
        for item in scored_conditions[1:5]:
            d = item["disease"]
            differentials.append({
                "id": d["id"],
                "name": d["name"],
                "icd10": d["icd10"],
                "system": d["system"],
                "urgency": d["urgency"],
                "probability": item["probability"],
                "description": d["description"]
            })

    # Overall Urgency determination
    overall_urgency = primary.get("urgency", "Routine")
    if vital_assessment["vital_triage"] == "High Risk / Critical":
        overall_urgency = "Emergency"
    elif vital_assessment["vital_triage"] == "Medium Risk / Caution" and overall_urgency == "Routine":
        overall_urgency = "Urgent"

    # Red Flag Synthesis
    detected_red_flags = []
    # Add vital critical alerts
    for a in vital_assessment.get("alerts", []):
        if a["type"] == "critical":
            detected_red_flags.append(a["message"])
    # Add disease specific red flags if probability high
    if primary.get("probability", 0) > 40:
        detected_red_flags.extend(primary.get("red_flags", [])[:3])

    result = {
        "primary_diagnosis": primary,
        "differential_diagnoses": differentials,
        "overall_urgency": overall_urgency,
        "vital_assessment": vital_assessment,
        "detected_symptoms": [SYMPTOM_DICTIONARY.get(s, s) for s in combined_symptoms],
        "red_flags": list(set(detected_red_flags)),
        "recommended_tests": primary.get("recommended_tests", []),
        "clinical_management": primary.get("clinical_management", []),
        "ai_powered_by": "MediAI Clinical Engine (Architected by Shashank Dixit)"
    }

    # Optional Gemini generative enhancement
    gemini_insights = generate_ai_diagnosis_insights(payload, result, api_key)
    if gemini_insights:
        result["gemini_enhanced"] = True
        result["gemini_insights"] = gemini_insights
        result["ai_powered_by"] = "Google Gemini AI + MediAI Clinical Rule Engine (Architected by Shashank Dixit)"
    else:
        result["gemini_enhanced"] = False

    return result
