from langgraph.graph import StateGraph, END

from app.agents.state import AgentState

from app.agents.nodes.fetch_user_node import fetch_user_node
from app.agents.nodes.parse_resume_node import parse_resume_node
from app.agents.nodes.analyze_job_node import analyze_job_node
from app.agents.nodes.calculate_match_node import calculate_match_node
from app.agents.nodes.cover_letter_node import cover_letter_node


builder = StateGraph(AgentState)

builder.add_node("fetch_user", fetch_user_node)
builder.add_node("parse_resume", parse_resume_node)
builder.add_node("analyze_job", analyze_job_node)
builder.add_node("calculate_match", calculate_match_node)
builder.add_node("cover_letter", cover_letter_node)

builder.set_entry_point("fetch_user")

builder.add_edge("fetch_user", "parse_resume")
builder.add_edge("parse_resume", "analyze_job")
builder.add_edge("analyze_job", "calculate_match")
builder.add_edge("calculate_match", "cover_letter")
builder.add_edge("cover_letter", END)

job_graph = builder.compile()