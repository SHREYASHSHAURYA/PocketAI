import os
import io
import pdfplumber
import pytesseract
from PIL import Image
from langchain_core.documents import Document

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def load_documents(folder_path):
    documents = []

    for file in sorted(os.listdir(folder_path)):
        path = os.path.join(folder_path, file)

        if file.endswith(".pdf"):
            documents.extend(_load_pdf(path))

        elif file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                documents.append(Document(page_content=content, metadata={"source": file}))

    return documents


def _load_pdf(path):
    docs = []

    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                docs.append(Document(
                    page_content=text.strip(),
                    metadata={"source": path, "page": i + 1}
                ))
            else:
                buf = io.BytesIO()
                page.to_image(resolution=300).save(buf, format="PNG")
                buf.seek(0)
                ocr_text = pytesseract.image_to_string(Image.open(buf), config="--psm 6").strip()
                if ocr_text:
                    docs.append(Document(
                        page_content=ocr_text,
                        metadata={"source": path, "page": i + 1}
                    ))

    return docs