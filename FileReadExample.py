# Retrieve the argument 'entryId'
entryId = demisto.args().get('entryId')
# Function which takes the entryId for a json file as an arg and returns the json
def get_file(entry_id):
    fp = demisto.executeCommand('getFilePath', {'id': entry_id})
    fp = fp[0]['Contents']['path']
    with open(fp, 'r') as f:
        data = json.loads(f.read())
    return data


get_file(entryId)
