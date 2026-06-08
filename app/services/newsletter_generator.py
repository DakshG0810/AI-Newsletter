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

URL: {article.url}

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
8. Every story MUST end with a source link in markdown format.
(via [Source Name](Article URL))

Examples:

(via [TechCrunch](https://techcrunch.com/example))

(via [The Verge](https://theverge.com/example))

Do not place links anywhere else.
Do not place source names at the end of paragraphs.
Use the exact format above.
9. Every story MUST end with a source citation in EXACTLY this format
Example format:

## Top Stories

* **Headline:** Summary text. (via [TechCrunch](https://example.com))

* **Headline:** Summary text. (via [The Verge](https://example.com))

## Research & Models

* **Headline:** Summary text. (via [MarkTechPost](https://example.com))

Use bullet points throughout the newsletter.
Keep the structure exactly like the example.

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