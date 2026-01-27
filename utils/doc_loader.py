import io

import pdfplumber


def load_document_text(uploaded_file) -> tuple[str, dict]:
    filename = uploaded_file.name
    file_bytes = uploaded_file.getvalue()
    ext = filename.split(".")[-1].lower()

    if ext == "pdf":
        text = _extract_pdf_text(file_bytes)
        return text, {"filename": filename, "document_type": "pdf"}

    if ext == "txt":
        text = file_bytes.decode("utf-8", errors="replace")
        return text, {"filename": filename, "document_type": "txt"}

    raise ValueError("Unsupported file type. Please upload a PDF or TXT.")


def _extract_pdf_text(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts)
