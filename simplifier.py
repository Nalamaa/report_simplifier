# from typing import Optional
# import re, random
# from typing import Dict, List

# """
# Offline rule-based simplified medical report analyzer.
# This replaces LLM dependency. No internet required.
# """

# # Normal ranges (extendable)
# NORMAL_RANGES = {
#     "hemoglobin": (12, 15),
#     "haemoglobin": (12, 15),
#     "hb": (12, 15),
#     "glucose": (70, 140),
#     "rbs": (70, 140),
#     "fasting glucose": (70, 110),
#     "platelets": (150000, 450000),
#     "wbc": (4000, 11000),
#     "rbc": (4.0, 5.5),
#     "creatinine": (0.6, 1.2),
# }

# DOCTOR_SUGGESTIONS = {
#     "hemoglobin": "General Physician / Hematologist",
#     "hb": "General Physician / Hematologist",
#     "glucose": "Diabetologist / Endocrinologist",
#     "rbs": "Diabetologist / Endocrinologist",
#     "platelets": "Hematologist",
#     "wbc": "General Physician",
#     "rbc": "Hematologist",
#     "creatinine": "Nephrologist (Kidney Specialist)",
# }

# # ✅ Variation pools
# ADVICE_OPTIONS = [
#     "Maintain a balanced diet and stay hydrated. Get proper rest.",
#     "Eat nutritious food, drink plenty of water, and rest adequately.",
#     "Focus on a healthy diet, regular water intake, and enough sleep.",
#     "Stay hydrated, eat balanced meals, and take adequate rest.",
#     "Follow a healthy lifestyle and consult a doctor if symptoms continue."
# ]

# FOLLOWUP_OPTIONS = [
#     "Consult a doctor if symptoms continue.",
#     "If values stay abnormal, visit a certified doctor.",
#     "Seek medical review if abnormalities persist.",
#     "Follow up with a healthcare provider if needed.",
# ]

# DISCLAIMER_OPTIONS = [
#     "This is an automated interpretation. Always consult a certified doctor.",
#     "This report is AI-based and for guidance only. Please seek medical advice.",
#     "Automated analysis — not a replacement for professional diagnosis.",
#     "For educational purposes. Consult a qualified medical professional for final opinion.",
# ]

# def extract_number(text: str) -> Optional[float]:
#     match = re.search(r"(\d+\.?\d*)", text)
#     return float(match.group(1)) if match else None

# def classify_value(name, value, low, high):
#     if value < low: return "Low"
#     if value > high: return "High"
#     return "Normal"

# def summarize_medical_text(structured: Dict) -> Dict:
#     parameters = structured.get("parameters", [])
#     results = []
#     summary_lines = []

#     for p in parameters:
#         name = p.get("name", "").lower()
#         raw = p.get("raw_line", "")
#         value = p.get("value") or extract_number(raw)
        
#         if value is None:
#             continue
        
#         for key, (low, high) in NORMAL_RANGES.items():
#             if key in name:
#                 status = classify_value(key, value, low, high)
#                 normal = f"{low}-{high}"
#                 doctor = DOCTOR_SUGGESTIONS.get(key, "General Physician")

#                 if status == "Low":
#                     interp = f"{key.title()} is low ({value}). Could be deficiency or anemia."
#                 elif status == "High":
#                     interp = f"{key.title()} is high ({value}). Could indicate metabolic or health issue."
#                 else:
#                     interp = f"{key.title()} ({value}) is normal."

#                 results.append({
#                     "name": key.title(),
#                     "value": value,
#                     "normal_range": normal,
#                     "interpretation": status,
#                     "possible_causes": "Lifestyle, diet, dehydration, illness (general possibilities)",
#                     "doctor_type": doctor
#                 })
                
#                 summary_lines.append(interp)
#                 break

#     if not results:
#         simplified = "No clear lab values detected. Please upload a clearer medical report."
#         doctor = "General Physician"
#     else:
#         simplified = " | ".join(summary_lines)
#         doctor = "General Physician"

#     final = {
#         "simplified_report": simplified,
#         "parameter_details": results,
#         "advice": random.choice(ADVICE_OPTIONS) + " " + random.choice(FOLLOWUP_OPTIONS),
#         "doctor_type": doctor,
#         "disclaimer": random.choice(DISCLAIMER_OPTIONS),
#     }
    
