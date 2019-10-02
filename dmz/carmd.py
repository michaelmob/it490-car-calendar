import requests
vin = "vin=1GNALDEK9FZ108495"
mileage = "mileage=50000"
year = "year=2002"
make = "make=Ford"
model = "model=Focus"
#api_endpoint = "http://api.carmd.com/v3.0/maint?%s&%s" %(vin, mileage)
api_endpoint = "http://api.carmd.com/v3.0/maint?%s&%s&%s&%s" %(year, make, model, mileage)
header = {"content-type":"application/json", "authorization":"Basic MGE2OTJlMWQtY2M5YS00OWMwLTlmYTItNzNjZGFjMjYyZjBm", "partner-token":"8205959faed74cbcb946419b79e80a87"}  
request = requests.get(url = api_endpoint, headers = header)
response = request.json()
print(response)