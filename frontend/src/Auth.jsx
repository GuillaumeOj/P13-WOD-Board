import PropTypes from 'prop-types';
import React, {
  createContext, useEffect, useState, useContext,
} from 'react';
import { useHistory } from 'react-router-dom';

import { useAlert } from './Alert';
import { useApi } from './Api';

const authContext = createContext();

function useProvideAuth() {
  const history = useHistory();
  const { api } = useApi();

  const { addAlert } = useAlert();
  const [user, setUser] = useState(null);
  const [userId, setUserId] = useState();

  const signOut = () => {
    sessionStorage.removeItem('user');
    setUser(null);
    addAlert({ message: 'You are logged out.', alertType: 'warning' });
    history.replace('/');
  };

  const signIn = (userData) => {
    sessionStorage.setItem('user', JSON.stringify(userData));

    setUser(userData);

    addAlert({ message: 'You are logged in.', alertType: 'success' });
  };

  useEffect(async () => {
    if (user && user.access_token && user.token_type) {
      const response = await api({
        method: 'get', url: '/api/user/current/', silent: false, user,
      });

      if (response) {
        setUserId(response.id);
      }
    }
  }, [user]);

  useEffect(() => {
    if (user === null) {
      const userSession = sessionStorage.getItem('user');
      if (userSession !== null) {
        setUser(JSON.parse(userSession));
      }
    }
  }, []);

  return {
    user,
    userId,
    signIn,
    signOut,
  };
}

export function ProvideAuth({ children }) {
  const auth = useProvideAuth();
  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}
ProvideAuth.propTypes = {
  children: PropTypes.element.isRequired,
};

export const useAuth = () => useContext(authContext);
