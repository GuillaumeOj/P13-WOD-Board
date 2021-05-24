import axios from 'axios';
import PropTypes from 'prop-types';
import React, { createContext, useContext } from 'react';

import { useAlert } from './Alert';

const apiContext = createContext();

function useApiProvider() {
  const { addAlert } = useAlert();
  const api = async ({
    user, method, data, url, silent,
  }) => {
    if (method && url) {
      const headers = {};

      if (user) {
        headers.Authorization = `${user.token_type} ${user.access_token}`;
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
            if (typeof detail === 'string') {
              addAlert({ message: detail, alertType: 'error' });
            } else if (detail.isArray) {
              detail.map((item) => addAlert({ message: item.msg, alertType: 'error' }));
            }
          }
        });
    }
    return <></>;
  };

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
