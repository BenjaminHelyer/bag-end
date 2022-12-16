import unittest
from processCounter import lambda_handler
import json

class JsonsForTesting():
    """
    Holds some JSONS that will be used in testing.
    """
    getRequest = {
            "http": {
                "method": "GET"
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


if __name__ == '__main__':
    print("Testing the Lambda handler function.")

    unittest.main()
