from fastapi import UploadFile
import mimetypes
import docx
import PyPDF2
from PIL import Image
import pytesseract
import io

def extract_text_from_file(file, contents):
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type is None:
        raise ValueError("Не удалось определить тип файла")
    if mime_type == 'application/pdf':
        return extract_text_from_pdf(contents)
    elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return extract_text_from_docx(contents)
    elif mime_type.startswith('image'):
        return extract_text_from_image(contents)
    else:
        raise ValueError(f"Тип файла {mime_type} не поддерживается")

def extract_text_from_pdf(contents):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(contents):
    doc = docx.Document(io.BytesIO(contents))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_image(contents):
    img = Image.open(io.BytesIO(contents))
    text = pytesseract.image_to_string(img)
    return text