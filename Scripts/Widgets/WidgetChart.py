import random
# Get the argument 'searchQuery'
query = demisto.args().get('searchQuery')
# Use the search query to find indicators in xsoar
indicators = demisto.executeCommand("findIndicators", {'query': query})[0]['Contents']
# Create an array of dicts where the indicator is the 'name' and the 'data' is a random value between 1 and 25
result = [{'name': x['value'], 'data': [random.randrange(1, 25)]} for x in indicators]
# Slice results to just 20 values
result = result[:20]
# Results must be returned as a json string
return_results(json.dumps(result))
