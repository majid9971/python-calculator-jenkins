import unittest
from app import app  # Import the Flask app

class TestCalculatorAPI(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_add(self):
        response = self.app.get('/calculate?num1=10&num2=5&operation=add')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 15)

    def test_subtract(self):
        response = self.app.get('/calculate?num1=10&num2=5&operation=subtract')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 5)

    def test_multiply(self):
        response = self.app.get('/calculate?num1=10&num2=5&operation=multiply')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 50)

    def test_divide(self):
        response = self.app.get('/calculate?num1=10&num2=5&operation=divide')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 2)

    def test_divide_by_zero(self):
        response = self.app.get('/calculate?num1=10&num2=0&operation=divide')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "Division by zero is not allowed")

    def test_missing_parameters(self):
        response = self.app.get('/calculate?num1=10&operation=add')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "All parameters (num1, num2, operation) are required")

    def test_invalid_operation(self):
        response = self.app.get('/calculate?num1=10&num2=5&operation=modulus')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "Invalid operation")

    def test_invalid_number_format(self):
        response = self.app.get('/calculate?num1=abc&num2=5&operation=add')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "Invalid number format")

if __name__ == '__main__':
    unittest.main()
