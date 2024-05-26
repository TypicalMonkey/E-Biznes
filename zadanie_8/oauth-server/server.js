const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());

app.use(bodyParser.json());

app.post('/auth/token', async (req, res) => {
  const { code } = req.body;

  try {
    const response = await axios.post('https://github.com/login/oauth/access_token', {
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET,
      redirect_uri: process.env.REDIRECT_URI,
      code,
    }, {
      headers: {
        accept: 'application/json'
      }
    });

    const { access_token } = response.data;
    const newToken = generateNewToken();
    res.json({ newToken });
  } catch (error) {
    console.error('Error fetching token:', error);
    res.status(500).send('Internal Server Error');
  }
});

const generateNewToken = () => {
  return 'newlyGeneratedToken';
};

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
