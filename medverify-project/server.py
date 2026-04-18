"""
MedVerify Backend — FastAPI
Run: uvicorn server:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
import bcrypt
import json
import re
import os
import time
import base64
import datetime
import google.generativeai as genai
from PIL import Image
import pytesseract
import io

# ── Config ──────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "medverify-secret-2025")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 8

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(title="MedVerify API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# ── In-memory DB (replace with MongoDB/SQLite for production) ─
FACULTY_DB = {
    "faculty@hospital.com": {
        "password": bcrypt.hashpw(b"medverify2025", bcrypt.gensalt()).decode(),
        "name": "Dr. Sarah Chen",
        "dept": "Internal Medicine",
        "role": "Senior Faculty",
    },
    "admin@medverify.com": {
        "password": bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode(),
        "name": "Admin User",
        "dept": "Administration",
        "role": "Administrator",
    },
}

audit_log = []  # In-memory audit log

# ── Models ───────────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: str
    password: str

class AnalysisResponse(BaseModel):
    success: bool
    risk_score: int
    verdict: str
    risk_level: str
    extracted_fields: dict
    observations: list
    rule_checks: list
    raw_text: str
    debug_info: str
    student_name: str
    student_id: str
    analysed_by: str
    timestamp: str

# ── Auth helpers ─────────────────────────────────────────────
def create_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email not in FACULTY_DB:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# ── OCR ─────────────────────────────────────────────────────
def extract_text_ocr(image_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"[OCR failed: {str(e)}]"

# ── Gemini Analysis ──────────────────────────────────────────
ANALYSIS_PROMPT = """
You are a medical certificate verification expert. Analyze this medical certificate image and OCR text.

OCR Extracted Text:
{ocr_text}

Perform a detailed fraud detection analysis. Return ONLY valid JSON (no markdown, no explanation):

{{
  "risk_score": <integer 0-100, higher = more suspicious>,
  "verdict": "<one sentence summary>",
  "risk_level": "<LOW|MEDIUM|HIGH>",
  "extracted_fields": {{
    "patient_name": "<name or null>",
    "doctor_name": "<name or null>",
    "doctor_registration": "<reg number or null>",
    "hospital_name": "<hospital or null>",
    "issue_date": "<date or null>",
    "valid_from": "<date or null>",
    "valid_until": "<date or null>",
    "diagnosis": "<diagnosis or null>",
    "signature_present": <true|false>,
    "stamp_present": <true|false>
  }},
  "observations": [
    "<observation 1>",
    "<observation 2>",
    "<observation 3>"
  ],
  "rule_checks": [
    {{"name": "Doctor Registration Number", "pass": <true|false>, "detail": "<reason>"}},
    {{"name": "Valid Date Range", "pass": <true|false>, "detail": "<reason>"}},
    {{"name": "Medical Terminology", "pass": <true|false>, "detail": "<reason>"}},
    {{"name": "Hospital/Clinic Details", "pass": <true|false>, "detail": "<reason>"}},
    {{"name": "Doctor Signature", "pass": <true|false>, "detail": "<reason>"}},
    {{"name": "Official Stamp/Seal", "pass": <true|false>, "detail": "<reason>"}},
    {{"name": "Consistent Formatting", "pass": <true|false>, "detail": "<reason>"}},
    {{"name": "No Suspicious Alterations", "pass": <true|false>, "detail": "<reason>"}}
  ]
}}
"""

def analyze_with_gemini(image_bytes: bytes, ocr_text: str, retries: int = 3) -> dict:
    model = genai.GenerativeModel("gemini-1.5-flash")
    image = Image.open(io.BytesIO(image_bytes))
    prompt = ANALYSIS_PROMPT.format(ocr_text=ocr_text[:2000])

    last_error = None
    for attempt in range(retries):
        try:
            response = model.generate_content([prompt, image])
            raw = response.text.strip()

            # Strip markdown fences if present
            raw = re.sub(r"^```json\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            raw = raw.strip()

            result = json.loads(raw)
            result["_debug"] = f"Attempt {attempt+1} succeeded. Raw length: {len(raw)}"
            return result
        except json.JSONDecodeError as e:
            last_error = f"JSON parse error on attempt {attempt+1}: {str(e)}"
            time.sleep(1.5 ** attempt)
        except Exception as e:
            last_error = f"Gemini error on attempt {attempt+1}: {str(e)}"
            time.sleep(1.5 ** attempt)

    # Fallback response
    return {
        "risk_score": 50,
        "verdict": "Analysis inconclusive — manual review required.",
        "risk_level": "MEDIUM",
        "extracted_fields": {k: None for k in [
            "patient_name","doctor_name","doctor_registration","hospital_name",
            "issue_date","valid_from","valid_until","diagnosis","signature_present","stamp_present"
        ]},
        "observations": ["AI analysis failed after 3 attempts. Please review manually."],
        "rule_checks": [],
        "_debug": last_error or "Unknown error",
    }

# ── Routes ───────────────────────────────────────────────────
@app.get("/")
def health():
    return {"status": "ok", "service": "MedVerify API", "version": "2.0"}

@app.post("/api/login")
def login(req: LoginRequest):
    user = FACULTY_DB.get(req.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not bcrypt.checkpw(req.password.encode(), user["password"].encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(req.email)
    return {
        "token": token,
        "user": {
            "email": req.email,
            "name": user["name"],
            "dept": user["dept"],
            "role": user["role"],
        },
    }

@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(...),
    student_name: str = Form(""),
    student_id: str = Form(""),
    current_user: str = Depends(verify_token),
):
    if not file.content_type.startswith("image/") and file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only images and PDFs supported")

    image_bytes = await file.read()

    # OCR
    ocr_text = extract_text_ocr(image_bytes)

    # Gemini
    result = analyze_with_gemini(image_bytes, ocr_text)

    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    faculty = FACULTY_DB[current_user]

    # Save to audit log
    audit_log.append({
        "student_name": student_name or "Unknown",
        "student_id": student_id or "—",
        "file_name": file.filename,
        "risk_level": result.get("risk_level", "MEDIUM"),
        "risk_score": result.get("risk_score", 0),
        "analysed_by": faculty["name"],
        "timestamp": timestamp,
    })

    return {
        "success": True,
        "risk_score": result.get("risk_score", 0),
        "verdict": result.get("verdict", ""),
        "risk_level": result.get("risk_level", "MEDIUM"),
        "extracted_fields": result.get("extracted_fields", {}),
        "observations": result.get("observations", []),
        "rule_checks": result.get("rule_checks", []),
        "raw_text": ocr_text,
        "debug_info": result.get("_debug", ""),
        "student_name": student_name,
        "student_id": student_id,
        "analysed_by": faculty["name"],
        "timestamp": timestamp,
    }

@app.get("/api/audit")
def get_audit(current_user: str = Depends(verify_token)):
    return {"logs": audit_log[::-1]}  # newest first

@app.get("/api/stats")
def get_stats(current_user: str = Depends(verify_token)):
    total = len(audit_log)
    flagged = sum(1 for r in audit_log if r["risk_level"] == "HIGH")
    approved = sum(1 for r in audit_log if r["risk_level"] == "LOW")
    avg_score = int(sum(r["risk_score"] for r in audit_log) / total) if total else 0
    return {
        "total_analyzed": total,
        "flagged": flagged,
        "approved": approved,
        "avg_risk_score": avg_score,
    }
