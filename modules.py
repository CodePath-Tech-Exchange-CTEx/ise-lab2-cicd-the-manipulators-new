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
    """Displays the progress summary and workout list page."""
    
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
    """Write a good docstring here."""
    pass


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