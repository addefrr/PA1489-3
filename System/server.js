const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// MySQL connection
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',  
    password: 'AlbinArdianWille_BTH24',  
    database: 'BurgerOrderDB'
});

// Connect to MySQL
db.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL:', err);
    } else {
        console.log('Connected to MySQL');
    }
});

// Route to handle order submission
app.post('/send-data', (req, res) => {
    const { item, side, comment, pickup, delivery } = req.body;

    const query = `INSERT INTO orders (item, side, comment, pickup, delivery) VALUES (?, ?, ?, ?, ?)`;
    db.query(query, [item, side, comment, pickup ? 1 : 0, delivery ? 1 : 0], (err, result) => {
        if (err) {
            console.error('Error inserting order:', err);
            res.status(500).json({ error: 'Failed to submit order' });
        } else {
            res.status(200).json({ message: 'Order submitted successfully' });
        }
    });
});

// Route to fetch the latest order
app.get('/get-data', (req, res) => {
    const query = `SELECT * FROM orders ORDER BY created_at DESC LIMIT 1`;
    db.query(query, (err, result) => {
        if (err) {
            console.error('Error fetching orders:', err);
            res.status(500).json({ error: 'Failed to fetch order' });
        } else if (result.length > 0) {
            res.status(200).json(result[0]);
        } else {
            res.status(200).json({ message: 'No orders found' });
        }
    });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
