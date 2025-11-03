# medical_parser.py
import re

# Basic helpers to parse lines like "pH 7.29 7.350-7.450"
number_re = re.compile(r"[-+]?\d*\.\d+|\d+")
range_re = re.compile(r"(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)")

def extract_metadata(text):
    """
    Try to capture basic header metadata (hospital, bill date, doctor) from top of OCR text.
    Returns dict with keys possibly present.
    """
    meta = {}
    # sample regexes - robust to case
    hospital = re.search(r"([A-Z ]{3,}HOSPITAL|HOSPITAL\s*[:\-]?\s*[A-Z0-9\- ]+)", text, re.IGNORECASE)
    if hospital:
        meta['hospital'] = hospital.group(0).strip()
    date = re.search(r"(\d{1,2}[-/]\w{3,}[-/]\d{2,4}|\d{1,2}\s*[-/]\s*\w{3}\s*[-/]\s*\d{2,4}|\d{2}-[A-Za-z]{3}-\d{2,4})", text)
    if date:
        meta['date'] = date.group(0).strip()
    doctor = re.search(r"(Dr\.?\s+[A-Z][A-Za-z .]+)", text)
    if doctor:
        meta['doctor'] = doctor.group(0).strip()
    return meta

def find_table_block(text):
    """
    Try to find the parameters block — between words like 'Parameter' and 'Arterial Blood Gases' or end.
    """
    start = None
    end = None
    s_match = re.search(r"\bParameter\b", text, re.IGNORECASE)
    if s_match:
        start = s_match.end()
    # look for known section that might end the table
    e_match = re.search(r"\bARTERIAL BLOOD GASES\b|\bArterial Blood Gases\b|\bBlood Gas Values\b", text, re.IGNORECASE)
    if e_match:
        end = e_match.start()
    if start is None:
        # fallback: look for the first long newline block after headers
        start = 0
    return text[start:end].strip() if end else text[start:].strip()

def parse_parameter_line(line):
    """
    Try to parse a single line like:
      "pH 7.29 7.350 - 7.450 Potentiometry"
      "cNa+ 134 134.0 - 146.0 mmol/L"
      "ctHb 10.9 Calculated"
    Return dict or None.
    """
    orig = line.strip()
    if not orig:
        return None

    # compress spaces
    parts = re.split(r"\s{2,}|\t|\s(?=[A-Za-z%°\(\)0-9])", orig)
    # fallback split by whitespace
    if len(parts) < 2:
        parts = orig.split()
    # try name is first token
    name = parts[0]
    # find first number occurrence
    nums = number_re.findall(orig)
    value = None
    unit = None
    normal_range = None
    if nums:
        value = nums[0]
        # search for an explicit range after the value in the line
        r = range_re.search(orig)
        if r:
            normal_range = f"{r.group(1)} - {r.group(2)}"
        # attempt to find unit (e.g., mmol/L, mmHg, mEq/L)
        unit_match = re.search(r"(mmol\/L|mmHg|mEq\/L|g\/dL|%|mEq|mmol|mg\/dL|L|mL)", orig)
        if unit_match:
            unit = unit_match.group(0)
    # final sanity
    return {
        "raw_line": orig,
        "name": name,
        "value": value,
        "unit": unit,
        "normal_range": normal_range
    }

def parse_parameters(text):
    """
    Parse the parameters block into a list of dicts.
    """
    block = find_table_block(text)
    lines = [l.strip() for l in block.splitlines() if l.strip()]
    params = []
    for line in lines:
        # ignore header-like lines
        if re.search(r"parameter|specimen|results|biological reference", line, re.IGNORECASE):
            continue
        parsed = parse_parameter_line(line)
        if parsed:
            params.append(parsed)
    return params

def parse_text_to_structured(text):
    """
    Return structured dict: metadata + parameters list + raw_text
    """
    meta = extract_metadata(text)
    params = parse_parameters(text)
    return {"metadata": meta, "parameters": params, "raw_text": text}
