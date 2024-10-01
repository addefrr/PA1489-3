import pytest
from flask import json
from app import app  # Import Flask app from the main app file
from unittest.mock import patch, MagicMock

# Fixture to set up the test client
@pytest.fixture
def client():
    app.config['TESTING'] = True  # Set app to testing mode
    with app.test_client() as client:
        yield client

# Test the index route
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200  # Check if status is OK
    assert b'burgerorderer' in response.data  # Check if 'burgerorderer' page is rendered

# Test the /send-data route
@patch('app.mysql.connection.cursor')  # Mock the MySQL cursor
def test_send_data(mock_cursor, client):
    mock_cur = MagicMock()  # Create a mock cursor object
    mock_cursor.return_value = mock_cur  # Return the mock cursor when called
    
    # Mocking the MySQL connection commit and close
    mock_cur.execute.return_value = None
    mock_cur.close.return_value = None

    # Data to send
    data = {
        'item': 'Cheeseburger',
        'side': 'Fries',
        'comment': 'No pickles',
        'order_type': 'Delivery'
    }

    # Send a POST request to /send-data
    response = client.post('/send-data', json=data)
    
    # Check the response status and JSON content
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'Order placed successfully!'
    
    # Assert the MySQL cursor execute was called with correct SQL and parameters
    mock_cur.execute.assert_called_once_with(
        "INSERT INTO orders(burger_name, side_name, comment, order_type) VALUES(%s, %s, %s, %s)",
        ('Cheeseburger', 'Fries', 'No pickles', 'Delivery')
    )

# Test the /kitchenview route with mocked database results
@patch('app.mysql.connection.cursor')  # Mock the MySQL cursor
def test_kitchenview(mock_cursor, client):
    mock_cur = MagicMock()  # Create a mock cursor object
    mock_cursor.return_value = mock_cur  # Return the mock cursor when called
    
    # Mock MySQL fetchall and execute results
    mock_cur.execute.return_value = 1  # Simulate 1 row returned from the query
    mock_cur.fetchall.return_value = [
        ('Cheeseburger', 'Fries', 'No pickles', 'Delivery'),
        ('Veggie Burger', 'Salad', 'Extra dressing', 'Pickup')
    ]
    
    # Send a GET request to /kitchenview
    response = client.get('/kitchenview')
    
    # Check if the response is OK and contains expected order details
    assert response.status_code == 200
    assert b'Cheeseburger' in response.data
    assert b'Fries' in response.data
    assert b'No pickles' in response.data
    assert b'Delivery' in response.data
    assert b'Veggie Burger' in response.data
    assert b'Salad' in response.data

    # Assert that the MySQL cursor was used to fetch orders
    mock_cur.execute.assert_called_once_with("SELECT burger_name, side_name, comment, order_type FROM orders")
