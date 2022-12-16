import os
import json
        
def lambda_handler(event, context):
    # put it this way for local testing for now
    # will adjust later once we figure out a way to do this locally
    try:
        json_region = os.environ['AWS_REGION']
    except:
        json_region = "us-east-1"

    # I'm not sure how to gracefully handle the case where it's passed an empty event
    # Maybe it should return an error status code?
    # Something like the following
    if event is None:
        response = ErrorHandler.emptyEventResponse
        return response
    else:
        try:
            bookName = event["name"]
        except:
            bookName = "Les Miserables"
    
    response = {
        "statusCode": 200,
        "updatedResponse": 3,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Region ": json_region
        }),
        "name": bookName
    }

    return response

class ErrorHandler():
    emptyEventResponse = {
        "statusCode": 400,
        "description": "Error: event object passed to Lambda function is empty"
    }
