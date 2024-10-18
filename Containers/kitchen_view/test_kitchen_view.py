import unittest
from app import app  # Import the Flask app

class kitchen_view_test(unittest.TestCase):

    # Set up the test environment
    def setUp(self):
        # Enable testing mode
        app.config['TESTING'] = True  
         # Create a test client
        self.client = app.test_client() 

    # Running tests on the homepage 
    def test_homepage(self):
        # Send a GET request to the home page
        response = self.client.get('/') 
        # Check if the response status is 200 meaning it works properly
        self.assertEqual(response.status_code, 200)  

    # Test the /get-orders API
    def test_get_orders(self):
        # Send a GET request to /get-orders
        response = self.client.get('/get-orders')
        # Again checking to make sure it returns 200 
        self.assertEqual(response.status_code, 200)  

# Run the tests
if __name__ == '__main__':
    unittest.main()