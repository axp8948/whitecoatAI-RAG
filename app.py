import streamlit as st
import os
from dotenv import load_dotenv
from models.factory import get_llm
from ingestion.pipeline import run_extraction_pipeline
from rag.context_builder import build_summary_context
from core.prompts import OVERALL_SUMMARY_PROMPT

# Load environment
load_dotenv()

# Initialize LLM
llm = get_llm()

# Page config
st.set_page_config(
    page_title="WhiteCoatAI",
    page_icon="👨‍⚕️",
    layout="centered"
)

st.title("👨‍⚕️ WhiteCoatAI")
st.markdown("AI-powered medical lab report summarization")

uploaded_file = st.file_uploader(
    "Upload your medical report (PDF or TXT)",
    type=["pdf", "txt"]
)

if uploaded_file:

    with st.spinner("Extracting structured lab data..."):
        extraction_result = run_extraction_pipeline(uploaded_file, llm)

    structured_labs = extraction_result.get("structured_data", {}).get("tests", [])

    if not structured_labs:
        st.error("No lab data could be extracted.")
        st.stop()

    # Optional preview
    with st.expander("View Extracted Lab Data"):
        st.json(structured_labs)

    # Build strict RAG context
    context = build_summary_context(structured_labs)

    prompt = OVERALL_SUMMARY_PROMPT.format(context=context)

    with st.spinner("Generating AI summary..."):
        summary = llm.generate(prompt)

    st.subheader("🧠 AI Summary")
    st.write(summary)

st.markdown("---")
st.caption("This tool is for informational purposes only. Always consult a healthcare professional.")
