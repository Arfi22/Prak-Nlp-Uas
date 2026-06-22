import os

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant"
)

PROJECT_NAME = os.getenv(
    "LANGSMITH_PROJECT",
    "finmentor-nlp-uas"
)