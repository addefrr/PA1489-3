from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Load database settings from db.yaml
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']  # Set MySQL host
app.config['MYSQL_USER'] = db['mysql_user']  # Set MySQL user
app.config['MYSQL_PASSWORD'] = db['mysql_password']  # Set MySQL password
app.config['MYSQL_DB'] = db['mysql_db']  # Set MySQL database name

mysql = MySQL(app)  # Initialize MySQL

@app.route('/')  # Define the route for the home page
def index():
    return render_template('burgerorderer/burgerorderer.html')  # Render the burger order page

# Route to receive and store data from the order form
@app.route('/send-data', methods=['POST'])
def send_data():
    data = request.json  # Get the JSON data sent in the request
    burger_name = data['item']  # Get the selected burger
    side_name = data['side']  # Get the selected side
    comment = data['comment']  # Get any optional comment
    order_type = data.get('order_type', 'Pickup')  # Get order_type value, default to 'Pickup'

    # Insert the order into the MySQL database without burger_id (since it is AUTO_INCREMENT)
    cur = mysql.connection.cursor()  # Create a cursor to interact with the database
    cur.execute("""
        INSERT INTO orders(burger_name, side_name, comment, order_type) 
        VALUES(%s, %s, %s, %s)  # Use placeholders for values to prevent SQL injection
    """, (burger_name, side_name, comment, order_type))
    mysql.connection.commit()  # Commit the transaction to save changes
    cur.close()  # Close the cursor

    return jsonify({'status': 'Order placed successfully!'})  # Return JSON response indicating success


# Route to display orders in the kitchen view
@app.route('/kitchenview')
def kitchenview():
    cur = mysql.connection.cursor()  # Create a cursor to interact with the database
    result_value = cur.execute("SELECT burger_id, burger_name, side_name, comment, order_type FROM orders")  # Execute SQL query to fetch orders
    if result_value > 0:  # Check if any orders were found
        userDetails = cur.fetchall()  # Fetch all order details
        return render_template('kitchenview/kitchenview.html', userDetails=userDetails)  # Render the kitchen view page with order details
    cur.close()  # Close the cursor
    return 'No orders to show!'  # Return a message if no orders are found

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
