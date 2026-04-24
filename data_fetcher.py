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
import streamlit as st

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
        FROM `jesus-munoz-utep.ISE.Workouts`
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
        FROM `jesus-munoz-utep.ISE.Users`
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
    FROM `jesus-munoz-utep.ISE.INFORMATION_SCHEMA.COLUMNS`
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
            'timestamp': row.Timestamp.strftime('%Y-%m-%d %H:%M') if row.Timestamp else '',
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
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return {
        'advice_id': f'advice_{user_id}_{datetime.datetime.now().timestamp()}',
        'timestamp': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
        'content': response.text.strip().replace("\\'", "'").replace("\'", "'"),
        'image': random.choice([
            'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            None, None,
        ]),
    }

@st.cache_data(ttl=300)
def get_genai_analytics_summary(user_id):
    """Returns a GenAI-generated analytics summary based on the user's workout data.
    Input: user_id
    Output: A dictionary with keys for all three analytics panels.
    """
    import datetime
    from google import genai
    from google.genai.types import HttpOptions

    workouts = get_user_workouts(user_id)
    profile = get_user_profile(user_id)

    prompt = f"""
    You are a fitness analytics coach. Based on the user's workout history, return a JSON object only with no markdown or backticks.
    
    User profile: {profile}
    Recent workouts: {workouts}

    Return exactly this JSON structure:
    {{
        "workouts_predicted": <int, how many workouts they will likely do this week based on their pattern>,
        "risk_day": "<day of week they are most likely to skip>",
        "risk_analysis": "<one sentence explaining why that day is a risk>",
        "streak_potential": <int, how many consecutive days they could streak>,
        "risk_alerts": ["<alert 1>", "<alert 2>"],
        "strength_growth": "<short strength projection e.g. +10% in 3 weeks>",
        "endurance_status": "<short endurance trend description>",
        "goal": "<inferred fitness goal based on their activity>",
        "eta_to_goal": "<estimated time to reach goal e.g. 5 weeks>"
    }}
    """

    client = genai.Client(http_options=HttpOptions(api_version="v1"), vertexai=True, project="jesus-munoz-utep", location="us-central1")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    import json
    clean = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(clean)

def get_initial_challenges():
    return [
        {"id": "1", "description": "3 Days Challenge: 50 Burpees every morning", "reward": 30},
        {"id": "2", "description": "3 Days Challenge: 60 Push-ups daily", "reward": 35},
        {"id": "3", "description": "5 Days Challenge: 100 Jumping Jacks + 30 Squats", "reward": 45},
        {"id": "4", "description": "5 Days Challenge: 1-minute Plank + 40 Push-ups", "reward": 50},
        {"id": "5", "description": "7 Days Challenge: 70 Push-ups + 50 Sit-ups daily", "reward": 65},
        {"id": "6", "description": "7 Days Challenge: 100 Squats + 2-minute Plank", "reward": 70},
        {"id": "7", "description": "10 Days Challenge: 100 Burpees + 100 Jumping Jacks", "reward": 90},
        {"id": "8", "description": "10 Days Challenge: 150 Push-ups + 100 Sit-ups", "reward": 100},
        {"id": "9", "description": "14 Days Challenge: 200 Squats + 3-minute Plank daily", "reward": 120},
    ]


def generate_ai_challenge():
    import json
    import time
    from google import genai
    from google.genai.types import HttpOptions

    prompt = """
    You are a fitness challenge generator. Generate a single fitness challenge for a user.

    Return a JSON object only (no markdown, no backticks) with exactly this structure:
    {
        "description": "<A specific, actionable fitness challenge string, e.g. '3 Days Challenge: 50 Burpees every morning'>",
        "reward": <int, reward amount between 30 and 120 based on difficulty>
    }
    """

    client = genai.Client(
        http_options=HttpOptions(api_version="v1"),
        vertexai=True,
        project="jesus-munoz-utep",
        location="us-central1"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    clean = response.text.strip().replace("```json", "").replace("```", "")
    result = json.loads(clean)

    return {
        "id": str(int(time.time())),  # unique ID
        "description": result["description"],
        "reward": result["reward"]
    }