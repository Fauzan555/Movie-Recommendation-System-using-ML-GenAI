import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_explanation(selected_movie, recommended_movie, overview):
    """
    Generate a natural language explanation using LLaMA (Groq)
    """

    prompt = f"""
The user liked the movie {selected_movie}.

Explain why the movie {recommended_movie} is recommended.
Use simple, non-technical language.
Limit the explanation to 2–3 sentences.

Movie overview:
{overview}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()