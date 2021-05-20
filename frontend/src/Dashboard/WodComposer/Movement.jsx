import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

export default function Movement({
  uuid, movementId, removeGoal, setMovementId,
}) {
  const [id, setId] = useState();
  const [name, setName] = useState();

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

  const selectMovement = (itemId) => {
    setMovements([]);
    setMovementId(itemId);
  };

  useEffect(() => {
    if (movementId && movementId !== id) {
      axios
        .get(`/api/movement/${movementId}`)
        .then((response) => {
          if (response.data.name !== name) { setName(response.data.name); }
          setId(movementId);
        });
    }
  }, [movementId]);

  return uuid && (
    <div className="field movement">
      <label htmlFor={`movementName-${uuid}`}>Name*:&nbsp;</label>
      <div className="movementInput">
        <input
          name={`movementName-${uuid}`}
          id={`movementName-${uuid}`}
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
                key={`movements-${item.name}`}
                value={item.name}
                onClick={() => selectMovement(item.id)}
              >
                {item.name}
              </button>
            ))}
          </div>
          )}
        </div>
      </div>
      <button className="button warning" type="button" onClick={() => removeGoal(uuid)}>
        X
      </button>
    </div>
  );
}

Movement.propTypes = {
  uuid: PropTypes.string.isRequired,
  movementId: PropTypes.number,
  removeGoal: PropTypes.func.isRequired,
  setMovementId: PropTypes.func.isRequired,
};

Movement.defaultProps = {
  movementId: null,
};
