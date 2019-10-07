from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
SCOPES = "https://www.googleapis.com/auth/youtube"
store = file.Storage('youtube_token.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('youtube_key.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('youtube', 'v3', credentials=creds)
'''calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
if calendar_list_entry['accessRole']:
	startTime = datetime.strptime(input("Please enter in the start time for the event in this format: (ex. September 02, 2018, 09:00PM) "), '%B %m, %Y, %I:%M%p').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
	endTime = datetime.strptime(input("Please enter in the end time for the event in this format: (es. September 03, 2018, 11:25AM) "), '%B %m, %Y, %I:%M%p').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
	event = {
		'summary': input("What's the name of the event? "),
		#'location': snip,
		#'description': snip,
		'start': {
			'dateTime': startTime,
			'timeZone': 'America/New_York',
		},
		'end': {
			'dateTime': endTime,
			'timeZone': 'America/New_York',
		},
	}
	event = service.events().insert(calendarId='primary', body=event).execute()
	print(f"The event has been created! View it at {event.get('htmlLink')}!")
	result = service.calendarList().list().execute()	#get calendars
	#print(result['items'][0])
	calendar_id = result['items'][0]['id']
	result = service.events().list(calendarId=calendar_id, timeZone="America/New_York").execute()	#get calendar events
	print(result['items'][0])'''