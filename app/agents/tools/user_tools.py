from langchain_core.tools import tool


@tool
async def get_user_profile_tool(user_profile: dict):
    """Return formatted user profile."""

    return f"""
    Name: {user_profile.get('name')}
    Desired Job: {user_profile.get('desired_job_title')}
    Skills: {user_profile.get('skills')}
    Experience: {user_profile.get('experience_level')}
    Preferences: {user_profile.get('job_preferences')}
    """