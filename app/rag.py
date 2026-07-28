import os
import math

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def chunk_text(text: str, chunk_size: int = 500):
    """
    Split text into chunks of approximately
    chunk_size words.
    """

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk:
            chunks.append(chunk)

    return chunks


def create_embedding(text: str):
    """
    Generate an embedding for the given text.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def cosine_similarity(a, b):
    """
    Calculate cosine similarity between two vectors.
    """

    dot_product = sum(
        x * y
        for x, y in zip(a, b)
    )

    magnitude_a = math.sqrt(
        sum(x * x for x in a)
    )

    magnitude_b = math.sqrt(
        sum(y * y for y in b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def generate_answer(question: str, context: str):
    """
    Generate an answer using the OpenAI LLM
    based on the user's question and retrieved context.
    """

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using only the
information provided in the context below.

If the answer cannot be found in the context,
clearly say that the information is not available
in the uploaded documents.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You answer questions based on "
                    "the provided document context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content