// server.js
const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
require('dotenv').config();

app.use(cors());
app.use(express.static('public')); // serve index.html

const CLIENT_ID = process.env.FATSECRET_CLIENT_ID || '9ea5cf43b88b4cf2b84275bf967290cc';
const CLIENT_SECRET = process.env.FATSECRET_CLIENT_SECRET || '4df6c19ab6434c17960c1c2c623f1a08';

app.get('/api/token', async (req, res) => {
  try {
    const params = new URLSearchParams();
    params.append('grant_type', 'client_credentials');
    params.append('scope', 'basic');

    const response = await axios.post(
      'https://oauth.fatsecret.com/connect/token',
      params,
      {
        auth: {
          username: CLIENT_ID,
          password: CLIENT_SECRET
        },
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );

    res.json({ token: response.data.access_token });
  } catch (err) {
    console.error('Token fetch failed:', err.response?.data || err.message);
    res.status(500).json({ error: 'Failed to get token' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
