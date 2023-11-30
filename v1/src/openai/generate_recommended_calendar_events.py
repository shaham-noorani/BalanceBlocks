import os
import openai
import json

from dotenv import load_dotenv

load_dotenv()


def format_time_breakdowns(time_breakdowns, time_left_in_each_category):
    # format: "category (description): time left"
    formatted_time_breakdowns = ""
    for time_breakdown in time_breakdowns:
        formatted_time_breakdowns += f"{time_breakdown['Category']} ({time_breakdown['Description']}): {time_left_in_each_category[time_breakdown['Category']]} hours left\n"

    return formatted_time_breakdowns


def format_upcoming_events(upcoming_events):
    # format: "title on date from start AM/PM to end AM/PM"
    formatted_upcoming_events = ""
    for event in upcoming_events:
        start_date = event["start"].split("T")[0]
        start_time = event["start"].split("T")[1].split("-")[0]
        end_time = event["end"].split("T")[1].split("-")[0]
        formatted_upcoming_events += (
            f"{event['title']} on {start_date} from {start_time} to {end_time}\n"
        )

    return formatted_upcoming_events


def generate_recommended_calendar_events(
    time_breakdowns, time_left_in_each_category, upcoming_events
):
    openai.api_key = os.environ.get("OPEN_AI_TOKEN")

    formatted_time_breakdowns = format_time_breakdowns(
        time_breakdowns, time_left_in_each_category
    )
    formatted_upcoming_events = format_upcoming_events(upcoming_events)

    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant trained to help with scheduling events in a calendar and providing JSON formatted responses.",
        },
        {
            "role": "user",
            "content": (
                f"I need to organize my schedule for the week."
                f"Here's the breakdown: {formatted_time_breakdowns}"
                f"I also have these events already scheduled: {formatted_upcoming_events}"
                f"Can you help me schedule the remaining activities and provide it in JSON format?"
            ),
        },
    ]

    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-1106:personal::8Oh54Lke",
        messages=messages,
        max_tokens=1000,
        temperature=0,
    )

    reccomended_events = response["choices"][0]["message"]["content"]

    with open("out.json", "w") as outfile:
        outfile.write(reccomended_events)

    # turn JSON into python dictionary
    reccomended_events = json.loads(reccomended_events)

    return reccomended_events


