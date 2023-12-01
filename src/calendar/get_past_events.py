import datetime
import json

from calendar_service import CalendarService, getCategory


def calculate_duration(start: str, end: str):
    start_dt = datetime.datetime.fromisoformat(start)
    end_dt = datetime.datetime.fromisoformat(end)

    return (end_dt - start_dt).total_seconds() / 3600


def calculate_hours_per_category(events):
    category_hours = {category: 0 for category in getCategory.values()}

    for event in events:
        duration = calculate_duration(event["start"], event["end"])
        category = event["category"]
        category_hours[category] += duration

    return category_hours


def five_or_more_days_have_at_least_two_events(events):
    events_by_day = {}
    for event in events:
        day = event["start"][:10]
        if day not in events_by_day:
            events_by_day[day] = []
        events_by_day[day].append(event)

    events_per_day = [len(events_by_day[day]) for day in events_by_day]
    return sum([1 for num_events in events_per_day if num_events >= 2]) >= 5


def parse_event_results(events_results):
    # Remove events that are all day events
    events_results["items"] = [
        event for event in events_results["items"] if "dateTime" in event["start"]
    ]

    # Create a list of events with just the title, start, end, and label
    events = []
    for event in events_results["items"]:
        category = getCategory.get(event.get("colorId", "-1"), "Other")

        if category == "SEC" and event["summary"].count(" ") == 0:
            event["summary"] = "SEC FOCUS TIME"
        elif category == "School" and event["summary"].count(" ") == 0:
            event["summary"] = "SCHOOL FOCUS TIME"

        events.append(
            {
                "title": event["summary"],
                "start": event["start"]["dateTime"],
                "end": event["end"]["dateTime"],
                "category": getCategory.get(event.get("colorId", "-1"), "Other"),
            }
        )

    return events


def fetch_events_for_last_n_weeks(n):
    service = CalendarService.get_instance()
    today = datetime.datetime.now()

    weekly_events = {}

    for week in range(n):
        print(f"Fetching events for {week} weeks ago")

        start_date = today - datetime.timedelta(days=(week + 1) * 7 - today.weekday())
        end_date = today - datetime.timedelta(days=week * 7 - today.weekday())

        events_results = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_date.isoformat() + "Z",
                timeMax=end_date.isoformat() + "Z",
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = parse_event_results(events_results)

        if (
            five_or_more_days_have_at_least_two_events(events)
            and calculate_hours_per_category(events)["Other"] < 12
        ):
            week_as_string = (
                start_date.strftime("%Y-%m-%d") + " to " + end_date.strftime("%Y-%m-%d")
            )
            weekly_events[week_as_string] = events
        else:
            print("week not added")

    # print number of weeks added
    print("Number of weeks added:", len(weekly_events))

    return weekly_events


def save_events_with_test_train_split(events):
    train_events = {}
    test_events = {}

    # save 80% of the events as train events
    num_train_events = int(len(events) * 0.8)
    for i in range(num_train_events):
        train_events[list(events.keys())[i]] = list(events.values())[i]

    # save 20% of the events as test events
    for i in range(num_train_events, len(events)):
        test_events[list(events.keys())[i]] = list(events.values())[i]

    with open("../../data/train_events.json", "w") as outfile:
        json.dump(train_events, outfile)

    with open("../../data/test_events.json", "w") as outfile:
        json.dump(test_events, outfile)


events = fetch_events_for_last_n_weeks(70)

# save to all_past_events.json
with open("../../data/all_past_events.json", "w") as outfile:
    json.dump(events, outfile)
