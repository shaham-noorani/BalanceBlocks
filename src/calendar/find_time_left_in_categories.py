import datetime


def get_time_left_in_each_category(events, time_breakdowns):
    time_left_in_each_category = {}

    for time_breakdown in time_breakdowns:
        category = time_breakdown["Category"]
        time_left_in_each_category[category] = float(time_breakdown["Hours"])

    time_left_in_each_category["Other"] = 5

    for event in events:
        category = event["category"]
        start = datetime.datetime.strptime(event["start"], "%Y-%m-%dT%H:%M:%S%z")
        end = datetime.datetime.strptime(event["end"], "%Y-%m-%dT%H:%M:%S%z")
        duration = (end - start).total_seconds() / 3600

        time_left_in_each_category[category] -= duration

    return time_left_in_each_category
