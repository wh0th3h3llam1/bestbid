# Python Script to Send Email to A Single Client
# This Code Currently Works Only for Gmail Accounts
# Author : wh0am1
# GitHub : https://github.com/wh0th3h3llam1

import smtplib
from bestbid.credentials import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(receipent, subject, message):
	
	try:
		server = smtplib.SMTP("{0}:{1}".format(EMAIL_HOST, EMAIL_PORT))
		server.ehlo()
		server.starttls()
		server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

		# Sending the Mail
		msg = MIMEMultipart()

		msg['From'] = EMAIL_HOST_USER
		msg['To'] = receipent
		msg['Subject'] = subject
		msg.attach(MIMEText(message, 'plain'))

		text = msg.as_string()

		# print("Sending Email to " + receipent + "...")
		print(type(receipent))
		server.sendmail(EMAIL_HOST_USER, receipent, text)
		print("Email Sent Successfully.")
		
	except Exception as e:
		print(e)
		raise e
	finally:
		server.quit()



# Gmail SMTP Server
	# server = smtplib.SMTP('smtp.gmail.com:587') 465

# Yahoo SMTP Server
	# server = smtplib.SMTP('smtp.mail.yahoo.com:465') 587