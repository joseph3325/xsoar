"""
Example script which can be used as a pre-processing rule
For this to be available ensure you tag the script with the tag 'preProcessing'
"""
# Grabs data from incoming incident
incident = demisto.incidents()[0]

# Pick field to dedup/drop incidnets based on
alarm_id = incident['CustomFields']['lralarmid']

# Searches for existing incidents.
query_string = "-status:Closed and lralarmid:{}".format(alarm_id)
res = demisto.executeCommand('getIncidents', {'query': query_string})

# Get the old incident data
old_incident = res[0]['Contents']['data'][0]

# If an old incident already exists...
if old_incident:
    occurences = old_incident['CustomFields'].get('occurences', 1)
    if occurences:
        occurences = occurences + 1

    # Update the name
    demisto.executeCommand('setIncident', {
        "id": old_incident["id"],
        "occurences": occurences,
        "name": "Repeated Incident for Alarm ID: {} - {} Occurences".format(alarm_id, occurences)
    })

    # Do not create the existing incident.
    return_results(False)
else:
    # Create the incident
    return_results(True)
