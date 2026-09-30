from ollama import chat
from pydantic import BaseModel
from typing import List, Optional

# 1. Define the exact JSON structure we want the AI to return
class Vulnerability(BaseModel):
    issue_type: str
    severity: str
    description: str
    suggested_fix: str

class SecurityReport(BaseModel):
    is_secure: bool
    vulnerabilities: List[Vulnerability]
    patched_code: Optional[str]

# 2. A deliberately vulnerable block of code (SQL Injection & Hardcoded Secret)
vulnerable_code = """
def get_user_data(user_id):
    secret_api_key = "AKIAIOSFODNN7EXAMPLE"
    query = "SELECT * FROM users WHERE id = " + user_id
    db.execute(query)
    return db.fetchall()
"""

print("Analyzing code for vulnerabilities...")

# 3. Call the local model and force it to output our Pydantic schema
response = chat(
    model='llama3.2:1b',
    messages=[
        {
            'role': 'system',
            'content': 'You are a senior cybersecurity application security engineer. Analyze the provided code, identify vulnerabilities, and provide patched code.'
        },
        {
            'role': 'user',
            'content': f"Analyze this code:\n\n{vulnerable_code}"
        }
    ],
    format=SecurityReport.model_json_schema(), 
)

# 4. Parse the AI's JSON output back into a Python object
report = SecurityReport.model_validate_json(response.message.content)

# 5. Output the results neatly
print(f"\nIs Code Secure? {report.is_secure}\n")
for vuln in report.vulnerabilities:
    print(f"[{vuln.severity.upper()}] {vuln.issue_type}")
    print(f"Details: {vuln.description}")
    print(f"Fix: {vuln.suggested_fix}\n")
    
print("--- PATCHED CODE ---")
print(report.patched_code)