
# SMTP IMPORTS
from validate_email import validate_email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl

# IMAP IMPORTS
import imaplib
import email
from email.header import decode_header
from email import utils

# Other Imports
import os
import re
import tempfile


def check_connection(app_email):
	try:
		imap = imaplib.IMAP4_SSL(app_email.imap_server)
		imap.login(app_email.email, app_email.password)
		imap.close()
		imap.logout()
		return True
	except imaplib.IMAP4.error as ex:
		return {"error": ex}


def get_connection(app_email):
	try:
		imap = imaplib.IMAP4_SSL(app_email.imap_server)
		imap.login(app_email.email, app_email.password)
		return imap
	except imaplib.IMAP4.error as ex:
		print(ex)
		return False


def get_email_subjects(category, page, app_email):
	subjects = {}
	paginator = {}
	last_index = False

	imap = get_connection(app_email)
	
	if imap:
		status, messages = imap.select(category)
		# number of top emails to fetch
		N = 10 * page
		# total number of emails
		messages = int(messages[0])
		if N > messages:
			N = messages
			last_index = True
		
		next_index = page
		prev_index = page
		if last_index:
			next_index = page
		else:
			next_index = page+1
		P = N - 10
		if P < 1:
			P = 0
		for i in range(messages-P, messages-N, -1):
			# fetch the email message by ID
			res, msg = imap.fetch(str(i), "(RFC822)")
			for response in msg:
				if isinstance(response, tuple):
					# parse a bytes email into a message object
					msg = email.message_from_bytes(response[1])
					# decode the email subject
					subject, encoding = decode_header(msg["Subject"])[0]
					if isinstance(subject, bytes):
						# if it's a bytes, decode to str
						subject = subject.decode(encoding)
					# decode email sender
					From, encoding = decode_header(msg.get("From"))[0]
					if isinstance(From, bytes):
						From = From.decode(encoding)
					# decode the email Date
					date, encoding = decode_header(msg.get("Date"))[0]
					datetime_obj = utils.parsedate_to_datetime(date)
					# Check Attachment
					attachment = False
					# if the email message is multipart 
					if msg.is_multipart():
						# iterate over email parts
						for part in msg.walk():
							# extract content type of email
							content_type = part.get_content_type()
							content_disposition = str(part.get("Content-Disposition"))
							if content_type == "text/plain" and "attachment" not in content_disposition:
								attachment = False
							elif "attachment" in content_disposition:
								attachment = True

					from_list = From.split('"')
					first_index = False
					if page == 1:
						first_index = True
					if first_index:
						prev_index = page
					else:
						prev_index = page-1

					paginator = {'last_index': last_index, 'first_index': first_index, 
					'prev_index': prev_index, 'next_index': next_index}
					if len(from_list) > 2:
						subjects.setdefault(str(i), {'from_name': from_list[1], 'from_email': from_list[2], 
							'subject':subject, 'datetime':datetime_obj, 'is_attachment': attachment})
					else:
						subjects.setdefault(str(i), {'from_name': From, 'from_email': From, 
							'subject':subject, 'datetime':datetime_obj, 'is_attachment': attachment})
					print("Subject:", subject)
					print("From:", From)
					# print(messages)
					# print("msg:", msg)

		# close the connection and logout
		imap.close()
		imap.logout()
		return [subjects, paginator]
	else:
		return False



def email_labels(app_email):
	labels = {}
	imap = get_connection(app_email)
	if imap:
		status, directories = imap.list()
		for directory in directories:
			directory_name = directory.decode().split('"')[-2]
			directory_name = '"' + directory_name + '"'
			resp, mail_count = imap.select(directory_name)
			labels.setdefault(directory.decode().split('"')[-2], mail_count[0])
		# close the connection and logout
		imap.close()
		imap.logout()
		return labels
	else:
		return imap


def gmail_labels(app_email):
	labels = {}
	imap = get_connection(app_email)
	if imap:
		# Get Labels
		status, directories = imap.list(directory="[Gmail]")
		for directory in directories:
			directory_name = directory.decode().split('"')[-2]
			directory_name = '"' + directory_name + '"'
			resp, mail_count = imap.select(mailbox=directory_name, readonly=True)
			labels.setdefault(directory.decode().split('"')[-2], mail_count[0])
		# close the connection and logout
		imap.close()
		imap.logout()
		return labels
	else:
		return False


def non_gmail_labels(app_email):
	mail_labels = gmail_labels(app_email)
	all_labels = email_labels(app_email)
	for name, num in mail_labels.items():
		all_labels.pop(name)
	return all_labels


def email_number(category, app_email):
	num = 0
	imap = get_connection(app_email)
	if imap:
		app_email = app_emails[0]
		# create an IMAP4 class with SSL 
		imap = imaplib.IMAP4_SSL(app_email.imap_server)
		# authenticate
		imap.login(app_email.email, app_email.password)
		status, messages = imap.select(category)
		# total number of emails
		num = int(messages[0])
		# close the connection and logout
		imap.close()
		imap.logout()
		return num
	else:
		return False


