"""
Example of the schema for a duration widget
Source: https://docs.paloaltonetworks.com/cortex/cortex-xsoar/6-9/cortex-xsoar-admin/widgets/create-a-custom-widget-using-an-automation-script/widget-type-examples-using-automation-scripts
"""
result = [
    {
        'name': 'Duration Example',
        'data': [120]
    }
        ]

# The return type should be a string (any name) and an integer. The time is displayed in seconds.
return_results(json.dumps(result))
