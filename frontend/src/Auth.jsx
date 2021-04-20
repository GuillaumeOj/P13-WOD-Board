import React, {
  useEffect, useState, useContext, createContext,
} from 'react';
import { useCookies } from 'react-cookie';
import { useHistory } from 'react-router-dom';

import { useAlert } from './Alert';

const authContext = createContext();

function useProvideAuth() {
  const history = useHistory();
  const { addAlert } = useAlert();
  const [cookies, setCookie, removeCookie] = useCookies(['user']);
  const [user, setUser] = useState(null);

  const signOut = () => {
    removeCookie('user');
    setUser(null);
    addAlert({ message: 'You are logged out.', alertType: 'success' });
    history.push('/');
  };

  const signIn = (tokenData) => {
    if (tokenData) {
      setCookie('user', tokenData, { path: '/' });
    }
  };

  useEffect(() => {
    setUser(cookies.user);
  }, [cookies]);

  return {
    user,
    signIn,
    signOut,
  };
}

// eslint-disable-next-line react/prop-types
export function ProvideAuth({ children }) {
  const auth = useProvideAuth();
  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}

export const useAuth = () => useContext(authContext);
