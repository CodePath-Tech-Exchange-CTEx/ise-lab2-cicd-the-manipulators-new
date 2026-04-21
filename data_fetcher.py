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
    client = bigquery.Client()
    query = """
        SELECT
            WorkoutId,
            StartTimestamp,
            EndTimestamp,
            StartLocationLat,
            StartLocationLong,
            EndLocationLat,
            EndLocationLong,
            TotalDistance,
            TotalSteps,
            CaloriesBurned
        FROM `kenneth-ly-csu-fullerton.ISE.Workouts`
        WHERE UserId = @UserId
        """
            
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("UserId", "STRING", user_id)
        ])

    results = client.query(query, job_config=job_config).result()

    workouts = []
    for row in results:
        workouts.append({
            'workout_id': row.WorkoutId,
            'start_timestamp': row.StartTimestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'end_timestamp': row.EndTimestamp.strftime('%Y-%m-%d %H:%M:%S'),  
            'start_lat_lng': (row.StartLocationLat, row.StartLocationLong),
            'end_lat_lng': (row.EndLocationLat, row.EndLocationLong),
            'distance': row.TotalDistance,
            'steps': row.TotalSteps,
            'calories_burned': int(row.CaloriesBurned),
        })

    return workouts


def get_user_profile(user_id):
    """Returns information about the given user.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    client = bigquery.Client()

    query = """
        SELECT
            Name,
            Username,
            DateofBirth,
            ImageUrl
        FROM `kenneth-ly-csu-fullerton.ISE.Users`
        WHERE UserId = @UserId
            """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("UserId", "STRING", user_id)
        ])

    result = client.query(query, job_config=job_config).result()

    for row in result:
        user_profile = {
            'full_name': row.Name,
            'username': row.Username,
            'date_of_birth': row.DateofBirth.strftime('%Y-%m-%d'),
            'profile_image': row.ImageUrl,
            'friends': []
        }

    query = """
    SELECT column_name
    FROM `kenneth-ly-csu-fullerton.ISE.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'Friends'
    """
    result = client.query(query).result()

    for row in result:
        user_profile['friends'].append(row.column_name)
    
    return user_profile


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
        FROM `kenneth-ly-csu-fullerton.ISE.Posts`
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
        FROM `kenneth-ly-csu-fullerton.ISE.Posts` p
        JOIN `kenneth-ly-csu-fullerton.ISE.Users` u ON u.UserId = p.AuthorId
        WHERE p.AuthorId IN (
            SELECT UserId2 FROM `kenneth-ly-csu-fullerton.ISE.Friends`
            WHERE UserId1 = @user_id
            UNION DISTINCT
            SELECT UserId1 FROM `kenneth-ly-csu-fullerton.ISE.Friends`
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
    import datetime
    from google import genai
    from google.genai.types import HttpOptions

    image_options = {
        'running': 'https://images.unsplash.com/photo-1571008887538-b36bb32f4571',
        'weightlifting': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48',
        'yoga': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b',
        'cycling': 'https://images.unsplash.com/photo-1541625602330-2277a4c46182',
        'general_fitness': 'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1',
    }

    workouts = get_user_workouts(user_id)
    posts = get_user_posts(user_id)

    prompt = f"""
    You are a fitness coach. Based on the user's recent activity, give them short motivational advice.
    Recent workouts: {workouts}
    Recent posts: {posts}

    Respond in this EXACT format and nothing else:
    ADVICE: <one or two sentence motivational advice>
    IMAGE: <one of: running, weightlifting, yoga, cycling, general_fitness>

    Pick the IMAGE key that best matches the advice or workout type. Do not explain the image choice.
    """

    client = genai.Client(http_options=HttpOptions(api_version="v1"), vertexai=True, project="kenneth-ly-csu-fullerton", location="us-central1")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    # Parse the response
    advice_text = response.text.strip()  # fallback: use full response if no ADVICE: prefix
    image_key = 'general_fitness'

    for line in response.text.strip().splitlines():
        if line.startswith('ADVICE:'):
            advice_text = line.replace('ADVICE:', '').strip().replace('\\', '')
        elif line.startswith('IMAGE:'):
            key = line.replace('IMAGE:', '').strip().lower()
            if key in image_options:
                image_key = key

    return {
        'advice_id': f'advice_{user_id}_{datetime.datetime.now().timestamp()}',
        'timestamp': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
        'content': advice_text,
        'image': random.choice([
            image_options[image_key],
            None, None,  # None twice so image is not populated 100% of the time
        ]),
    }