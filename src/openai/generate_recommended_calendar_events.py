import os
from openai import OpenAI
import json

from dotenv import load_dotenv

load_dotenv()


def format_time_breakdowns(time_left_in_each_category: dict[str, float]):
    formatted_time_breakdowns = ""
    for category, hours in time_left_in_each_category.items():
        formatted_time_breakdowns += f'"{category}": {hours}, '

    return formatted_time_breakdowns[:-2]


def format_upcoming_events(upcoming_events):
    # format: "{"title": "Austin", "start": "2023-11-26T18:00:00-06:00", "end": "2023-11-27T00:00:00-06:00", "category": "Kyleigh"}"
    formatted_upcoming_events = ""
    for event in upcoming_events:
        formatted_upcoming_events += f'{{"title": "{event["title"]}", "start": "{event["start"]}", "end": "{event["end"]}", "category": "{event["category"]}"}}, '

    return formatted_upcoming_events[:-2]


def generate_recommended_calendar_events(time_left_in_each_category, upcoming_events):
    client = OpenAI(
        api_key=os.environ.get("OPEN_AI_TOKEN"),
    )

    formatted_time_breakdowns = format_time_breakdowns(time_left_in_each_category)
    formatted_upcoming_events = format_upcoming_events(upcoming_events)

    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant trained to help with blocking time in my calendar and providing JSON formatted responses.",
        },
        {
            "role": "user",
            "content": f"I need to allocate time for various activities based on my preferences and existing commitments. Here is how many hours I want to spend on each area of my life and my current commitments for the week of 2023-12-03 to 2023-12-9. Hours in each category: {formatted_time_breakdowns}. Existing commitments: {formatted_upcoming_events}. Please suggest a schedule for the remaining activities and output it in JSON format.",
        },
    ]

    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal::8QqfuHx6",
        messages=messages,
        max_tokens=1000,
        temperature=0,
    )

    reccomended_events = str(response.choices[0].message.content)

    print(reccomended_events)

    with open("../../data/out.json", "w") as outfile:
        outfile.write(reccomended_events)

    reccomended_events = json.loads(reccomended_events)

    return reccomended_events


time_left_in_each_category = {
    "Kyleigh": 23.0,
    "Friends": 7,
    "Active": 5.0,
    "Chill": 3.0,
    "SEC": 7,
    "Job Hunt": 5.0,
    "School": 3,
    "Tigers": 2,
    "AggieInnovators": 4,
    "Learning": 10.0,
}

