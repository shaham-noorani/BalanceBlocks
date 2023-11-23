import requests

import os
from dotenv import load_dotenv

load_dotenv()


def get_upcoming_tasks_on_notion_database():
    token = os.environ.get("NOTION_TOKEN")
    databaseID = os.environ.get("NOTION_DATABASE_ID")

    url = f"https://api.notion.com/v1/databases/{databaseID}/query"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22",
    }

    data = {
        "filter": {
            "property": "Status",
            "status": {"equals": "Not started"},
        }
    }

    response = requests.post(url, headers=headers, json=data)
    data = response.json()

    task_list = []
    for task in data["results"]:
        title = task["properties"]["Task"]["title"][0]["plain_text"]
        due_date = task["properties"]["Due"]["date"]["start"]
        category = task["properties"]["T"]["select"]["name"]
        priority = task["properties"]["Priority"]["select"]["name"]
        time_estimate_hours = task["properties"]["H"]["number"]

        task_list.append(
            {
                "title": title,
                "due_date": due_date,
                "category": category,
                "priority": priority,
                "time_estimate_hours": time_estimate_hours,
            }
        )

    return task_list
