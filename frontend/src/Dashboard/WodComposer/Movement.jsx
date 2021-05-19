import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

export default function Movement({
  index, movementId, removeGoal, updateMovement,
}) {
  const [id, setId] = useState(movementId);
  const [name, setName] = useState('');

  const [movements, setMovements] = useState([]);

  const searchMovements = (event) => {
    const currentValue = event.target.value;
    if (currentValue) {
      axios
        .get(`/api/movement/movements/${currentValue}`)
        .then((response) => {
          setMovements(response.data);
          setName(currentValue);
        });
    } else { setMovements([]); }
  };

  const selectMovement = (itemId, itemName) => {
    setId(itemId);
    setName(itemName);
    setMovements([]);
  };

  useEffect(() => { updateMovement(id); }, [id]);
  useEffect(() => { if (movementId !== id) { setId(movementId); } }, [movementId]);

  useEffect(() => {
    if (id) {
      axios
        .get(`/api/movement/${id}`)
        .then((response) => { setName(response.data.name); setId(response.data.id); });
    }
  }, [id]);

  return (
    <div className="field movement">
      <label htmlFor={`movementName-${index}`}>Name*:&nbsp;</label>
      <div className="movementInput">
        <input
          name={`movementName-${index}`}
          id={`movementName-${index}`}
          value={name}
          onChange={searchMovements}
          required
          placeholder="Burpees, Sit Up, etc."
        />
        <div className="completion">
          {movements && (
          <div className="types">
            {movements.map((item) => (
              <button
                className="button type"
                type="button"
                key={`movements-${item.id}`}
                value={item.name}
                onClick={() => selectMovement(item.id, item.name)}
              >
                {item.name}
              </button>
            ))}
          </div>
          )}
        </div>
      </div>
      <button className="button warning" type="button" onClick={() => removeGoal(index)}>
        X
      </button>
    </div>
  );
}

Movement.propTypes = {
  index: PropTypes.number.isRequired,
  movementId: PropTypes.number,
  removeGoal: PropTypes.func.isRequired,
  updateMovement: PropTypes.func.isRequired,
};

Movement.defaultProps = {
  movementId: null,
};
