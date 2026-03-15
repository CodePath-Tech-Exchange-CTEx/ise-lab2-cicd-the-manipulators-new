#############################################################################
# community_page.py
# Displays 10 most recent posts from friends
# Displays 1 GenAI advice
# This file contains the community feed page of the app.
#############################################################################

import streamlit as st
from modules import display_post, display_genai_advice
from data_fetcher import get_friends_posts, get_genai_advice

userId = 'user1'

def display_community_page():
    """Displays the community feed - friends' posts + GenAI advice."""
    st.set_page_config(layout="wide")
    st.title('Community Feed')

    st.subheader("What your friends are up to")
    posts = get_friends_posts(userId)

    if not posts:
        st.info("No posts from friends yet!")
    else:
        for i in range(0, len(posts), 2):
            col1, col2 = st.columns(2)

            with col1:
                post = posts[i]
                display_post(
                    username=post['username'],
                    user_image=post['user_image'],
                    timestamp=post['timestamp'],
                    content=post['content'],
                    post_image=post['image']
                )

            with col2:
                if i + 1 < len(posts):
                    post = posts[i + 1]
                    display_post(
                        username=post['username'],
                        user_image=post['user_image'],
                        timestamp=post['timestamp'],
                        content=post['content'],
                        post_image=post['image']
                    )

    # --- GenAI Advice ---
    st.divider()
    st.subheader("Your AI Health Tip")
    advice = get_genai_advice(userId)

    advice_col, _ = st.columns([1, 1])
    with advice_col: 
        display_genai_advice(
            timestamp=advice['timestamp'],
            content=advice['content'],
            image=advice['image']
        )