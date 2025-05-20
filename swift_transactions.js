const express = require('express');
const mysql = require('mysql2');

const app = express();
const port = 3000;

// Buat koneksi pool ke MySQL
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',          // ganti dengan user MySQL kamu
  password: 'aligeno',// ganti dengan password MySQL kamu
  database: 'swift_transactions_db', // database yang benar
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// Endpoint root untuk cek server jalan
app.get('/', (req, res) => {
  res.send('🚀 Server Swift Transactions API jalan!');
});

// Endpoint untuk ambil data transaksi swift
app.get('/transactions', (req, res) => {
  const sql = 'SELECT * FROM swift_transactions LIMIT 10';

  pool.query(sql, (err, results) => {
    if (err) {
      console.error('Gagal query:', err);
      return res.status(500).json({ error: 'Gagal mengambil data transaksi' });
    }
    res.json(results);
  });
});

// Jalankan server
app.listen(port, () => {
  console.log(`🚀 Server jalan di http://localhost:${port}`);
});

