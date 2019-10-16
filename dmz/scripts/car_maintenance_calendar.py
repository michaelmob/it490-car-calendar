import sys
import requests
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import urllib.request
from bs4 import BeautifulSoup
from google_auth_oauthlib.flow import Flow
event_log = "car_maintenance_event.log"
date = datetime.date.today()
maint_events = []
def event_logging(event):
	#Writes to events to the event log file
	global event_log
	file = open(event_log, "w+")
	file.write(event)
	file.close()
def google_oauth2(secret_file, SCOPES):
	#Returns user's oauth2 credentials to access their Google Calendar
	flow = Flow.from_client_secrets_file(secret_file, scopes=SCOPES, redirect_uri = 'urn:ietf:wg:oauth:2.0:oob')
	auth_url, _ = flow.authorization_url(prompt='consent')
	print('Authorization URL: {}'.format(auth_url))
	code = input("Authorization code: ")
	flow.fetch_token(code=code)
	return flow.credentials
def get_date_for_day(date_format, day):
	#Returns the date for the current week's Saturday
	global date
	day_of_week = date.strftime('%A')
	while (day_of_week != day):
		date += datetime.timedelta(days=1)
		day_of_week = date.strftime('%A')
	return date.strftime(date_format)
def get_date_for_days(num_of_weeks, date_format):
	#Returns the date for the Saturday for the following amount of weeks
	global date
	weeks = []
	for week in range(num_of_weeks):
		weeks.append(get_date_for_day(date_format, day))
		date += datetime.timedelta(days=1)
	return weeks
def maint_event(summary, start_time, end_time):
	#Returns the format for creating events in Google Calendar
	return {'summary':summary, 'start':{'dateTime': start_time,'timeZone': 'America/New_York'},'end':{'dateTime': end_time,'timeZone': 'America/New_York'}}
def get_car_maint(api_endpoint, header, year, make, model):
	#Retrieves car maintenance information and inputs it into the maint_events list
	global weeks, maint_events
	event_logging("Querying Carmd Maintenance:  %s %s %s" %(year, make, model))
	request = requests.get(url = api_endpoint, headers = header)
	car_maint = request.json()
	event_logging("Retrieved Carmd Maintenance: %s %s %s" %(year, make, model))
	for maint in car_maint['data']:
		if int(maint['due_mileage']) <= int(current_mileage):
			maint_events.append(maint_event("%s %s %s %s" %(year, make, model, maint['desc']), weeks[0], weeks[0]))
		elif int(maint['due_mileage']) > int(current_mileage) and int(maint['due_mileage']) <= (int(current_mileage) + int(weekly_mileage)):
            		maint_events.append(maint_event("%s %s %s %s" %(year, make, model, maint['desc']), weeks[1], weeks[1]))
		else:
            		maint_events.append(maint_event("%s %s %s %s" %(year, make, model, maint['desc']), weeks[2], weeks[2]))
def get_youtube_playlist(search_string):
	#Returns the YouTube playlist for each car maintenance information
	playlist = []
	search = urllib.parse.quote(search_string)
	url_link = "https://www.youtube.com/results?search_query=%s" %(search)
	event_logging("Querying YouTube For: %s" %(search_string))
	response = urllib.request.urlopen(url_link)
	raw_html = response.read()
	event_logging("Retrieved YouTube Playlist For: %s" %(search_string))
	soup = BeautifulSoup(raw_html, "html.parser")
	for video in soup.findAll(attrs={"class":"yt-uix-tile-link"}):
		playlist.append("https://www.youtube.com%s" %(video["href"]))
	return playlist
def generate_response():
	#Returns the response for the frontend
	global maint_events
	response = {}
	for event in maint_events:
		current_event = service.events().insert(calendarId='primary', body=event).execute()
		response[event['summary']] = [{"calendar_event" : current_event.get('htmlLink')}, {"playlist" : get_youtube_playlist(event['summary'])}]
	return response
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Type:\tpython3 car_maintenance_calendar.py --noauth_local_webserver")
		exit()
	SCOPES = "https://www.googleapis.com/auth/calendar"
	secret_file = "calendar_key.json"
	'''store = file.Storage('calendar_token.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('calendar_key.json', SCOPES)
		creds = tools.run_flow(flow, store)'''
	creds = google_oauth2(secret_file, SCOPES)
	service = build('calendar', 'v3', credentials=creds)
	calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
	date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
	day = 'Saturday'
	num_of_weeks = 4
	weeks = get_date_for_days(num_of_weeks, date_format)
	year = input("Year: ")
	make = input("Make: ").upper()
	model = input("Model: ").upper()
	current_mileage = int(input("Current Mileage: "))
	weekly_mileage = int(input("Weekly Mileage: "))
	mileage = str(int(current_mileage) + int(weekly_mileage))
	api_endpoint = "http://api.carmd.com/v3.0/maint?year=%s&make=%s&model=%s&mileage=%s" %(year, make, model, mileage)
	header = {"content-type":"application/json", "authorization":"Basic MGE2OTJlMWQtY2M5YS00OWMwLTlmYTItNzNjZGFjMjYyZjBm", "partner-token":"8205959faed74cbcb946419b79e80a87"}  
	get_car_maint(api_endpoint, header, year, make, model)
	if calendar_list_entry['accessRole']:
		my_response = generate_response()
		for key in my_response:
			print("\n%s:\nCalendar Event:\n%s\nPlaylist:\n%s\n" %(key, my_response[key][0]['calendar_event'], my_response[key][1]['playlist']))
