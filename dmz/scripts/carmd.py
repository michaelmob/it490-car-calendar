import sys
import requests
if len(sys.argv) < 5:
    print("syntax:\npython carmd.py YEAR MAKE MODEL MILEAGE")
    quit()
year = "year=" + sys.argv[1]
make = "make=" + sys.argv[2]
model = "model=" + sys.argv[3]
mileage = "mileage=" + sys.argv[4]
api_endpoint = "http://api.carmd.com/v3.0/maint?%s&%s&%s&%s" %(year, make, model, mileage)
header = {"content-type":"application/json", "authorization":"Basic MGE2OTJlMWQtY2M5YS00OWMwLTlmYTItNzNjZGFjMjYyZjBm", "partner-token":"8205959faed74cbcb946419b79e80a87"}  
request = requests.get(url = api_endpoint, headers = header)
response = request.json()
print(response)
