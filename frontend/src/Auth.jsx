import PropTypes from 'prop-types';
import React, {
  createContext, useEffect, useState, useContext,
} from 'react';
import { useHistory } from 'react-router-dom';

import { useAlert } from './Alert';

const authContext = createContext();

function useProvideAuth() {
  const history = useHistory();

  const { addAlert } = useAlert();
  const [user, setUser] = useState(null);
  const [userId] = useState();

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
