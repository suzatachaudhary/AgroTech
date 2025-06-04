# Dictionary to store user activity history
user_activity = {}

def log_user_activity(user_name, activity):
    
    #Logs the activity of a user.
   
    if user_name not in user_activity:
        user_activity[user_name] = []  # Initialize activity list for the user
    user_activity[user_name].append(activity)
    return "Activity logged successfully."

def get_user_history(activity):

    # Retrieves the history of a user's activity
    if activity in user_activity:
        return user_activity[activity]
    return "No history found for this user."
