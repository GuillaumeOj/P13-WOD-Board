import React from 'react';
import { CookiesProvider } from 'react-cookie';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';

import App from './App';
import { ProvideAuth } from './Auth';

import './scss/index.scss';

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <CookiesProvider>
        <ProvideAuth>
          <App />
        </ProvideAuth>
      </CookiesProvider>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root'),
);
