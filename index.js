const express = require('express');
const app = express();
require('dotenv').config();
const swiftRoutes = require('./routes/swift');

app.use(express.json());
app.use('/api/swift', swiftRoutes);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`🚀 SwiftNet API running at http://localhost:${PORT}`);
});
