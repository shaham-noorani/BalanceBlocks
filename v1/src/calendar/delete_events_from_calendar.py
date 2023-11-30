from src.calendar.calendar import CalendarService


def delete_events_from_calendar(event_ids):
    service = CalendarService.get_instance()

    for event_id in event_ids:
        service.events().delete(calendarId="primary", eventId=event_id).execute()

    print("Deleted events from calendar")
