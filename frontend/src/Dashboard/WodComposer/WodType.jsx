import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { useAlert } from '../../Alert';

export default function WodType({ setWodTypeId }) {
  const { addAlert } = useAlert();

  const [id, setId] = useState();
  const [name, setName] = useState('');

  const [wodTypes, setWodTypes] = useState([]);

  const searchWodTypes = (event) => {
    const currentValue = event.target.value;
    setId();
    setName(currentValue);
    if (currentValue) {
      axios
        .get(`/api/type/list/${currentValue}`)
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

  const selectWodType = (itemId, itemName) => {
    setId(itemId);
    setName(itemName);
    setWodTypes([]);
  };

  useEffect(() => { setWodTypeId(id); }, [id]);

  return (
    <div className="field">
      <label htmlFor="wodType">Type of WOD*:&nbsp;</label>
      <input
        name="wodType"
        id="wodType"
        value={name}
        onChange={searchWodTypes}
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
              onClick={() => selectWodType(item.id, item.name)}
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
WodType.propTypes = {
  setWodTypeId: PropTypes.func.isRequired,
};
