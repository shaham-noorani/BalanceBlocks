getCategory = {
    "1": "SEC",
    "2": "Active",
    "3": "Kyleigh",
    "4": "Chill",
    "5": "Job Hunting",
    "6": "AggieInnovators",
    "7": "School",
    "9": "SEC",
    "10": "Friends",
    "11": "Tigers",
    "-1": "Other",
}

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class CalendarService:
    instance = None

    def __init__(self):
        if not CalendarService.instance:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                scopes=["https://www.googleapis.com/auth/calendar"],
            )
            creds = flow.run_local_server(port=0)
            CalendarService.instance = build("calendar", "v3", credentials=creds)
        else:
            pass

    @staticmethod
    def get_instance():
        if not CalendarService.instance:
            CalendarService()
        return CalendarService.instance
