# BalanceBlocks

## Overview

This Python application is designed to manage and optimize your weekly calendar. It interacts with your Google Calendar, calculates the time left for various categories of activities, and generates recommendations for scheduling new events. Leverages a fine-tuned version of `GPT-3.5-turbo`

## Features

Event Fetching: Retrieves upcoming events from your Google Calendar.
Time Analysis: Calculates the remaining time available in different categories.
Event Recommendation: Suggests new events to add to your calendar based on available time and existing commitments.
Calendar Integration: Adds and deletes events from your Google Calendar.
Notion Integration: Fetches tasks from a Notion database.

## Setup

Python Version: Ensure you have Python 3.8 or higher installed.
Dependencies: Install required libraries using pip install -r requirements.txt (create this file with all necessary libraries).
Google Calendar API: Follow Google's guide to set up access to the Google Calendar API.
Notion API: Set up Notion API integration (if using the Notion task fetching feature).
Environment Variables: Place your Google and Notion API tokens in a .env file at the root.


## Usage


Run main.py to start the application.
The script will fetch events from your Google Calendar, suggest new events, and give you the option to add them to your calendar.
If integrated with Notion, uncomment the relevant sections to fetch tasks from your Notion database.


## Files and Modules


`main.py`: The main script to run the application.
`src/calendar/*.py`: Modules for interacting with the Google Calendar API and managing calendar events.
`src/openai/generate_recommended_calendar_events.py`: Uses OpenAI to generate recommended events.
`get_upcoming_tasks_on_notion_database.py`: (Commented out) Fetches tasks from a Notion database.


## Configuration

Modify `time_breakdowns.csv` to reflect your weekly time allocation.
Adjust `categories` in getCategory dictionary as needed.


## Future Enhancements

Integrate more advanced AI recommendations.
Provide a more interactive user interface.
Expand the integration to include other calendar and task management services.
