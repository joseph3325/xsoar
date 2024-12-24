import requests, json
from datetime import datetime, timezone

# Constants
API_KEY = '<keyHere>'
KEY_ID = '<keyIDHere>'
INSTANCE_NAME = 'secops-xsoar'
TARGET_INCIDENT_ID = '60388'
BASE_URL = f'https://api-{INSTANCE_NAME}.crtx.us.paloaltonetworks.com'
# URL for getting current incident data
GET_URL = f'{BASE_URL}/xsoar/public/v1/incident/load/{TARGET_INCIDENT_ID}'
# URL for updating the target incident
UPDATE_URL = f'{BASE_URL}/xsoar/public/v1/incident'
# Headers
HEADERS = {
    "Authorization": API_KEY,
    "x-xdr-auth-id": KEY_ID,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Timestamp in ISO 8601 format
timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

# Get existing incident
response = requests.get(GET_URL, headers=HEADERS)
response.raise_for_status()  # Raise an error for bad status codes
incident = response.json()
# print(json.dumps(incident, indent=3))
# Update incident
# incident['CustomFields']['details'] = 'Test'
incident['details'] = 'Test Deets'
# Must update the modified timestamp for the database to accept the change
incident['modified'] = timestamp
# Post updated incident
response = requests.post(UPDATE_URL, headers=HEADERS, json=incident)
# Print response status code and body
print(response.status_code)
print(response.text)
