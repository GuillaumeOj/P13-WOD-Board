import axios from 'axios';
import React, { useState } from 'react';

import { useAlert } from '../../Alert';
import { useAuth } from '../../Auth';

export default function Wod() {
  const { addAlert } = useAlert();
  const { user } = useAuth();
  const headers = { Authorization: `${user.tokenType} ${user.accessToken}` };
  const config = { headers };

  const [id, setId] = useState(-1);
  const [name, setName] = useState('');

  const [wodTypes, setWodTypes] = useState([]);

  const searchWodTypes = (event) => {
    const currentValue = event.target.value;
    setName(currentValue);
    if (currentValue) {
      axios
        .get(`/api/type/list/${currentValue}`, config)
        .then((response) => setWodTypes(response.data))
        .catch((error) => {
          if (error) {
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
                message: 'Impossible to retrieve WOD types',
                alertType: 'error',
              });
            }
          }
        });
    } else { setWodTypes([]); }
  };

  return (
    <div className="field">
      <label htmlFor="wodType">Type of WOD*:&nbsp;</label>
      <input
        name="wodType"
        id="wodType"
        value={name}
        onChange={searchWodTypes}
        onBlur={() => {
          console.log(id);
        }}
        required
        placeholder="AMRAP, EMOM, etc."
      />
      <div className="completion">
        {wodTypes && (
        <div className="types">
          {wodTypes.map((item) => (
            <button
              className="button type"
              type="button"
              key={item.id}
              value={item.name}
              onClick={() => {
                setId(item.id);
                setName(item.name);
                setWodTypes([]);
              }}
            >
              {item.name}
            </button>
          ))}
        </div>
        )}
      </div>
    </div>
  );
}
