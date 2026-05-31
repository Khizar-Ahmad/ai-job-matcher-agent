from pathlib import Path

from docx import Document
from pypdf import PdfReader


async def parse_pdf(file_path: str):
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


async def parse_docx(file_path: str):
    document = Document(file_path)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )


async def parse_resume(file_path: str):
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return await parse_pdf(file_path)

    if extension == ".docx":
        return await parse_docx(file_path)

    raise Exception("Unsupported file type")