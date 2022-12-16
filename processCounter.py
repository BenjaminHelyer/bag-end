import os
import json
        
def lambda_handler(event, context):
    # put it this way for local testing for now
    # will adjust later once we figure out a way to do this locally
    try:
        json_region = os.environ['AWS_REGION']
    except:
        json_region = "us-east-1"

    # default response so we can adjust the parts we need later
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "{}"
    }

    # I'm not sure how to gracefully handle the case where it's passed an empty event
    # Maybe it should return an error status code?
    # Something like the following
    if event is None:
        response = ErrorHandler.emptyEventResponse
        return response
    else:
        if event["http"]["method"] == "GET":
            response["body"] = "{ \"message\": \"I received a GET Request\" }"

    return response

class ErrorHandler():
    emptyEventResponse = {
        "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: event object passed to Lambda function is empty\" }"
    }
