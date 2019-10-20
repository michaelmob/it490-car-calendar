#In GMail type https://myaccount.google.com/lesssecureapps
import os
import smtplib
email = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.ehlo()
smtp_server.starttls()
smtp_server.ehlo()
smtp_server.login(email, password)
msg = "Subject: Car-Calendar\n\nTesting Car-Calendar Notification 3"
smtp_server.sendmail(email, "lgw3@njit.edu", msg)
smtp_server.close()
