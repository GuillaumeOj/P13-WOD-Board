import React from 'react';
import { CookiesProvider } from 'react-cookie';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';

import { AlertProvider } from './Alert';
import { ApiProvider } from './Api';
import App from './App';
import { ProvideAuth } from './Auth';

import './scss/index.scss';

ReactDOM.render(
  <React.StrictMode>
    <AlertProvider>
      <CookiesProvider>
        <ApiProvider>
          <BrowserRouter>
            <ProvideAuth>
              <App />
            </ProvideAuth>
          </BrowserRouter>
        </ApiProvider>
      </CookiesProvider>
    </AlertProvider>
  </React.StrictMode>,
  document.getElementById('root'),
);
