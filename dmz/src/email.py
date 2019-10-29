#!/usr/bin/env python3
import os, smtplib


def send_email(users_email, subject, body):
	"""
	Sends an email with the subject/body arguments to the specified email address
	"""
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
		print("Email Notification Successfully Sent To %s" %(users_email))
	except:
		print("%s email login failure" %(account))
