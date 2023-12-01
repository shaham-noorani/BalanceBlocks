from calendar_service import CalendarService
from delete_events_from_calendar import delete_events_from_calendar


def add_events_to_calendar(events):
    service = CalendarService.get_instance()

    added_event_ids = []
    for event in events:
        event = {
            "summary": event["title"],
            "start": {"dateTime": event["start"]},
            "end": {"dateTime": event["end"]},
        }

        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )

        added_event_ids.append(created_event["id"])

    return added_event_ids


events = [
    {
        "title": "STATISTICAL MODELS",
        "start": "2023-12-04T14:45:00-06:00",
        "end": "2023-12-04T15:35:00-06:00",
        "category": "School",
    },
    {
        "title": "DINNER",
        "start": "2023-12-04T19:00:00-06:00",
        "end": "2023-12-04T20:00:00-06:00",
        "category": "Kyleigh",
    },
    {
        "title": "Home",
        "start": "2023-12-04T21:15:00-06:00",
        "end": "2023-12-04T22:15:00-06:00",
        "category": "SEC",
    },
    {
        "title": "INFO STORAGE & RETRIEVAL",
        "start": "2023-12-05T10:20:00-06:00",
        "end": "2023-12-05T11:10:00-06:00",
        "category": "School",
    },
    {
        "title": "CLOUD COMPUTING",
        "start": "2023-12-05T16:10:00-06:00",
        "end": "2023-12-05T17:25:00-06:00",
        "category": "School",
    },
    {
        "title": "DINNER",
        "start": "2023-12-05T17:30:00-06:00",
        "end": "2023-12-05T18:30:00-06:00",
        "category": "Kyleigh",
    },
    {
        "title": "Home",
        "start": "2023-12-05T19:00:00-06:00",
        "end": "2023-12-05T22:00:00-06:00",
        "category": "SEC",
    },
    {
        "title": "INFO STORAGE & RETRIEVAL",
        "start": "2023-12-06T10:20:00-06:00",
        "end": "2023-12-06T11:10:00-06:00",
        "category": "School",
    },
    {
        "title": "Lunch",
        "start": "2023-12-06T12:30:00-06:00",
        "end": "2023-12-06T13:30:00-06:00",
        "category": "Kyleigh",
    },
    {
        "title": "MACHINE LEARNING",
        "start": "2023-12-06T13:30:00-06:00",
        "end": "2023-12-06T14:20:00-06:00",
        "category": "School",
    },
    {
        "title": "Home",
        "start": "2023-12-06T15:00:00-06:00",
        "end": "2023-12-06T20:00:00-06:00",
        "category": "SEC",
    },
    {
        "title": "DINNER",
        "start": "2023-12-06T18:00:00-06:00",
        "end": "2023-12-06T19:00:00-06:00",
        "category": "Kyleigh",
    },
    {
        "title": "Home",
        "start": "2023-12-06T21:00:00-06:00",
        "end": "2023-12-06T22:30:00-06:00",
        "category": "SEC",
    },
    {
        "title": "INFO STORAGE & RETRIEVAL",
        "start": "2023-12-07T10:20:00-06:00",
        "end": "2023-12-07T11:10:00-06:00",
        "category": "School",
    },
    {
        "title": "Lunch",
        "start": "2023-12-07T13:00:00-06:00",
        "end": "2023-12-07T14:00:00-06:00",
        "category": "Kyleigh",
    },
    {
        "title": "Home",
        "start": "2023-12-07T14:30:00-06:00",
        "end": "2023-12-07T17:00:00-06:00",
        "category": "SEC",
    },
    {
        "title": "DINNER",
        "start": "2023-12-07T17:00:00-06:00",
        "end": "2023-12-07T18:00:00-06:00",
        "category": "Kyleigh",
    },
    {
        "title": "Home",
        "start": "2023-12-07T19:30:00-06:00",
        "end": "2023-12-07T22:00:00-06:00",
        "category": "SEC",
    },
]

ids = add_events_to_calendar(events)

answer = input("Do you want to delete the events? (y/n) ")
if answer == "y":
    delete_events_from_calendar(ids)
