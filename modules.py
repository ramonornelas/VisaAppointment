import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
# import requests_mock

def send_email(subject, message):

	# Set up the SMTP server
	smtp_server = "smtp.gmail.com"
	smtp_port = 587
	smtp_username = "ornelas.carlos@gmail.com"
	smtp_password = "xstqhkkvrabtalxp"

	# Create the email message
	sender = "ornelas.carlos@gmail.com"
	# receiver = "ornelas.carlos@gmail.com, nokktarehezth@gmail.com"
	receiver = "ornelas.carlos@gmail.com"

	msg = MIMEMultipart()
	msg["From"] = sender
	msg["To"] = receiver
	msg["Subject"] = subject
	msg.attach(MIMEText(message, "plain"))

	# Connect to the SMTP server and send the email
	try:
		with smtplib.SMTP(smtp_server, smtp_port) as server:
			server.starttls()
			server.login(smtp_username, smtp_password)
			server.send_message(msg)
	except Exception as e:
		return "An error occurred: " + str(e)

def get_cookie_from_file():
	# Get the cookie value from a text file
	file_path = "visa_data.txt"

	# Open the text file in read mode
	file = open(file_path, "r")

	# Read the file line by line
	lines = file.readlines()

	for index, line in enumerate(lines):
		if line.startswith("Cookie:"):
			cookie = lines[index + 1]
			# Check if the file has more lines after the cookie value to remove the 'New line' character
			if len(lines) > index + 2:
				# Remove the last character
				cookie = cookie[:-1]

	# Close the file
	file.close()

	return cookie

def check_dates(city_code, city_name, target_date, cookie):

	# Get data from the API
	url = "https://ais.usvisa-info.com/es-mx/niv/schedule/52250562/appointment/days/" + str(city_code) + ".json?appointments[expedite]=false"

	headers = {
		"Cookie": cookie,
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest"
	}

	# Send a GET request to the endpoint
	response = requests.get(url, headers=headers)

	"""
	# Create a requests_mock instance
	with requests_mock.Mocker() as mocker:
		# Define a mock response for a specific API endpoint
		dates_empty = False
		if dates_empty:
			mocker.get('https://api.example.com/endpoint', json=[])
		else:
			mocker.get('https://api.example.com/endpoint', json=[{"date": "2026-01-01"},{"date": "2025-02-01"}])

		# Make a request to the mocked API endpoint
		response = requests.get('https://api.example.com/endpoint')
	
	"""

	# Check the response status code
	if response.status_code == 200:
		# Parse the response content as JSON
		try:
			data = response.json()
		except:
			subject = "Visa - Formato de respuesta incorrecto"
			message = "https://ais.usvisa-info.com/es-mx/niv/schedule/52250562/appointment"
			send_email(subject, message)
			return "Error"

		# Check if there is an available date for appointment
		if len(data) != 0:
			available_date = data[0]["date"]
			if available_date < target_date:
				subject = "Visa - Fecha disponible!!! (" + city_name + " / " + available_date + ")"
				message = "https://ais.usvisa-info.com/es-mx/niv/schedule/52250562/appointment"
				send_email(subject, message)
				return 'AVAILABLE DATE!!! ' + str(available_date)
			else:
				return 'First available date: ' + str(available_date)
		else:
			return 'No dates available.'

	else:
		if response.status_code == 401:
			subject = "Visa - Terminó la sesión"
			message = "https://ais.usvisa-info.com/es-mx/niv/schedule/52250562/appointment"
		else:
			subject = "Visa - Se generó un error"
			message = "https://ais.usvisa-info.com/es-mx/niv/schedule/52250562/appointment"
		send_email(subject, message)
		return "An error occurred. Status code: " + str(response.status_code)