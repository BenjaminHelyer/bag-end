import unittest
from myDateTimeFunction import lambda_handler
import json

class JsonsForTesting():
    """
    Holds some JSONS that will be used in testing.
    """
    books = {
            "name": "Les Miserables",
            "author": "Victor Hugo",
            "century": "19th"
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
            "description": "Error: event object passed to Lambda function is empty"
        }   

        # gets the result from the Lambda handler function
        result = lambda_handler(None, None)

        # assert whether the tests are equal
        self.assertEqual(result, expectedResult)

    def test_books(self):
        """
        Unit test for the books.json file.
        """
        
        expectedResult = {
            "statusCode": 200,
            "updatedResponse": 3,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "Region ": "us-east-1"
            }),
            "name": "Les Miserables"
        }

        # gets the result from the Lambda handler function
        result = lambda_handler(JsonsForTesting.books, None)

        # assert whether the tests are equal
        self.assertEqual(result, expectedResult)


if __name__ == '__main__':
    print("Testing the Lambda handler function.")

    unittest.main()
