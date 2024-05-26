import React from 'react';

const Home = () => {
  const handleLogin = () => {
    const client_id = 'Ov23liOJtdermarjTi11';
    const redirect_uri = 'http://localhost:3000/callback';
    const auth_url = `https://github.com/login/oauth/authorize?client_id=${client_id}&redirect_uri=${redirect_uri}&scope=user`;

    window.location.href = auth_url;
  };

  return (
    <div>
      <h1>OAuth2 Client</h1>
      <button onClick={handleLogin}>Login with Github</button>
    </div>
  );
};

export default Home;
