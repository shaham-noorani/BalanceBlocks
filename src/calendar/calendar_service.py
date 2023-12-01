import pickle
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


class CalendarService:
    instance = None
    creds_file = "token.pkl"

    def __init__(self):
        if not CalendarService.instance:
            creds = None
            # Check if token file exists
            if os.path.exists(self.creds_file):
                with open(self.creds_file, "rb") as token:
                    creds = pickle.load(token)

            # If no valid credentials are available, then either refresh the token or log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json",
                        scopes=["https://www.googleapis.com/auth/calendar"],
                    )
                    creds = flow.run_local_server(port=0)

                # Save the credentials for the next run
                with open(self.creds_file, "wb") as token:
                    pickle.dump(creds, token)

            CalendarService.instance = build("calendar", "v3", credentials=creds)
        else:
            pass

    @staticmethod
    def get_instance():
        if not CalendarService.instance:
            CalendarService()
        return CalendarService.instance


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
