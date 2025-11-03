from utils.medical_utils import map_findings_to_advice

def generate_advice(simplified_text):
    # This can use LLM prompts or simple rule-based logic with regex/keywords
    advice, precautions, doctor_type = map_findings_to_advice(simplified_text)
    return advice, precautions, doctor_type
