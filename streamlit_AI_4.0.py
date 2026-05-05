import streamlit as st
from openai import OpenAI
import PyPDF2

# 🔹 Page config
st.set_page_config(page_title="AI Analyzer", layout="wide")

st.title("📊 AI File Analyzer")
st.caption("🔒 Your API key is not stored. Used only for this session.")

# 🔹 API key input
api_key = st.text_input("Enter your OpenAI API Key", type="password")

if not api_key:
    st.info("Enter your API key to continue")
    st.stop()

# 🔹 Validate API key
try:
    client = OpenAI(api_key=api_key)
except:
    st.error("Invalid API key")
    st.stop()

# 🔹 Layout
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload TXT, CSV, or PDF")

    mode = st.selectbox("Mode", ["summarize", "analyze", "qa"])

    if mode == "qa":
        question = st.text_input("Enter your question")

with col2:
    st.markdown("### Result")

text = ""

# 🔹 File handling
if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]

    if file_type in ["txt", "csv"]:
        text = uploaded_file.read().decode("utf-8")

    elif file_type == "pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()

# 🔹 Run AI
if st.button("🚀 Run AI"):

    if not uploaded_file:
        st.warning("Please upload a file")

    else:
        # Build prompt
        if mode == "summarize":
            prompt = f"Summarize:\n{text}"

        elif mode == "analyze":
            prompt = f"Analyze this data and give insights:\n{text}"

        elif mode == "qa":
            if not question:
                st.warning("Enter a question")
                st.stop()
            prompt = f"{text}\n\nQuestion: {question}"

        # Call AI
        with st.spinner("Processing..."):
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

        # 🔹 Output
        col2.success("Done!")
        col2.write(result)

        # 🔹 Download
        col2.download_button(
            "Download Result",
            result,
            "ai_result.txt"
        )