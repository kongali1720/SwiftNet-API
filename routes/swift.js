const express = require('express');
const router = express.Router();
const { sendSwift } = require('../controllers/swiftController');

router.post('/send', sendSwift);

module.exports = router;
