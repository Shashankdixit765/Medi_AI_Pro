"""
Clinical Laboratory Report Analyzer
Reference ranges, biomarker evaluations, and automated diagnostic summaries.
Architected by Shashank Dixit
"""

from typing import Dict, Any, List

# Standard Adult Reference Ranges
LAB_TEST_RANGES = {
    "hemoglobin": {
        "name": "Hemoglobin (Hb)",
        "unit": "g/dL",
        "low": 12.0,
        "high": 17.5,
        "critical_low": 7.0,
        "critical_high": 20.0,
        "interpretation_low": "Microcytic/Normocytic Anemia (blood loss, iron deficiency, or chronic disease).",
        "interpretation_high": "Polycythemia, chronic hypoxia, or hemoconcentration/dehydration."
    },
    "wbc": {
        "name": "White Blood Cell Count (WBC)",
        "unit": "x10^3/µL",
        "low": 4.0,
        "high": 11.0,
        "critical_low": 2.0,
        "critical_high": 30.0,
        "interpretation_low": "Leukopenia (bone marrow suppression, viral illness, or autoimmune).",
        "interpretation_high": "Leukocytosis (acute bacterial infection, systemic inflammation, or stress response)."
    },
    "platelets": {
        "name": "Platelet Count",
        "unit": "x10^3/µL",
        "low": 150.0,
        "high": 450.0,
        "critical_low": 50.0,
        "critical_high": 1000.0,
        "interpretation_low": "Thrombocytopenia (increased bleeding risk, ITP, drug-induced, or liver disease).",
        "interpretation_high": "Thrombocytosis (reactive inflammatory state or essential thrombocythemia)."
    },
    "fasting_glucose": {
        "name": "Fasting Plasma Glucose",
        "unit": "mg/dL",
        "low": 70.0,
        "high": 99.0,
        "critical_low": 54.0,
        "critical_high": 300.0,
        "interpretation_low": "Hypoglycemia (excess insulin, fasting, or endocrine disorder).",
        "interpretation_high": "Impaired Fasting Glucose (100-125: Prediabetes; >=126: Diabetes Mellitus)."
    },
    "hba1c": {
        "name": "Glycated Hemoglobin (HbA1c)",
        "unit": "%",
        "low": 4.0,
        "high": 5.6,
        "critical_low": 3.5,
        "critical_high": 12.0,
        "interpretation_low": "Below normal glycation (recent severe hemolysis or hemoglobinopathy).",
        "interpretation_high": "Prediabetes (5.7% - 6.4%) or uncontrolled Diabetes Mellitus (>= 6.5%)."
    },
    "creatinine": {
        "name": "Serum Creatinine",
        "unit": "mg/dL",
        "low": 0.6,
        "high": 1.2,
        "critical_low": 0.3,
        "critical_high": 4.0,
        "interpretation_low": "Decreased muscle mass or hyperfiltration.",
        "interpretation_high": "Impaired renal function, Acute Kidney Injury (AKI), or Chronic Kidney Disease (CKD)."
    },
    "egfr": {
        "name": "Estimated GFR (eGFR)",
        "unit": "mL/min/1.73m²",
        "low": 90.0,
        "high": 130.0,
        "critical_low": 15.0,
        "critical_high": 160.0,
        "interpretation_low": "Decreased glomerular filtration (<60: CKD Stage 3+; <15: Kidney Failure).",
        "interpretation_high": "Normal or hyperfiltration state."
    },
    "total_cholesterol": {
        "name": "Total Cholesterol",
        "unit": "mg/dL",
        "low": 120.0,
        "high": 200.0,
        "critical_low": 80.0,
        "critical_high": 350.0,
        "interpretation_low": "Severe hypocholesterolemia (malnutrition or severe liver disease).",
        "interpretation_high": "Hypercholesterolemia (elevated cardiovascular risk)."
    },
    "ldl": {
        "name": "LDL Cholesterol ('Bad' Cholesterol)",
        "unit": "mg/dL",
        "low": 50.0,
        "high": 100.0,
        "critical_low": 20.0,
        "critical_high": 190.0,
        "interpretation_low": "Low LDL level (generally favorable, or severe cachexia).",
        "interpretation_high": "Atherogenic Dyslipidemia; requires dietary intervention or Statin therapy."
    },
    "hdl": {
        "name": "HDL Cholesterol ('Good' Cholesterol)",
        "unit": "mg/dL",
        "low": 40.0,
        "high": 80.0,
        "critical_low": 25.0,
        "critical_high": 120.0,
        "interpretation_low": "Low protective HDL; heightened cardiovascular risk.",
        "interpretation_high": "Cardioprotective high HDL level."
    },
    "triglycerides": {
        "name": "Triglycerides",
        "unit": "mg/dL",
        "low": 50.0,
        "high": 150.0,
        "critical_low": 30.0,
        "critical_high": 500.0,
        "interpretation_low": "Low triglyceride level.",
        "interpretation_high": "Hypertriglyceridemia (metabolic syndrome risk; >500 risks acute pancreatitis)."
    },
    "alt": {
        "name": "ALT (SGPT - Liver Enzyme)",
        "unit": "U/L",
        "low": 7.0,
        "high": 56.0,
        "critical_low": 0.0,
        "critical_high": 500.0,
        "interpretation_low": "Normal liver transaminase.",
        "interpretation_high": "Hepatocellular injury (Fatty liver, viral hepatitis, toxin, or medication effect)."
    },
    "ast": {
        "name": "AST (SGOT - Liver Enzyme)",
        "unit": "U/L",
        "low": 10.0,
        "high": 40.0,
        "critical_low": 0.0,
        "critical_high": 500.0,
        "interpretation_low": "Normal transaminase level.",
        "interpretation_high": "Hepatic, cardiac, or skeletal muscle damage."
    },
    "tsh": {
        "name": "Thyroid Stimulating Hormone (TSH)",
        "unit": "µIU/mL",
        "low": 0.4,
        "high": 4.5,
        "critical_low": 0.05,
        "critical_high": 20.0,
        "interpretation_low": "Primary Hyperthyroidism or suppressed pituitary production.",
        "interpretation_high": "Primary Hypothyroidism (Hashimoto's or thyroid underactivity)."
    },
    "crp": {
        "name": "C-Reactive Protein (CRP)",
        "unit": "mg/L",
        "low": 0.0,
        "high": 3.0,
        "critical_low": 0.0,
        "critical_high": 50.0,
        "interpretation_low": "Absence of acute systemic inflammatory process.",
        "interpretation_high": "Elevated acute phase reactant (bacterial infection, active inflammation, trauma)."
    }
}

