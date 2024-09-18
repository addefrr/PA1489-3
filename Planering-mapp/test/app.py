from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Variable to store the shared data
shared_data = {}

# Route for Frontend A to send data
@app.route('/send-data', methods=['POST'])
def send_data():
    global shared_data
    shared_data = request.json  # Store the received JSON data
    return jsonify({'message': 'Data received'})  # Respond with a confirmation

# Route for Frontend B to get the stored data
@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(shared_data)  # Return the stored data as JSON

# Serving the Frontend A and Frontend B HTML pages
@app.route('/frontendA')
def frontend_a():
    return render_template('frontendA.html')

@app.route('/frontendB')
def frontend_b():
    return render_template('frontendB.html')

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
