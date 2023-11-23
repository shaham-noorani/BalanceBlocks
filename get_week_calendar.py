from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import google.auth
import datetime
import os


# Function to authenticate and get the service
def get_calendar_service():
    creds = None

    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/calendar.readonly"],
    )
    creds = flow.run_local_server(port=0)

    return build("calendar", "v3", credentials=creds)


# Function to fetch events
def fetch_events():
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + "Z"

    # Calculate the upcoming Saturday
    next_saturday = datetime.datetime.now() + datetime.timedelta(
        (5 - datetime.datetime.now().weekday()) % 7
    )
    next_saturday = (
        next_saturday.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()
        + "Z"
    )

    # Call the Calendar API and get the upcoming events
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            timeMax=next_saturday,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events_results = events_result.get("items", [])

    # Create a list of events with just the title, start, and end
    events = []
    for event in events_results:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        events.append(
            {
                "title": event["summary"],
                "start": start,
                "end": end,
            }
        )

    return events
