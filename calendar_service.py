from datetime import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_events():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    now_in_ms = datetime.now().timestamp() * 1000

    # add to_date, one month from now
    one_day_in_ms = 86400000
    month_in_ms = 30 * one_day_in_ms
    to_date = str(datetime.fromtimestamp((now_in_ms + month_in_ms) / 1000).isoformat()) + 'Z'

    # call the Calendar API
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=to_date,
                                          maxResults=100, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    return format_events(events)


def format_events(events):
    formatted_events = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        formatted_events.append({'description': event['summary'], 'date': start[5:].replace('-', '.') + '.', 'summary': event['description']})
    return formatted_events
