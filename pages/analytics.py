#############################################################################
# analytics_page.py
#
# Analytics page for the fitness app.
# Displays personalized forecasts, risk alerts, and growth projections
# using GenAI-powered insights from the user's workout data.
#############################################################################

import streamlit as st
from modules import display_analytics


def display_analytics_page(username, user_image, timestamp, workouts_list, genai_summary):
    """Renders the full Analytics page.

    Displays the shared navbar at the top, then the analytics dashboard
    containing this-week forecast, risk alerts, and growth projections
    powered by GenAI analysis of the user's workout history.

    Parameters
    ----------
    username : str
        The display name of the logged-in user.
    user_image : str
        File path or URL for the user's profile picture.
    timestamp : str or datetime
        The date/time the analytics were last generated (e.g. "2024-02-20 10:34").
    workouts_list : list[dict]
        The user's workout records. Each dict should contain:
            'workout_id', 'start_timestamp', 'end_timestamp',
            'distance', 'calories_burned', 'steps'.
    genai_summary : dict
        GenAI-generated insights with the following keys:
            'workouts_predicted' (int)   : Predicted workouts this week.
            'risk_day'          (str)    : Day most likely to be skipped.
            'risk_analysis'     (str)    : Explanation of the risk pattern.
            'streak_potential'  (int)    : Potential streak length in days.
            'risk_alerts'       (list)   : List of alert strings.
            'strength_growth'   (str)    : Strength projection (e.g. "+10% in 3 weeks").
            'endurance_status'  (str)    : Endurance trend description.
            'goal'              (str)    : User's current fitness goal.
            'eta_to_goal'       (str)    : Estimated time to reach goal.

    Returns
    -------
    None
    """
    display_analytics(username, user_image, timestamp, workouts_list, genai_summary)