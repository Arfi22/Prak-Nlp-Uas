from __future__ import annotations

from langchain_groq import ChatGroq
from .config import GROQ_MODEL


def get_llm(temperature: float = 0.2):
    """
    Membuat objek chat model Groq untuk LangChain.
    """
    return ChatGroq(
        model=GROQ_MODEL,
        temperature=temperature
    )