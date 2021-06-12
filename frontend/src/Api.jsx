import axios from 'axios';
import PropTypes from 'prop-types';
import React, {
  createContext, useEffect, useContext, useState,
} from 'react';
import { useCookies } from 'react-cookie';

import { useAlert } from './Alert';

const apiContext = createContext();

function useApiProvider() {
  const { addAlert } = useAlert();
  const [cookies] = useCookies();

  const [csrftoken, setCsrftoken] = useState(null);

  const api = async ({
    user, method, data, url, silent,
  }) => {
    if (method && url) {
      const headers = { 'Content-type': 'application/json' };

      if (user) {
        headers.Authorization = `${user.token_type} ${user.access_token}`;
      }

      if (csrftoken) {
        headers['X-CSRFToken'] = csrftoken;
      }

      if (data instanceof FormData) {
        headers['Content-Type'] = 'application/x-www-form-urlencoded';
      }

      const config = {
        method,
        url,
        headers,
        data,
      };

      return axios(config)
        .then((response) => response.data)
        .catch((error) => {
          if (error.response.data && !silent) {
            const { detail } = error.response.data;
            if (detail && typeof detail === 'string') {
              addAlert({ message: detail, alertType: 'error' });
            } else if (detail && detail.isArray) {
              detail.map((item) => addAlert({ message: item.msg, alertType: 'error' }));
            }
          }
        });
    }
    return <></>;
  };

  useEffect(() => {
    if (cookies.csrftoken && csrftoken === null) {
      setCsrftoken(cookies.csrftoken);
    }
  }, []);

  return { api };
}

export function ApiProvider({ children }) {
  const api = useApiProvider();
  return <apiContext.Provider value={api}>{children}</apiContext.Provider>;
}
ApiProvider.propTypes = {
  children: PropTypes.element.isRequired,
};

export const useApi = () => useContext(apiContext);
