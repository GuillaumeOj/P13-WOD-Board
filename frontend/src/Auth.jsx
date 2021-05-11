import axios from 'axios';
import PropTypes from 'prop-types';
import React, {
  createContext, useEffect, useState, useContext,
} from 'react';
import { useCookies } from 'react-cookie';
import { useHistory } from 'react-router-dom';

import { useAlert } from './Alert';

const authContext = createContext();

function useProvideAuth() {
  const history = useHistory();
  const { addAlert } = useAlert();
  const [cookies, setCookies, removeCookies] = useCookies();
  const [user, setUser] = useState(null);

  const signOut = () => {
    setUser(null);
    addAlert({ message: 'You are logged out.', alertType: 'warning' });
    history.replace('/');
  };

  const signIn = (tokenData) => {
    setUser(tokenData);
    addAlert({ message: 'You are logged in.', alertType: 'success' });
  };

  const userId = async () => {
    if (!user.access_token && !user.token_type) {
      return '';
    }

    const config = {
      headers: { Authorization: `${user.token_type} ${user.access_token}` },
    };

    return axios
      .get('/api/user/current/', config)
      .then((response) => response.data.id)
      .catch((error) => {
        if (error.response) {
          if (error.response.data) {
            const { detail } = error.response.data;

            if (typeof detail === 'string') {
              addAlert({ message: detail, alertType: 'error' });
            } else {
              detail.map((item) => addAlert({ message: item.msg, alertType: 'error' }));
            }
          }
        } else {
          addAlert({
            message: 'Impossible to retrieve user\'s id',
            alertType: 'error',
          });
        }
      });
  };

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
