from app.services.summarizer import client
from app.models.article import Article


def generate_newsletter_content(
    articles,
):

    article_text = ""

    for article in articles:

        article_text += f"""
Title: {article.title}

Source: {article.source}

Summary:
{article.summary}

--------------------
"""

    prompt = f"""
You are an editor of a premium daily AI newsletter.

Using the stories below, create a concise newsletter.

Structure:

Top Stories

Research & Models

Industry News

Quick Takes

Keep the newsletter under 800 words.

Before writing:

1. Group articles covering the same story.
2. Merge duplicate stories into one entry.
3. Prioritize stories by significance.
4. Focus on developments from the last 24-48 hours.
5. Mention sources where appropriate.
6. Do not repeat the same company announcement twice.
7. Use only information provided in the articles.

Stories:

{article_text}
"""

    try:

        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=prompt
        )

        return response.text

    except Exception as e:

        print(f"Newsletter generation failed: {e}")

        return "Newsletter generation failed."