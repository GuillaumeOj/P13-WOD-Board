import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { useApi } from '../../Api';
import { useAuth } from '../../Auth';

export default function WodType({ wodTypeId, setWodTypeId }) {
  const { user } = useAuth();
  const { api } = useApi();

  const [id, setId] = useState();
  const [name, setName] = useState('');

  const [wodTypes, setWodTypes] = useState([]);

  const searchWodTypes = async (event) => {
    const currentValue = event.target.value;
    setId();
    setName(currentValue);
    if (currentValue) {
      const response = await api({
        method: 'get', url: `/api/type/list/${currentValue}`, silent: true, user,

      });
      if (response) {
        setWodTypes(response);
      }
    } else { setWodTypes([]); }
  };

  const selectWodType = (itemId, itemName) => {
    setId(itemId);
    setName(itemName);
    setWodTypes([]);
  };

  useEffect(() => { if (wodTypeId !== id) { setId(wodTypeId); } }, [wodTypeId]);

  useEffect(async () => {
    if (id) {
      const response = await api({
        method: 'get', url: `/api/type/${id}`, silent: true, user,
      });
      if (response) {
        setName(response.name); setId(id); setWodTypeId(id);
      }
    }
  }, [id]);

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
  wodTypeId: PropTypes.number,
};
WodType.defaultProps = {
  wodTypeId: null,
};
