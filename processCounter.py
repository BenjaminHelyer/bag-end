import os
import json
import boto3
        
def lambda_handler(event, context):
    """
    The event should have the following keys:
        'operation': operation for interacting with the database
        'payload': payload for the database
    """
    # default response so we can adjust the parts we need later
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "{}"
    }

    # object that instantiates the database so we can interact with it
    database = Db()

    # dictionary for functions to perform on a given operation
    opsFuncs = {
        'POST' : database.create,
        'GET' : database.read,
        'PUT' : database.update,
        'DELETE': database.delete
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

class Db:
    """
    Class that holds functions and information for interacting with the database.
    """
    def __init__(self,tableName='bagend-app-CountTable-UQA7T802H60N'):
        # should likely find a way such that the table name can be changed here when we update it in AWS SAM
        self.tableName = tableName
        # should also likely find a way such that the development table isn't the same as the production table
        # neither this nor the previous comment are *essential* for this project, so keeping it this way for now
        self.dynamo = boto3.resource('dynamodb').Table(self.tableName)

    def create(self, payload):
        self.dynamo.put_item(Item=payload)
        return "{ \"message\": \"I received a POST Request\" }"
    def read(self, payload):
        return "{ \"message\": \"I received a GET Request\" }"
    def update(self, payload):
        return "{ \"message\": \"I received a PUT Request\" }"
    def delete(self, payload):
        return "{ \"message\": \"I received a DELETE Request\" }"


class ErrorHandler:
    """
    Class that holds functions and information relating to errors.
    """
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
