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
            "operation": "elephant",
            "payload": "bear"
        }

    postRequest = {
            "operation": "POST",
            "payload": {
                    "id": "1234ABCD",
                    "number": 5
                }
        }

    getRequest = {
            "operation": "GET",
            "payload": "{ myKey : myVal }"
        }

    putRequest = {
            "operation": "PUT",
            "payload": "{ myKey : myVal }"
        }

    deleteRequest = {
            "operation": "DELETE",
            "payload": "{ myKey : myVal }"
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
                "body": "{ \"message\": \"Error: unknown operation or payload\" }"
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
                "body": "{ \"message\": \"Error: unknown operation or payload\" }"
        }

        result = lambda_handler(JsonsForTesting.anotherJunkRequest, None)

        self.assertEqual(result, expectedResult)

    def test_post_request(self):
        """
        Unit test for a POST request from the API.
        """

        expectedResult = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"I received a POST Request\" }"
        }

        result = lambda_handler(JsonsForTesting.postRequest, None)

        self.assertEqual(result, expectedResult)

    def test_get_request(self):
        """
        Unit test for a GET request from the API.
        """

        expectedResult = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"I received a GET Request\" }"
        }

        result = lambda_handler(JsonsForTesting.getRequest, None)

        self.assertEqual(result, expectedResult)

    def test_put_request(self):
        """
        Unit test for a PUT request from the API.
        """

        expectedResult = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"I received a PUT Request\" }"
        }

        result = lambda_handler(JsonsForTesting.putRequest, None)

        self.assertEqual(result, expectedResult)

    def test_delete_request(self):
        """
        Unit test for a DELETE request from the API.
        """

        expectedResult = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "{ \"message\": \"I received a DELETE Request\" }"
        }

        result = lambda_handler(JsonsForTesting.deleteRequest, None)

        self.assertEqual(result, expectedResult)



if __name__ == '__main__':
    print("Testing the Lambda handler function.")

    unittest.main()
