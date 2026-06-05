from app.services.summarizer import client
import json


def rank_article(articles):

    article_list = []

    for article in articles:

        article_list.append(
            f"""
ID: {article.id}
Title: {article.title}
Source: {article.source}
"""
        )

    prompt = f"""
You are an AI newsletter editor.

Your job is to identify stories that matter to:
- AI engineers
- founders
- investors
- researchers

Rate each story from 1-10.

Scoring:

10 = Major AI breakthrough, flagship model launch,
     major funding round, major regulation,
     major acquisition, industry-changing event

8-9 = Significant model launches,
      strategic partnerships,
      important research,
      notable company announcements

5-7 = Interesting developments

1-4 = Minor updates, tutorials,
      opinion pieces, niche news

Return ONLY valid JSON.

Example:

{{
    "1": 9,
    "2": 5,
    "3": 10
}}

Stories:

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
            f"Failed to parse ranking response: {e}"
        )

        print(
            f"Gemma response:\n{response.text}"
        )

        return {}