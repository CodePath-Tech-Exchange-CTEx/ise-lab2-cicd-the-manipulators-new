#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component
from datetime import datetime #to calculate total time summary (Jesus Munoz)
from datetime import datetime #to calculate total time summary (Jesus Munoz)
import streamlit as st



# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Displays a single user post in a two-column card layout.

    The post renders a large post image on the left, and on the right
    shows the user's profile image alongside their username and timestamp,
    with the post content displayed below.

    Parameters
    ----------
    username : str
        The display name of the user who created the post.
    user_image : str
        File path, URL, or image object for the user's profile picture.
    timestamp : str or datetime
        The date/time the post was created (e.g. "2024-02-20 10:34").
    content : str
        The text body of the post.
    post_image : str
        File path, URL, or image object for the post's main image.

    Returns
    -------
    None
    """
    data = { # Line written by Claude
        'USERNAME':   username, # Line written by Claude
        'USER_IMAGE': user_image, # Line written by Claude
        'TIMESTAMP':  timestamp, # Line written by Claude
        'CONTENT':    content, # Line written by Claude
        'POST_IMAGE': post_image, # Line written by Claude
    } # Line written by Claude

    html_file_name = "display_post" # Line written by Claude
    create_component(data, html_file_name, height=280) # Line written by Claude
    return data # Line written by Claude


def display_activity_summary(workouts_list):
    """
    Calculates activity metrics and renders a multi-component dashboard.

    This function processes a list of workout dictionaries to generate cumulative 
    totals (distance, calories, steps) and formats individual workout data into 
    HTML-styled boxes. 

    Args:
        workouts_list (list[dict]): A list of workout records. Each dictionary 
            should contain:
            - 'workout_id' (str): ID for the workout.
            - 'start_timestamp' (str): ISO formatted start time.
            - 'end_timestamp' (str): ISO formatted end time.
            - 'distance' (float): Distance covered in miles.
            - 'calories_burned' (int): Total calories burned.
            - 'steps' (int): Total step count.

    """
    
    # 1. Current Date
    current_date = datetime.now().strftime("%b %d, %Y")

    # 2. Calculate Totals - Sum up all workouts' metrics for the summary circles
    total_distance = sum(w.get('distance', 0) for w in workouts_list)
    total_calories = sum(w.get('calories_burned', 0) for w in workouts_list)
    total_steps = sum(w.get('steps', 0) for w in workouts_list)

    # 3. Build Workout Boxes - Create individual bordered boxes for each workout
    workout_boxes = []
    for workout in workouts_list:
        try:
            start = datetime.strptime(workout['start_timestamp'], '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(workout['end_timestamp'], '%Y-%m-%d %H:%M:%S')
            duration = end - start
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            time_str = f"{hours:02d}:{minutes:02d}"
        except:
            time_str = "00:30"

        
        box_html = '<div class="workout-item"><div class="workout-id">Workout ID: ' + workout['workout_id'] + '</div><div>Total Time: ' + time_str + '</div><div>Calories: ' + str(workout['calories_burned']) + '</div><div>Steps: ' + str(workout['steps']) + '</div><div>Distance: ' + str(workout['distance']) + ' mi</div></div>'
        workout_boxes.append(box_html)
    
    # Join all workout boxes into a single string (no separators needed)
    workout_content = ''.join(workout_boxes)

    # 4. Final data bundle
    data = {
        'DATE': current_date,
        'TOTAL_DISTANCE': round(total_distance, 1),
        'TOTAL_CALORIES': total_calories,
        'TOTAL_STEPS': total_steps,
        'WORKOUT_LIST': workout_content  
    }

    # 5. Render
    create_component(data, "display_activity_summary", height=900)
    

def display_recent_workouts(workouts_list):
    """Displays a single user recent workouts in a three rows.

    The page contain three rows of user's recent workouts. 
    Each row consist of details about the workout, which includes
    the name, calories burned, start and end times, steps taken and distance.
    
    Parameters
    ----------
    workouts_list : list[dict[str, str | int | float | tuple[float, float]]]
        The list of user's workouts with extra info. Each workout is a dictionary with the following keys:
            'workout_id',
            'start_timestamp',
            'end_timestamp',
            'start_lat_lng',
            'end_lat_lng',
            'distance',
            'steps',
            'calories_burned'. 
    

    Returns
    -------
    data_list: list[dict[str, str | int | float | tuple[float, float]]]
        The list of user's workouts with extra info. Each workout is a dictionary with the following keys:
            'WORKOUT_NAME',
            'CALORIES_BURNED',
            'START_TIME',
            'END_TIME',
            'STEPS',
            'DISTANCE'. 
    """
    html_file_name = "display_recent_workouts_header"
    data = {
        "TITLE" : "RECENT WORKOUTS"
    }
    create_component(data, html_file_name)

    html_file_name = "display_recent_workouts"

    recent_workouts = workouts_list[:3]
    data_list = []
    for workout in recent_workouts:
        data = {
            'WORKOUT_NAME': workout['workout_id'],
            'CALORIES_BURNED': workout['calories_burned'],
            'START_TIME': workout['start_timestamp'][11:],
            'END_TIME': workout['end_timestamp'][11:],
            'STEPS': workout['steps'],
            'DISTANCE': workout['distance']
        }
        data_list.append(data)
        create_component(data, html_file_name)

    return data_list


def display_genai_advice(timestamp, content, image):
    """Displays generative AI advice in a two-column card layout.

    The post renders a large image on the left, and on the right
    shows the timestamp and content of the generated AI advice. 

    Parameters
    ----------
    timestamp : str or datetime
        The date/time the post was created (e.g. "2024-02-20 10:34").
    content : str
        The text body of the post.
    image : str
        File path, URL, or image object for the post's main image.

    Returns
    -------
    None
    """
    data = { # Line written by Claude
        'TIMESTAMP': timestamp, # Line written by Claude
        'CONTENT':   content, # Line written by Claude
        'IMAGE':     image, # Line written by Claude
    } # Line written by Claude

    html_file_name = "display_genai_advice" # Line written by Claude
    create_component(data, html_file_name, height=450) # Line written by Claude
    return data # Line written by Claude

def display_navbar():
    # 1. The custom CSS to match your FIRST screenshot exactly
    st.markdown("""
        <style>
            /* 1. The main Navbar container */
            div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background-color: #DFDFDF;
                z-index: 9999;
                padding: 15px 0px;
                /* REMOVED: border-bottom: 6px solid #2b2b2b; */
                border-bottom: none !important; /* Forces the line to disappear */
                display: flex;
                justify-content: center;
            }

            /* 2. The Buttons */
            div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
                background-color: #C0DCFF !important;
                color: #111111 !important;
                border: none !important;        /* Removes the button's own border */
                outline: none !important;       /* Removes the focus outline */
                border-radius: 12px !important;
                font-family: 'DM Sans', sans-serif !important;
                font-weight: 700 !important;
                padding: 10px 20px !important;
                min-width: 140px !important;
                transition: background-color 0.2s ease !important;
                box-shadow: none !important;    /* Ensures no shadow looks like a line */
            }

            /* 3. Hover effect */
            div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
                background-color: #A8CCF5 !important;
                border: none !important;
            }

            /* 4. Spacing for page content */
            .main .block-container {
                padding-top: 80px !important;
            }
            
            header[data-testid="stHeader"] {
                visibility: hidden;
                height: 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # 2. The Layout: Use columns to center the buttons
    # We use empty 'spacer' columns on the left and right to force centering
    left_spacer, col1, col2, col3, right_spacer = st.columns([2, 1, 1, 1, 2])

    with col1:
        if st.button("Home", key="nav_home"):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("Challenges", key="nav_challenges"):
            st.session_state.page = "challenges"
            st.rerun()
    with col3:
        if st.button("Analytics", key="nav_analytics"):
            st.session_state.page = "analytics"
            st.rerun()

def _load_analytics_css():
    with open("custom_components/analytics_styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
 
 
def display_forecast_panel(workouts_predicted, risk_day, risk_analysis, streak_potential):
    """Renders the This Week Forecast panel.
 
    Displays predicted workout count, the highest-risk skip day,
    a GenAI risk analysis blurb, and the user's streak potential —
    all inside a styled card. Intended to be called inside a Streamlit
    column by display_analytics().
 
    Parameters
    ----------
    workouts_predicted : int or str
        Number of workouts predicted for the week (e.g. 4).
    risk_day : str
        The day most likely to be skipped (e.g. "Friday").
    risk_analysis : str
        GenAI explanation of why that day is a risk.
    streak_potential : int or str
        How many consecutive days the user could streak (e.g. 6).
 
    Returns
    -------
    None
    """
    st.markdown(
        f"""
        <div class="analytics-section-title">This Week Forecast</div>
        <div class="analytics-panel">
          <div class="forecast-row">
            <div>
              <div class="forecast-item-label">Workouts Predicted</div>
              <div class="forecast-item-value">
                <span class="forecast-pill">{workouts_predicted} / 5</span>
              </div>
            </div>
            <div>
              <div class="forecast-item-label">Risk Day</div>
              <div class="forecast-item-value">{risk_day}</div>
            </div>
            <div>
              <div class="forecast-item-label">Risk Analysis</div>
              <div class="forecast-item-value">{risk_analysis}</div>
            </div>
            <div>
              <div class="forecast-item-label">Streak Potential</div>
              <div class="forecast-item-value">
                <span class="forecast-pill">{streak_potential} days</span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
 
def display_risk_alerts_panel(risk_alerts):
    """Renders the Risk Alerts panel.
 
    Displays each alert as a left-accented chip card. If no alerts
    exist, shows a friendly fallback message. Intended to be called
    inside a Streamlit column by display_analytics().
 
    Parameters
    ----------
    risk_alerts : list[str]
        A list of alert strings generated by GenAI (e.g.
        ["You tend to skip after 2 rest days",
         "Your activity dropped vs last week"]).
        Pass an empty list if there are no alerts.
 
    Returns
    -------
    None
    """
    chips_html = (
        "".join(f'<div class="risk-alert-chip">{alert}</div>' for alert in risk_alerts)
        if risk_alerts
        else '<div class="risk-alert-chip">No alerts this week 🎉</div>'
    )
 
    st.markdown(
        f"""
        <div class="analytics-section-title">Risk Alerts</div>
        <div class="analytics-panel">
          {chips_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
 
 
def display_growth_panel(strength_growth, endurance_status, goal, eta_to_goal):
    """Renders the Growth Projections panel.
 
    Displays four growth metrics — strength trajectory, endurance
    status, current goal, and ETA — each in its own inset card.
    Intended to be called inside a Streamlit column by display_analytics().
 
    Parameters
    ----------
    strength_growth : str
        Strength projection description (e.g. "+10% in 3 weeks").
    endurance_status : str
        Endurance trend description (e.g. "Improving steadily").
    goal : str
        The user's current fitness goal (e.g. "Build endurance").
    eta_to_goal : str
        Estimated time to reach the goal (e.g. "5 weeks").
 
    Returns
    -------
    None
    """
    st.markdown(
        f"""
        <div class="analytics-section-title">Growth Projections</div>
        <div class="analytics-panel">
          <div class="growth-row">
            <div class="growth-item">
              <div class="growth-item-label">Strength</div>
              <div class="growth-item-value">{strength_growth}</div>
            </div>
            <div class="growth-item">
              <div class="growth-item-label">Endurance</div>
              <div class="growth-item-value">{endurance_status}</div>
            </div>
            <div class="growth-item">
              <div class="growth-item-label">Goal</div>
              <div class="growth-item-value">{goal}</div>
            </div>
            <div class="growth-item">
              <div class="growth-item-label">ETA to Goal</div>
              <div class="growth-item-value">{eta_to_goal}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def display_analytics(username, user_image, timestamp, workouts_list, genai_summary):
    """Orchestrates the full Analytics dashboard.
 
    Injects shared CSS once, renders the user profile header, then
    lays out three columns and delegates each panel to its own function:
      - col1 → display_forecast_panel()
      - col2 → display_risk_alerts_panel()
      - col3 → display_growth_panel()
 
    Parameters
    ----------
    username : str
        The display name of the logged-in user.
    user_image : str
        File path or URL for the user's profile picture.
    timestamp : str or datetime
        The date/time the analytics snapshot was generated.
    workouts_list : list[dict]
        The user's workout records (reserved for future metric calculations).
    genai_summary : dict
        GenAI-generated insights. Expected keys:
            'workouts_predicted' (int)
            'risk_day'           (str)
            'risk_analysis'      (str)
            'streak_potential'   (int)
            'risk_alerts'        (list[str])
            'strength_growth'    (str)
            'endurance_status'   (str)
            'goal'               (str)
            'eta_to_goal'        (str)
 
    Returns
    -------
    None
    """
    # ── Inject shared CSS once ────────────────────────────────────────────────
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    _load_analytics_css()
 
    # ── User profile header ───────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="analytics-header">
          <div class="analytics-avatar">USER<br>IMAGE</div>
          <div>
            <div class="analytics-username">{username}</div>
            <div class="analytics-timestamp">{timestamp}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
    # ── Unpack GenAI summary with safe fallbacks ──────────────────────────────
    workouts_predicted = genai_summary.get('workouts_predicted', '—')
    risk_day           = genai_summary.get('risk_day', '—')
    risk_analysis      = genai_summary.get('risk_analysis', '—')
    streak_potential   = genai_summary.get('streak_potential', '—')
    risk_alerts        = genai_summary.get('risk_alerts', [])
    strength_growth    = genai_summary.get('strength_growth', '—')
    endurance_status   = genai_summary.get('endurance_status', '—')
    goal               = genai_summary.get('goal', '—')
    eta_to_goal        = genai_summary.get('eta_to_goal', '—')
 
    # ── Three-column panel layout ─────────────────────────────────────────────
    col1, col2, col3 = st.columns(3, gap="medium")
 
    with col1:
        display_forecast_panel(workouts_predicted, risk_day, risk_analysis, streak_potential)
 
    with col2:
        display_risk_alerts_panel(risk_alerts)
 
    with col3:
        display_growth_panel(strength_growth, endurance_status, goal, eta_to_goal)
 
    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="analytics-footer">Analytics powered by GenAI · Data refreshes each session</div>',
        unsafe_allow_html=True,
    )