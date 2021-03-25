import React from 'react';
import { Helmet } from 'react-helmet';

function App() {
  return (
    <div className="App">
      <Helmet>
        <title>Welcome to WOD Board!</title>
      </Helmet>
      <header>
        <div className="logo">
          <img src={`${process.env.PUBLIC_URL}logo.png`} className="brand_logo" alt="logo" />
          <h1 className="brand_name">
            WOD Board
          </h1>
        </div>
      </header>
    </div>
  );
}

export default App;
