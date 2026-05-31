# from langchain_google_genai import ChatGoogleGenerativeAI

# from app.core.config import settings


# model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     google_api_key=settings.GOOGLE_API_KEY,
#     temperature=0.2,
#     max_output_tokens=2048,
# )
# import os
# import asyncio
# from huggingface_hub import InferenceClient

# API_TOKEN = os.getenv("API_TOKEN")
# MODEL_ID = os.getenv("MODEL_ID", "HuggingFaceH4/zephyr-7b-beta")


# import os
# import asyncio

# from dotenv import load_dotenv
# from huggingface_hub import InferenceClient

# load_dotenv()

# API_TOKEN = os.getenv("API_TOKEN")
# MODEL_ID = os.getenv("MODEL_ID")

# print("TOKEN:", API_TOKEN)
# print("MODEL:", MODEL_ID)


# client = InferenceClient(
#     model=MODEL_ID,
#     token=API_TOKEN
# )

# class LLMService:

#     @staticmethod
#     async def generate(prompt: str) -> str:

#         # optional safety trim (token control)
#         prompt = prompt[:6000]

#         print("PROMPT:\n", prompt)

#         try:
#             # Run blocking HF call in a thread (NON-BLOCKING FASTAPI SAFE)
#             response = await asyncio.to_thread(
#                 client.chat_completion,
#                 messages=[
#                     {
#                         "role": "system",
#                         "content": (
#                             "You are an expert AI assistant for job applications. "
#                             "You write cover letters, analyze resumes, and answer job-related questions professionally."
#                         )
#                     },
#                     {
#                         "role": "user",
#                         "content": prompt
#                     }
#                 ],
#                 max_tokens=300,
#                 temperature=0.5,
#             )

#             result = response.choices[0].message.content

#             print("RESPONSE:\n", result)

#             return result

#         except Exception as e:
#             print("HF API error:", e)
#             return "AI service temporarily unavailable"


import os
import asyncio

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

client = Groq(api_key=GROQ_API_KEY)


class LLMService:

    @staticmethod
    async def generate(prompt: str,call_type:str) -> str:

        # optional safety trim (token control)
        # prompt = prompt[:6000]
        Max_Tokens=1024
        if call_type=="question_answer":
            Max_Tokens= 2048


        print("PROMPT:\n", prompt)

        try:
            # Run blocking Groq call in a thread (NON-BLOCKING FASTAPI SAFE)
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert AI assistant for job applications. "
                            "You write cover letters, analyze resumes, and answer job-related questions professionally."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=Max_Tokens,
                temperature=0.5,
            )

            result = response.choices[0].message.content

            print("RESPONSE:\n", result)

            return result

        except Exception as e:
            print("Groq API error:", e)
            return "AI service temporarily unavailable"