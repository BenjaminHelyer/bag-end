import os
import json
        
def lambda_handler(event, context):
    """
    The event should have the following keys:
        'operation': operation for interacting with the database
        'payload': payload for the database
    """
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

    # dictionary for functions to perform on a given operation
    opsFuncs = {
        'POST' : Db.create,
        'GET' : Db.read,
        'PUT' : Db.update,
        'DELETE': Db.delete
    }

    # I'm not sure how to gracefully handle the case where it's passed an empty event
    # Maybe it should return an error status code?
    # Something like the following
    if event is None:
        # case where we don't even have an event
        response = ErrorHandler.emptyEventResponse
    elif 'operation' not in event.keys():
        # case in which we don't even have an operation key in the event
        response = ErrorHandler.badOpPayload
    else:
        if event['operation'] in opsFuncs and event['payload'] is not None:
            # call the relevent function from the Db class with the given payload
            opsResult = opsFuncs[event['operation']](event['payload'])
            response["body"] = opsResult
        else:
            # send an error response indicating we got a bad operation or payload
            response = ErrorHandler.badOpPayload

    return response

class Db():
    """
    Class that holds functions and information for interacting with the database.
    """
    def create(payload):
        return "{ \"message\": \"I received a POST Request\" }"
    def read(payload):
        return "{ \"message\": \"I received a GET Request\" }"
    def update(payload):
        return "{ \"message\": \"I received a PUT Request\" }"
    def delete(payload):
        return "{ \"message\": \"I received a DELETE Request\" }"


class ErrorHandler():
    emptyEventResponse = {
        "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: event object passed to Lambda function is empty\" }"
    }

    badOpPayload = {
        "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: unknown operation or payload\" }"
    }
