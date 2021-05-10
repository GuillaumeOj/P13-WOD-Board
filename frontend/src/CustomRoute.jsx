import PropTypes from 'prop-types';
import React from 'react';
import { Route, Redirect } from 'react-router-dom';

import { useAuth } from './Auth';

export function PrivateRoute({ children, ...rest }) {
  const { user } = useAuth();

  return (
    <Route
      {...rest}
      render={
        ({ location }) => (
          (user !== null) ? (
            children
          ) : (
            <Redirect to={{
              pathname: '/signin',
              state: {
                from: location,
              },
            }}
            />
          )
        )
      }
    />
  );
}
PrivateRoute.propTypes = {
  children: PropTypes.element.isRequired,
};

export function AnonymRoute({ children, ...rest }) {
  const { user } = useAuth();

  return (
    <Route
      {... rest}
      render={
        ({ location }) => (
          user ? (
            <Redirect to={{
              pathname: '/dashboard',
              state: {
                from: location,
              },
            }}
            />
          ) : (
            children
          )
        )
      }
    />
  );
}
AnonymRoute.propTypes = {
  children: PropTypes.element.isRequired,
};
