import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMMA_API_KEY")
)


def summarize_article(articles):

    article_list = []

    for article in articles:

        article_list.append(
            f"""
ID: {article.id}

TITLE:
{article.title}

CONTENT:
{article.content[:2000]}
"""
        )

    prompt = f"""
You are the editor of a premium AI newsletter.

Create summaries for all articles.

Requirements:
- 3-4 sentences each
- Professional
- Human sounding
- Explain what happened
- Explain why it matters
- Focus on impact
- Keep it concise
- No markdown
- No bullet points

Return ONLY valid JSON.

Example:

{{
    "1": "OpenAI launched a new model that improves reasoning capabilities. The release signals a major push toward enterprise adoption and could increase competition across the AI industry.",
    "2": "Anthropic announced..."
}}

Articles:

{chr(10).join(article_list)}
"""

    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt
    )

    cleaned = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        return json.loads(cleaned)

    except Exception as e:

        print(
            f"Failed to parse summaries: {e}"
        )

        print(
            f"Gemma response:\n{response.text}"
        )

        return {}