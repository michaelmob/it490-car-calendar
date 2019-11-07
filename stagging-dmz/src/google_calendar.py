import os
import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow



def get_flow():
    """
    Create flow object.
    """
    return Flow.from_client_secrets_file(
        os.getenv('GOOGLE_SECRETS_FILE'),
        scopes='https://www.googleapis.com/auth/calendar.events',
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )


def get_oauth_link():
    """
    Get oauth login link.
    """
    flow = get_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')

    return auth_url


def get_flow_credentials():
    """
    Get flow stuff.

    This needs to be updated to get a refresher token.
    """
    flow = get_flow()
    flow.fetch_token(code=oauth_code)
    return flow.credentials


def add_events(oauth_code, events):
    """
    Add events to google calendar.

    `events` should be a dict containing the keys: summary, date
    """
    flow = get_flow()
    flow.fetch_token(code=oauth_code)

    service = build('calendar', 'v3', credentials=flow.credentials)
    calendar_events = service.events()
    result = []

    for event in events:
        event_date = {
            'date': event['date'],
            'timeZone': 'America/Los_Angeles'
        }
        body = {
            'summary': event['summary'],
            'start': event_date,
            'end': event_date
        }
        calendar_event = calendar_events.insert(calendarId='primary', body=body).execute()
        result.append(calendar_event.get('htmlLink'))

    return result
