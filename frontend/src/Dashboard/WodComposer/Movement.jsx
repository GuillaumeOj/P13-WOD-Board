import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { useAlert } from '../../Alert';
import { MovementPropType } from '../../Type';
import { useInput } from '../../Utils';

export default function Movement({ movement, removeMovement, updateMovement }) {
  const { id } = movement;

  const { addAlert } = useAlert();

  const [movementId, setMovementId] = useState(movement.movementId);
  const [name, setName] = useState(movement.name);
  const [repetition, setRepetition] = useInput(movement.repetition);
  const [durationMinutes, setDurationMinutes] = useInput(movement.durationMinutes);
  const [durationSeconds, setDurationSeconds] = useInput(movement.durationSeconds);

  const [movements, setMovements] = useState([]);

  useEffect(() => {
    updateMovement({
      id,
      movementId: parseInt(movementId, 10),
      name,
      repetition: parseInt(repetition, 10),
      durationMinutes: parseInt(durationMinutes, 10),
      durationSeconds: parseInt(durationSeconds, 10),
    });
  }, [movementId, name, repetition, durationMinutes, durationSeconds]);

  const searchMovement = async (movementName) => {
    axios
      .get(`/api/movement/${movementName}`)
      .then((response) => setMovements(response.data))
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
  };

  const selectMovement = async (event) => {
    const movementName = event.target.value;
    if (movementName) {
      await searchMovement(movementName);
      setName(movementName);
    } else {
      setMovements([]);
      setName('');
    }
  };

  return (
    movement && (
      <div className="movement">
        <div className="lead field">
          <label htmlFor={`movementName-${id}`}>Name:&nbsp;</label>
          <div className="input">
            <input
              type="text"
              id={`movementName-${id}`}
              name={`movementName-${id}`}
              value={name}
              onChange={selectMovement}
            />
            <div className="completion">
              {movements && (
                <div className="types">
                  {movements.map((item) => (
                    <button
                      className="button type"
                      type="button"
                      key={item.id}
                      value={item.name}
                      onClick={() => {
                        setMovementId(item.movement_id);
                        setName(item.name);
                        setMovements([]);
                      }}
                    >
                      {item.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
          <button className="button warning" type="button" onClick={() => removeMovement(id)}>
            X
          </button>
        </div>
        <div className="group">
          <div className="field">
            <label htmlFor={`repetitionMovement-${id}`}>Repetition:&nbsp;</label>
            <input
              type="number"
              id={`repetitionMovement-${id}`}
              name={`repetitionMovement-${id}`}
              value={repetition}
              onChange={setRepetition}
              min="0"
            />
          </div>
          <div className="field">
            <label htmlFor={`durationMinutes-${id}`}>Minutes:&nbsp;</label>
            <input
              type="number"
              id={`durationMinutes-${id}`}
              name={`durationMinutes-${id}`}
              value={durationMinutes}
              onChange={setDurationMinutes}
              min="0"
            />
          </div>
          <div className="field">
            <label htmlFor={`durationSeconds-${id}`}>Seconds:&nbsp;</label>
            <input
              type="number"
              id={`durationSeconds-${id}`}
              name={`durationSeconds-${id}`}
              value={durationSeconds}
              onChange={setDurationSeconds}
              min="0"
            />
          </div>
        </div>
      </div>
    )
  );
}
Movement.propTypes = {
  movement: MovementPropType.isRequired,
  removeMovement: PropTypes.func.isRequired,
  updateMovement: PropTypes.func.isRequired,
};
