#!/usr/bin/env python3

#Must use python3.6 or higher
import os, sys, json
from datetime import date, datetime
from dotenv import load_dotenv; load_dotenv()
from ez import ez_consume
import smtplib
import requests
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import urllib.request
from bs4 import BeautifulSoup
from google_auth_oauthlib.flow import Flow



def get_dates_for_day(num_of_weeks, date_format, day):
	#Returns a list with the date String for the specified day, for each week for the number of weeks supplied in num_of_weeks argument
	weeks = []
	date = datetime.date.today()
	day_of_week = date.strftime('%A')
	while (day_of_week != day):
		date += datetime.timedelta(days=1)
		day_of_week = date.strftime('%A')
	weeks.append(date.strftime(date_format))
	for week in range(num_of_weeks):
		date += datetime.timedelta(days=7)
		weeks.append(date.strftime(date_format))
	return weeks



def event_logging(event):
	#Writes events to the event log file
	event_log = "car_maintenance_event.log"
	current_time = datetime.datetime.now()
	event = "%s|%s\n" %(current_time.strftime("%m/%d/%Y|%H:%M:%S"), event)
	file = open(event_log, "a+")
	file.write(event)
	file.close()
	#ez_log('LOG', 'DMZ', event)



def google_oauth2_link(secret_file, SCOPES):
	#Returns user's oauth2 authorization url to access their Google Calendar
	flow = Flow.from_client_secrets_file(secret_file, scopes=SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
	auth_url, _ = flow.authorization_url(prompt='consent')
	event_logging("oauth2 URL sent: {}".format(auth_url))
	return {"oauth2_link" : auth_url}



def google_oauth2_creds(secret_file, SCOPES, code):
	#Returns user's oauth2 credentials to access their Google Calendar
	event_logging("Received user's oauth2 confirmation code")
	try:
		flow = Flow.from_client_secrets_file(secret_file, scopes=SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
		#auth_url, _ = flow.authorization_url(prompt='consent')
		flow.fetch_token(code=code)
		event_logging("Successfully retrieved user's oauth2 token")
		return flow.credentials
	except:
		print("Failure retreiving user's oauth2 token")
		event_logging("Failure retrieveing user's oauth2 token")



def get_youtube_playlist(search_string):
	#Returns the YouTube playlist for each car maintenance information
	playlist = []
	try:
		search = urllib.parse.quote(search_string)
		url_link = "https://www.youtube.com/results?search_query=%s" %(search)
		event_logging("Querying YouTube For: %s" %(search_string))
		response = urllib.request.urlopen(url_link)
		raw_html = response.read()
		event_logging("Received YouTube Query Response For: %s" %(search_string))
		soup = BeautifulSoup(raw_html, "html.parser")
		for video in soup.findAll(attrs={"class":"yt-uix-tile-link"}):
			playlist.append("https://www.youtube.com%s" %(video["href"]))
		return playlist
	except:
		print("%s does not exist on YouTube" %(search_string))
		event_logging("%s does not exist on YouTube" %(search_string))




def maint_event(summary, start_time, end_time):
	#Returns the format for creating events in Google Calendar
	return {'summary':summary, 'start':{'dateTime': start_time,'timeZone': 'America/New_York'},'end':{'dateTime': end_time,'timeZone': 'America/New_York'}}




def get_car_maint(header, api_maint_endpoint, year, make, model, current_mileage, weekly_mileage, weeks):
	#Returns car maintenance information as a list
	maint_events = []		#Hold the maint_event of each scheduled maintenance item for the car
	event_logging("Querying CarMD Maintenance API Endpoint:  %s %s %s" %(year, make, model))
	print(api_maint_endpoint)
	request = requests.get(url = api_maint_endpoint, headers = header)
	car_maint = request.json()
	#print(car_maint)
	event_logging("Received CarMD Maintenance API Endpoint Response: %s %s %s" %(year, make, model))
	for maint in car_maint['data']:
		#Checks if the car maintenance item associated with each mileage landmark falls within the range of what the car's mileage is for the current week, next week, or following week
		#Based on which week the car's mileage will fall within the range of the maintenance mileage landmark, the maint_event for that specific maintenance item will be created
		#with the assigned week's date it should be serviced, and then this maint event will be added to the maint_events list which is the all of the car's maintenance scheduled
		if int(maint['due_mileage']) <= int(current_mileage):
			maint_events.append(maint_event("%s %s %s %s" %(year, make, model, maint['desc']), weeks[0], weeks[0]))
		elif int(maint['due_mileage']) > int(current_mileage) and int(maint['due_mileage']) <= (int(current_mileage) + int(weekly_mileage)):
			maint_events.append(maint_event("%s %s %s %s" %(year, make, model, maint['desc']), weeks[1], weeks[1]))
		else:
			maint_events.append(maint_event("%s %s %s %s" %(year, make, model, maint['desc']), weeks[2], weeks[2]))
	return maint_events




def send_maint_info(creds, maint_events):
	#Adds maintenance events to the user's Google Calendar, then populates the response dictionary to send to frontend
	response = {}														#Holds each car's maintenance event summary, Google Calendar Schedule Link, and Youtube playlist of how to service
	event_logging("Attempting to access user's Google Calendar")
	service = build('calendar', 'v3', credentials=creds)									#Instantiating calendar service
	calendar_list_entry = service.calendarList().get(calendarId='primary').execute() 					#Grabing calendar's properties
	if calendar_list_entry['accessRole']:
		event_logging("Successfully Accessed User's Google Calendar")
		for event in maint_events:
			event_logging("Attempting to schedule %s in User's Google Calendar" %(event["summary"]))
			try:
				current_event = service.events().insert(calendarId='primary', body=event).execute()		#Adding car maintenance event to Google Calendar
				event_logging("Successfully scheduled %s in User's Google Calendar" %(event["summary"]))
				response[event['summary']] = [{"calendar_event" : current_event.get('htmlLink')}, {"playlist" : get_youtube_playlist(event['summary'])}] #Adding dictionary object of the car maintenance name, link to show Google Calendar event, and youtube playlist for how to service the maintenance
			except:
				event_logging("Failure scheduling %s in User's Google Calendar" %(event["summary"]))
		for key in response:												#Example how to parse through my response dictionary to display neatly
			print("\n%s:\nCalendar Event:\n%s\nPlaylist:\n%s\n" %(key, response[key][0]['calendar_event'], response[key][1]['playlist']))
	else:
		event_logging("Failure Accessing User's Google Calendar")
		response["Error"] = "Permissions Denied Accessing User's Google Calendar"
	return response




def send_email(users_email, subject, body):
	#Sends email to an email address
	account = os.getenv("EMAIL_ADDRESS")
	password = os.getenv("EMAIL_PASSWORD")
	smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
	smtp_server.ehlo()
	smtp_server.starttls()
	smtp_server.ehlo()
	event_logging("%s attempting email login" %(account))
	try:
		smtp_server.login(account, password)
		msg = "Subject: %s\n\n%s" %(subject, body)
		smtp_server.sendmail(account, users_email, msg)
		smtp_server.close()
		event_logging("%s email login success" %(account))
	except:
		print("%s email login failure" %(account))
		event_logging("%s email login failure" %(account))




def email_recall_info(header, api_recall_endpoint, year, make, model, users_email):
	#Emails the information if the car is recalled or not to the user
	event_logging("Querying CarMD Recall API Endpoint: %s %s %s" %(year, make, model))
	print(api_recall_endpoint)
	request = requests.get(url = api_recall_endpoint, headers = header)
	car_recall = request.json()
	print(car_recall)
	event_logging("Received CarMD Recall API Endpoint Response: %s %s %s" %(year, make, model))
	subject = "%s %s %s Recall Info:" %(year, make, model)
	body = " "
	if len(car_recall["data"]) < 1:
		body += "No recall data associated with %s %s %s" %(year, make, model)
	else:
		for recall in car_recall["data"]:
			body += "%s\n" %(recall["desc"])
	send_email(users_email, subject, body)




def default(value):
	"""
	Convert date/times to strings. Fixes 'datetime not JSON serializable'.
	"""
	if isinstance(value, date) or isinstance(value, datetime):
		return value.isoformat()




def callback(ch, method, props, body):
	try:
		data = json.loads(body)
		print(data)
	except:
		return  # Malformed JSON

	# No data means no work to be done
	if not data:
		return

	# Collect values
	action = data.get('action')
	
	result = {}
	if action == 'oauth2_link':
		#Retrieves the users car's year, make, model, current_mileage, weekly_mileage
		#Sends the oauth2 url authorization link for the user to grant access to their Google Calendar
		year = str(data["year"])
		make = str(data["make"])
		model = str(data["model"])
		current_mileage = str(data["current_mileage"])
		weekly_mileage = str(data["weekly_mileage"])
		values_file = open("values_file.txt", "w+")
		values_file.write("%s\n%s\n%s\n%s\n%s" %(year, make, model, current_mileage, weeekly_mileage))
		values_file.close()
		header = {"content-type":"application/json", "authorization":"Basic MGE2OTJlMWQtY2M5YS00OWMwLTlmYTItNzNjZGFjMjYyZjBm", "partner-token":"8205959faed74cbcb946419b79e80a87"}
		secret_file = "calendar_key.json"
		SCOPES = "https://www.googleapis.com/auth/calendar"
		result = google_oauth2_link(secret_file, SCOPES)
	elif action == 'car_maint':
		#Retrieves the user's email address, and oauth2 authorization code
		#Sends the car maintenance info
		users_email = data["users_email"]
		code = data["oauth2_code"]
		values_file = open("values_file.txt", "r")
		values_list = []
		for line in values_file.read():
			values_list.append(line)
		year = values_list[0]
		make = values_list[1]
		model = values_list[2]
		current_mileage = values_list[3]
		weekly_mileage = values_list[4]
		mileage = int(current_mileage) + int(weekly_mileage)
		header = {"content-type":"application/json", "authorization":"Basic MGE2OTJlMWQtY2M5YS00OWMwLTlmYTItNzNjZGFjMjYyZjBm", "partner-token":"8205959faed74cbcb946419b79e80a87"}
		api_maint_endpoint = "http://api.carmd.com/v3.0/maint?year=%s&make=%s&model=%s&mileage=%d" %(year, make, model, mileage)
		api_recall_endpoint = "http://api.carmd.com/v3.0/recall?year=%s&make=%s&model=%s&mileage=%d" %(year, make, model, mileage)
		secret_file = "calendar_key.json"
		SCOPES = "https://www.googleapis.com/auth/calendar"
		creds = google_oauth2_creds(secret_file, SCOPES, code)
		date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
		day = 'Saturday'
		num_of_weeks = 4
		weeks = get_dates_for_day(num_of_weeks, date_format, day)
		maint_events = get_car_maint(header, api_maint_endpoint, year, make, model, current_mileage, weekly_mileage, weeks)
		email_recall_info(header, api_recall_endpoint, year, make, model, users_email)
		result = send_maint_info(creds, maint_events)
	else:
		result['message'] = 'UNKNOWN_ACTION'
	
	return json.dumps(result, default=default)




if __name__ == '__main__':
	ez_consume('DMZ', 'dmz-queue-rpc', callback)
