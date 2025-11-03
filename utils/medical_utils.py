# # Example: mapping keywords from simplified_text to advice
# def map_findings_to_advice(text):
#     import re
#     advice, precautions, doctor_type = "", "", ""

#     mappings = [
#         (r"\banemia\b", "Increase iron intake; consider iron supplements.", "Eat leafy greens, avoid strenuous activity.", "Hematologist"),
#         (r"\bdiabetes\b", "Start tracking blood sugar; consult doctor.", "Avoid sugar, test glucose regularly.", "Endocrinologist"),
#         (r"\bstroke\b|\bbrain\b", "Emergency consultation needed.", "Lie down, monitor consciousness.", "Neurologist"),
#         (r"\bfracture\b|\bbone\b", "Immobilize limb; go to ER.", "Do not move injured part.", "Orthopedist"),
#         (r"\bpregnancy\b|\bobstetric\b", "Schedule prenatal checkup.", "Maintain hydration, rest.", "Gynecologist"),
#         # Add mappings as needed...
#     ]

#     found = False
#     for pattern, a, p, d in mappings:
#         if re.search(pattern, text, re.IGNORECASE):
#             advice, precautions, doctor_type = a, p, d
#             found = True
#             break

#     if not found:
#         advice = "Consult with a general practitioner for next steps."
#         precautions = "Monitor symptoms, prepare previous health records."
#         doctor_type = "General Physician"

#     return advice, precautions, doctor_type

def map_findings_to_advice(text):
    import re

    rules = [
        (r"\banemia\b|\blow hemoglobin\b", 
         "Increase iron-rich food (greens, dates, dal).", 
         "Avoid heavy work if feeling tired", 
         "Hematologist"),
        
        (r"\bdiabetes\b|\bhigh glucose\b|\bhyperglycemia\b", 
         "Reduce sugar and white rice, walk daily.", 
         "Monitor blood glucose weekly", 
         "Endocrinologist"),
        
        (r"\brenal\b|\bcreatinine\b|\bkidney\b", 
         "Drink enough water and avoid excess salt.", 
         "Avoid painkillers without doctor advice", 
         "Nephrologist"),
    ]

    for pattern, advice, precaution, doctor in rules:
        if re.search(pattern, text, re.IGNORECASE):
            return advice, precaution, doctor

    return (
        "Follow balanced diet and stay hydrated.",
        "Monitor symptoms and rest well.",
        "General Physician"
    )
