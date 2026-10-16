"""
Emergency Triage and Vital Signs Assessment Engine
Modified National Early Warning Score (NEWS2) & Clinical Risk Stratification
Architected by Shashank Dixit
"""

from typing import Dict, Any, List

def assess_vitals(vitals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates vital signs against physiological thresholds.
    Returns categorized warnings, NEWS score, and clinical stability indicators.
    """
    if not vitals or not isinstance(vitals, dict):
        vitals = {}
    alerts = []
    score = 0
    categories = {}

    # 1. Blood Pressure (Systolic / Diastolic)
    systolic = vitals.get("systolic_bp")
    diastolic = vitals.get("diastolic_bp")
    if systolic is not None:
        try:
            sys_val = float(systolic)
            if sys_val < 90:
                score += 3
                alerts.append({"type": "critical", "message": f"Hypotension detected (Systolic {sys_val} mmHg < 90 mmHg). Risk of circulatory shock."})
                categories["blood_pressure"] = "Hypotension (Low)"
            elif sys_val <= 120:
                categories["blood_pressure"] = "Optimal / Normal"
            elif sys_val <= 139:
                categories["blood_pressure"] = "Elevated / Prehypertension"
            elif sys_val < 180:
                score += 1
                alerts.append({"type": "warning", "message": f"Hypertension Stage 1/2 detected (Systolic {sys_val} mmHg)."})
                categories["blood_pressure"] = "Hypertension"
            else:
                score += 3
                alerts.append({"type": "critical", "message": f"Hypertensive Crisis alert (Systolic {sys_val} mmHg >= 180 mmHg). Urgent medical management required."})
                categories["blood_pressure"] = "Hypertensive Crisis"
        except (ValueError, TypeError):
            pass

    if diastolic is not None:
        try:
            dia_val = float(diastolic)
            if dia_val >= 120:
                score += 3
                alerts.append({"type": "critical", "message": f"Critical Diastolic pressure ({dia_val} mmHg >= 120 mmHg)."})
        except (ValueError, TypeError):
            pass

    # 2. Heart Rate / Pulse
    heart_rate = vitals.get("heart_rate")
    if heart_rate is not None:
        try:
            hr = float(heart_rate)
            if hr < 40:
                score += 3
                alerts.append({"type": "critical", "message": f"Severe Bradycardia (Heart rate {hr} bpm < 40 bpm)."})
                categories["heart_rate"] = "Severe Bradycardia"
            elif hr < 51:
                score += 1
                alerts.append({"type": "warning", "message": f"Bradycardia (Heart rate {hr} bpm)."})
                categories["heart_rate"] = "Bradycardia"
            elif hr <= 90:
                categories["heart_rate"] = "Normal"
            elif hr <= 110:
                score += 1
                alerts.append({"type": "info", "message": f"Mild Tachycardia (Heart rate {hr} bpm)."})
                categories["heart_rate"] = "Mild Tachycardia"
            elif hr <= 130:
                score += 2
                alerts.append({"type": "warning", "message": f"Moderate Tachycardia (Heart rate {hr} bpm)."})
                categories["heart_rate"] = "Moderate Tachycardia"
            else:
                score += 3
                alerts.append({"type": "critical", "message": f"Severe Tachycardia ({hr} bpm > 130 bpm). Requires urgent ECG."})
                categories["heart_rate"] = "Severe Tachycardia"
        except (ValueError, TypeError):
            pass

    # 3. Oxygen Saturation (SpO2)
    spo2 = vitals.get("spo2")
    if spo2 is not None:
        try:
            o2 = float(spo2)
            if o2 >= 96:
                categories["spo2"] = "Optimal Oxygenation"
            elif o2 >= 93:
                score += 1
                categories["spo2"] = "Mild Hypoxia (Borderline)"
                alerts.append({"type": "warning", "message": f"Mild Hypoxia: SpO2 is {o2}%. Close monitoring advised."})
            elif o2 >= 88:
                score += 2
                categories["spo2"] = "Moderate Hypoxia"
                alerts.append({"type": "critical", "message": f"Moderate Hypoxia detected (SpO2 {o2}%). Supplementary oxygen recommended."})
            else:
                score += 3
                categories["spo2"] = "Severe Hypoxia"
                alerts.append({"type": "critical", "message": f"CRITICAL HYPOXIA (SpO2 {o2}% < 88%). Immediate emergency oxygen therapy needed."})
        except (ValueError, TypeError):
            pass

    # 4. Temperature (°C or converted from °F)
    temp = vitals.get("temperature")
    if temp is not None:
        try:
            t = float(temp)
            # If temp > 60, assume Fahrenheit and convert
            if t > 60:
                t = round((t - 32) * 5 / 9, 1)

            if t < 35.0:
                score += 3
                alerts.append({"type": "critical", "message": f"Hypothermia ({t}°C / {round(t*9/5+32, 1)}°F). Re-warming required."})
                categories["temperature"] = "Hypothermia"
            elif t <= 36.0:
                score += 1
                categories["temperature"] = "Subnormal"
            elif t <= 37.5:
                categories["temperature"] = "Afebrile (Normal)"
            elif t <= 38.5:
                score += 1
                alerts.append({"type": "info", "message": f"Low-grade fever ({t}°C / {round(t*9/5+32, 1)}°F)."})
                categories["temperature"] = "Low-Grade Pyrexia"
            elif t <= 39.5:
                score += 2
                alerts.append({"type": "warning", "message": f"High fever ({t}°C / {round(t*9/5+32, 1)}°F). Antipyretic indicated."})
                categories["temperature"] = "High Pyrexia"
            else:
                score += 3
                alerts.append({"type": "critical", "message": f"Hyperpyrexia ({t}°C / {round(t*9/5+32, 1)}°F > 39.5°C). Urgent active cooling needed."})
                categories["temperature"] = "Hyperpyrexia"
        except (ValueError, TypeError):
            pass

    # 5. Respiratory Rate
    resp_rate = vitals.get("respiratory_rate")
    if resp_rate is not None:
        try:
            rr = float(resp_rate)
            if rr < 9:
                score += 3
                alerts.append({"type": "critical", "message": f"Severe Bradypnea (Respiratory rate {rr}/min). Impending respiratory arrest."})
                categories["respiratory_rate"] = "Bradypnea"
            elif rr <= 11:
                score += 1
                categories["respiratory_rate"] = "Borderline Slow"
            elif rr <= 20:
                categories["respiratory_rate"] = "Normal Eupnea"
            elif rr <= 24:
                score += 2
                alerts.append({"type": "warning", "message": f"Tachypnea ({rr}/min). Increased work of breathing."})
                categories["respiratory_rate"] = "Tachypnea"
            else:
                score += 3
                alerts.append({"type": "critical", "message": f"Severe Tachypnea ({rr}/min > 24/min). Respiratory distress."})
                categories["respiratory_rate"] = "Severe Tachypnea"
        except (ValueError, TypeError):
            pass

    # 6. Blood Glucose
    glucose = vitals.get("glucose")
    if glucose is not None:
        try:
            glu = float(glucose)
            if glu < 54:
                score += 3
                alerts.append({"type": "critical", "message": f"Critical Severe Hypoglycemia ({glu} mg/dL). Immediate oral simple sugars or IV Dextrose 50%."})
                categories["glucose"] = "Critical Hypoglycemia"
            elif glu < 70:
                score += 2
                alerts.append({"type": "warning", "message": f"Hypoglycemia ({glu} mg/dL). Patient requires fast-acting carbohydrate snack."})
                categories["glucose"] = "Hypoglycemia"
            elif glu <= 140:
                categories["glucose"] = "Normal Range"
            elif glu <= 200:
                categories["glucose"] = "Elevated Hyperglycemia"
            elif glu <= 300:
                score += 1
                alerts.append({"type": "warning", "message": f"Marked Hyperglycemia ({glu} mg/dL)."})
                categories["glucose"] = "Marked Hyperglycemia"
            else:
                score += 3
                alerts.append({"type": "critical", "message": f"Critical Hyperglycemia ({glu} mg/dL > 300 mg/dL). High risk of DKA or HHS."})
                categories["glucose"] = "Critical Hyperglycemia"
        except (ValueError, TypeError):
            pass

    # 7. BMI Calculation
    height = vitals.get("height_cm")
    weight = vitals.get("weight_kg")
    bmi = None
    bmi_category = None
    if height and weight:
        try:
            h_m = float(height) / 100.0
            w_kg = float(weight)
            if h_m > 0 and w_kg > 0:
                bmi = round(w_kg / (h_m * h_m), 1)
                if bmi < 18.5:
                    bmi_category = "Underweight"
                elif bmi < 25.0:
                    bmi_category = "Normal Weight"
                elif bmi < 30.0:
                    bmi_category = "Overweight"
                elif bmi < 35.0:
                    bmi_category = "Obesity (Class I)"
                else:
                    bmi_category = "Severe Obesity (Class II/III)"
        except (ValueError, TypeError):
            pass

    # Determine Overall Vital Risk Level
    if score >= 5 or any(a["type"] == "critical" for a in alerts):
        vital_triage = "High Risk / Critical"
        vital_color = "red"
    elif score >= 2:
        vital_triage = "Medium Risk / Caution"
        vital_color = "amber"
    else:
        vital_triage = "Low Risk / Stable"
        vital_color = "green"

    return {
        "news2_score": score,
        "vital_triage": vital_triage,
        "vital_color": vital_color,
        "alerts": alerts,
        "categories": categories,
        "bmi": bmi,
        "bmi_category": bmi_category
    }
