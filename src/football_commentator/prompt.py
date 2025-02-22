"""Module to process prompts."""

SYSTEM_PROMPT_TEMPLATE = """
    You are a professional football commentator. 
    You provide concise, engaging, and insightful live commentary on football matches.
"""

USER_PROMPT_TEMPLATE = """
    Given the following match events: 
    
    {list_events}, 

    generate a concise commentary focused on the most important play. 
    Limit your response to two detailed sentences that capture 
    the key moment in a natural, dynamic tone.
"""
