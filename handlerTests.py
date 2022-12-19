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

    badOpAsStringRequest = {
            "body": "{ \n \"operation\": \"elephant\",\n\"payload\": \"Item\"}"
    }

    goodOpAsStringRequest = {
            "body": """{
                    "operation": "create",
                    "payload": {
                        "Item": {
                            "id": "1234ABCD",
                            "number": 5
                        }
                    }
                }
                """
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

    def test_bad_op_str(self):
        """
        Unit test for a bad operation as a string within the body of the event.
        """

        expectedResult = {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "{ \"message\": \"Error: bad operation or payload\" }"
        }

        result = lambda_handler(JsonsForTesting.badOpAsStringRequest, None)

        self.assertEqual(result, expectedResult)

    def test_good_op_str(self):
        """
        Unit test for a good operation as a string within the body of the event.
        """

        expectedResult = {
                "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                "body": "{ \"message\": \"The response to the 'create' request was \" }"
        }

        result = lambda_handler(JsonsForTesting.goodOpAsStringRequest, None)

        self.assertEqual(result, expectedResult)



if __name__ == '__main__':
    print("Testing the Lambda handler function.")

    unittest.main()

    # myTests = TestLambda()
    # myTests.test_bad_op_str()
