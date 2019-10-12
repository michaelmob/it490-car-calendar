import datetime

date = datetime.date.today()
date_format = '%B %m, %Y, %I:%M%p'
day = 'Saturday'
num_of_weeks = 10
def get_date_for_day(date_format, day):
	global date
	day_of_week = date.strftime('%A')
	while (day_of_week != day):
        	date += datetime.timedelta(days=1)
        	day_of_week = date.strftime('%A')
	print("Day: %s\tDate: %s" %(day_of_week, date))
def get_date_for_days(num_of_weeks):
	global date
	for week in range(num_of_weeks):
		get_date_for_day(date_format, day)
		date += datetime.timedelta(days=1)
if __name__ == "__main__":
	get_date_for_days(num_of_weeks)
