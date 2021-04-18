import * as Sentry from '@sentry/react';
import { Integrations } from '@sentry/tracing';
import React from 'react';
import { CookiesProvider } from 'react-cookie';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';

import { AlertProvider } from './Alert';
import App from './App';
import { ProvideAuth } from './Auth';

import './scss/index.scss';

if (process.env.NODE_ENV === 'production') {
  Sentry.init({
    dsn:
      'https://cff175f8ab4f41e7a1f4f2a35b3e9d2a@o453278.ingest.sentry.io/5704650',
    integrations: [new Integrations.BrowserTracing()],

    // Set tracesSampleRate to 1.0 to capture 100%
    // of transactions for performance monitoring.
    // We recommend adjusting this value in production
    tracesSampleRate: 1.0,
  });
}

ReactDOM.render(
  <React.StrictMode>
    <AlertProvider>
      <BrowserRouter>
        <CookiesProvider>
          <ProvideAuth>
            <App />
          </ProvideAuth>
        </CookiesProvider>
      </BrowserRouter>
    </AlertProvider>
  </React.StrictMode>,
  document.getElementById('root'),
);
