const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

// Set up middleware
app.use(bodyParser.json());
app.use(express.static('public'));

// Set up MySQL connection
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'your_password', // Replace with your MySQL root password
    database: 'burger_orders'
});

connection.connect(err => {
    if (err) {
        console.error('Error connecting to the database:', err);
        return;
    }
    console.log('Connected to MySQL database');
});

// Route to handle order submissions
app.post('/send-data', (req, res) => {
    const { item, side, comment, pickup, delivery } = req.body;
    const orderType = pickup ? 'Pickup' : 'Delivery';
    
    const sql = 'INSERT INTO orders (item, side, comment, order_type) VALUES (?, ?, ?, ?)';
    connection.query(sql, [item, side, comment, orderType], (err, results) => {
        if (err) {
            console.error('Error inserting order into database:', err);
            res.status(500).send('Error processing order');
            return;
        }
        res.json({ success: true });
    });
});

// Route to retrieve the most recent order
app.get('/get-data', (req, res) => {
    const sql = 'SELECT * FROM orders ORDER BY created_at DESC LIMIT 1';
    connection.query(sql, (err, results) => {
        if (err) {
            console.error('Error retrieving order from database:', err);
            res.status(500).send('Error fetching orders');
            return;
        }
        res.json(results[0] || {});
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
