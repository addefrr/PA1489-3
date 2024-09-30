from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Laddar databasinställningar från db.yaml
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# Route för att ta emot och lagra data från beställningsformuläret
@app.route('/send-data', methods=['POST'])
def send_data():
    data = request.json
    burger_name = data['item']  # Hämtar vald burgare
    side_name = data['side']  # Hämtar vald side
    comment = data['comment']  # Hämtar eventuell kommentar
    order_type = data.get('order_type', 'Pickup')  # Få värdet från order_type eller sätt till 'Pickup' som standard

    # Infoga beställningen i MySQL-databasen med comment och order_type
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO orders(burger_name, side_name, comment, order_type) 
        VALUES(%s, %s, %s, %s)
    """, (burger_name, side_name, comment, order_type))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'Order placed successfully!'})  # Returnerar JSON som svar

# Route för att visa beställningarna i kitchenview
@app.route('/kitchenview')
def kitchenview():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT burger_name, side_name, comment, order_type FROM orders")
    if result_value > 0:
        userDetails = cur.fetchall()
        return render_template('kitchenview.html', userDetails=userDetails)
    cur.close()
    return 'No orders to show!'

if __name__ == '__main__':
    app.run(debug=True)