import unittest
from app import app
from flask import json
from unittest.mock import patch, MagicMock

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.testclient()
        self.app.testing = True

    @patch('app.mysql.connection.cursor')
    def testsenddata(self, mockcursor):
        # Create a mock cursor object
        mock_cur = MagicMock()
        mock_cursor.return_value = mock_cur

        # Mock the execute and commit methods
        mock_cur.execute.return_value = None
        mock_cur.connection.commit.return_value = None

        # Test data
        test_data = {
            'item': 'Cheeseburger',
            'side': 'Fries',
            'comment': 'No pickles',
            'order_type': 'Delivery'
        }

        # Send a POST request to /send-data
        response = self.app.post('/send-data', 
                                data=json.dumps(test_data),
                                content_type='application/json')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected message
        self.assertEqual(json.loads(response.data), {'status': 'Order placed successfully!'})

        # Check if the database insert was called with the correct data
        mock_cur.execute.assert_called_once_with(
            "INSERT INTO orders(burger_name, side_name, comment, order_type) VALUES(%s, %s, %s, %s)",
            ('Cheeseburger', 'Fries', 'No pickles', 'Delivery')
        )

        # Check if the database commit was called
        mock_cur.connection.commit.assert_called_once()

if __name == '__main':
    unittest.main()