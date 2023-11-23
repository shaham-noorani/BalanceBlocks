# imports

# setup dotenv
import os
from dotenv import load_dotenv

load_dotenv()

# read time breakdown from time_breakdowns.csv
import csv

time_breakdowns = []
with open("time_breakdowns.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        time_breakdowns.append(row)

# get task list from notion
from get_notion_task_list import get_upcoming_tasks_on_notion_database

tasks = get_upcoming_tasks_on_notion_database()

print(tasks)

# get calendar events from today to end of week (Saturday)

# add events to calendar

# ask user if they would like to keep the added events or restart with any changes
