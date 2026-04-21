#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from community_page import display_community_page
from login_page import display_login_page, FAKE_USER_ID
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

userId = 'user1'


def display_app_page():
    """Displays the home page of the app."""
    st.title('Welcome to SDS!')

    # An example of displaying a custom component called "my_custom_component"
    value = st.text_input('Enter your name')
    display_my_custom_component(value)

def display_genai_advice_page():
    """Displays the genai advice page."""
    advice = get_genai_advice(userId) # Line written by Claude
    display_genai_advice( # Line written by Claude
        timestamp=advice['timestamp'], # Line written by Claude
        content=advice['content'], # Line written by Claude
        image=advice['image'] # Line written by Claude
    ) # Line written by Claude

def display_post_page():
    """Displays the post page."""
    posts = get_user_posts(userId) # Line written by Claude
    profile = get_user_profile(userId) # Line written by Claude
    for post in posts: # Line written by Claude
        display_post( # Line written by Claude
            username=profile['username'], # Line written by Claude
            user_image=profile['profile_image'], # Line written by Claude
            timestamp=post['timestamp'], # Line written by Claude
            content=post['content'], # Line written by Claude
            post_image=post['image'] # Line written by Claude
        ) # Line written by Claude

def display_activity_summary_page():
    """Displays the progress summary and workout list page."""
    #Fetch the data from your data_fetcher
    user_workouts = get_user_workouts(userId)
 
    # Pass that data into your UI module function
    display_activity_summary(user_workouts)

def display_recent_workouts_page():
    """Displays the recent workouts page."""
    workouts = get_user_workouts(userId) 
    display_recent_workouts(workouts) 

    
def display_activity_summary_page():
    """Displays the progress summary and workout list page."""
    #Fetch the data from your data_fetcher
    user_workouts = get_user_workouts(userId)
 
    # Pass that data into your UI module function
    display_activity_summary(user_workouts)

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="SDS")

    if not st.session_state.get('logged_in'):
        display_login_page()
    else:
        st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
          /* Collapse Streamlit's header so the navbar sits flush at the very top */
          header[data-testid="stHeader"] {
            height: 0 !important;
            min-height: 0 !important;
            padding: 0 !important;
          }
          /* Push page content below the fixed navbar */
          .block-container {
            padding-top: 90px !important;
          }
          /* Fixed navbar */
          .fixed-navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 9999;
            background: #DFDFDF;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            padding: 14px 24px;
            border-bottom: 6px solid #2b2b2b;
          }
          .nav-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 140px;
            padding: 14px 28px;
            background: #C0DCFF;
            border: none;
            border-radius: 10px;
            font-family: 'DM Sans', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            color: #111111;
            cursor: pointer;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
          }
          .nav-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          }
          .nav-btn.active {
            background: #a8ccf5;
          }
        </style>
        <nav class="fixed-navbar">
          <button class="nav-btn active">Home</button>
          <button class="nav-btn">Challenges</button>
          <button class="nav-btn">Analytics</button>
        </nav>
        """, unsafe_allow_html=True)
        display_community_page()