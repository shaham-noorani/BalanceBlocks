from src.calendar.calendar import CalendarService


# add events to calendar and return ids of events added
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
