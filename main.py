from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from ollama import chat
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(
    title="SecureCode AI API",
    description="Local AI-powered application security scanner endpoint.",
    version="1.0.0"
)

# Add CORS middleware here (after app is initialized)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Define request body schema
class CodeScanRequest(BaseModel):
    code: str

# Define response body schema
class Vulnerability(BaseModel):
    issue_type: str
    severity: str
    description: str
    suggested_fix: str

class SecurityReport(BaseModel):
    is_secure: bool
    vulnerabilities: List[Vulnerability]
    patched_code: Optional[str]


@app.get("/")
def read_root():
    return {"status": "online", "service": "SecureCode AI API"}


@app.post("/scan", response_model=SecurityReport)
def scan_code(payload: CodeScanRequest):
    if not payload.code.strip():
        raise HTTPException(status_code=400, detail="Code payload cannot be empty.")
    
    try:
        response = chat(
            model='llama3.2:1b',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a senior cybersecurity application security engineer. Analyze the provided code, identify vulnerabilities, and provide patched code.'
                },
                {
                    'role': 'user',
                    'content': f"Analyze this code:\n\n{payload.code}"
                }
            ],
            format=SecurityReport.model_json_schema(),
        )
        
        report = SecurityReport.model_validate_json(response.message.content)
        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")