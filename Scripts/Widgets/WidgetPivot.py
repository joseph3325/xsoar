"""
Schema for creating pivots in a widget
Source: https://docs.paloaltonetworks.com/cortex/cortex-xsoar/6-9/cortex-xsoar-admin/widgets/create-a-custom-widget-using-an-automation-script/widget-type-examples-using-automation-scripts
"""

data = [
    {"name": "Phishing", "data": [50], "dataType": "incidents", "Query": "type:Phishing",  "pivot": "type:Phishing"},
    {"name": "Access", "data": [50], "dataType": "incidents", "query": "type:Access",  "pivot": "type:Access"},
    {"name": "IP", "data": [50], "dataType": "indicators", "query": "type:IP", "pivot": "type:IP"}
]

return_results(json.dumps(data))
