MAX_RESUME_CHARACTERS = 5000
MAX_JOB_DESCRIPTION_CHARACTERS = 4000
MAX_QUESTION_CHARACTERS = 1000


async def trim_text(
    text: str,
    limit: int
):

    if not text:
        return ""

    text = text.strip()

    return text[:limit]