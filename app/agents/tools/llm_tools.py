from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from app.services.llm_service import model


@tool
async def generate_text_tool(prompt: str):
    """Generate text using Gemini."""

    response = await model.ainvoke([
        HumanMessage(content=prompt)
    ])

    return response.content