# time_breakdowns = [
#     {
#         "Category": "Kyleigh",
#         "Hours": "25",
#         "Description": "She is my girlfriend. I like to spend time with her at lunch, dinner, and at night.",
#     },
#     {
#         "Category": "Friends",
#         "Hours": "10",
#         "Description": "This could be lunch or dinner or hanging out (playing tennis or ping pong or getting boba). Typically lunch or afternoon/evening",
#     },
#     {
#         "Category": "Active",
#         "Hours": "5",
#         "Description": "Bouldering or playing tennis or running. Typically in the morning or afternoon and could be with friends",
#     },
#     {
#         "Category": "Chill",
#         "Hours": "10",
#         "Description": "Watching anime - this is typically at night",
#     },
#     {
#         "Category": "SEC",
#         "Hours": "15",
#         "Description": "This is my student organization - I'm a manager so this involves lots of meetings. Typically in the morning or afternoon",
#     },
#     {
#         "Category": "Job Hunt",
#         "Hours": "5",
#         "Description": "This is for applying to jobs and networking over zoom. I like to do this in the morning or afternoon",
#     },
#     {
#         "Category": "School",
#         "Hours": "10",
#         "Description": "Going to class and doing assignments. This is typically in the morning or afternoon",
#     },
#     {
#         "Category": "Tigers",
#         "Hours": "5",
#         "Description": "This is my network (involves weekly meetings and hanging out and occasional interviews or trips). This can happen at any time",
#     },
#     {
#         "Category": "AggieInnovators",
#         "Hours": "5",
#         "Description": "This is a student organization I'm trying to start that is an oncampus incubator. This work can happen at any time",
#     },
#     {
#         "Category": "Learning",
#         "Hours": "10",
#         "Description": "Reading books or working on coding projects or watching videos. This is typically done at night",
#     },
# ]
# time_left_in_each_category = {
#     "Kyleigh": 24.0,
#     "Friends": 9.5,
#     "Active": 5.0,
#     "Chill": 3.0,
#     "SEC": 4.5,
#     "Job Hunt": 5.0,
#     "School": 7.08,
#     "Tigers": 3.0,
#     "AggieInnovators": 5.0,
#     "Learning": 10.0,
# }
# upcoming_events = [
#     {
#         "title": "Protrip social-time tbd",
#         "start": "2023-12-03T17:00:00-06:00",
#         "end": "2023-12-03T19:00:00-06:00",
#         "category": "SEC",
#     },
#     {
#         "title": "Journal + Plan Week",
#         "start": "2023-12-03T22:00:00-06:00",
#         "end": "2023-12-03T23:00:00-06:00",
#         "category": "Chill",
#     },
#     {
#         "title": "INFO STORAGE & RETRIEVAL",
#         "start": "2023-12-04T10:20:00-06:00",
#         "end": "2023-12-04T11:10:00-06:00",
#         "category": "School",
#     },
#     {
#         "title": "MACHINE LEARNING",
#         "start": "2023-12-04T11:30:00-06:00",
#         "end": "2023-12-04T12:20:00-06:00",
#         "category": "School",
#     },
#     {
#         "title": "Lunch",
#         "start": "2023-12-04T12:30:00-06:00",
#         "end": "2023-12-04T13:30:00-06:00",
#         "category": "Kyleigh",
#     },
#     {
#         "title": "Sparks with Shaham",
#         "start": "2023-12-04T13:30:00-06:00",
#         "end": "2023-12-04T14:30:00-06:00",
#         "category": "SEC",
#     },
#     {
#         "title": "CLOUD COMPUTING",
#         "start": "2023-12-04T16:10:00-06:00",
#         "end": "2023-12-04T17:25:00-06:00",
#         "category": "School",
#     },
#     {
#         "title": "SEC General Council Meeting",
#         "start": "2023-12-04T20:15:00-06:00",
#         "end": "2023-12-04T21:15:00-06:00",
#         "category": "SEC",
#     },
#     {
#         "title": "Kyleigh",
#         "start": "2023-12-04T22:30:00-06:00",
#         "end": "2023-12-05T00:00:00-06:00",
#         "category": "Chill",
#     },
#     {
#         "title": "G17",
#         "start": "2023-12-05T08:00:00-06:00",
#         "end": "2023-12-05T09:00:00-06:00",
#         "category": "Tigers",
#     },
#     {
#         "title": "Kyleigh",
#         "start": "2023-12-05T22:30:00-06:00",
#         "end": "2023-12-06T00:00:00-06:00",
#         "category": "Chill",
#     },
#     {
#         "title": "call mom",
#         "start": "2023-12-05T22:30:00-06:00",
#         "end": "2023-12-05T23:00:00-06:00",
#         "category": "Friends",
#     },
#     {
#         "title": "Sparks with Shaham",
#         "start": "2023-12-06T11:30:00-06:00",
#         "end": "2023-12-06T12:30:00-06:00",
#         "category": "SEC",
#     },
#     {
#         "title": "Shaham / Megha",
#         "start": "2023-12-06T14:00:00-06:00",
#         "end": "2023-12-06T15:00:00-06:00",
#         "category": "SEC",
#     },
#     {
#         "title": "G17",
#         "start": "2023-12-06T20:00:00-06:00",
#         "end": "2023-12-06T21:00:00-06:00",
#         "category": "Tigers",
#     },
#     {
#         "title": "Kyleigh",
#         "start": "2023-12-06T22:30:00-06:00",
#         "end": "2023-12-07T00:00:00-06:00",
#         "category": "Chill",
#     },
#     {
#         "title": "Shaham / Sean 1:1",
#         "start": "2023-12-07T11:00:00-06:00",
#         "end": "2023-12-07T12:00:00-06:00",
#         "category": "SEC",
#     },
#     {
#         "title": "CF x VPD",
#         "start": "2023-12-07T12:30:00-06:00",
#         "end": "2023-12-07T13:30:00-06:00",
#         "category": "SEC",
#     },
#     {
#         "title": "Matthew x Shaham 1:1's",
#         "start": "2023-12-07T13:30:00-06:00",
#         "end": "2023-12-07T14:30:00-06:00",
#         "category": "SEC",
#     },
#     {
#         "title": "Weekly EB Meeting",
#         "start": "2023-12-07T18:00:00-06:00",
#         "end": "2023-12-07T19:30:00-06:00",
#         "category": "SEC",
#     },
#     {
#         "title": "Kyleigh",
#         "start": "2023-12-07T22:30:00-06:00",
#         "end": "2023-12-08T00:00:00-06:00",
#         "category": "Chill",
#     },
# ]

# print(
#     generate_recommended_calendar_events(
#         time_breakdowns, time_left_in_each_category, upcoming_events
#     )[0]["title"]
# )
