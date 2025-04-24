import os
from flask import Flask, render_template, request
from newsapi import NewsApiClient
from newspaper import Article
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("NEWS_API_KEY")
newsapi = NewsApiClient(api_key=API_KEY)

PAGE_SIZE = 4
TOPICS = ['general', 'technology', 'business', 'sports', 'science', 'health', 'entertainment']

def fetch_articles(topic='general', page=1):
    articles_data = []
    try:
        top_headlines = newsapi.get_top_headlines(
            category=topic,
            language='en',
            page_size=PAGE_SIZE,
            page=page
        )
        for news in top_headlines.get('articles', []):
            try:
                article_url = news.get('url')
                article = Article(article_url)
                article.download()
                article.parse()

                articles_data.append({
                    'title': news.get('title'),
                    'url': article_url,
                    'content': article.text[:120] + '...' if len(article.text) > 120 else article.text,
                    'image': article.top_image or 'https://via.placeholder.com/400x200.png?text=No+Image',
                    'timestamp': datetime.strptime(news['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                })
            except Exception as e:
                print(f"Skipping article: {e}")
                continue
    except Exception as e:
        print(f"Failed to fetch articles: {e}")
    return articles_data

@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    topic = request.args.get('topic', default='general', type=str)
    articles = fetch_articles(topic=topic, page=page)
    return render_template('index.html', articles=articles, page=page, topic=topic, topics=TOPICS)

if __name__ == '__main__':
    app.run(debug=True)
