#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def setUp(self):
        self.result = display_post(
            username="johndoe",
            user_image="https://example.com/avatar.jpg",
            timestamp="2024-02-20 10:34 AM",
            content="Some content here.",
            post_image="https://example.com/post.jpg"
        )

    def test_username_in_data(self):
        """Username should be passed through correctly."""
        self.assertEqual(self.result['USERNAME'], "johndoe")

    def test_content_in_data(self):
        """Content should be passed through correctly."""
        self.assertEqual(self.result['CONTENT'], "Some content here.")

    def test_timestamp_in_data(self):
        """Timestamp should be passed through correctly."""
        self.assertEqual(self.result['TIMESTAMP'], "2024-02-20 10:34 AM")

    def test_all_keys_present(self):
        """All required template keys should be present in the data."""
        for key in ['USERNAME', 'USER_IMAGE', 'TIMESTAMP', 'CONTENT', 'POST_IMAGE']:
            self.assertIn(key, self.result)

    def test_no_empty_username(self):
        """Username should not be empty."""
        self.assertGreater(len(self.result['USERNAME']), 0)


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def setUp(self):
        self.result = display_genai_advice(
            timestamp="2024-01-01 00:00:00",
            content="You are doing great! Keep it up.",
            image="https://example.com/advice.jpg"
        )

    def test_timestamp_in_data(self):
        """Timestamp should be passed through correctly."""
        self.assertEqual(self.result['TIMESTAMP'], "2024-01-01 00:00:00")

    def test_content_in_data(self):
        """Content should be passed through correctly."""
        self.assertEqual(self.result['CONTENT'], "You are doing great! Keep it up.")

    def test_image_in_data(self):
        """Image should be passed through correctly."""
        self.assertEqual(self.result['IMAGE'], "https://example.com/advice.jpg")

    def test_all_keys_present(self):
        """All required template keys should be present in the data."""
        for key in ['TIMESTAMP', 'CONTENT', 'IMAGE']:
            self.assertIn(key, self.result)

    def test_no_username_key(self):
        """GenAI advice should not contain a USERNAME key since there is no user."""
        self.assertNotIn('USERNAME', self.result)


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def setUp(self):
        self.result = display_recent_workouts(
            [{
                'workout_id': 'workout0', 
                'start_timestamp': '2024-01-01 00:00:00', 
                'end_timestamp': '2024-01-01 00:30:00', 
                'start_lat_lng': (1.46, 4.95), 
                'end_lat_lng': (1.79, 4.99), 
                'distance': 0.3, 
                'steps': 19452, 
                'calories_burned': 62
                }]
        )[0]

    def test_all_keys_present(self):    
        """Checks if all keys are presesnt in the data."""
        for key in ['WORKOUT_NAME', 'CALORIES_BURNED', 'START_TIME', 'END_TIME', 'STEPS', 'DISTANCE']:
            self.assertIn(key, self.result)


    def test_workout_name(self):
        """Checks if workout name is the workout id."""
        self.assertEqual(self.result['WORKOUT_NAME'], 'workout0')

    def test_calories_burned(self):
        """Checks if calories burned is correct."""
        self.assertEqual(self.result['CALORIES_BURNED'], 62)

    def test_start_time(self):
        """Checks if start time is correct."""
        self.assertEqual(self.result['START_TIME'], '2024-01-01 00:00:00')

    def test_end_time(self):
        """Checks if end time is correct."""
        self.assertEqual(self.result['END_TIME'], '2024-01-01 00:30:00')

    def test_steps(self):
        """Checks if steps is correct."""
        self.assertEqual(self.result['STEPS'], 19452)

    def test_distance(self):
        """Checks if distance is correct."""
        self.assertEqual(self.result['DISTANCE'], 0.3)

if __name__ == "__main__":
    unittest.main()
