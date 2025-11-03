# import pytesseract
# from PIL import Image
# import tempfile
# import fitz  # PyMuPDF
# from ocr_utils import parse_ocr_output

# async def extract_report_text(file):
#     # Save uploaded file temporarily
#     tmp = tempfile.NamedTemporaryFile(delete=False)
#     tmp.write(await file.read())
#     tmp.close()

#     text = ""

#     # ✅ PDF handling
#     if file.filename.lower().endswith(".pdf"):
#         doc = fitz.open(tmp.name)
#         for page in doc:
#             text += page.get_text()
#         doc.close()

#     # ✅ Image handling
#     else:
#         img = Image.open(tmp.name)
#         text = pytesseract.image_to_string(img)

#     if not text.strip():
#         return {"raw_text": ""}

#     # ✅ Always pass as dict to parser
#     structured = parse_ocr_output({"raw_text": text})

#     # Return both raw + extracted params
#     return {
#         "raw_text": text,
#         "parameters": structured.get("parameters", [])
#     }
import pytesseract
from PIL import Image, ImageFilter, ImageOps
import tempfile
import fitz  # PyMuPDF
from ocr_utils import parse_ocr_output

def preprocess_image(img):
    img = img.convert("L")  # grayscale
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.SHARPEN)
    return img

async def extract_report_text(file):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(await file.read())
    tmp.close()

    text = ""

    if file.filename.lower().endswith(".pdf"):
        doc = fitz.open(tmp.name)
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text += page_text
            else:
                pix = page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img = preprocess_image(img)
                text += pytesseract.image_to_string(img)
        doc.close()

    else:
        img = Image.open(tmp.name)
        img = preprocess_image(img)
        text = pytesseract.image_to_string(img)

    if not text.strip():
        return {"raw_text": ""}

    structured = parse_ocr_output({"raw_text": text})

    return {
        "raw_text": text,
        "parameters": structured.get("parameters", [])
    }
