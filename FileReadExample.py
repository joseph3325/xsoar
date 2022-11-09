entryId = demisto.args().get('entryId')


def get_file(entry_id):
    fp = demisto.executeCommand('getFilePath', {'id': entry_id})
    fp = fp[0]['Contents']['path']
    with open(fp, 'r') as f:
        data = json.loads(f.read())
    return data
