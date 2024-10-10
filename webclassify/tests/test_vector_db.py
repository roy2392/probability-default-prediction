import unittest
from unittest.mock import patch, MagicMock
from app.vector_db import store_vector, search_similar


class TestVectorDB(unittest.TestCase):

    @patch('app.vector_db.client')
    @patch('app.vector_db.model')
    def test_store_vector_new_url(self, mock_model, mock_client):
        # Mock the SentenceTransformer to return a dummy vector
        mock_model.encode.return_value = [0.1, 0.2, 0.3]

        # Mock the Qdrant client's search to return an empty result (URL not stored)
        mock_client.search.return_value = []

        # Mock the upsert function to simulate storing a vector
        mock_client.upsert.return_value = None

        # Test data
        content = "This is a test article about literature."
        url = "https://example-literature.com"
        category = "Books & Literature"

        # Call store_vector and assert the result
        vector_id = store_vector(content, url, category)
        self.assertIsNotNone(vector_id)

        # Ensure the model was called to encode content
        mock_model.encode.assert_called_with(content)

        # Ensure the client.search was called to check if URL exists
        mock_client.search.assert_called_once()

        # Ensure the client.upsert was called to store the new vector
        mock_client.upsert.assert_called_once()

    @patch('app.vector_db.client')
    @patch('app.vector_db.model')
    def test_store_vector_existing_url(self, mock_model, mock_client):
        # Mock the SentenceTransformer to return a dummy vector
        mock_model.encode.return_value = [0.1, 0.2, 0.3]

        # Mock the Qdrant client's search to return a result (URL already stored)
        mock_client.search.return_value = [
            MagicMock(payload={"url": "https://example-literature.com"}, id="existing-id")
        ]

        # Test data
        content = "This is a test article about literature."
        url = "https://example-literature.com"
        category = "Books & Literature"

        # Call store_vector and assert it returns the existing ID
        vector_id = store_vector(content, url, category)
        self.assertEqual(vector_id, "existing-id")

        # Ensure the model.encode was called to encode the URL
        mock_model.encode.assert_called_with(url)

        # Ensure the client.search was called to check if URL exists
        mock_client.search.assert_called_once()

        # Ensure the client.upsert was not called since the URL already exists
        mock_client.upsert.assert_not_called()

    @patch('app.vector_db.client')
    @patch('app.vector_db.model')
    @patch('app.vector_db.classify_website')
    def test_search_similar(self, mock_classify_website, mock_model, mock_client):
        # Mock the SentenceTransformer to return a dummy vector
        mock_model.encode.return_value = [0.1, 0.2, 0.3]

        # Mock the classify_website to return a specific category
        mock_classify_website.return_value = "Books & Literature"

        # Mock the Qdrant client's search to return results
        mock_client.search.return_value = [
            MagicMock(payload={"url": "https://example-literature1.com", "category": "Books & Literature"}, score=0.9),
            MagicMock(payload={"url": "https://example-literature2.com", "category": "Books & Literature"}, score=0.85),
            MagicMock(payload={"url": "https://example-other.com", "category": "Other"}, score=0.8)
        ]

        # Test data
        query = "Books & Literature"
        limit = 5

        # Call search_similar and assert the results are filtered correctly
        results = search_similar(query, limit)
        self.assertEqual(len(results), 2)  # Should only return items in the "Books & Literature" category
        self.assertEqual(results[0]["url"], "https://example-literature1.com")
        self.assertEqual(results[1]["url"], "https://example-literature2.com")

        # Ensure the model.encode was called to encode the query
        mock_model.encode.assert_called_with(query)

        # Ensure the client.search was called to search for similar vectors
        mock_client.search.assert_called_once()


if __name__ == '__main__':
    unittest.main()