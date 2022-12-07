import os
import json
        
def lambda_handler(event, context):
    json_region = os.environ['AWS_REGION']

    response = {
        "statusCode": 200,
        "updatedResponse": 1,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Region ": json_region
        })
    }
    return response
