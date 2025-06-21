# app.py
import streamlit as st
from utils.pdf_extractor import extract_text_from_pdfs
from utils.llm_processor import get_filled_fields
from utils.docx_filler import fill_template
from io import BytesIO

st.set_page_config(page_title="GLR Insurance Template Filler", layout="centered")

st.title("📄 GLR Insurance Template Filler")
st.markdown("Upload your insurance template and photo reports to auto-fill.")

template_file = st.file_uploader("Upload .docx template", type=["docx"])
pdf_files = st.file_uploader("Upload photo reports (.pdf)", type=["pdf"], accept_multiple_files=True)

if st.button("Generate Filled Template") and template_file and pdf_files:
    with st.spinner("Processing..."):
        extracted_text = extract_text_from_pdfs(pdf_files)
        template_text = template_file.read().decode("utf-8", errors="ignore")

        kv_data = get_filled_fields(template_text, extracted_text)
        filled_doc = fill_template(template_file, kv_data)

        # Save to BytesIO for download
        output = BytesIO()
        filled_doc.save(output)
        output.seek(0)

        st.success("Template filled successfully!")
        st.download_button("📥 Download Filled Template", output, file_name="filled_template.docx")
