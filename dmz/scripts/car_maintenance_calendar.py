import sys
import requests
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

date = datetime.date.today()
maint_events = []

def get_date_for_day(date_format, day):
	global date
	day_of_week = date.strftime('%A')
	while (day_of_week != day):
		date += datetime.timedelta(days=1)
		day_of_week = date.strftime('%A')
	return date.strftime(date_format)
def get_date_for_days(num_of_weeks, date_format):
	global date
	weeks = []
	for week in range(num_of_weeks):
		weeks.append(get_date_for_day(date_format, day))
		date += datetime.timedelta(days=1)
	return weeks
def maint_event(summary, start_time, end_time):
	return {'summary':summary, 'start':{'dateTime': start_time,'timeZone': 'America/New_York'},'end':{'dateTime': end_time,'timeZone': 'America/New_York'}}
def get_car_maint(api_endpoint, header):
	global weeks, maint_events
	request = requests.get(url = api_endpoint, headers = header)
	car_maint = request.json()
	for maint in car_maint['data']:
		if int(maint['due_mileage']) <= int(current_mileage):
			#print("%s\tMileage: %s\tMaintence: %s" %(weeks[0], maint['due_mileage'], maint['desc']))
			maint_events.append(maint_event(maint['desc'], weeks[0], weeks[0]))
		elif int(maint['due_mileage']) > int(current_mileage) and int(maint['due_mileage']) <= (int(current_mileage) + int(weekly_mileage)):
			#print("%s\tMileage: %s\tMaintence: %s" %(weeks[1], maint['due_mileage'], maint['desc']))
            		maint_events.append(maint_event(maint['desc'], weeks[1], weeks[1]))
		else:
			#print("%s\tMileage: %s\tMaintence: %s" %(weeks[2], maint['due_mileage'], maint['desc']))
            		maint_events.append(maint_event(maint['desc'], weeks[2], weeks[2]))

if __name__ == "__main__":
	'''if len(sys.argv) < 6:
        	print("syntax:\npython carmd.py YEAR MAKE MODEL CURRENT-MILEAGE WEEKLY-MILEAGE")
        	quit()'''
	SCOPES = "https://www.googleapis.com/auth/calendar"
	store = file.Storage('calendar_token.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('calendar_key.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('calendar', 'v3', credentials=creds)
	calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
	#date_format = '%B %d, %Y, %I:%M%p'
	date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
	day = 'Saturday'
	num_of_weeks = 4
	weeks = get_date_for_days(num_of_weeks, date_format)
	'''year = "year=" + sys.argv[1]
	make = "make=" + sys.argv[2]
	model = "model=" + sys.argv[3]
	current_mileage = sys.argv[4]
	weekly_mileage = sys.argv[5]'''
	year = "year=" + input("Year: ")
	make = "make=" + input("Make: ")
	model = "model=" + input("Model: ")
	current_mileage = int(input("Current Mileage: "))
	weekly_mileage = int(input("Weekly Mileage: "))
	mileage = "mileage=" + str(int(current_mileage) + int(weekly_mileage))
	api_endpoint = "http://api.carmd.com/v3.0/maint?%s&%s&%s&%s" %(year, make, model, mileage)
	header = {"content-type":"application/json", "authorization":"Basic MGE2OTJlMWQtY2M5YS00OWMwLTlmYTItNzNjZGFjMjYyZjBm", "partner-token":"8205959faed74cbcb946419b79e80a87"}  
	get_car_maint(api_endpoint, header)
	if calendar_list_entry['accessRole']:
		for event in maint_events:
			current_event = service.events().insert(calendarId='primary', body=event).execute()
			print(f"The event has been created! View it at {current_event.get('htmlLink')}")
