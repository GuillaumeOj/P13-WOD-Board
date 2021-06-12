import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { useApi } from '../../Api';
import { useAuth } from '../../Auth';

export default function Movement({
  uuid, movementId, removeGoal, setMovementId,
}) {
  const { api } = useApi();
  const { user } = useAuth();

  const [id, setId] = useState();
  const [name, setName] = useState();

  const [movements, setMovements] = useState([]);

  const searchMovements = async (event) => {
    const currentValue = event.target.value;
    if (currentValue) {
      const response = await api({
        method: 'get', url: `/api/movement/movements/${currentValue}`, silent: true, user,
      });
      if (response) {
        setMovements(response);
        setName(currentValue);
      }
    } else { setMovements([]); }
  };

  const selectMovement = (itemId) => {
    setMovements([]);
    setMovementId(itemId);
  };

  useEffect(async () => {
    if (movementId && movementId !== id) {
      const response = await api({
        method: 'get', url: `/api/movement/${movementId}`, silent: true, user,
      });
      if (response) {
        if (response.name !== name) { setName(response.name); }
        setId(movementId);
      }
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
