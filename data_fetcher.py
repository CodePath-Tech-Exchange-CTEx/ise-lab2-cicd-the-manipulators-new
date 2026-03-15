#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#
# You will re-write these functions in Unit 3, and are welcome to alter the
# data returned in the meantime. We will replace this file with other data when
# testing earlier units.
#############################################################################

import random
from google.cloud import bigquery

users = {
    'user1': {
        'full_name': 'Remi',
        'username': 'remi_the_rems',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user2', 'user3', 'user4'],
    },
    'user2': {
        'full_name': 'Blake',
        'username': 'blake',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1'],
    },
    'user3': {
        'full_name': 'Jordan',
        'username': 'jordanjordanjordan',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1', 'user4'],
    },
    'user4': {
        'full_name': 'Gemmy',
        'username': 'gems',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1', 'user3'],
    },
}


def get_user_sensor_data(user_id, workout_id):
    """Returns a list of timestampped information for a given workout.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    sensor_data = []
    sensor_types = [
        'accelerometer',
        'gyroscope',
        'pressure',
        'temperature',
        'heart_rate',
    ]
    for index in range(random.randint(5, 100)):
        random_minute = str(random.randint(0, 59))
        if len(random_minute) == 1:
            random_minute = '0' + random_minute
        timestamp = '2024-01-01 00:' + random_minute + ':00'
        data = random.random() * 100
        sensor_type = random.choice(sensor_types)
        sensor_data.append(
            {'sensor_type': sensor_type, 'timestamp': timestamp, 'data': data}
        )
    return sensor_data


def get_user_workouts(user_id):
    """Returns a list of user's workouts.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    workouts = []
    for index in range(random.randint(1, 3)):
        random_lat_lng_1 = (
            1 + random.randint(0, 100) / 100,
            4 + random.randint(0, 100) / 100,
        )
        random_lat_lng_2 = (
            1 + random.randint(0, 100) / 100,
            4 + random.randint(0, 100) / 100,
        )
        workouts.append({
            'workout_id': f'workout{index}',
            'start_timestamp': '2024-01-01 00:00:00',
            'end_timestamp': '2024-01-01 00:30:00',
            'start_lat_lng': random_lat_lng_1,
            'end_lat_lng': random_lat_lng_2,
            'distance': random.randint(0, 200) / 10.0,
            'steps': random.randint(0, 20000),
            'calories_burned': random.randint(0, 100),
        })
    return workouts


def get_user_profile(user_id):
    """Returns information about the given user.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    if user_id not in users:
        raise ValueError(f'User {user_id} not found.')
    return users[user_id]


def get_user_posts(user_id):
    """Returns a list of a user's posts.
    Some data in a post may not be populated.
    Input: user_id
    Output: A list of posts. Each post is a dictionary with keys user_id, post_id, timestamp, content, and image.   
    """
    client = bigquery.Client()
    
    query = """
        SELECT 
            PostId,
            AuthorId,
            Timestamp,
            ImageUrl,
            Content
        FROM `jesus-munoz-utep.ISE.Posts`
        WHERE AuthorId = @AuthorId
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("AuthorId", "STRING", user_id)
        ]
    )

    results = client.query(query, job_config=job_config).result()
    
    posts = []
    for row in results:
        posts.append({
            'user_id': row.AuthorId,
            'post_id': row.PostId,
            'timestamp': row.Timestamp,
            'content': row.Content,    # may be None
            'image': row.ImageUrl,     # may be None
        })
    
    return posts

def get_friends_posts(user_id):
    """Fetches the 10 most recent posts from a user's friends."""
    client = bigquery.Client()
    
    query = """
        SELECT 
            p.PostId,
            p.AuthorId,
            p.Timestamp,
            p.ImageUrl,
            p.Content,
            u.Username,
            u.ImageUrl as UserImageUrl
        FROM `jesus-munoz-utep.ISE.Posts` p
        JOIN `jesus-munoz-utep.ISE.Users` u ON u.UserId = p.AuthorId
        WHERE p.AuthorId IN (
            SELECT UserId2 FROM `jesus-munoz-utep.ISE.Friends`
            WHERE UserId1 = @user_id
            UNION DISTINCT
            SELECT UserId1 FROM `jesus-munoz-utep.ISE.Friends`
            WHERE UserId2 = @user_id
        )
        ORDER BY p.Timestamp DESC
        LIMIT 10
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    )
    
    results = client.query(query, job_config=job_config).result()
    
    posts = []
    for row in results:
        posts.append({
            'username': row.Username,
            'user_image': row.UserImageUrl,
            'timestamp': row.Timestamp,
            'content': row.Content,
            'image': row.ImageUrl
        })
    
    return posts

def get_genai_advice(user_id):
    """Returns the most recent advice from the GenAI API model based on the user's information.
    Images should not be populated 100% of the time.
    Input: user_id
    Output: A single dictionary with keys advice_id, timestamp, content, and image.
    """
    import datetime
    from google import genai
    from google.genai.types import HttpOptions

    # Fetch user's data to give AI context
    workouts = get_user_workouts(user_id)
    posts = get_user_posts(user_id)

    # Build a prompt with the user data
    prompt = f"""
    You are a fitness coach. Based on the user's recent activity, give them short motivational advice.
    Recent workouts: {workouts}
    Recent posts: {posts}

    Respond with either a one or two-sentence long short motivational sentence.
    """

    client = genai.Client(http_options=HttpOptions(api_version="v1"), vertexai=True, project="jesus-munoz-utep", location="us-central1")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return {
        'advice_id': f'advice_{user_id}_{datetime.datetime.now().timestamp()}',
        'timestamp': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
        'content': response.text,
        'image': random.choice([
            'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            None, None,  # None twice so image is not populated 100% of the time
        ]),
    }
