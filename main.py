import datetime
import csv

from src.calendar.get_upcoming_calendar_events import fetch_events
from src.calendar.find_time_left_in_categories import get_time_left_in_each_category
from src.openai.generate_recommended_calendar_events import (
    generate_recommended_calendar_events,
)
from src.calendar.add_events_to_calendar import add_events_to_calendar
from src.calendar.delete_events_from_calendar import delete_events_from_calendar

# setup dotenv
import os
from dotenv import load_dotenv

load_dotenv()

# read time breakdown from time_breakdowns.csv
time_breakdowns = []
with open("data/time_breakdowns.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        time_breakdowns.append(row)

# get task list from notion
# from get_notion_task_list import get_upcoming_tasks_on_notion_database

# tasks = get_upcoming_tasks_on_notion_database()
# print(tasks)


# get calendar events from today to end of week (Saturday)
start_date = datetime.datetime(2023, 12, 3).isoformat() + "Z"
upcoming_events = fetch_events(start_date)

# get time left in each category
time_left_in_each_category = get_time_left_in_each_category(
    upcoming_events, time_breakdowns
)


def generate_reccomendations_and_ask_user():
    # generate reccomended calendar events
    recommended_events = generate_recommended_calendar_events(
        time_breakdowns, time_left_in_each_category, upcoming_events
    )

    # add events to calendar
    added_event_ids = add_events_to_calendar(recommended_events)

    # ask user if they would like to keep the added events or restart with any changes
    keep_events = input("Would you like to keep the added events? (y/n): ")

    if keep_events == "n":
        delete_events_from_calendar(added_event_ids)
        generate_reccomendations_and_ask_user()
    else:
        print("Hope you have a productive week!")


generate_reccomendations_and_ask_user()
