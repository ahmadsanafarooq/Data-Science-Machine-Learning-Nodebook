import fitz 
from docx import Document
import os

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file type. Please upload a PDF or DOCX file."

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([p.text for p in doc.paragraphs])
