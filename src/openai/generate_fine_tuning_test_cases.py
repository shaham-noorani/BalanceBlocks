import json
from datetime import datetime
import random

categories = [
    "Active",
    "Kyleigh",
    "Chill",
    "Job Hunting",
    "AggieInnovators",
    "School",
    "SEC",
    "Friends",
    "Tigers",
    "Other",
]


def calculate_duration(start, end):
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    return (end_dt - start_dt).total_seconds() / 3600


def calculate_hours_per_category(events):
    category_hours = {category: 0 for category in categories}

    for event in events:
        duration = calculate_duration(event["start"], event["end"])
        category = event["category"]
        category_hours[category] += duration

    return category_hours


def generate_training_data():
    with open("../../data/all_past_events.json", "r") as fin:
        calendar_data = json.load(fin)

    fout = open("../../data/fine_tuning_test_cases.jsonl", "w")

    for week, events in calendar_data.items():
        existing_commitments = []
        existing_commitments_split = random.uniform(0.1, 0.4)

        hour_targets = calculate_hours_per_category(events)
        already_committed_hours = {category: 0 for category in hour_targets.keys()}

        for event in events:
            duration = calculate_duration(event["start"], event["end"])
            category = event["category"]

            # make sure classes and sec meetings are existing commitments
            if (
                category == "School" or category == "SEC"
            ) and not "FOCUS TIME" in event["title"]:
                already_committed_hours[category] += duration
                existing_commitments.append(event)
                existing_commitments_split -= 0.05
                continue

            if random.random() < existing_commitments_split:
                already_committed_hours[category] += duration
                existing_commitments.append(event)

        remaining_hours = {
            cat: hour_targets[cat] - already_committed_hours.get(cat, 0)
            for cat in hour_targets
        }

        system_message = {
            "role": "system",
            "content": "You are an AI assistant trained to help with blocking time in my calendar and providing JSON formatted responses.",
        }

        user_message = {
            "role": "user",
            "content": f"I need to allocate time for various activities based on my preferences and existing commitments. Here is how many hours I want to spend on each area of my life and my current commitments for the week of {week}. Hours in each category: {json.dumps(remaining_hours)}. Existing commitments: {json.dumps(existing_commitments)}. Please suggest a schedule for the remaining activities and output it in JSON format.",
        }

        remaining_events = [
            event for event in events if event not in existing_commitments
        ]
        assistant_message = {
            "role": "assistant",
            "content": json.dumps(remaining_events),
        }

        training_data_entry = {
            "messages": [system_message, user_message, assistant_message]
        }

        # Write to file
        fout.write(json.dumps(training_data_entry) + "\n")

    fout.close()


generate_training_data()
