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
          <img
            src={`${process.env.PUBLIC_URL}logo.png`}
            className="brand_logo"
            alt="logo"
          />
          <h1 className="brand_name">WOD Board</h1>
        </div>
        <nav className="navbar">
          <ol className="crumbs">
            <li>
              <a href="/">Register</a>
            </li>
            <li>
              <a href="/">Sign In</a>
            </li>
          </ol>
        </nav>
      </header>
    </div>
  );
}

export default App;
