# import re


# async def extract_skills(text: str):
#     text = text.lower()

#     possible_skills = [
#         "python",
#         "react",
#         "node.js",
#         "fastapi",
#         "docker",
#         "postgresql",
#         "aws",
#         "mongodb",
#         "typescript",
#         "redis",
#         "kubernetes",
#     ]

#     found = []

#     for skill in possible_skills:
#         if re.search(rf"\\b{re.escape(skill)}\\b", text):
#             found.append(skill)

#     return list(set(found))

# import re

# SKILL_ALIASES = {
#     "react": [
#         "react",
#         "reactjs",
#         "react.js",
#         "react js",
#     ],
#     "node.js": [
#         "node",
#         "nodejs",
#         "node.js",
#         "node js",
#     ],
#     "python": [
#         "python",
#         "python3",
#     ],
#     "fastapi": [
#         "fastapi",
#         "fast api",
#     ],
#     "typescript": [
#         "typescript",
#         "ts",
#     ],
#     "javascript": [
#         "javascript",
#         "js",
#     ],
#     "mongodb": [
#         "mongodb",
#         "mongo",
#     ],
#     "postgresql": [
#         "postgresql",
#         "postgres",
#         "psql",
#     ],
#     "docker": [
#         "docker",
#         "docker-compose",
#     ],
#     "aws": [
#         "aws",
#         "amazon web services",
#     ],
#     "redis": [
#         "redis",
#     ],
#     "kubernetes": [
#         "kubernetes",
#         "k8s",
#     ],
#     "ruby": [
#         "ruby",
#         "ruby on rails",
#         "rails",
#     ],
# }


# async def extract_skills(text: str):
#     text = text.lower()
#     found = set()

#     for canonical_skill, aliases in SKILL_ALIASES.items():
#         for alias in aliases:
#             pattern = rf"\b{re.escape(alias)}\b"

#             if re.search(pattern, text):
#                 found.add(canonical_skill)
#                 break

#     return sorted(list(found))

import json

from app.services.llm_service import LLMService
from app.utils.prompts import SKILL_EXTRACTION_PROMPT,SKILL_INFERENCE_PROMPT


async def extract_skills_llm(text: str) -> list[str]:

    prompt = SKILL_EXTRACTION_PROMPT.format(text=text[:6000])

    raw = await LLMService.generate(prompt,"extract_skills")

    try:
        clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        skills = json.loads(clean)
    except json.JSONDecodeError:
        skills = []

    return sorted(skills)


async def infer_missing_skills(
    resume_skills: list[str],
    job_skills: list[str],
) -> list[str]:

    # Only evaluate skills not already matched
    unmatched = list(set(job_skills) - set(resume_skills))

    if not unmatched:
        return []

    prompt = SKILL_INFERENCE_PROMPT.format(
        resume_skills=", ".join(resume_skills),
        unmatched_skills=", ".join(unmatched),
    )

    raw = await LLMService.generate(prompt,"infer_skills")

    try:
        clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        inferred = json.loads(clean)
    except json.JSONDecodeError:
        inferred = []

    return inferred


async def calculate_similarity(
    resume_skills: list[str],
    job_skills: list[str]
):
    if not job_skills:
        return 0

    matched = set(resume_skills).intersection(set(job_skills))

    percentage = (
        len(matched) / len(job_skills)
    ) * 100

    return round(percentage, 2)