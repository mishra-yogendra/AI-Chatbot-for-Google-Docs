import os
from groq import Groq
from dotenv import load_dotenv
from config import LLM_MODEL
from utils.prompts import SYSTEM_PROMPT

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY not found. Please add it to a .env file."
    )

client = Groq(api_key=GROQ_API_KEY)


def generate_answer(context_docs, user_query, chat_history):
    """
    Generate answer using Groq Llama-3 with RAG context + chat history
    """

    context = "\n\n".join(
        f"[Section {i+1}] {doc.page_content}"
        for i, doc in enumerate(context_docs)
    )

    history = ""
    for turn in chat_history[-5:]:
        history += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"

    prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{history}

Context:
{context}

Question:
{user_query}
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content
