# import re

# def extract_lab_values(raw_text: str):
#     """
#     Extracts common lab values in format:

#     Test Name
#     optional desc...
#     12.4
#     gm/dL
#     12.0-15.0
#     """

#     pattern = r"""
#         (?P<name>[A-Za-z ()/+%]+)\n              # Test name
#         (?:.*?\n){0,3}?                          # optional method/specimen lines
#         (?P<value>[\d.]+)\n                      # numeric value
#         (?P<unit>[A-Za-z/%]+)?\n?                # optional unit (gm/dL)
#         (?P<range>[\d.]+\s*[-–]\s*[\d.]+)?       # optional reference range
#     """

#     matches = re.finditer(pattern, raw_text, re.VERBOSE)

#     params = []
#     for m in matches:
#         name = m.group("name").strip()
#         value = m.group("value")
#         unit = m.group("unit") or ""
#         ref_range = m.group("range") or ""

#         # filter out garbage / headers
#         if name.lower() in ["name", "age", "referrer", "branch", "haematology", "biochemistry"]:
#             continue

#         # validate number
#         try:
#             value_float = float(value)
#         except:
#             continue

#         params.append({
#             "name": name,
#             "value": value_float,
#             "unit": unit,
#             "normal_range": ref_range,
#             "raw_line": f"{name}: {value_float} {unit} (Range {ref_range if ref_range else 'N/A'})"
#         })

#     return params

# def parse_ocr_output(ocr_data):
#     raw = ocr_data.get("raw_text") if isinstance(ocr_data, dict) else ocr_data
    
#     if not raw or not raw.strip():
#         return {"parameters": [], "metadata": {}}

#     params = extract_lab_values(raw)

#     return {
#         "parameters": params,
#         "raw_text": raw,
#         "metadata": {}
#     }

import re

LAB_PATTERNS = [
    # Pattern 1: Hb: 10.8 g/dL (inline format)
    r"(?P<name>[A-Za-z0-9 +()/%.:-]{2,30})[: ]+(?P<value>\d+\.?\d*)\s*(?P<unit>[A-Za-z/%]+)?\s*(\((?P<range>\d+\.?\d*\s*[-–]\s*\d+\.?\d*)\))?",

    # Pattern 2: Hb 10.8 g/dL 12-15
    r"(?P<name>[A-Za-z0-9 +()/%.:-]{2,30})\s+(?P<value>\d+\.?\d*)\s*(?P<unit>[A-Za-z/%]+)\s+(?P<range>\d+\.?\d*\s*[-–]\s*\d+\.?\d*)",
]

def extract_lab_values(raw_text: str):
    text = raw_text.replace("\t", " ").replace(":", " ").strip()
    text = re.sub(r"\s{2,}", " ", text)

    params = []
    seen = set()

    for pattern in LAB_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            name = m.group("name").strip()
            value = m.group("value")
            unit = m.group("unit") or ""
            ref_range = m.group("range") or ""

            if not name or not value:
                continue

            key = f"{name}-{value}"
            if key in seen:
                continue
            seen.add(key)

            try:
                value_float = float(value)
            except:
                continue

            params.append({
                "name": name,
                "value": value_float,
                "unit": unit,
                "normal_range": ref_range,
                "raw_line": f"{name}: {value_float} {unit} (Range {ref_range if ref_range else 'N/A'})"
            })

    return params

def parse_ocr_output(ocr_data):
    raw = ocr_data.get("raw_text") if isinstance(ocr_data, dict) else ocr_data

    if not raw or not raw.strip():
        return {"parameters": [], "metadata": {}}

    params = extract_lab_values(raw)

    return {
        "parameters": params,
        "raw_text": raw,
        "metadata": {}
    }
