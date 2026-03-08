#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest

# Using MagicMock fakes objects rather than having to create a BigQuery connection - Kenneth
from unittest.mock import patch, MagicMock
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_workouts, get_user_sensor_data

class TestGenAIAdvice(unittest.TestCase):

    @patch('data_fetcher.get_user_workouts')
    @patch('data_fetcher.get_user_posts')
    @patch('google.genai.Client')
    def _make_mock_client(self, mock_client, mock_posts, mock_workouts, advice_text='Keep it up!'):
        """Helper to set up mocked genai client and user data."""
        mock_workouts.return_value = [{'workout_id': 'workout0', 'steps': 5000}]
        mock_posts.return_value = [{'post_id': 'post1', 'content': 'Feeling great!'}]
        mock_response = MagicMock()
        mock_response.text = advice_text
        mock_client.return_value.models.generate_content.return_value = mock_response
        return mock_client, mock_posts, mock_workouts

    @patch('data_fetcher.get_user_workouts')
    @patch('data_fetcher.get_user_posts')
    @patch('google.genai.Client')
    def test_returns_dict(self, mock_client, mock_posts, mock_workouts):
        """Test that the function returns a dictionary."""
        mock_workouts.return_value = []
        mock_posts.return_value = []
        mock_response = MagicMock()
        mock_response.text = 'Keep going!'
        mock_client.return_value.models.generate_content.return_value = mock_response

        result = get_genai_advice('user1')
        self.assertIsInstance(result, dict)

    @patch('data_fetcher.get_user_workouts')
    @patch('data_fetcher.get_user_posts')
    @patch('google.genai.Client')
    def test_returns_correct_keys(self, mock_client, mock_posts, mock_workouts):
        """Test that the returned dictionary has all required keys."""
        mock_workouts.return_value = []
        mock_posts.return_value = []
        mock_response = MagicMock()
        mock_response.text = 'Keep going!'
        mock_client.return_value.models.generate_content.return_value = mock_response

        result = get_genai_advice('user1')
        self.assertIn('advice_id', result)
        self.assertIn('timestamp', result)
        self.assertIn('content', result)
        self.assertIn('image', result)

    @patch('data_fetcher.get_user_workouts')
    @patch('data_fetcher.get_user_posts')
    @patch('google.genai.Client')
    def test_content_comes_from_genai(self, mock_client, mock_posts, mock_workouts):
        """Test that content is the text returned by the GenAI API."""
        mock_workouts.return_value = []
        mock_posts.return_value = []
        mock_response = MagicMock()
        mock_response.text = 'You are crushing it!'
        mock_client.return_value.models.generate_content.return_value = mock_response

        result = get_genai_advice('user1')
        self.assertEqual(result['content'], 'You are crushing it!')

    @patch('data_fetcher.get_user_workouts')
    @patch('data_fetcher.get_user_posts')
    @patch('google.genai.Client')
    def test_advice_id_contains_user_id(self, mock_client, mock_posts, mock_workouts):
        """Test that advice_id contains the user_id."""
        mock_workouts.return_value = []
        mock_posts.return_value = []
        mock_response = MagicMock()
        mock_response.text = 'Nice work!'
        mock_client.return_value.models.generate_content.return_value = mock_response

        result = get_genai_advice('user1')
        self.assertIn('user1', result['advice_id'])

    @patch('data_fetcher.get_user_workouts')
    @patch('data_fetcher.get_user_posts')
    @patch('google.genai.Client')
    def test_image_not_always_populated(self, mock_client, mock_posts, mock_workouts):
        """Test that image is not populated 100% of the time."""
        mock_workouts.return_value = []
        mock_posts.return_value = []
        mock_response = MagicMock()
        mock_response.text = 'Keep going!'
        mock_client.return_value.models.generate_content.return_value = mock_response

        # Run many times to check that None appears at least once
        images = set()
        for _ in range(20):
            result = get_genai_advice('user1')
            images.add(result['image'])

        self.assertIn(None, images)

class TestGetUserPosts(unittest.TestCase):

    def _make_mock_row(self, post_id, author_id, timestamp, image_url, content):
        """Helper to create a mock BigQuery row."""
        row = MagicMock()
        row.PostId = post_id
        row.AuthorId = author_id
        row.Timestamp = timestamp
        row.ImageUrl = image_url
        row.Content = content
        return row

    @patch('data_fetcher.bigquery.Client')
    def test_returns_list(self, mock_client):
        """Test that the function returns a list."""
        mock_client.return_value.query.return_value.result.return_value = []
        result = get_user_posts('user1')
        self.assertIsInstance(result, list)

    @patch('data_fetcher.bigquery.Client')
    def test_returns_correct_keys(self, mock_client):
        """Test that each post has the required keys."""
        mock_row = self._make_mock_row('post1', 'user1', '2024-01-01', 'image_url', 'Hello!')
        mock_client.return_value.query.return_value.result.return_value = [mock_row]

        posts = get_user_posts('user1')
        self.assertEqual(len(posts), 1)
        self.assertIn('user_id', posts[0])
        self.assertIn('post_id', posts[0])
        self.assertIn('timestamp', posts[0])
        self.assertIn('content', posts[0])
        self.assertIn('image', posts[0])

    @patch('data_fetcher.bigquery.Client')
    def test_returns_correct_values(self, mock_client):
        """Test that post values are correctly mapped from BigQuery columns."""
        mock_row = self._make_mock_row('post1', 'user1', '2024-01-01', 'image_url', 'Hello!')
        mock_client.return_value.query.return_value.result.return_value = [mock_row]

        posts = get_user_posts('user1')
        self.assertEqual(posts[0]['user_id'], 'user1')
        self.assertEqual(posts[0]['post_id'], 'post1')
        self.assertEqual(posts[0]['image'], 'image_url')
        self.assertEqual(posts[0]['content'], 'Hello!')

    @patch('data_fetcher.bigquery.Client')
    def test_empty_posts_for_unknown_user(self, mock_client):
        """Test that an unknown user returns an empty list."""
        mock_client.return_value.query.return_value.result.return_value = []
        result = get_user_posts('nonexistent_user')
        self.assertEqual(result, [])

    @patch('data_fetcher.bigquery.Client')
    def test_handles_null_fields(self, mock_client):
        """Test that None values for content and image are handled."""
        mock_row = self._make_mock_row('post1', 'user1', '2024-01-01', None, None)
        mock_client.return_value.query.return_value.result.return_value = [mock_row]

        posts = get_user_posts('user1')
        self.assertIsNone(posts[0]['image'])
        self.assertIsNone(posts[0]['content'])

    @patch('data_fetcher.bigquery.Client')
    def test_multiple_posts(self, mock_client):
        """Test that multiple posts are all returned."""
        mock_rows = [
            self._make_mock_row('post1', 'user1', '2024-01-01', 'img1', 'Post 1'),
            self._make_mock_row('post2', 'user1', '2024-01-02', None, 'Post 2'),
        ]
        mock_client.return_value.query.return_value.result.return_value = mock_rows

        posts = get_user_posts('user1')
        self.assertEqual(len(posts), 2)

class TestDataFetcher(unittest.TestCase):

    def test_foo(self):
        """Tests foo."""
        pass

if __name__ == "__main__":
    unittest.main()