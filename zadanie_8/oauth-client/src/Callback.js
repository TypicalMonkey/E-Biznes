import React, { useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Callback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const fetchToken = async () => {
      const params = new URLSearchParams(window.location.search);
      const code = params.get('code');

      if (code) {
        try {
          const response = await axios.post('http://localhost:5000/auth/token', { code });
          const { newToken } = response.data;
          localStorage.setItem('token', newToken);
          navigate('/');
        } catch (error) {
          console.error('Error fetching token:', error);
        }
      }
    };

    fetchToken();
  }, [navigate]);

  return <div>Loading...</div>;
};

export default Callback;
