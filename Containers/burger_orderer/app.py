import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'flaskapp_orders.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Orders model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    burger_name = db.Column(db.String(100), nullable=False)
    side_name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(200))
    order_type = db.Column(db.String(50), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('burgerorderer.html')

# Route to receive and store data from the order form
@app.route('/send-data', methods=['POST'])
def send_data():
    data = request.json
    burger_name = data['item']
    side_name = data['side']
    comment = data['comment']
    order_type = data.get('order_type', 'Pickup')

    # Insert the order into the SQLite database
    new_order = Order(burger_name=burger_name, side_name=side_name, comment=comment, order_type=order_type)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'status': 'Order placed successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
