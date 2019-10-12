import sys
import requests
import datetime
if len(sys.argv) < 6:
	print("syntax:\npython carmd.py YEAR MAKE MODEL CURRENT-MILEAGE WEEKLY-MILEAGE")
	quit()
date = datetime.date.today()
date_format = '%B %m, %Y, %I:%M%p'
day = 'Saturday'
num_of_weeks = 4
def get_date_for_day(date_format, day):
	global date
	day_of_week = date.strftime('%A')
	while (day_of_week != day):
		date += datetime.timedelta(days=1)
		day_of_week = date.strftime('%A')
	return ("%s\t%s" %(day_of_week, date))
def get_date_for_days(num_of_weeks):
	global date
	weeks = []
	for week in range(num_of_weeks):
		weeks.append(get_date_for_day(date_format, day))
		date += datetime.timedelta(days=1)
	return weeks
weeks = get_date_for_days(num_of_weeks)
year = "year=" + sys.argv[1]
make = "make=" + sys.argv[2]
model = "model=" + sys.argv[3]
current_mileage = sys.argv[4]
weekly_mileage = sys.argv[5]
mileage = "mileage=" + str(int(current_mileage) + int(weekly_mileage))
api_endpoint = "http://api.carmd.com/v3.0/maint?%s&%s&%s&%s" %(year, make, model, mileage)
header = {"content-type":"application/json", "authorization":"Basic MGE2OTJlMWQtY2M5YS00OWMwLTlmYTItNzNjZGFjMjYyZjBm", "partner-token":"8205959faed74cbcb946419b79e80a87"}  
request = requests.get(url = api_endpoint, headers = header)
car_maint = request.json()
for maint in car_maint['data']:
	if int(maint['due_mileage']) <= int(current_mileage):
		 print("%s:\tMileage: %s\tMaintence: %s" %(weeks[0], maint['due_mileage'], maint['desc']))
	elif int(maint['due_mileage']) > int(current_mileage) and int(maint['due_mileage']) <= (int(current_mileage) + int(weekly_mileage)):
		print("%s:\tMileage: %s\tMaintence: %s" %(weeks[1], maint['due_mileage'], maint['desc']))
	else:
		print("%s:\tMileage: %s\tMaintence: %s" %(weeks[2], maint['due_mileage'], maint['desc']))