def get_email(uid, category, app_email):
	email_data = {}
	imap = get_connection(app_email)
	if imap:
		status, messages = imap.select(category)
		# number of top emails to fetch
		N = 10
		# total number of emails
		messages = int(messages[0])
		if messages >= uid:
			res, msg = imap.fetch(str(uid), "(RFC822)")
			for response in msg:
				if isinstance(response, tuple):
					# parse a bytes email into a message object
					msg = email.message_from_bytes(response[1])

					# decode the email subject
					subject, encoding = decode_header(msg["Subject"])[0]
					if isinstance(subject, bytes):
						# if it's a bytes, decode to str
						subject = subject.decode(encoding)

					# decode email sender
					From, encoding = decode_header(msg.get("From"))[0]
					if isinstance(From, bytes):
						From = From.decode(encoding)
					print("Subject:", subject)
					print("From:", From)

					# decode the email Date
					date, encoding = decode_header(msg.get("Date"))[0]
					datetime_obj = utils.parsedate_to_datetime(date)

					# decode the email Body
					body = None
					attachments = {}
					is_attachment = False
					# if the email message is multipart
					if msg.is_multipart():
						# iterate over email parts
						for part in msg.walk():
							# extract content type of email
							content_type = part.get_content_type()
							content_disposition = str(part.get("Content-Disposition"))
							try:
								# get the email body
								body = part.get_payload(decode=True).decode()
							except:
								pass
							if content_type == "text/plain" and "attachment" not in content_disposition:
								# print text/plain emails and skip attachments
								print(body)
							elif "attachment" in content_disposition:
								# download attachment
								filename = part.get_filename()
								if filename:
									folder_name = clean(subject)
									base = 'email-attachments'
									folder_name = os.path.join(base, folder_name)
									if not os.path.isdir(folder_name):
										# make a folder for this email (named after the subject)
										os.mkdir(folder_name)
									filepath = os.path.join(folder_name, filename)
									if not os.path.isfile(filepath):
										# download attachment and save it
										open(filepath, "wb").write(part.get_payload(decode=True))
									attachments.setdefault(filename, filepath)
									is_attachment = True
					else:
						# extract content type of email
						content_type = msg.get_content_type()
						# get the email body
						body = msg.get_payload(decode=True).decode()
						if content_type == "text/plain":
							# print only text email parts
							print(body)

					from_dict = From.split('"')
					if len(from_dict) > 2:
						email_data = {'from_name': from_dict[1], 'from_email': from_dict[2], 
							'subject':subject, 'datetime':datetime_obj, 'is_attachment': is_attachment, 
							'attachments': attachments, 'body': body, 'id':uid}
					else:
						email_data = {'from_name': From, 'from_email': From, 
							'subject':subject, 'datetime':datetime_obj, 'is_attachment': is_attachment, 
							'attachments': attachments, 'body': body, 'id':uid}

		# close the connection and logout
		imap.close()
		imap.logout()
		return email_data
	else:
		return False


def send_email(email_data, app_email):
	# Send TEXT Mime Email
	subject = email_data['subject']
	email = email_data['email_address']
	email_body = email_data['content']
	attachments = email_data['attachments']

	smtp_server = app_email.smtp_server
	port = app_email.smtp_port  # For starttls
	sender_email = app_email.email
	password = app_email.password

	message = MIMEMultipart("alternative")
	message["Subject"] = subject
	message["From"] = sender_email
	message["To"] = email

	# Turn these into plain/html MIMEText objects
	email_body_text = textify(email_body)
	part1 = MIMEText(email_body_text, "plain")
	part2 = MIMEText(email_body, "html")

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(part1)
	message.attach(part2)

	if attachments != []:
		for attachment in attachments:
			part = MIMEBase("application", "octet-stream")
			part.set_payload(attachment.read())
			encoders.encode_base64(part)
			part.add_header(
				"Content-Disposition",
				f"attachment; filename= {attachment}",
			)
			message.attach(part)

	'''
	filename = "document.pdf"  # In same directory as script
	# Open PDF file in binary mode
	with open(filename, "rb") as attachment:
		# Add file as application/octet-stream
		# Email client can usually download this automatically as attachment
		part = MIMEBase("application", "octet-stream")
		part.set_payload(attachment.read())

	# Encode file in ASCII characters to send by email    
	encoders.encode_base64(part)

	# Add header as key/value pair to attachment part
	part.add_header(
		"Content-Disposition",
		f"attachment; filename= {filename}",
	)'''

	
	# message.attach(part)

	# Create a secure SSL context
	context = ssl.create_default_context()

	# Try to log in to server and send email
	try:
		server = smtplib.SMTP(smtp_server,port)
		server.ehlo() # Can be omitted
		server.starttls(context=context) # Secure the connection
		server.ehlo() # Can be omitted
		server.login(sender_email, password)
		# Send email
		server.sendmail(sender_email, email, message.as_string())
	except Exception as e:
		# Print any error messages to stdout
		print(e)
		return False
	finally:
		server.quit()
	return True
	


def textify(html):
	# Remove html tags and continuous whitespaces 
	text_only = re.sub('[ \t]+', ' ', strip_tags(html))
	# Strip single spaces in the beginning of each line
	return text_only.replace('\n ', '\n').strip()


def clean(text):
	# clean text for creating a folder
	return "".join(c if c.isalnum() else "_" for c in text)

