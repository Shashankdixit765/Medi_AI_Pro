"""
Healthcare Diagnosis Knowledge Base
Curated Clinical Conditions, ICD-10 Codes, Symptoms, Red Flags, and Diagnostics.
Architected by Shashank Dixit
"""

DISEASES_DB = [
    {
        "id": "acute_coronary_syndrome",
        "name": "Acute Coronary Syndrome (Myocardial Infarction / Angina)",
        "system": "Cardiovascular",
        "icd10": "I21.9",
        "urgency": "Emergency",
        "primary_symptoms": ["chest_pain", "chest_tightness", "radiating_arm_pain", "radiating_jaw_pain", "shortness_of_breath", "diaphoresis"],
        "secondary_symptoms": ["nausea", "dizziness", "fatigue", "palpitations", "anxiety"],
        "red_flags": [
            "Crushing retrosternal chest pressure lasting > 15 minutes",
            "Radiation of pain to left arm, neck, or jaw",
            "Associated diaphoresis (cold clammy sweat) and dyspnea",
            "History of coronary artery disease or multiple cardiovascular risk factors"
        ],
        "recommended_tests": [
            "Immediate 12-lead Electrocardiogram (ECG)",
            "Serial Cardiac Troponin (cTnI / cTnT)",
            "Complete Blood Count (CBC) and Basic Metabolic Panel (BMP)",
            "Echocardiogram (TTE)",
            "Coronary Angiography if STEMI or high-risk NSTEMI"
        ],
        "clinical_management": [
            "Call emergency medical services (112 / 108 / 911) IMMEDIATELY.",
            "Administer chewed Aspirin 300mg immediately (unless contraindicated / allergic).",
            "Keep patient in semi-recumbent position and minimize physical exertion.",
            "Administer supplemental oxygen if SpO2 < 90%.",
            "Sublingual Nitroglycerin if systolic BP > 100 mmHg and no recent PDE-5 inhibitor use."
        ],
        "description": "Critical acute reduction of blood flow through coronary arteries, potentially causing myocardial ischemia or infarction."
    },
    {
        "id": "ischemic_stroke",
        "name": "Acute Ischemic Stroke / Transient Ischemic Attack (TIA)",
        "system": "Neurological",
        "icd10": "I63.9",
        "urgency": "Emergency",
        "primary_symptoms": ["facial_droop", "arm_weakness", "speech_difficulty", "sudden_numbness", "vision_loss", "ataxia"],
        "secondary_symptoms": ["severe_headache", "confusion", "dizziness", "loss_of_balance"],
        "red_flags": [
            "Sudden unilateral facial droop or asymmetric smile",
            "Sudden arm or leg weakness / inability to lift arm",
            "Slurred speech, aphasia, or inability to comprehend speech",
            "Sudden onset diplopia, monocular blindness, or hemianopia"
        ],
        "recommended_tests": [
            "Emergent non-contrast CT Head to exclude intracerebral hemorrhage",
            "CT Angiography (CTA) of head and neck for large vessel occlusion (LVO)",
            "Blood glucose immediately (to rule out severe hypoglycemia)",
            "Coagulation profile (PT/INR, aPTT)",
            "ECG and telemetry monitoring (screen for Atrial Fibrillation)"
        ],
        "clinical_management": [
            "CALL EMERGENCY RESCUE IMMEDIATELY — TIME IS BRAIN (4.5 hr thrombolysis window).",
            "Note exact 'Time Last Known Well' (TLKW).",
            "Do NOT administer aspirin or oral food/liquids until hemorrhage is ruled out by CT.",
            "Maintain head of bed flat or slightly elevated (15-30 degrees) if not vomiting.",
            "Avoid aggressive blood pressure lowering unless BP > 220/120 mmHg or thrombolysis candidate."
        ],
        "description": "Focal neurological deficit caused by rapid occlusion of cerebral vasculature leading to cerebral tissue ischemia."
    },
    {
        "id": "pneumonia_community",
        "name": "Community-Acquired Pneumonia (CAP)",
        "system": "Respiratory",
        "icd10": "J18.9",
        "urgency": "Urgent",
        "primary_symptoms": ["productive_cough", "fever", "chills", "shortness_of_breath", "pleuritic_chest_pain"],
        "secondary_symptoms": ["fatigue", "loss_of_appetite", "green_yellow_sputum", "myalgia", "tachypnea"],
        "red_flags": [
            "SpO2 < 92% on room air",
            "Respiratory rate > 30 breaths per minute",
            "Confusion or altered mental status (CURB-65 criteria)",
            "Hemoptysis (coughing up fresh blood)"
        ],
        "recommended_tests": [
            "Chest X-Ray (PA and lateral views)",
            "Complete Blood Count (CBC with differential — leukocytosis with left shift)",
            "C-Reactive Protein (CRP) / Procalcitonin",
            "Sputum gram stain and culture",
            "Pulse oximetry and arterial blood gas if severe"
        ],
        "clinical_management": [
            "Empirical antimicrobial therapy tailored to CURB-65 severity score (e.g. Amoxicillin/Clavulanate or Azithromycin).",
            "Hydration, antipyretics (Paracetamol) for fever control.",
            "Chest physiotherapy and postural drainage.",
            "Hospital admission if CURB-65 score >= 2 or oxygen desaturation."
        ],
        "description": "Acute infection of the pulmonary parenchymal tissue by bacterial, viral, or fungal pathogens."
    },
    {
        "id": "acute_appendicitis",
        "name": "Acute Appendicitis",
        "system": "Gastrointestinal",
        "icd10": "K35.8",
        "urgency": "Emergency",
        "primary_symptoms": ["abdominal_pain", "right_lower_quadrant_pain", "periumbilical_pain", "anorexia", "nausea", "vomiting"],
        "secondary_symptoms": ["low_grade_fever", "rebound_tenderness", "constipation", "diarrhea"],
        "red_flags": [
            "Migration of pain from periumbilical region to McBurney's point (right iliac fossa)",
            "Marked rebound tenderness and involuntary abdominal guarding (peritonitis risk)",
            "High spike fever with sudden relief of pain (suggests perforation)",
            "Inability to tolerate any oral intake"
        ],
        "recommended_tests": [
            "Abdominal Ultrasound (graded compression technique)",
            "Contrast-enhanced CT scan of abdomen & pelvis",
            "CBC with differential (marked neutrophilia)",
            "Serum Beta-hCG (in women of childbearing age to exclude ectopic pregnancy)",
            "Urinalysis (rule out nephrolithiasis or UTI)"
        ],
        "clinical_management": [
            "Nil per Os (NPO / Nothing by mouth) immediately in anticipation of surgery.",
            "Prompt surgical consultation for laparoscopic or open appendectomy.",
            "Intravenous crystalloid fluids and IV broad-spectrum antibiotics.",
            "Adequate intravenous analgesia once surgical evaluation is underway."
        ],
        "description": "Acute inflammation and obstruction of the vermiform appendix, risking gangrene and perforation."
    },
    {
        "id": "type2_diabetes_hyperglycemia",
        "name": "Type 2 Diabetes Mellitus / Decompensated Hyperglycemia",
        "system": "Endocrine",
        "icd10": "E11.9",
        "urgency": "Urgent",
        "primary_symptoms": ["polyuria", "polydipsia", "unexplained_weight_loss", "fatigue", "blurred_vision"],
        "secondary_symptoms": ["slow_healing_sores", "frequent_infections", "paresthesia", "dry_mouth"],
        "red_flags": [
            "Kussmaul breathing (deep, rapid respirations) and fruity breath odor (DKA warning)",
            "Random blood glucose > 300 mg/dL or presence of urinary ketones",
            "Severe dehydration, lethargy, or confusion (Hyperosmolar Hyperglycemic State)",
            "Non-healing diabetic foot ulcers with signs of infection/gangrene"
        ],
        "recommended_tests": [
            "Fasting Plasma Glucose (FPG) and 2-hour Postprandial Glucose (PPG)",
            "Glycated Hemoglobin (HbA1c)",
            "Urine microalbumin-to-creatinine ratio (ACR)",
            "Comprehensive Metabolic Panel (CMP) including serum creatinine and eGFR",
            "Lipid Profile (Total cholesterol, LDL, HDL, Triglycerides)"
        ],
        "clinical_management": [
            "Lifestyle modification: Medical nutrition therapy (low glycemic index) and 150 min/week moderate aerobic exercise.",
            "First-line pharmacotherapy: Metformin (titrated) unless eGFR < 30 mL/min.",
            "Consider SGLT2 inhibitors or GLP-1 receptor agonists if atherosclerotic CVD, heart failure, or CKD present.",
            "Self-monitoring of blood glucose (SMBG) and annual diabetic retinopathy/podiatry screening."
        ],
        "description": "Chronic metabolic disorder characterized by insulin resistance and relative insulin deficiency resulting in persistent hyperglycemia."
    },
    {
        "id": "hypertension_stage2",
        "name": "Essential Hypertension / Hypertensive Urgency",
        "system": "Cardiovascular",
        "icd10": "I10",
        "urgency": "Urgent",
        "primary_symptoms": ["elevated_bp", "headache", "occipital_pain", "dizziness", "palpitations"],
        "secondary_symptoms": ["epistaxis", "visual_blurring", "tinnitus", "fatigue"],
        "red_flags": [
            "Blood pressure >= 180/120 mmHg with target organ damage (Hypertensive Emergency)",
            "Chest pain, acute pulmonary edema (severe shortness of breath)",
            "Papilledema, acute encephalopathy, or focal neurological deficit",
            "Acute renal failure or hematuria"
        ],
        "recommended_tests": [
            "Automated repeated resting blood pressure measurements",
            "12-Lead ECG (assess left ventricular hypertrophy)",
            "Serum Electrolytes (Sodium, Potassium) and Serum Creatinine",
            "Urinalysis (screen for proteinuria / hematuria)",
            "Fasting lipid panel and fasting blood sugar"
        ],
        "clinical_management": [
            "If Hypertensive Emergency (organ damage present): immediate ICU admission with IV titratable antihypertensives (e.g. Labetalol, Nicardipine).",
            "If Hypertensive Urgency (no organ damage): Oral antihypertensive therapy (ACE-i, ARB, CCB, or Thiazide) with outpatient titration.",
            "Dietary Approaches to Stop Hypertension (DASH) diet with sodium reduction (< 2000 mg/day).",
            "Cessation of smoking, weight reduction, and moderation of alcohol."
        ],
        "description": "Sustained arterial systemic blood pressure >= 140/90 mmHg increasing long-term risk of stroke, myocardial infarction, and kidney failure."
    },
    {
        "id": "bronchial_asthma_exacerbation",
        "name": "Bronchial Asthma / Acute Exacerbation",
        "system": "Respiratory",
        "icd10": "J45.901",
        "urgency": "Urgent",
        "primary_symptoms": ["wheezing", "shortness_of_breath", "chest_tightness", "dry_cough", "nocturnal_cough"],
        "secondary_symptoms": ["rapid_breathing", "accessory_muscle_use", "anxiety", "difficulty_speaking"],
        "red_flags": [
            "'Silent chest' on auscultation (minimal air movement, imminent respiratory arrest)",
            "Peak Expiratory Flow Rate (PEFR) < 50% of predicted/personal best",
            "Cyanosis, exhaustion, bradycardia, or confusion",
            "Inability to speak complete sentences in one breath"
        ],
        "recommended_tests": [
            "Spirometry / Peak Expiratory Flow (PEF) pre- and post-bronchodilator",
            "Pulse oximetry (monitor continuous SpO2)",
            "Arterial Blood Gas (ABG) if severe distress or deteriorating",
            "Chest X-Ray (to exclude pneumothorax or consolidated pneumonia)"
        ],
        "clinical_management": [
            "Inhaled short-acting beta-2 agonist (SABA - Salbutamol 4-8 puffs via spacer or nebulizer).",
            "Oral systemic corticosteroids (Prednisone 40-50 mg daily for 5-7 days).",
            "Inhaled Ipratropium bromide added for moderate to severe exacerbations.",
            "Supplemental high-flow oxygen to maintain SpO2 93-95%."
        ],
        "description": "Chronic inflammatory airway disease featuring episodic reversible bronchospasm, mucosal edema, and mucus hypersecretion."
    },
    {
        "id": "gastroesophageal_reflux_disease",
        "name": "Gastroesophageal Reflux Disease (GERD) / Dyspepsia",
        "system": "Gastrointestinal",
        "icd10": "K21.9",
        "urgency": "Routine",
        "primary_symptoms": ["heartburn", "acid_regurgitation", "epigastric_pain", "retrosternal_burning"],
        "secondary_symptoms": ["dysphagia", "sour_taste", "chronic_cough", "globus_sensation", "hoarseness"],
        "red_flags": [
            "Progressive dysphagia (difficulty swallowing) or odynophagia (painful swallowing)",
            "Unintentional significant weight loss",
            "Persistent vomiting or hematemesis (coffee-ground emesis)",
            "New onset dyspeptic symptoms in patients aged > 55 years"
        ],
        "recommended_tests": [
            "Upper Gastrointestinal Endoscopy (EGD) if alarm features present",
            "Helicobacter pylori stool antigen or urea breath test",
            "24-Hour Ambulatory Esophageal pH/Impedance monitoring (refractory cases)",
            "Complete Blood Count (rule out microcytic iron deficiency anemia)"
        ],
        "clinical_management": [
            "Trial of daily Proton Pump Inhibitors (e.g. Omeprazole 20mg or Pantoprazole 40mg before breakfast for 4-8 weeks).",
            "Elevate head of bed by 15-20 cm and avoid meals within 3 hours of sleeping.",
            "Avoid dietary triggers (caffeine, chocolate, fatty foods, peppermint, citrus, alcohol).",
            "Weight management and avoidance of tight-fitting abdominal garments."
        ],
        "description": "Retrograde flow of gastric contents into the esophagus causing troublesome mucosal irritation and discomfort."
    },
    {
        "id": "urinary_tract_infection_pyelonephritis",
        "name": "Urinary Tract Infection (UTI) / Acute Pyelonephritis",
        "system": "Genitourinary",
        "icd10": "N39.0",
        "urgency": "Urgent",
        "primary_symptoms": ["dysuria", "urinary_frequency", "urinary_urgency", "suprapubic_pain", "cloudy_urine"],
        "secondary_symptoms": ["flank_pain", "fever_with_rigors", "hematuria", "foul_smelling_urine", "nausea"],
        "red_flags": [
            "High fever with costovertebral angle tenderness (renal flank tenderness -> Pyelonephritis)",
            "Gross visible hematuria or inability to pass urine (acute urinary retention)",
            "Septic signs: hypotension, tachycardia, altered mental state (urosepsis risk)",
            "UTI symptoms in pregnancy or immunocompromised patients"
        ],
        "recommended_tests": [
            "Urinalysis (Urine dipstick: leukocyte esterase and nitrites)",
            "Urine microscopy (pyuria, bacteriuria, WBC casts)",
            "Urine culture and antimicrobial sensitivity (clean-catch midstream)",
            "Renal Ultrasound if suspected nephrolithiasis, obstruction, or refractory pyelonephritis"
        ],
        "clinical_management": [
            "Targeted antibiotic therapy (e.g., Nitrofurantoin 100mg BID for uncomplicated cystitis, or Ceftriaxone/Ciprofloxacin for pyelonephritis).",
            "Generous oral hydration to facilitate urinary tract flushing.",
            "Urinary analgesics (e.g. Phenazopyridine) for symptomatic burning relief for up to 48 hours.",
            "Re-evaluate after 48-72 hours if fever or symptoms persist."
        ],
        "description": "Infection of the lower or upper urinary tract, predominantly caused by uropathogenic Escherichia coli."
    },
    {
        "id": "migraine_with_without_aura",
        "name": "Migraine Headache (with or without Aura)",
        "system": "Neurological",
        "icd10": "G43.909",
        "urgency": "Routine",
        "primary_symptoms": ["throbbing_headache", "unilateral_headache", "photophobia", "phonophobia", "nausea"],
        "secondary_symptoms": ["visual_aura", "scotoma", "vomiting", "neck_stiffness_mild", "fatigue"],
        "red_flags": [
            "Sudden explosive thunderclap headache reaching maximum severity in < 1 minute (rule out Subarachnoid Hemorrhage)",
            "Headache accompanied by high fever, petechial rash, and rigid neck (rule out Bacterial Meningitis)",
            "New onset focal neurological deficit that persists > 60 minutes",
            "New onset headache in patient with history of malignancy or age > 50"
        ],
        "recommended_tests": [
            "Clinical diagnosis per International Classification of Headache Disorders (ICHD-3)",
            "Neuroimaging (Brain MRI or non-contrast CT) if red flag symptoms present",
            "Fundoscopy to inspect optic discs for papilledema",
            "Erythrocyte sedimentation rate (ESR) in patients > 50 (screen for Giant Cell Arteritis)"
        ],
        "clinical_management": [
            "Acute abortive therapy: Triptans (e.g. Sumatriptan 50-100mg) or NSAIDs (Naproxen 500mg) taken early in attack.",
            "Antiemetics (Metoclopramide or Ondansetron) for associated nausea.",
            "Rest in a quiet, darkened room with adequate oral hydration.",
            "Preventive therapy (Propranolol, Topiramate, or Amitriptyline) if >= 4 disabling headache days per month."
        ],
        "description": "Neurovascular disorder marked by recurrent severe unilateral pulsating headaches often triggered by stress, sensory stimuli, or hormonal fluctuations."
    },
    {
        "id": "generalized_anxiety_panic_disorder",
        "name": "Generalized Anxiety / Acute Panic Episode",
        "system": "Psychiatric",
        "icd10": "F41.1",
        "urgency": "Routine",
        "primary_symptoms": ["anxiety", "palpitations", "hyperventilation", "tremor", "sweating", "impending_doom"],
        "secondary_symptoms": ["dizziness", "chest_tightness", "paresthesia", "insomnia", "muscle_tension"],
        "red_flags": [
            "Active suicidal ideation or intent (Immediate emergency intervention required)",
            "Must strictly rule out acute organic emergencies (Myocardial Infarction, Pulmonary Embolism, Thyrotoxicosis, Hypoglycemia)",
            "Extreme agitation with psychotic features or severe drug toxicity"
        ],
        "recommended_tests": [
            "Screening ECG to rule out underlying arrhythmia or ischemia",
            "Thyroid Stimulating Hormone (TSH) to exclude hyperthyroidism",
            "Fingerstick blood glucose to exclude hypoglycemia",
            "Complete Blood Count and basic toxicology screen if clinically indicated",
            "Validated psychometric screening (GAD-7 and PHQ-9)"
        ],
        "clinical_management": [
            "Immediate grounding techniques: 4-7-8 diaphragmatic breathing and cognitive reassurance.",
            "Cognitive Behavioral Therapy (CBT) as the gold standard non-pharmacological treatment.",
            "Pharmacotherapy: SSRIs / SNRIs (e.g. Sertraline or Escitalopram) as first-line maintenance.",
            "Limit stimulant intake (caffeine, energy drinks, nicotine) and practice structured sleep hygiene."
        ],
        "description": "Excessive, uncontrollable worry and physiological autonomic arousal characterized by palpitations, tremulousness, and dyspnea."
    },
    {
        "id": "osteoarthritis_knee_hip",
        "name": "Degenerative Joint Disease (Osteoarthritis)",
        "system": "Musculoskeletal",
        "icd10": "M19.90",
        "urgency": "Routine",
        "primary_symptoms": ["joint_pain", "joint_stiffness", "reduced_range_of_motion", "crepitus", "pain_worse_with_activity"],
        "secondary_symptoms": ["morning_stiffness_brief", "bony_enlargement", "joint_swelling", "instability"],
        "red_flags": [
            "Acutely hot, swollen, erythematous single joint with severe pain (rule out Septic Arthritis)",
            "Systemic symptoms: high fever, unexplained weight loss, night sweats",
            "Morning stiffness persisting > 1 hour (suggests inflammatory arthritis like Rheumatoid Arthritis)",
            "Sudden loss of joint function or suspected fracture after trauma"
        ],
        "recommended_tests": [
            "Weight-bearing Plain Radiographs (X-rays) showing joint space narrowing, subchondral sclerosis, and osteophytes",
            "Arthrocentesis (synovial fluid analysis) if acute joint effusion present to rule out infection or crystals (gout/pseudogout)",
            "ESR and CRP (typically normal in osteoarthritis)",
            "Rheumatoid Factor (RF) and Anti-CCP if inflammatory arthritis suspected"
        ],
        "clinical_management": [
            "Low-impact aerobic physical therapy, quadriceps strengthening, and weight reduction (reduces knee joint load by 4x).",
            "First-line topical NSAIDs (e.g., Diclofenac gel) followed by oral NSAIDs at lowest effective dose.",
            "Assistive devices (walking canes, knee braces) and shock-absorbing footwear.",
            "Intra-articular corticosteroid or hyaluronic acid injections for symptomatic flare-ups; orthopedic referral for joint arthroplasty if refractory."
        ],
        "description": "Progressive mechanical and biochemical wear-and-tear degradation of articular cartilage and underlying subchondral bone."
    },
    {
        "id": "acute_viral_gastroenteritis",
        "name": "Acute Viral Gastroenteritis (Stomach Flu)",
        "system": "Gastrointestinal",
        "icd10": "A08.4",
        "urgency": "Routine",
        "primary_symptoms": ["watery_diarrhea", "nausea", "vomiting", "abdominal_cramps", "low_grade_fever"],
        "secondary_symptoms": ["headache", "myalgia", "dehydration", "dry_mouth"],
        "red_flags": [
            "Signs of severe dehydration: sunken eyes, skin turgor loss, anuria, postural hypotension",
            "Bloody or mucoid stools (dysentery -> bacterial etiology like Salmonella/Shigella)",
            "Severe localized unremitting abdominal pain",
            "Diarrhea persisting > 7 days or inability to retain fluids for > 24 hours"
        ],
        "recommended_tests": [
            "Clinical evaluation primarily",
            "Serum electrolytes (Sodium, Potassium, Bicarbonate) and Creatinine if marked dehydration",
            "Stool routine microscopy, culture, and Clostridioides difficile toxin PCR if severe or prolonged",
            "Stool viral antigen multiplex panel (Norovirus, Rotavirus)"
        ],
        "clinical_management": [
            "Oral Rehydration Therapy (WHO ORS) taken in frequent small sips.",
            "Gradual resumption of light, bland diet (BRAT: Bananas, Rice, Applesauce, Toast).",
            "Antiemetics (Ondansetron 4-8mg) if needed to facilitate oral rehydration.",
            "Avoid antimotility agents (Loperamide) in cases with fever or bloody stools."
        ],
        "description": "Acute viral infection of the gastrointestinal tract mucosa, typically self-limiting within 2 to 5 days."
    },
    {
        "id": "covid19_viral_respiratory_infection",
        "name": "COVID-19 / Acute Upper Respiratory Viral Infection",
        "system": "Respiratory",
        "icd10": "U07.1",
        "urgency": "Urgent",
        "primary_symptoms": ["fever", "dry_cough", "fatigue", "loss_of_taste_smell", "sore_throat", "nasal_congestion"],
        "secondary_symptoms": ["body_aches", "headache", "diarrhea", "shortness_of_breath"],
        "red_flags": [
            "SpO2 dropping below 93% on room air",
            "Persistent thoracic pain or pressure",
            "New onset confusion, lethargy, or inability to wake up",
            "Pale, gray, or blue-colored skin, lips, or nail beds (cyanosis)"
        ],
        "recommended_tests": [
            "Rapid SARS-CoV-2 Antigen Test or RT-PCR Nasopharyngeal Swab",
            "Continuous pulse oximetry monitoring (6-minute walk test if borderline)",
            "Complete Blood Count (lymphopenia is a characteristic feature)",
            "Inflammatory markers (Ferritin, D-Dimer, CRP) in high-risk patients",
            "Chest CT or X-ray if respiratory compromise occurs"
        ],
        "clinical_management": [
            "Home isolation with respiratory precautions to prevent transmission.",
            "Rest, adequate hydration, Paracetamol for pyrexia and myalgias.",
            "Early antiviral therapy (e.g. Nirmatrelvir/Ritonavir - Paxlovid) within 5 days of onset for high-risk individuals.",
            "Immediate hospital evaluation if SpO2 drops or breathing difficulty accelerates."
        ],
        "description": "Infection caused by SARS-CoV-2 targeting the respiratory epithelium with potential for systemic hyperinflammatory cascade."
    },
    {
        "id": "allergic_rhinitis_sinusitis",
        "name": "Allergic Rhinitis / Acute Rhino-Sinusitis",
        "system": "ENT",
        "icd10": "J30.9",
        "urgency": "Routine",
        "primary_symptoms": ["sneezing", "clear_rhinorrhea", "nasal_congestion", "itchy_watery_eyes", "facial_pressure"],
        "secondary_symptoms": ["post_nasal_drip", "fatigue", "dry_cough", "headache"],
        "red_flags": [
            "Periorbital swelling, erythema, or ophthalmoplegia (orbital cellulitis risk)",
            "Severe unilateral forehead pain with high fever",
            "Visual disturbances or double vision",
            "Signs of meningeal irritation (stiff neck, altered consciousness)"
        ],
        "recommended_tests": [
            "Clinical diagnosis through anterior rhinoscopy",
            "Allergen-specific IgE blood testing (RAST) or skin prick allergy testing",
            "Sinus CT scan without contrast (reserved for chronic or complicated sinusitis)"
        ],
        "clinical_management": [
            "Intranasal corticosteroid spray (Fluticasone or Mometasone 1-2 sprays per nostril daily).",
            "Second-generation non-sedating oral antihistamines (Cetirizine, Loratadine, or Fexofenadine).",
            "Isotonic nasal saline irrigation (Neti pot / saline spray) to clear mucosal allergens.",
            "Environmental allergen avoidance (HEPA air filters, anti-dust mite covers)."
        ],
        "description": "IgE-mediated inflammatory response of the nasal mucous membranes to airborne environmental allergens."
    }
]

