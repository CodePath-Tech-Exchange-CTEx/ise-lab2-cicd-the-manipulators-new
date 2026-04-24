import streamlit as st
from data_fetcher import get_initial_challenges
from modules import display_challenges_grid

def display_challenges_page(user_id):
    if 'total_coins' not in st.session_state:
        st.session_state.total_coins = 0
    if 'my_challenges' not in st.session_state:          # ← must match
        st.session_state.my_challenges = get_initial_challenges()
    
    display_challenges_grid()