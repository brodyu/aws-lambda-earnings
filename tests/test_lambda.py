import json
import unittest
import lambda_function

class lambdaTest(unittest.TestCase):

    def setUp(self):
        self.event = {"numbers":[5,7]}
        self.a = 5
        self.b = 7

    def test_lambda_handler(self):
        result = lambda_function.lambda_handler(self.event,'')
        data = json.loads(result["body"])
        print("data: ",data)
        expected_response = {"addition": 12, "multiplication": 35}
        self.assertEqual(data, expected_response)

    def test_sum(self):
       result = lambda_function.sum(self.a,self.b)
       self.assertEqual(result, self.a + self.b)


    def test_func_multiply(self):
        result = lambda_function.multiply(self.a,self.b)
        self.assertEqual(result, self.a * self.b)