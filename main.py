from fastapi import FastAPI, File, UploadFile, HTTPException
from report_processor import extract_report_text
from simplifier import summarize_medical_text
from translator import TranslatorService
from advice_generator import generate_advice
import asyncio, sys, traceback

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title="Medical Report Analyzer")
translator_service = TranslatorService()

def clean_output(value):
    """Clean list-like strings coming from LLM output."""
    if isinstance(value, list):
        return ", ".join(value)
    if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
        try:
            import ast
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return ", ".join(parsed)
        except:
            pass
    return value

@app.post("/analyze_report")
async def analyze_report(file: UploadFile = File(...), target_language: str = "en"):
    try:
        data = await extract_report_text(file)

        print("\n✅ OCR Output Type:", type(data))
        print("✅ OCR Output Preview:", str(data)[:600])

        if not data or not isinstance(data, dict) or not data.get("raw_text"):
            raise HTTPException(status_code=400, detail="No readable text found in the uploaded file.")

        simplified_result = summarize_medical_text(data)

        print("\n✅ Simplified Result Type:", type(simplified_result))

        if not simplified_result or "simplified_report" not in simplified_result:
            raise HTTPException(status_code=500, detail="Summarization failed. Received no output.")

        simplified_text = clean_output(simplified_result.get("simplified_report", ""))

        try:
            translated_text = translator_service.translate_text(simplified_text, target_language)
        except Exception:
            print("❌ Translation Error:\n", traceback.format_exc())
            translated_text = simplified_text  # fallback

        advice = clean_output(simplified_result.get("advice") or generate_advice(simplified_text))
        doctor_type = clean_output(simplified_result.get("doctor_type", "General Physician"))
        precautions = clean_output(simplified_result.get("precautions", "Maintain hydration and follow doctor's advice"))

        return {
            "simplified_report": simplified_text,
            "translated_report": translated_text or simplified_text,   # ✅ fallback
            "advice": advice,
            "precautions": precautions or "Maintain hydration and follow doctor's advice",  # ✅ ensure exists
            "doctor_type": doctor_type
        }
    except Exception:
        print("❌ Server Error:\n", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error. Check backend logs.")
