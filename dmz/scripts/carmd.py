import sys
import requests
if len(sys.argv) < 6:
	print("syntax:\npython carmd.py YEAR MAKE MODEL CURRENT-MILEAGE WEEKLY-MILEAGE")
	quit()
year = "year=" + sys.argv[1]
make = "make=" + sys.argv[2]
model = "model=" + sys.argv[3]
current_mileage = sys.argv[4]
weekly_mileage = sys.argv[5]
mileage = "mileage=" + str(int(current_mileage) + int(weekly_mileage))
api_endpoint = "http://api.carmd.com/v3.0/maint?%s&%s&%s&%s" %(year, make, model, mileage)
#print(api_endpoint)
header = {"content-type":"application/json", "authorization":"Basic MGE2OTJlMWQtY2M5YS00OWMwLTlmYTItNzNjZGFjMjYyZjBm", "partner-token":"8205959faed74cbcb946419b79e80a87"}  
request = requests.get(url = api_endpoint, headers = header)
car_maint = request.json()
#print(car_maint)
for maint in car_maint['data']:
	if int(maint['due_mileage']) <= int(current_mileage):
		 print("Current Week:\tMileage: %s\tMaintence: %s" %(maint['due_mileage'], maint['desc']))
	elif int(maint['due_mileage']) > int(current_mileage) and int(maint['due_mileage']) <= (int(current_mileage) + int(weekly_mileage)):
		print("Next Week:\tMileage: %s\tMaintence: %s" %(maint['due_mileage'], maint['desc']))
	else:
		print("Following Week:\tMileage: %s\tMaintence: %s" %(maint['due_mileage'], maint['desc']))
