import React from 'react';
import { Helmet } from 'react-helmet';

import './scss/App.scss';

function App() {
  return (
    <div className="App">
      <Helmet>
        <title>Welcome to WOD Board!</title>
      </Helmet>
      <header className="App-header">
        <img src={`${process.env.PUBLIC_URL}logo.png`} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.jsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
