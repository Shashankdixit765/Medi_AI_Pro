# 🩺 MediAI Pro — AI-Powered Healthcare Diagnosis Assistant
### *Clinical Decision Support, Modified NEWS2 Triage, Laboratory Biomarker Analytics & AI Medical Consultation*
**Created, Architected & Engineered by [Shashank Dixit]**

---

## 🌟 Executive Overview
**MediAI Pro** is a modern, responsive, and clinical-grade full-stack web application designed to support patients and clinicians with early risk stratification, automated triage, differential diagnoses, vital signs assessment, and lab report interpretation.

Built with a **Dual AI Engine Architecture**, MediAI Pro operates seamlessly offline using an internal clinical reasoning matrix and modified NEWS2 (National Early Warning Score) system, with optional generative intelligence powered by the Google Gemini API.

---

## ✨ Key Capabilities & Modules

### 1. 🩺 Multi-Modal Symptom Checker & Triage
- **Natural Language Narrative Analysis**: Describe complaints in free text (e.g. *"crushing chest pain radiating to left arm"*).
- **Body System Filters**: Cardiovascular, Respiratory, Neurological, Gastrointestinal, Endocrine, Genitourinary, Musculoskeletal, ENT, and Psychiatric.
- **Dynamic Symptom Tag Grid**: 40+ searchable symptom tags with real-time selection counters.
- **Patient Profile & Risk Modifiers**: Age, biological sex, comorbidities (Hypertension, Diabetes, Asthma, Coronary Artery Disease), smoking, and pregnancy status.
- **One-Click Instant Preset Scenarios**: Quick tests for Acute Coronary Syndrome, Community-Acquired Pneumonia, Acute Appendicitis, and Severe Migraine.

### 2. 💓 Modified NEWS2 Vital Signs & Biometrics Assessment
- Physiological threshold monitoring for:
  - **Blood Pressure**: Systolic & Diastolic (Hypotension, Stage 1/2 Hypertension, Hypertensive Crisis).
  - **Heart Rate**: Bradycardia, Normal, Tachycardia.
  - **SpO2 (Blood Oxygen %)**: Optimal, Mild Hypoxia, Critical Hypoxia (<88%).
  - **Temperature**: Hypothermia, Normal, Low/High Fever, Hyperpyrexia.
  - **Respiratory Rate**: Eupnea, Bradypnea, Tachypnea.
  - **Blood Glucose**: Hypoglycemia (<70 mg/dL) through Hyperglycemia (>300 mg/dL).
  - **Live BMI Indicator**: Real-time BMI category computation from height and weight.

### 3. 🧪 Laboratory Biomarker Analyzer
- Input grid for 15+ standard clinical biomarkers:
  - **Hematology**: Hemoglobin (Hb), White Blood Cells (WBC), Platelets.
  - **Metabolic / Endocrine**: Fasting Plasma Glucose, Glycated Hemoglobin (HbA1c).
  - **Renal Function**: Serum Creatinine, Estimated GFR (eGFR).
  - **Lipid Profile**: Total Cholesterol, LDL ("bad"), HDL ("good"), Triglycerides.
  - **Hepatic Profile**: ALT (SGPT), AST (SGOT).
  - **Inflammatory & Thyroid**: TSH, C-Reactive Protein (CRP).
- **Interactive Visual Spectrum Meters**: Shows exact pointer of patient value within biological reference intervals.
- One-click sample panel presets (Healthy Normal, Diabetic/Dyslipidemia, Renal/AKI).

### 4. 🤖 MediBot AI Conversational Assistant
- Evidence-based, empathetic medical dialogue assistant.
- Explains medical terms, vital signs, lab tests, and health questions.
- Pre-configured prompt pills for quick common inquiries.
- Includes clear safety guardrails and medical disclaimers.

### 5. 🚑 Emergency Hotlines & First-Aid Protocols
- Step-by-step interactive first aid guides:
  - **Adult CPR**: Hands-only 100-120 bpm protocol.
  - **Stroke F.A.S.T. Assessment**: Face, Arms, Speech, Time.
  - **Heart Attack Protocol**: Rest, aspirin guidelines, emergency dispatch.
  - **Choking (Heimlich Maneuver)**: Abdominal thrust sequence.
  - **Anaphylaxis Protocol**: Epinephrine auto-injector usage.
  - **Severe Hemorrhage**: Direct pressure and wound hemostasis.
- Click-to-dial Emergency Directory (Universal 112, Ambulance 108, Poison Control, Tele-MANAS).

### 6. 📄 Clinical Consultation Report Generator
- Formats a comprehensive clinical note ready to print or save as PDF.
- Summarizes patient demographics, vitals, primary diagnosis, ICD-10 codes, confidence scores, differentials, red flags, recommended diagnostics, and attending physician signature area.
- Formatted with watermark and author credit: **"Created by Shashank Dixit"**.

---

## 🏗️ Technical Architecture

```
health-ai-assistant/
│
├── app.py                      # FastAPI server with REST endpoints & Jinja2 templates
├── config.py                   # App metadata, author info, hotlines configuration
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows 1-click startup script
│
├── engine/
│   ├── __init__.py
│   ├── knowledge_base.py       # Disease database, ICD-10 codes, symptom weights
│   ├── diagnosis_engine.py     # Probabilistic multi-factor matching & triage
│   ├── emergency_triage.py     # Modified NEWS2 score & vitals evaluator
│   ├── lab_analyzer.py         # Reference intervals & biomarker interpreter
│   └── gemini_ai.py            # Gemini Generative AI integration & local fallback
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom styling, dark mode, glassmorphism, print CSS
│   └── js/
│       ├── app.js              # State manager, theme switcher, printable report
│       ├── symptom_checker.js  # Interactive triage form & dynamic results
│       ├── lab_analyzer.js     # Laboratory test evaluation & visual meters
│       └── chatbot.js          # Conversational MediBot AI assistant
│
└── templates/
    └── index.html              # Responsive single-page web application UI
```

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.10+ (Python 3.13 tested and verified)
- Modern web browser (Chrome, Edge, Firefox, Safari)

### Step 1: Open Terminal in Project Directory
```powershell
cd "C:\Users\Shashank\.gemini\antigravity\scratch\health-ai-assistant"
```

### Step 2: Install Dependencies (if not already installed)
```powershell
python -m pip install -r requirements.txt
```

### Step 3: Run the Server
Double-click `run.bat` or run:
```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### Step 4: Open in Web Browser
Navigate to:
```
http://127.0.0.1:8000
```

---

## 🔒 Security, Reliability & Privacy
- **Local-First Processing**: Patient inputs are evaluated locally by default. No personal health information (PHI) is transmitted or stored on unauthorized third-party servers.
- **Defensive Error Handling**: Full schema validation with Pydantic ensures invalid values never crash the engine.
- **Fail-Safe AI**: If an external API key is missing or the network drops, the local clinical engine takes over immediately with zero downtime.

---

## 👨‍💻 Project Attribution
- **Creator & Lead Architect**: **Shashank Dixit**
- **Project**: MediAI Pro — AI-Powered Healthcare Diagnosis Assistant
- **License**: Proprietary / Educational Open Health Initiative
