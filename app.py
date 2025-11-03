import streamlit as st
import requests

API_URL = "https://report-simplifier.onrender.com/analyze_report"

# ✅ Page config
st.set_page_config(page_title="🩺 Elder-Friendly Medical Report Helper", layout="wide")

# ✅ Modern Elder-friendly UI Theme
st.markdown("""
<style>

body {
    background-color: #EEF5FF;
    font-family: "Segoe UI", sans-serif;
}

/* Smooth cards */
.report-box {
    background: #FFFFFF;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #D6E6FF;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.07);
    margin-bottom: 25px;
    font-size: 22px;
    line-height: 1.6;
    color: #000 !important;
}

/* Global font */
html, body, div, span, input, textarea, select, button {
    font-size: 21px !important;
}

/* Title */
h1 {
    color: #003B95 !important;
    font-weight: 800;
}

/* Headings */
h2, h3 {
    color: #004FC5 !important;
    font-weight: 700;
}

/* Inputs & dropdowns */
input, textarea, select {
    background-color: #FFF8C2 !important;
    color: #000 !important;
    border: 2px solid #4C9AFF !important;
    border-radius: 12px !important;
    padding: 12px !important;
    font-size: 22px !important;
}

/* Dropdown fix */
div[data-baseweb="select"] * {
    color: black !important;
    font-size: 20px !important;
}

/* Placeholder */
::placeholder {
    color: #6B6B6B !important;
    font-size: 20px !important;
}

/* File uploader label */
section[data-testid="stFileUploader"] label {
    font-size: 22px !important;
    font-weight: bold;
    color: #003B95;
}

/* Buttons */
div.stButton > button {
    font-size: 24px !important;
    padding: 18px 28px;
    border-radius: 14px;
    background: #0A66C2;
    color: #fff;
    font-weight: bold;
    border: none;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
}
div.stButton > button:hover {
    background: #004A94 !important;
}

</style>
""", unsafe_allow_html=True)

# ✅ Title
st.markdown("<h1 style='text-align:center;'>🧓👵 Medical Report Helper for Elders</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:22px;'>Upload your medical report and receive a simple, easy-to-understand summary.</p>", unsafe_allow_html=True)


# ✅ Upload section
st.markdown("### 📂 Upload Medical Report")
uploaded_file = st.file_uploader(
    "Upload Report",
    type=["pdf", "png", "jpg", "jpeg"],
    label_visibility="collapsed"
)

# ✅ Language selection
st.markdown("### 🌐 Select Language for Summary")
languages = {"English": "en", "Tamil": "ta"}
target_lang = languages[st.selectbox(
    "Select Language",
    list(languages.keys()),
    index=0,
    label_visibility="collapsed"
)]

# ✅ Process Button
analyze = st.button("🔍 Analyze My Report")

if uploaded_file and analyze:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    params = {"target_language": target_lang}

    with st.spinner("⏳ Analyzing your report... Please wait..."):
        try:
            response = requests.post(API_URL, files=files, params=params)

            if response.status_code == 200:
                result = response.json()

                st.markdown("<h2>📋 Simple Explanation</h2>", unsafe_allow_html=True)
                st.markdown(f"<div class='report-box'>{result.get('simplified_report','No simplified report available.')}</div>", unsafe_allow_html=True)

                st.markdown("<h2>🌐 Translated (Your Language)</h2>", unsafe_allow_html=True)
                st.markdown(f"<div class='report-box'>{result.get('translated_report','No translation available.')}</div>", unsafe_allow_html=True)

                st.markdown("<h2>🩺 Doctor's Guidance</h2>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='report-box'>
                ✅ <b>Advice:</b> {result.get('advice','N/A')}<br>
                ✅ <b>Precautions:</b> {result.get('precautions','N/A')}<br>
                ✅ <b>Suggested Doctor:</b> {result.get('doctor_type','N/A')}
                </div>
                """, unsafe_allow_html=True)

            else:
                st.error(f"❌ Server Error: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Please start the FastAPI server first.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# ✅ Footer
st.markdown("<br><hr><p style='text-align:center; font-size:20px;'>💡 Tip: If text is hard to read, ask a family member to help you.</p>", unsafe_allow_html=True)
