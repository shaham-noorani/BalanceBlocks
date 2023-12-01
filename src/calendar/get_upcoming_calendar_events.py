import datetime

from calendar_service import CalendarService, getCategory


# Function to fetch events
def fetch_events(start_date):
    service = CalendarService.get_instance()

    # Calculate the upcoming Saturday from start_date
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
    next_saturday = start_date + datetime.timedelta((5 - start_date.weekday()) % 7)

    # Call the Calendar API and get the upcoming events
    events_results = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_date.isoformat() + "Z",
            timeMax=next_saturday.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    # Remove events that are all day events
    events_results["items"] = [
        event for event in events_results["items"] if "dateTime" in event["start"]
    ]

    # Create a list of events with just the title, start, end, and label
    events = []
    for event in events_results["items"]:
        events.append(
            {
                "title": event["summary"],
                "start": event["start"]["dateTime"],
                "end": event["end"]["dateTime"],
                "category": getCategory[event.get("colorId", "-1")],
            }
        )

    return events


start_date = datetime.datetime(2023, 12, 3).isoformat() + "Z"
upcoming_events = fetch_events(start_date)

print(upcoming_events)