SYMPTOM_DICTIONARY = {
    "chest_pain": "Chest pain, pressure, or tightness",
    "chest_tightness": "Feeling of heaviness or constriction in the chest",
    "radiating_arm_pain": "Pain radiating into the left or right arm",
    "radiating_jaw_pain": "Pain radiating to the jaw, neck, or teeth",
    "shortness_of_breath": "Dyspnea or difficulty breathing",
    "diaphoresis": "Profuse cold sweat / perspiration",
    "facial_droop": "One side of the face drooping or numb",
    "arm_weakness": "Arm drifting down or inability to lift limb",
    "speech_difficulty": "Slurred speech or difficulty finding words",
    "sudden_numbness": "Sudden loss of sensation on one side of body",
    "vision_loss": "Sudden blurriness, double vision, or blindness",
    "ataxia": "Loss of coordination or unstable walking",
    "productive_cough": "Cough with yellow, green, or rusty sputum",
    "fever": "Body temperature elevated above 38.0°C (100.4°F)",
    "chills": "Rigors or shivering episodes",
    "pleuritic_chest_pain": "Sharp chest pain worsening on deep inspiration",
    "abdominal_pain": "Generalized or localized abdominal discomfort",
    "right_lower_quadrant_pain": "Sharp pain in lower right quadrant (RLQ)",
    "periumbilical_pain": "Dull ache around the navel",
    "anorexia": "Total loss of appetite",
    "nausea": "Sensation of wanting to vomit",
    "vomiting": "Expulsion of stomach contents",
    "polyuria": "Excessive and frequent urination",
    "polydipsia": "Extreme, unquenchable thirst",
    "unexplained_weight_loss": "Rapid unintended loss of body weight",
    "elevated_bp": "Blood pressure reading >= 140/90 mmHg",
    "wheezing": "High-pitched whistling sound during breathing",
    "heartburn": "Burning retrosternal sensation behind the breastbone",
    "acid_regurgitation": "Sour or bitter fluid rising into throat",
    "dysuria": "Burning or stinging sensation during urination",
    "urinary_frequency": "Need to urinate very frequently in small amounts",
    "urinary_urgency": "Sudden intense urge to urinate",
    "throbbing_headache": "Pulsating intense head pain",
    "photophobia": "Sensitivity to bright light",
    "phonophobia": "Sensitivity to loud sounds",
    "joint_pain": "Aching or stiffness in joints (knees, hips, fingers)",
    "joint_stiffness": "Stiffness after periods of inactivity",
    "watery_diarrhea": "Frequent loose watery bowel movements",
    "loss_of_taste_smell": "Anosmia or ageusia (loss of smell or taste)",
    "sneezing": "Frequent paroxysmal sneezing",
    "nasal_congestion": "Blocked or stuffy nasal passages"
}

BODY_SYSTEMS = [
    {"id": "Cardiovascular", "name": "Cardiovascular & Heart", "icon": "fa-heart-pulse"},
    {"id": "Respiratory", "name": "Lungs & Respiratory", "icon": "fa-lungs"},
    {"id": "Neurological", "name": "Brain & Nervous System", "icon": "fa-brain"},
    {"id": "Gastrointestinal", "name": "Stomach & Digestion", "icon": "fa-stethoscope"},
    {"id": "Endocrine", "name": "Endocrine & Metabolic", "icon": "fa-dna"},
    {"id": "Genitourinary", "name": "Kidney & Urinary", "icon": "fa-droplet"},
    {"id": "Musculoskeletal", "name": "Bones & Joints", "icon": "fa-bone"},
    {"id": "ENT", "name": "Ear, Nose & Throat", "icon": "fa-head-side-cough"},
    {"id": "Psychiatric", "name": "Mental & Behavioral", "icon": "fa-shield-halved"}
]
