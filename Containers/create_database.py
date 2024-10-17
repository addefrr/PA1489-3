from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskapp_orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Orders model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    burger_name = db.Column(db.String(100), nullable=False)
    side_name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(200))
    order_type = db.Column(db.String(50), nullable=False)

# Initialize the database and add sample data
with app.app_context():
    db.create_all()  # Creates the database and tables
    
    # Check if the orders table is empty before adding sample data
    if Order.query.count() == 0:
        sample_orders = [
            Order(burger_name='CheeseBurger', side_name='Cheesy Fries', comment='no tomato', order_type='Delivery'),
            Order(burger_name='DoubleBurger', side_name='Large Fries', comment='', order_type='Pickup'),
            # Add more sample orders as needed
        ]
        db.session.bulk_save_objects(sample_orders)
        db.session.commit()
        print("Sample data added to the database.")
    else:
        print("Database already contains data.")

if __name__ == '__main__':
    print("Database created successfully.")
