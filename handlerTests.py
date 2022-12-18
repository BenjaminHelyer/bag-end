import unittest
from processCounter import lambda_handler
import json

class JsonsForTesting:
    """
    Holds some JSONS that will be used in testing.
    """
    junkRequest = {
            "junk": "moreJunk",
            "hello": "thisIsAllJunk"
        }

    anotherJunkRequest = {
            "body": {
                "operation": "elephant",
                "payload": "bear"
            }
        }

    opAsStringRequest = {
            "body": { "\n \"operation\": \"elephant\",\n\"payload\": \"bear\""
            }
    }

    createRequest = {
            "body": {
                "operation": "create",
                "payload": {
                    "Item": {
                        "id": "1234ABCD",
                        "number": 5
                    }
                }
            }
        }

    readRequest = {
            "body": {
                "operation": "read",
                "payload": {
                        "id": "1234ABCD"
                    }
            }
        }

    updateRequest = {
            "body": {
                "operation": "update",
                "payload": {
                        "id": "1234ABCD"
                    }
            }
        }

    deleteRequest = {
            "body": {
                "operation": "delete",
                "payload": {
                        "id": "1234ABCD"
                    }
            }
        }

    

class TestLambda(unittest.TestCase):
    """
    Test Object to use unittest library.
    """

    def test_empty_arg(self):
        """
        Basic test with no event argument for the Lambda handler function.
        """

        expectedResult = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: event object passed to Lambda function is empty\" }"
        }   

        # gets the result from the Lambda handler function
        result = lambda_handler(None, None)

        # assert whether the tests are equal
        self.assertEqual(result, expectedResult)
    
    def test_no_operation(self):
        """
        Sees if we catch a case where we have no operation in the event.
        """

        expectedResult = {
            "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "{ \"message\": \"Error: no body found in event. Event was: "
                        + str(JsonsForTesting.junkRequest)
                        + "\" }"
        }

        result = lambda_handler(JsonsForTesting.junkRequest, None)

        self.assertEqual(result, expectedResult)

    def test_bad_opeartion(self):
        """
        Tests if we catch the case where we have a bad operation in the event.
        """

        expectedResult = {
            "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "{ \"message\": \"Error: bad operation or payload\" }"
        }

        result = lambda_handler(JsonsForTesting.anotherJunkRequest, None)

        self.assertEqual(result, expectedResult)

    def test_create_request(self):
        """
        Unit test for a 'create' operation from the API.
        """

        expectedResult = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"The response to the 'create' request was \" }"
        }

        result = lambda_handler(JsonsForTesting.createRequest, None)

        self.assertEqual(result, expectedResult)

    def test_read_request(self):
        """
        Unit test for a 'read' request from the API.
        """

        expectedResult = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"The response to the 'read' request was \" }"
        }

        result = lambda_handler(JsonsForTesting.readRequest, None)

        self.assertEqual(result, expectedResult)

    def test_update_request(self):
        """
        Unit test for a 'update' request from the API.
        """

        expectedResult = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"The response to the 'update' request was \" }"
        }

        result = lambda_handler(JsonsForTesting.updateRequest, None)

        self.assertEqual(result, expectedResult)

    def test_delete_request(self):
        """
        Unit test for a 'delete' request from the API.
        """

        expectedResult = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"The response to the 'delete' request was \" }"
        }

        result = lambda_handler(JsonsForTesting.deleteRequest, None)

        self.assertEqual(result, expectedResult)

    def test_op_string_request(self):
        """
        Unit test for the case where the operation is held as a string in event['body'].
        This is what we suspect the events given by API Gateway are formatted as.
        """

        expectedResult = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"Error: no operation found in event['body']. event['body'] was: "
                    + str(JsonsForTesting.opAsStringRequest['body'])
                    + "\" }"
                    + "\n Type of event['body'] was: "
                    + str(type(JsonsForTesting.opAsStringRequest['body']))
        }

        result = lambda_handler(JsonsForTesting.opAsStringRequest, None)

        self.assertEqual(result, expectedResult)



if __name__ == '__main__':
    print("Testing the Lambda handler function.")

    unittest.main()
