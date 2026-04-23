#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from community_page import display_community_page
from login_page import display_login_page, FAKE_USER_ID
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts, display_navbar
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts


def main():
  userId = 'user1'
  st.set_page_config(layout="wide", page_title="SDS")

  if 'page' not in st.session_state:
    st.session_state.page = "home"

  if not st.session_state.get('logged_in'):
      display_login_page()
  else:
      # This stays at the top of every page
      display_navbar()
      
      # Logic to switch between pages
      if st.session_state.page == "home":
          display_community_page()
      elif st.session_state.page == "challenges":
          st.header("Challenges Page") # not needed
          # call display_challenges_page()
      elif st.session_state.page == "analytics":
          st.header("Analytics Page") # not needed
          # call display_analytics_page()



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
    main()