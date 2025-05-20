const db = require('../db');

exports.sendSwift = (req, res) => {
  const { sender, receiver, amount, currency, swift_code } = req.body;

  const sql = `
    INSERT INTO swift_transactions (sender, receiver, amount, currency, swift_code)
    VALUES (?, ?, ?, ?, ?)
  `;

  db.query(sql, [sender, receiver, amount, currency, swift_code], (err, result) => {
    if (err) return res.status(500).json({ error: err.message });
    res.status(200).json({ message: 'SWIFT transaction sent successfully', id: result.insertId });
  });
};
