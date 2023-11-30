import datetime
import json

from calendar_service import CalendarService, getCategory


def five_or_more_days_have_at_least_two_events(events):
    events_by_day = {}
    for event in events:
        day = event["start"][:10]
        if day not in events_by_day:
            events_by_day[day] = []
        events_by_day[day].append(event)

    events_per_day = [len(events_by_day[day]) for day in events_by_day]
    return sum([1 for num_events in events_per_day if num_events >= 2]) >= 5


def parse_event_results(events_results):
    # Remove events that are all day events
    events_results["items"] = [
        event for event in events_results["items"] if "dateTime" in event["start"]
    ]

    # Create a list of events with just the title, start, end, and label
    events = []
    for event in events_results["items"]:
        events.append(
            {
                "title": event["summary"],
                "start": event["start"]["dateTime"],
                "end": event["end"]["dateTime"],
                "category": getCategory.get(event.get("colorId", "-1"), "Other"),
            }
        )

    return events


def fetch_events_for_last_n_weeks(n):
    service = CalendarService.get_instance()
    today = datetime.datetime.now()

    weekly_events = {}

    for week in range(n):
        print(f"Fetching events for {week} weeks ago")

        start_date = today - datetime.timedelta(days=(week + 1) * 7 - today.weekday())
        end_date = today - datetime.timedelta(days=week * 7 - today.weekday())

        events_results = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_date.isoformat() + "Z",
                timeMax=end_date.isoformat() + "Z",
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = parse_event_results(events_results)

        if five_or_more_days_have_at_least_two_events(events):
            week_as_string = (
                start_date.strftime("%Y-%m-%d") + " to " + end_date.strftime("%Y-%m-%d")
            )
            weekly_events[week_as_string] = events
        else:
            print("week not added")

    return weekly_events


def save_events_with_test_train_split(events):
    train_events = {}
    test_events = {}

    # save 80% of the events as train events
    num_train_events = int(len(events) * 0.8)
    for i in range(num_train_events):
        train_events[list(events.keys())[i]] = list(events.values())[i]

    # save 20% of the events as test events
    for i in range(num_train_events, len(events)):
        test_events[list(events.keys())[i]] = list(events.values())[i]

    with open("train_events.json", "w") as outfile:
        json.dump(train_events, outfile)

    with open("test_events.json", "w") as outfile:
        json.dump(test_events, outfile)


import datetime
import json
import numpy as np

# import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from calendar_service import CalendarService, getCategory


# Function to preprocess events and extract features and target variables
def preprocess_events(events):
    X = []  # Features
    y = []  # Target variable (duration)

    for week_events in events.values():
        for event in week_events:
            # Extract relevant features (you may need to customize this)
            # Example: Using day of the week (0=Monday, 6=Sunday) and start time in seconds since midnight
            start_time = datetime.datetime.strptime(
                event["start"], "%Y-%m-%dT%H:%M:%S%z"
            )
            day_of_week = start_time.weekday()
            start_seconds = (
                start_time.hour * 3600 + start_time.minute * 60 + start_time.second
            )

            # Append features and target variable
            X.append([day_of_week, start_seconds])
            y.append(
                event["duration"]
            )  # You need to define how to calculate the duration

    return np.array(X), np.array(y)


# Fetch events for the last N weeks and split them
events = fetch_events_for_last_n_weeks(100)
save_events_with_test_train_split(events)

# Load the saved training and testing events
with open("train_events.json", "r") as infile:
    train_events = json.load(infile)
with open("test_events.json", "r") as infile:
    test_events = json.load(infile)

# Preprocess the training and testing events
X_train, y_train = preprocess_events(train_events)
X_test, y_test = preprocess_events(test_events)

# Standardize the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create a neural network model
model = keras.Sequential(
    [
        keras.layers.Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.Dense(1),  # Output layer with one neuron for regression
    ]
)

# Compile the model
model.compile(optimizer="adam", loss="mean_squared_error")

# Train the model on the training data
model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")
