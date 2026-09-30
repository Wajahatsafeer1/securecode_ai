import streamlit as st
import requests

# Page Styling & Configuration
st.set_page_config(
    page_title="SecureCode AI Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS Styling for a sleek security tool look
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #0E1117;
        font-weight: 700;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<p class="main-title">🛡️ SecureCode AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enterprise-Grade Local Application Security Testing (SAST) Powered by Llama</p>', unsafe_allow_html=True)

# Sidebar Information
with st.sidebar:
    st.header("⚙️ Scanner Config")
    st.info("Local Engine: **Llama 3.2:1b** via Ollama")
    st.markdown("---")
    st.markdown("### 🔒 Security Status")
    st.markdown("Backend API: `Online 🟢`")
    st.markdown("Privacy: **100% Local (Zero Cloud Leak)**")

# Main Interface Layout (Two Columns)
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("📝 Source Code Input")
    st.markdown("Paste any Python function or snippet below to scan for security flaws.")
    
    # Default vulnerable snippet for easy testing
    default_code = """def get_user_data(user_id):
    secret_api_key = "AKIAIOSFODNN7EXAMPLE"
    query = "SELECT * FROM users WHERE id = " + user_id
    db.execute(query)
    return db.fetchall()"""
    
    code_input = st.text_area("Code Editor", value=default_code, height=320)
    
    # Action Button
    scan_triggered = st.button("🚀 Run Security Audit", type="primary", use_container_width=True)

with col_output:
    st.subheader("📊 Vulnerability Audit Report")
    
    if scan_triggered:
        if not code_input.strip():
            st.warning("⚠️ Please provide a code snippet to scan.")
        else:
            with st.spinner("Analyzing code structure and checking security patterns..."):
                try:
                    # Send request to your FastAPI backend
                    response = requests.post(
                        "http://127.0.0.1:8000/scan",
                        json={"code": code_input},
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        report = response.json()
                        
                        # Overall Security Status Badge
                        if report.get("is_secure", False):
                            st.success("✅ **Code is Secure:** No major vulnerabilities identified.")
                        else:
                            st.error("🚨 **Security Alert:** Vulnerabilities Detected!")
                        
                        vulnerabilities = report.get("vulnerabilities", [])
                        
                        if vulnerabilities:
                            st.markdown(f"### 🔍 Identified Vulnerabilities ({len(vulnerabilities)})")
                            
                            # Render separate cards for each vulnerability
                            for idx, vuln in enumerate(vulnerabilities, 1):
                                severity = vuln.get("severity", "MEDIUM").upper()
                                issue_type = vuln.get("issue_type", "Unknown Vulnerability")
                                description = vuln.get("description", "No details provided.")
                                fix = vuln.get("suggested_fix", "No fix suggested.")
                                
                                # Use different colored alert boxes based on severity
                                if severity in ["CRITICAL", "HIGH"]:
                                    st.error(f"**#{idx} [{severity}] {issue_type}**\n\n_{description}_")
                                else:
                                    st.warning(f"**#{idx} [{severity}] {issue_type}**\n\n_{description}_")
                                
                                st.markdown(f"💡 **Recommended Fix:** `{fix}`")
                                st.markdown("---")
                        else:
                            st.info("No specific vulnerability items returned.")
                        
                        # Display Patched Code
                        patched_code = report.get("patched_code")
                        if patched_code:
                            st.markdown("### 🛠️ Secure Remediated Code")
                            st.code(patched_code, language="python")
                            
                    else:
                        st.error(f"Server Error ({response.status_code}): {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Could not connect to the FastAPI backend.")
                    st.info("Make sure your backend server is running by typing `uvicorn main:app --reload` in your terminal.")
    else:
        st.info("👈 Enter your code on the left and click **Run Security Audit** to see results here.")