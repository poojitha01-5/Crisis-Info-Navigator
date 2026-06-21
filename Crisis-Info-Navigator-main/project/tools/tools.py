from typing import Any, Dict, List
import os
import textwrap

import google.generativeai as genai


def _ensure_configured() -> None:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Please set it before calling disaster guidance."
        )
    genai.configure(api_key=api_key)


def hotline_lookup(region: str = "generic") -> Dict[str, str]:
    """
    Stubbed hotline lookup. This stays simple and generic.
    """
    if region.lower() in ("india", "in"):
        return {
            "general_emergency": "112",
            "disaster_management": "108",  # example
        }
    return {
        "general_emergency": "911/112 (depending on your country)",
        "disaster_management": "Check your local government's disaster helpline.",
    }


def calculator(expression: str) -> float:
    """
    Very small calculator tool using a restricted eval environment.
    """
    try:
        value = eval(expression, {"__builtins__": {}}, {})
        return float(value)
    except Exception:
        return float("nan")


def generic_search(query: str) -> List[Dict[str, str]]:
    """
    Stubbed generic search tool.
    """
    return [
        {
            "title": "Generic safety guidance",
            "snippet": f"High-level safety information for query: {query}",
            "link": "https://example.com/search",
        }
    ]


def generate_disaster_guidance_llm(
    disaster_type: str,
    phase: str,
    region: str,
    raw_input: str,
) -> str:
    """
    Use Google Gemini to generate non-medical safety guidance dynamically
    for any kind of disaster, based on the user input and detected phase.
    """
    _ensure_configured()

    system_instructions = textwrap.dedent(
        """
        You are a calm, factual, non-medical disaster safety assistant.

        Your job:
        - Give clear, short, actionable safety steps.
        - Prioritise immediate safety over everything else.
        - Never give medical diagnosis or detailed treatment instructions.
        - Do not invent hotline numbers or specific local services.
        - Encourage users to follow local authority and emergency service guidance.

        Output format:
        - A numbered list of 6–10 steps.
        - Each step should be one sentence.
        """
    ).strip()

    user_context = textwrap.dedent(
        f"""
        Disaster type (may be generic): {disaster_type}
        Phase: {phase}
        Region or country (if known): {region}
        User message: {raw_input}
        """
    ).strip()

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        [
            system_instructions,
            "",
            "Now generate safety guidance:\n",
            user_context,
        ]
    )
    text = response.text or ""
    return text.strip()
