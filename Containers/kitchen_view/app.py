import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'flaskapp_orders.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Orders model (must be the same as in BurgerOrderer)
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    burger_name = db.Column(db.String(100), nullable=False)
    side_name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(200))
    order_type = db.Column(db.String(50), nullable=False)

@app.route('/')
def kitchen_index():
    orders = Order.query.all()
    return render_template('kitchenview.html', userDetails=orders)

@app.route('/get-orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    orders_list = [{'id': order.id, 'burger_name': order.burger_name, 'side_name': order.side_name, 'comment': order.comment, 'order_type': order.order_type} for order in orders]
    return jsonify(orders_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
