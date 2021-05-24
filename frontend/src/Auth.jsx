import PropTypes from 'prop-types';
import React, {
  createContext, useEffect, useState, useContext,
} from 'react';
import { useCookies } from 'react-cookie';
import { useHistory } from 'react-router-dom';

import { useAlert } from './Alert';
import { useApi } from './Api';

const authContext = createContext();

function useProvideAuth() {
  const history = useHistory();
  const { api } = useApi();

  const { addAlert } = useAlert();
  const [cookies, setCookies, removeCookies] = useCookies();
  const [user, setUser] = useState(null);
  const [userId, setUserId] = useState();

  const signOut = () => {
    setUser(null);
    addAlert({ message: 'You are logged out.', alertType: 'warning' });
    history.replace('/');
  };

  const signIn = (tokenData) => {
    setUser(tokenData);
    addAlert({ message: 'You are logged in.', alertType: 'success' });
  };

  useEffect(async () => {
    if (user) {
      const response = await api({
        method: 'get', url: '/api/user/current/', silent: false, user,
      });

      if (response) {
        setUserId(response.id);
      }
    }
  }, [user]);

  useEffect(() => {
    setUser(cookies.user);
  }, []);

  useEffect(() => {
    if (user) {
      setCookies('user', user, { path: '/' });
    } else {
      removeCookies('user');
    }
  }, [user]);

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
