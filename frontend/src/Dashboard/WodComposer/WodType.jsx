import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

export default function WodType({ wodTypeId, setWodTypeId }) {
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
        .then((response) => setWodTypes(response.data));
    } else { setWodTypes([]); }
  };

  const selectWodType = (itemId, itemName) => {
    setId(itemId);
    setName(itemName);
    setWodTypes([]);
  };

  useEffect(() => { if (wodTypeId !== id) { setId(wodTypeId); } }, [wodTypeId]);

  useEffect(() => {
    if (id) {
      axios
        .get(`/api/type/${id}`)
        .then((response) => { setName(response.data.name); setId(id); setWodTypeId(id); });
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
