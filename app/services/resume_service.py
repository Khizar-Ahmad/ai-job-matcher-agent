import os
import uuid

from fastapi import UploadFile

from app.utils.file_parser import parse_resume
from app.utils.validators import validate_resume_file


class ResumeService:

    @staticmethod
    async def upload_and_extract_text(
        resume: UploadFile
    ):
        validate_resume_file(resume)

        extension = resume.filename.split('.')[-1]

        unique_filename = f"{uuid.uuid4()}.{extension}"

        file_path = f"uploads/{unique_filename}"

        with open(file_path, "wb") as file:
            content = await resume.read()
            file.write(content)

        extracted_text = await parse_resume(file_path)

        if os.path.exists(file_path):
            os.remove(file_path)

        return extracted_text