from newspaper import Article

def scrape_article(url: str):

    try:
        article = Article(url)

        article.download()
        article.parse()

        return article.text

    except Exception as e:
        print(f"Scraping error: {e}")
        return ""