upcoming_events = [
    {
        "title": "Pickleball",
        "start": "2023-12-03T11:00:00-06:00",
        "end": "2023-12-03T13:00:00-06:00",
        "category": "Friends",
    },
    {
        "title": "Parents Dinner!",
        "start": "2023-12-03T14:00:00-06:00",
        "end": "2023-12-03T15:00:00-06:00",
        "category": "Kyleigh",
    },
    {
        "title": "Valerie / Shaham",
        "start": "2023-12-03T16:00:00-06:00",
        "end": "2023-12-03T17:00:00-06:00",
        "category": "Friends",
    },
    {
        "title": "Protrip social!",
        "start": "2023-12-03T17:00:00-06:00",
        "end": "2023-12-03T19:00:00-06:00",
        "category": "SEC",
    },
    {
        "title": "Journal + Plan Week",
        "start": "2023-12-03T22:00:00-06:00",
        "end": "2023-12-03T23:00:00-06:00",
        "category": "Chill",
    },
    {
        "title": "INFO STORAGE & RETRIEVAL",
        "start": "2023-12-04T10:20:00-06:00",
        "end": "2023-12-04T11:10:00-06:00",
        "category": "School",
    },
    {
        "title": "MACHINE LEARNING",
        "start": "2023-12-04T11:30:00-06:00",
        "end": "2023-12-04T12:20:00-06:00",
        "category": "School",
    },
    {
        "title": "FW: Lunch: Student Leaders X COE Candidate Robert Bishop",
        "start": "2023-12-04T11:45:00-06:00",
        "end": "2023-12-04T12:45:00-06:00",
        "category": "Other",
    },
    {
        "title": "Lunch",
        "start": "2023-12-04T12:30:00-06:00",
        "end": "2023-12-04T13:30:00-06:00",
        "category": "Kyleigh",
    },
    {
        "title": "Sparks with Shaham",
        "start": "2023-12-04T13:30:00-06:00",
        "end": "2023-12-04T14:30:00-06:00",
        "category": "SEC",
    },
    {
        "title": "CLOUD COMPUTING",
        "start": "2023-12-04T16:10:00-06:00",
        "end": "2023-12-04T17:25:00-06:00",
        "category": "School",
    },
    {
        "title": "SEC General Council Meeting",
        "start": "2023-12-04T20:15:00-06:00",
        "end": "2023-12-04T21:15:00-06:00",
        "category": "SEC",
    },
    {
        "title": "Kyleigh",
        "start": "2023-12-04T22:30:00-06:00",
        "end": "2023-12-05T00:00:00-06:00",
        "category": "Chill",
    },
    {
        "title": "G17",
        "start": "2023-12-05T08:00:00-06:00",
        "end": "2023-12-05T09:00:00-06:00",
        "category": "Tigers",
    },
    {
        "title": "CS Reading Day Lunch",
        "start": "2023-12-05T13:00:00-06:00",
        "end": "2023-12-05T14:00:00-06:00",
        "category": "Other",
    },
    {
        "title": "EngDev Social",
        "start": "2023-12-05T15:00:00-06:00",
        "end": "2023-12-05T15:30:00-06:00",
        "category": "SEC",
    },
    {
        "title": "Peter / Shaham",
        "start": "2023-12-05T15:30:00-06:00",
        "end": "2023-12-05T16:30:00-06:00",
        "category": "Tigers",
    },
    {
        "title": "Kyleigh",
        "start": "2023-12-05T22:30:00-06:00",
        "end": "2023-12-06T00:00:00-06:00",
        "category": "Chill",
    },
    {
        "title": "call mom",
        "start": "2023-12-05T22:30:00-06:00",
        "end": "2023-12-05T23:00:00-06:00",
        "category": "Friends",
    },
    {
        "title": "Sparks with Shaham",
        "start": "2023-12-06T11:30:00-06:00",
        "end": "2023-12-06T12:30:00-06:00",
        "category": "SEC",
    },
    {
        "title": "FW: Lunch: Student Leaders X COE Candidate Srinath Ekkad",
        "start": "2023-12-06T11:45:00-06:00",
        "end": "2023-12-06T12:45:00-06:00",
        "category": "SEC",
    },
    {
        "title": "Shaham / Megha",
        "start": "2023-12-06T14:00:00-06:00",
        "end": "2023-12-06T15:00:00-06:00",
        "category": "SEC",
    },
    {
        "title": "G17",
        "start": "2023-12-06T20:00:00-06:00",
        "end": "2023-12-06T21:00:00-06:00",
        "category": "Tigers",
    },
    {
        "title": "Kyleigh",
        "start": "2023-12-06T22:30:00-06:00",
        "end": "2023-12-07T00:00:00-06:00",
        "category": "Chill",
    },
    {
        "title": "Yuval / Shaham",
        "start": "2023-12-07T09:00:00-06:00",
        "end": "2023-12-07T10:00:00-06:00",
        "category": "AggieInnovators",
    },
    {
        "title": "Shaham / Sean 1:1",
        "start": "2023-12-07T11:00:00-06:00",
        "end": "2023-12-07T12:00:00-06:00",
        "category": "SEC",
    },
    {
        "title": "ENGR 312 FINAL",
        "start": "2023-12-07T12:30:00-06:00",
        "end": "2023-12-07T14:30:00-06:00",
        "category": "School",
    },
    {
        "title": "Freshmen Involvement at SEC Career Fair",
        "start": "2023-12-07T13:00:00-06:00",
        "end": "2023-12-07T14:00:00-06:00",
        "category": "Other",
    },
    {
        "title": "Kyleigh",
        "start": "2023-12-07T22:30:00-06:00",
        "end": "2023-12-08T00:00:00-06:00",
        "category": "Chill",
    },
    {
        "title": "CS 412 FINAL",
        "start": "2023-12-08T15:30:00-06:00",
        "end": "2023-12-08T17:30:00-06:00",
        "category": "School",
    },
]

generate_recommended_calendar_events(time_left_in_each_category, upcoming_events)
