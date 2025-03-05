import streamlit as st
import pandas as pd
from datetime import datetime
from agent.agent import process_messages
from utils.format_message import get_formatted_message


# Title of the app
st.title("WhatsApp Events Assistant")
st.caption("🚀 An AI assistant to extract events from WhatsApp chat history")


# Ask the user to upload the WhatsApp history file
uploaded_file = st.file_uploader("Upload your WhatsApp history file", type=["txt"])

# If the file is uploaded, read the file and save it in a variable
if uploaded_file is not None:
    history_text = uploaded_file.read().decode("utf-8")

    # Format the message history
    formatted_history_text = get_formatted_message(history_text)

    # Process the messages and display the events   
    event_df = process_messages(formatted_history_text)

    # divider
    st.divider()

    # subheader
    st.subheader("Events Overview")

    # Display total number of events
    st.write(f"Total number of events: {len(event_df)}")

    # Display total number of participants
    st.write(f"Total number of participants: {len(event_df['participants'].explode().unique())}")


    # Create a copy of the event_df
    events_overview = event_df.copy()
    # Select the columns to display
    events_overview = events_overview[['event_date', 'time', 'event_name','participants', 'location']]
    # Sort the events by date, with the most recent events first
    events_overview = events_overview.sort_values(by='event_date', ascending=False)

    # display dataframe full width
    st.dataframe(events_overview, hide_index=True, use_container_width=True)


    # Function to display each event as a card
    def display_event_cards(event_df):
        today = datetime.now()  # Get the current date

        # Convert the 'date' column to datetime format for sorting
        event_df['event_date'] = pd.to_datetime(event_df['event_date'], format='%d.%m.%y')  # Adjust the format as needed

        # Sort the DataFrame by date, with the most recent events first
        sorted_events = event_df.sort_values(by='event_date', ascending=False)

        # Display events with labels
        for index, row in sorted_events.iterrows():
            event_date = row['event_date']  # Already in datetime format
            day_of_week = event_date.strftime('%A')  # Get the day of the week

            # Determine if the event is past or upcoming
            if event_date < today:
                event_label = f"<span style='color: #57606f; background-color: rgb(87 96 111 / 10%); padding: 1% 2%; border-radius: 4px; height: fit-content;'>Past Event</span>"
            else:
                event_label = f"<span style='color: #2ed573; background-color: #2ed5731f; padding: 1% 2%; border-radius: 4px; height: fit-content;'>Upcoming Event</span>" 

            # Custom card with border and shadow
            card_html = f"""
            <div style="display:flex; justify-content: space-between; border-radius: 8px; padding: 4%; margin: 10px 0; box-shadow: 2px 2px 20px rgba(0, 0, 0, 0.1);">
                <div>
                    <p style="font-weight: bold;">{event_date.strftime('%d.%m.%y')} - <span style="font-weight: normal;">{day_of_week}</span> </p>
                    <p>⏰ {row['time']}</p>
                    <p>📍 {row['location']}</p>
                    <p>Participants: {', '.join(row['participants'])}</p>
                    <p>Number of Participants: {row['number_of_participants']}</p>
                    <p>Not attending: {', '.join(row['not_attending'])}</p>
                    <p>Didn't confirm: {', '.join(row['didnt_confirm'])}</p>
                </div>
                {event_label}
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)  # Render the card

    # divider
    st.divider()

    # subheader
    st.subheader("Events Summary")

    # Display the events as cards
    display_event_cards(event_df)
