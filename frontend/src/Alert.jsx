import PropTypes from 'prop-types';
import React, { useState, useContext, createContext } from 'react';
import { v4 as uuidv4 } from 'uuid';

const alertContext = createContext();

function useProvideAlert() {
  const [messages, setMessages] = useState([]);

  const removeAlert = ({ id }) => {
    const updatedAlerts = messages.filter((item) => item.id !== id);
    setMessages(updatedAlerts);
  };

  const addAlert = ({ message, alertType }) => {
    const updatedAlerts = [...messages];
    const existingAlert = updatedAlerts.filter((item) => item.message === message);
    if (existingAlert.length === 0) {
      const id = uuidv4();
      const timerId = setTimeout(() => {
        removeAlert({ id });
      }, 5000);
      updatedAlerts.push({
        message,
        alertType,
        id,
        timerId,
      });
      setMessages(updatedAlerts);
    }
  };
  addAlert.propTypes = {
    message: PropTypes.string.isRequired,
    alertType: PropTypes.oneOf(['error', 'success', 'warning']).isRequired,
  };

  return {
    messages,
    addAlert,
    removeAlert,
  };
}

export function AlertProvider({ children }) {
  const alert = useProvideAlert();
  return (
    <alertContext.Provider value={alert}>{children}</alertContext.Provider>
  );
}
AlertProvider.propTypes = {
  children: PropTypes.element.isRequired,
};

export const useAlert = () => useContext(alertContext);

export function DisplayAlerts() {
  const { messages, removeAlert } = useAlert();

  return (
    <div className="alerts">
      {messages
        && messages.map(({
          message, alertType, id, timerId,
        }) => (
          <div key={id} className={`alert ${alertType}`}>
            <p>{message}</p>
            <button
              type="button"
              className="button-close"
              aria-label="Close"
              onClick={() => {
                clearTimeout(timerId);
                removeAlert({ id });
              }}
            />
          </div>
        ))}
    </div>
  );
}
