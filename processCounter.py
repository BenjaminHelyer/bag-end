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

    # object that instantiates the database
    database = Db()

    # objects taht instantiates the error handler
    err = ErrorHandler(event)

    # dictionary for functions to perform on a given operation
    opsFuncs = {
        'create' : database.create,
        'read' : database.read,
        'update' : database.update,
        'delete': database.delete
    }

    # I'm not sure how to gracefully handle the case where it's passed an empty event
    # Maybe it should return an error status code?
    # Something like the following
    if event is None:
        # case where we don't even have an event
        response = err.emptyEventResponse
    elif 'body' not in event.keys():
        # case in which we don't even have an operation key in the event
        response = err.noBodyKey
    else:
        # now we know the event has a body. So now we test for the event's operation key
        if type(event['body']) is not dict:
            # first of all, we try to convert the body contents using the JSON library
            try:
                # try to convert the body contents to a dict using the JSON loader
                bodyAsDict = json.loads(event['body'])
            except:
                # give a clear error if we can't load it using the JSON library
                response = err.badBodyFormat
                return response

            # at this point, turning the body into a dict succeeded
            # now we test for a good operation, finally performing the operation if we find it
            if 'operation' not in bodyAsDict.keys():
                response = err.noOpKey
            elif bodyAsDict['operation'] not in opsFuncs or bodyAsDict['payload'] is None:
                response = err.badOpPayload
            else:
                # have another error thrown here to catch what might be going wrong with API Gateway
                try:
                    opsResult = opsFuncs[bodyAsDict['operation']](bodyAsDict['payload'])
                    response['body'] = opsResult
                except:
                    response = err.troublePerformingOpsFuncs
        elif event['body']['operation'] in opsFuncs and event['body']['payload'] is not None:
            # call the relevent function from the Db class with the given payload
            opsResult = opsFuncs[event['body']['operation']](event['body']['payload'])
            response['body'] = opsResult
        else:
            # send an error response indicating we got a bad operation or payload
            response = err.badOpPayload

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
        itemToCreate = payload['Item']
        dbResponse = self.dynamo.put_item(Item=itemToCreate) # we have to put the arguments this way since the function only accepts keyword arguments
        return "{ \"message\": \"The response to the 'create' request was \" }"

    def read(self, payload):
        keyToRead = {'id': payload['Item']['id']}
        attributeKey = payload['Item']['attribute']
        dbResponse = self.dynamo.get_item(Key=keyToRead)
        attributeToReturn = dbResponse['Item'][attributeKey]
        return """{ "message": "The response to the 'read' request was """ + str(attributeToReturn) + """ " } """
            
    def update(self, payload):
        keyToUpdate = {'id': payload['Item']['id']}

        if payload['Item']['expression'] == '++':
            # expression for incrementing, which is the main expression we'll want for the visitor counter
            attribute = str(payload['Item']['attribute'])
            updateExpr = "set " + attribute + "=" + attribute + " + :val"
            attrVals = {':val': 1}
        else:
            # let's not raise an error response here for now, though we likely should if this were in use by more people
            return "{ \"message\": \"Only the increment expression is supported for now.\" }"

        dbResponse = self.dynamo.update_item(Key=keyToUpdate, UpdateExpression=updateExpr, ExpressionAttributeValues=attrVals)

        return "{ \"message\": \"The response to the 'update' request was \" }"

    def delete(self, payload):
        dbResponse = self.dynamo.delete_item(Key=payload)
        return "{ \"message\": \"The response to the 'delete' request was \" }"


class ErrorHandler:
    """
    Class that holds functions and information relating to errors.
    """
    def __init__(self, event):
        self.event = event

        self.emptyEventResponse = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: event object passed to Lambda function is empty\" }"
        }

        self.badOpPayload = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: bad operation or payload\" }"
        }

        self.noBodyKey = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: no body found in event. Event was: "
                    + str(self.event)
                    + "\" }"
        }

        self.noOpKey = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: event['body'] could be turned into dict, but no operation found in event['body']. event['body'] was: "
                    + str(self.getEventBody())
                    + "\" }"
                    + "\n Type of event['body'] was: "
                    + str(self.getEventBodyType())
        }

        self.badBodyFormat = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: event['body'] could not be turned into dict. event['body'] was: "
                    + str(self.getEventBody())
                    + "\" }"
                    + "\n Type of event['body'] was: "
                    + str(self.getEventBodyType())
        }

        self.troublePerformingOpsFuncs = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: trouble performing operation functions. event['body'] was: "
                    + str(self.getEventBody())
                    + "\" }"
                    + "\n Type of event['body'] was: "
                    + str(self.getEventBodyType())
        }

    def getEventBody(self):
        """
        Function that we use to get event['body'], or gracefully feed back None if we can't.
        """
        try:
            return self.event['body']
        except:
            return None

    def getEventBodyType(self):
        """
        Function that we use to get the type of event['body'], or gracefully feed back None if we can't.
        """
        try:
            return type(self.event['body'])
        except:
            return None
