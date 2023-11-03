import requests
import requests_mock

def get_mocked_data(number_of_dates):
  # Create a requests_mock instance
  with requests_mock.Mocker() as mocker:
    # Define a mock response for a specific API endpoint
    if number_of_dates == 0:
      mocker.get('https://api.example.com/endpoint', json=[])
    else:
      mocker.get('https://api.example.com/endpoint', json=[{"date": "2026-01-01"},{"date": "2025-02-01"}])

		# Make a request to the mocked API endpoint
    response = requests.get('https://api.example.com/endpoint')

    result = response;