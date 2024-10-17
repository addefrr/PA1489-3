import unittest
from app import app  # Import the Flask app

class BurgerOrdererTest(unittest.TestCase):

    # Set up the test environment
    def setUp(self):
        # Enable testing mode
        app.config['TESTING'] = True
        # Create a test client
        self.client = app.test_client()

    # Test the homepage
    def test_homepage(self):
        # Send a GET request to the home page
        response = self.client.get('/')
        # Check if the response status is 200
        self.assertEqual(response.status_code, 200)

    # Test the /send-data endpoint
    def test_send_data(self):
        # Create a sample order payload
        data = {
            'item': 'CheeseBurger',
            'side': 'Fries',
            'comment': 'No onions',
            'order_type': 'Pickup'
        }
        # Send a POST request to /send-data
        response = self.client.post('/send-data', json=data)
        # Check if the response status is 200
        self.assertEqual(response.status_code, 200)
        # Verify that the response contains a success message
        self.assertIn(b'Order placed successfully!', response.data)

# Run the tests
if __name__ == '__main__':
    unittest.main()
