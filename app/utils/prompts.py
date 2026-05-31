COVER_LETTER_PROMPT = """
You are an expert ATS optimized cover letter writer.

Generate a professional cover letter.

User Profile:
{user_profile}

Resume:
{resume_text}

Company Name:
{company_name}

Job Title:
{job_title}

Job Description:
{job_description}

Instructions:
- Keep it professional
- Keep it concise
- Highlight relevant skills
- Focus on business impact
- Make it ATS friendly
"""


# QUESTION_ANSWER_PROMPT = """
# You are helping a candidate answer a job application question.

# Question:
# {question}

# User Profile:
# {user_profile}

# Resume:
# {resume_text}

# Instructions:
# - Answer professionally
# - Keep answer concise
# - Use resume information
# - Match the job tone
# - Avoid hallucinations
# """


QUESTION_ANSWER_PROMPT = """
You are an expert job application assistant.

Answer each of the following job application questions based on the user's profile and resume.

User Profile:
{user_profile}

Resume:
{resume_text}

Questions:
{questions}

IMPORTANT:
- Answer every question individually and professionally.
- Keep answers concise
- Return ONLY a valid JSON array, no explanation, no markdown, no extra text.
- Each item must have exactly two keys: "question" and "answer".
- Start directly with "[" and end with "]".

Example format:
[
  {{"question": "Why do you want this job?", "answer": "..."}},
  {{"question": "What is your experience with React?", "answer": "..."}}
]
"""

SKILL_EXTRACTION_PROMPT = """
You are an expert skill extraction assistant.

Extract all skills from the provided text and return them as a JSON array.

IMPORTANT:
- Extract ALL types of skills: technical, soft, domain-specific, tools, frameworks, methodologies, certifications, etc.
- Normalize skill names to their canonical form:
    * "ReactJS", "React.js", "React JS" → "React"
    * "NodeJS", "Node.js", "Node JS" → "Node.js"
    * "Postgres", "psql" → "PostgreSQL"
    * "MS Excel", "Microsoft Excel" → "Excel"
    * "Amazon Web Services" → "AWS"
    * "Don't pick name as skill such as " → "Andrew NG"
    * Apply the same normalization logic to any domain or industry.
- Return ONLY a valid JSON array of strings, no explanation, no markdown, no extra text.
- Start directly with "[" and end with "]".

Text:
{text}
"""

SKILL_INFERENCE_PROMPT = """
You are an expert technical recruiter and skill assessor.

Based on the candidate's known skills, determine which of the unmatched job skills they likely possess implicitly.

Candidate's Known Skills:
{resume_skills}

Unmatched Job Skills to Evaluate:
{unmatched_skills}

RULES:
- Only infer a skill if the candidate's known skills STRONGLY imply it.
- Examples of strong implication:
    * Knows FastAPI / Express.js / Django → implicitly knows "OOP", "MVC", "REST APIs", "Web Architecture"
    * Knows PostgreSQL / MongoDB / MySQL → implicitly knows "Database Fundamentals", "SQL"
    * Knows React / Next.js / Vue → implicitly knows "Web Architecture", "Component Design", "JavaScript"
    * Knows Docker / Kubernetes → implicitly knows "DevOps", "Linux"
    * Knows LangChain / RAG / ChromaDB → implicitly knows "AI/ML Fundamentals", "Python"
    * Knows Redux / RTK Query → implicitly knows "State Management", "OOP"
    * For MBA/finance: knows Excel / financial modeling → implicitly knows "Data Analysis", "Reporting"
- Do NOT infer loosely or generously — only include what is near-certain.
- Return ONLY a valid JSON array of the inferred skills from the unmatched list, no explanation, no markdown.
- If nothing can be inferred, return an empty array: []
- Start directly with "[" and end with "]".
"""