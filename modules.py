#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component


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
    create_component(data, html_file_name, height=450) # Line written by Claude
    return data # Line written by Claude

def display_activity_summary(workouts_list):
    """Write a good docstring here."""
    pass


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
    None
    """
    html_file_name = "display_recent_workouts"

    recent_workouts = workouts_list[:3]
    for workout in recent_workouts:
        data = {
            'WORKOUT_NAME': workout['workout_id'],
            'CALORIES_BURNED': workout['calories_burned'],
            'START_TIME': workout['start_timestamp'],
            'END_TIME': workout['end_timestamp'],
            'STEPS': workout['steps'],
            'DISTANCE': workout['distance']
        }
        create_component(data, html_file_name, height=)

    return recent_workouts


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