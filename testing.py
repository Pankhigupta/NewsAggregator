import unittest
from unittest.mock import patch
from app import fetch_articles

class TestFetchArticles(unittest.TestCase):

    @patch('app.newsapi.get_top_headlines')
    def test_fetch_articles_valid(self, mock_get):
        mock_get.return_value = {
            'articles': [
                {
                    'title': 'Test Article',
                    'url': 'https://example.com',
                    'publishedAt': '2024-01-01T12:00:00Z'
                }
            ]
        }
        articles = fetch_articles(topic='technology', page=1)
        self.assertIsInstance(articles, list)

    @patch('app.newsapi.get_top_headlines')
    def test_fetch_articles_invalid_topic(self, mock_get):
        mock_get.side_effect = Exception('Invalid topic')
        articles = fetch_articles(topic='invalid', page=1)
        self.assertEqual(articles, [])

    @patch('app.newsapi.get_top_headlines')
    def test_fetch_articles_empty(self, mock_get):
        mock_get.return_value = {'articles': []}
        articles = fetch_articles(topic='general', page=1)
        self.assertEqual(len(articles), 0)

if __name__ == '__main__':
    unittest.main()
