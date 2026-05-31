from fastapi import UploadFile
from fastapi import HTTPException


ALLOWED_FILE_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]


def validate_resume_file(file: UploadFile):

    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed"
        )