"""
A simple example which demonstrates the format grouped widgets should have
Source: https://docs.paloaltonetworks.com/cortex/cortex-xsoar/6-9/cortex-xsoar-admin/widgets/create-a-custom-widget-using-an-automation-script/widget-type-examples-using-automation-scripts
"""

data = [
    {"name": "2018-04-03", "data": [14], "groups": [{"name": "Unclassified", "data": [10] }, {"name": "Access", "data": [4]}]},
    {"name": "2018-04-10", "data": [3], "groups": [{"name": "Unclassified", "data": [2] }, {"name": "Access", "data": [1] }]},
    {"name": "2018-04-17", "data": [1], "groups": [{"name": "Unclassified", "data": [1] }]},
    {"name": "2018-04-16", "data": [34], "groups": [{"name": "Unclassified", "data": [18] }, {"name": "Phishing", "data": [14] }]},
    {"name": "2018-04-15", "data": [17], "groups": [{"name": "Access", "data": [17] }]}
]
# Return data as a json string
return_results(json.dumps(data))
