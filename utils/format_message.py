from datetime import datetime
import re

def get_formatted_message(message):
    # Define a regex pattern to find timestamps in the format [DD/MM/YY, HH:MM:SS]
    pattern = r'\[(\d{2}/\d{2}/\d{2}), (\d{2}:\d{2}:\d{2})\]'
    
    # Function to replace each timestamp with the desired format
    def replace_timestamp(match):
        date_str = match.group(1)  # Get the date part
        time_str = match.group(2)  # Get the time part
        # Combine date and time for parsing
        full_datetime_str = f"{date_str} {time_str}"
        # Parse the datetime
        message_datetime = datetime.strptime(full_datetime_str, "%d/%m/%y %H:%M:%S")
        # Get the day of the week
        day_of_week = message_datetime.strftime("%A")
        # Return the formatted timestamp with the day of the week
        return f"[{date_str}, {day_of_week} {time_str}]"

    # Replace all timestamps in the message history
    formatted_message = re.sub(pattern, replace_timestamp, message)
    
    return formatted_message