#     return final
            # from typing import Optional, Dict
            # import re, random

            # """
            # Enhanced offline rule-based medical report analyzer.
            # Works even if OCR provides multiple formats.
            # """

            # NORMAL_RANGES = {
            #     "hemoglobin": (12, 15),
            #     "hb": (12, 15),
            #     "glucose": (70, 140),
            #     "rbs": (70, 140),
            #     "fasting glucose": (70, 110),
            #     "platelets": (150000, 450000),
            #     "wbc": (4000, 11000),
            #     "rbc": (4.0, 5.5),
            #     "creatinine": (0.6, 1.2),
            # }

            # DOCTOR_SUGGESTIONS = {
            #     "hemoglobin": "General Physician / Hematologist",
            #     "hb": "General Physician / Hematologist",
            #     "glucose": "Diabetologist / Endocrinologist",
            #     "rbs": "Diabetologist / Endocrinologist",
            #     "platelets": "Hematologist",
            #     "wbc": "General Physician",
            #     "rbc": "Hematologist",
            #     "creatinine": "Nephrologist (Kidney Specialist)",
            # }

            # ADVICE_OPTIONS = [
            #     "Maintain balanced food and water intake.",
            #     "Eat fresh, healthy meals and stay hydrated.",
            #     "Drink enough water and rest properly.",
            # ]

            # FOLLOWUP_OPTIONS = [
            #     "Consult a doctor if values remain abnormal.",
            #     "Seek medical advice for persistent issues.",
            # ]

            # DISCLAIMER_OPTIONS = [
            #     "This AI output is for support only — please consult a medical professional.",
            # ]

            # def extract_range(text):
            #     m = re.search(r"(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)", text)
            #     if m: return float(m.group(1)), float(m.group(2))
            #     return None

            # def summarize_medical_text(structured: Dict) -> Dict:
            #     parameters = structured.get("parameters", [])
            #     results = []
            #     summary = []
            #     critical_flags = []

            #     for p in parameters:
            #         name = p.get("name", "").lower()
            #         raw = p.get("raw_line", "")
            #         value = p.get("value")
            #         provided_range = p.get("normal_range")

            #         if value is None:
            #             m = re.search(r"(\d+\.?\d*)", raw)
            #             value = float(m.group(1)) if m else None
            #         if value is None: 
            #             continue

            #         # Determine range
            #         if provided_range:
            #             rng = extract_range(provided_range) or NORMAL_RANGES.get(name)
            #         else:
            #             rng = NORMAL_RANGES.get(name)

            #         if not rng:  # unknown marker, skip classification, only note value
            #             results.append({
            #                 "name": name.title(),
            #                 "value": value,
            #                 "normal_range": provided_range or "-",
            #                 "interpretation": "Value recorded",
            #                 "doctor_type": "General Physician"
            #             })
            #             continue

            #         low, high = rng

            #         if value < low:
            #             status = "Low"
            #             summary.append(f"{name.title()} is lower than normal ({value}).")
            #             critical_flags.append(name)
            #         elif value > high:
            #             status = "High"
            #             summary.append(f"{name.title()} is higher than normal ({value}).")
            #             critical_flags.append(name)
            #         else:
            #             status = "Normal"
            #             summary.append(f"{name.title()} is normal ({value}).")

            #         doctor = DOCTOR_SUGGESTIONS.get(name, "General Physician")

            #         results.append({
            #             "name": name.title(),
            #             "value": value,
            #             "normal_range": f"{low}-{high}",
            #             "interpretation": status,
            #             "doctor_type": doctor
            #         })

            #     final_summary = " ".join(summary) if summary else "Report values not clear — please upload a clear medical report."

            #     critical_note = ""
            #     if critical_flags:
            #         critical_note = f"⚠ Important: Your report shows concerns in {', '.join(critical_flags)}. Please consult a doctor."

            #     return {
            #         "simplified_report": final_summary + " " + critical_note,
            #         "parameter_details": results,
            #         "advice": random.choice(ADVICE_OPTIONS) + " " + random.choice(FOLLOWUP_OPTIONS),
            #         "doctor_type": "General Physician",
            #         "disclaimer": random.choice(DISCLAIMER_OPTIONS)
            #     }

from typing import Dict, Optional
import re, random

# ✅ Known lab tests & ranges
LAB_RANGES = {
    "hemoglobin": (12, 16),
    "rbc": (4.0, 5.5),
    "wbc": (4000, 10000),
    "neutrophils": (40, 80),
    "lymphocytes": (20, 40),
    "eosinophils": (1, 6),
    "monocytes": (2, 10),
}

TEST_KEYWORDS = {k: k for k in LAB_RANGES.keys()}

DOCTOR_SUGGESTIONS = {
    "hemoglobin": "General Physician / Hematologist",
    "rbc": "Hematologist",
    "wbc": "General Physician",
    "neutrophils": "General Physician",
    "lymphocytes": "General Physician",
    "eosinophils": "General Physician / Allergist",
    "monocytes": "General Physician",
}

def extract_number(text: str) -> Optional[float]:
    # ignore ranges like 1100 - 3300
    if re.search(r"\d+\s*-\s*\d+", text): return None

    m = re.search(r"(\d+\.?\d*)", text)
    return float(m.group(1)) if m else None

def classify(value, low, high):
    if value < low: return "Low"
    if value > high: return "High"
    return "Normal"

def summarize_medical_text(ocr_data: Dict) -> Dict:
    text = ocr_data.get("raw_text","")
    lines = text.split("\n")

    results = []
    pending_test = None

    for line in lines:
        l = line.lower().strip()

        # ✅ detect test name
        for test in TEST_KEYWORDS:
            if test in l and not re.search(r"\d", l):
                pending_test = test
                break
        
        # ✅ extract next numeric line for test
        if pending_test:
            value = extract_number(l)
            if value:
                low, high = LAB_RANGES[pending_test]
                status = classify(value, low, high)
                
                results.append({
                    "name": pending_test,
                    "value": value,
                    "normal_range": f"{low}-{high}",
                    "status": status,
                    "doctor_type": DOCTOR_SUGGESTIONS[pending_test]
                })
                pending_test = None

    # ✅ Build human sentences
    simplified_sentences = []
    problem_tests = []

    for r in results:
        if r["status"] == "Normal":
            simplified_sentences.append(f"{r['name'].title()} is normal ({r['value']}).")
        else:
            simplified_sentences.append(
                f"{r['name'].title()} is {r['status'].lower()} ({r['value']})."
            )
            problem_tests.append(r["name"].title())

    if not simplified_sentences:
        simplified_msg = "No clear medical values detected. Please upload a clearer report."
    else:
        simplified_msg = " ".join(simplified_sentences)

    if problem_tests:
        simplified_msg += f" ⚠ Please check: {', '.join(problem_tests)}."

    final = {
        "simplified_report": simplified_msg,
        "parameter_details": results,
        "advice": "Drink water, rest well, eat healthy. Consult doctor if symptoms persist.",
        "precautions": "Avoid stress, track symptoms, and keep hydrated.",
        "doctor_type": "General Physician",
        "disclaimer": "This is AI-based guidance. Always check with a doctor."
    }

    return final
