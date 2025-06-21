# utils/pdf_extractor.py
import fitz

def extract_text_from_pdfs(pdf_files):
    all_texts = []
    for pdf in pdf_files:
        doc = fitz.open(stream=pdf.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        all_texts.append(text)
    return "\n".join(all_texts)