def analyze_lab_report(submitted_values: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates submitted laboratory test metrics against established reference ranges.
    """
    analyzed_tests = []
    abnormal_count = 0
    critical_count = 0
    findings_summary = []

    for test_key, test_info in LAB_TEST_RANGES.items():
        if test_key in submitted_values and submitted_values[test_key] not in (None, ""):
            try:
                val = float(submitted_values[test_key])
                status = "Normal"
                color = "green"
                note = "Within reference range."

                # Critical checks
                if val <= test_info["critical_low"]:
                    status = "Critical Low"
                    color = "red"
                    critical_count += 1
                    note = f"CRITICALLY LOW: {test_info['interpretation_low']}"
                    findings_summary.append(f"{test_info['name']} is critically low ({val} {test_info['unit']}).")
                elif val >= test_info["critical_high"]:
                    status = "Critical High"
                    color = "red"
                    critical_count += 1
                    note = f"CRITICALLY HIGH: {test_info['interpretation_high']}"
                    findings_summary.append(f"{test_info['name']} is critically elevated ({val} {test_info['unit']}).")
                elif val < test_info["low"]:
                    status = "Low"
                    color = "amber"
                    abnormal_count += 1
                    note = test_info["interpretation_low"]
                    findings_summary.append(f"{test_info['name']} is below normal ({val} {test_info['unit']}).")
                elif val > test_info["high"]:
                    status = "High"
                    color = "amber"
                    abnormal_count += 1
                    note = test_info["interpretation_high"]
                    findings_summary.append(f"{test_info['name']} is elevated ({val} {test_info['unit']}).")

                # Percentage along reference bar for UI rendering
                range_span = (test_info["high"] - test_info["low"]) * 2.0
                if range_span <= 0:
                    range_span = 1.0
                pct = ((val - test_info["low"]) / range_span) * 100.0 + 50.0
                pct = max(5.0, min(95.0, pct))

                analyzed_tests.append({
                    "key": test_key,
                    "name": test_info["name"],
                    "value": val,
                    "unit": test_info["unit"],
                    "reference_low": test_info["low"],
                    "reference_high": test_info["high"],
                    "status": status,
                    "color": color,
                    "interpretation": note,
                    "bar_percentage": round(pct, 1)
                })
            except (ValueError, TypeError):
                continue

    # Clinical impression
    if critical_count > 0:
        overall_severity = "Critical Alert"
        badge_color = "red"
        advice = "One or more laboratory values are in the critical range. Immediate physician or emergency consultation is required to prevent acute decompensation."
    elif abnormal_count > 0:
        overall_severity = "Abnormal Findings"
        badge_color = "amber"
        advice = "Several parameters deviate from standard biological reference ranges. Schedule a clinical review with your primary care provider for differential evaluation."
    else:
        overall_severity = "All Analyzed Markers Normal"
        badge_color = "green"
        advice = "All supplied biomarkers are within normal clinical intervals. Continue healthy nutritional habits and routine wellness screenings."

    return {
        "tests": analyzed_tests,
        "total_analyzed": len(analyzed_tests),
        "abnormal_count": abnormal_count,
        "critical_count": critical_count,
        "overall_severity": overall_severity,
        "badge_color": badge_color,
        "findings_summary": findings_summary,
        "advice": advice
    }
