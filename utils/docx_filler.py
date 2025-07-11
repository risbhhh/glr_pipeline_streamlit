# utils/docx_filler.py
from docx import Document
import re
import json

def fill_template(docx_file, kv_string):
    if isinstance(kv_string, str):
        kv_pairs = json.loads(kv_string)
    else:
        kv_pairs = kv_string  # Already a dict, use directly

    doc = Document(docx_file)

    for p in doc.paragraphs:
        for key, value in kv_pairs.items():
            if f"{{{{{key}}}}}" in p.text:
                inline = p.runs
                for i in range(len(inline)):
                    inline[i].text = re.sub(rf"\{{{{{key}}}}}", value, inline[i].text)

    return doc
