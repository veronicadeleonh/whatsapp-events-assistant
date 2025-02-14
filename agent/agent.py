from pydantic import BaseModel, Field
from openai import OpenAI   
import json
import pandas as pd
from dotenv import load_dotenv
from agent.prompts import SYSTEM_PROMPT


load_dotenv()

client = OpenAI()

class CalendarEvent(BaseModel):
    event_date: str = Field(description="The date of the event. Not the date the message timestamp.")
    time: str = Field(description="The time of the event")
    event_name: str = Field(description="The name of the event")
    participants: list[str] = Field(description="The participants of the event")
    number_of_participants: int = Field(description="The number of participants of the event")
    not_attending: list[str] = Field(description="The people who are not attending the event")
    didnt_confirm: list[str] = Field(description="The people who didn't confirm the event")
    location: str = Field(description="The location of the event")

class CalendarEvents(BaseModel):
    events: list[CalendarEvent]

def process_messages(message):
    
    # Initialize the OpenAI client
    client = OpenAI()

    # Make the OpenAI API call to extract the events
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        response_format=CalendarEvents,
    )

    # Parse the response
    response = completion.choices[0].message.parsed

    return pd.DataFrame([json.loads(event.model_dump_json()) for event in response.events])