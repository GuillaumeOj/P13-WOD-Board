import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { useAlert } from '../../Alert';
import { GoalPropType } from '../../Type';
import { useInput } from '../../Utils';

export default function Goal({ goal, removeGoal, updateGoal }) {
  const { uuid, id } = goal;

  const { addAlert } = useAlert();

  const [movementId, setMovementId] = useState(goal.movementId);
  const [name, setName] = useState(goal.name);
  const [repetition, setRepetition] = useInput(goal.repetition);
  const [durationMinutes, setDurationMinutes] = useInput(goal.durationMinutes);
  const [durationSeconds, setDurationSeconds] = useInput(goal.durationSeconds);

  const [movements, setMovements] = useState([]);

  useEffect(() => {
    updateGoal({
      id,
      uuid,
      movementId: parseInt(movementId, 10),
      name,
      repetition: parseInt(repetition, 10),
      durationMinutes: parseInt(durationMinutes, 10),
      durationSeconds: parseInt(durationSeconds, 10),
    });
  }, [movementId, name, repetition, durationMinutes, durationSeconds]);

  const searchMovement = (movementName) => {
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
              message: 'Impossible to retrieve movements',
              alertType: 'error',
            });
          }
        }
      });
  };

  const selectMovement = (event) => {
    const movementName = event.target.value;
    if (movementName) {
      searchMovement(movementName);
      setName(movementName);
    } else {
      setMovements([]);
      setName('');
    }
  };

  return (
    goal && (
      <>
        <hr className="divider" />
        <div className="movement">
          <div className="lead field">
            <label htmlFor={`movementName-${uuid}`}>Name:&nbsp;</label>
            <div className="input">
              <input
                type="text"
                id={`movementName-${uuid}`}
                name={`movementName-${uuid}`}
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
            <button className="button warning" type="button" onClick={() => removeGoal(uuid)}>
              X
            </button>
          </div>
          <div className="group">
            <div className="field">
              <label htmlFor={`repetitionMovement-${uuid}`}>Repetition:&nbsp;</label>
              <input
                type="number"
                id={`repetitionMovement-${uuid}`}
                name={`repetitionMovement-${uuid}`}
                value={repetition}
                onChange={setRepetition}
                min="0"
              />
            </div>
            <div className="field">
              <label htmlFor={`durationMinutes-${uuid}`}>Minutes:&nbsp;</label>
              <input
                type="number"
                id={`durationMinutes-${uuid}`}
                name={`durationMinutes-${uuid}`}
                value={durationMinutes}
                onChange={setDurationMinutes}
                min="0"
              />
            </div>
            <div className="field">
              <label htmlFor={`durationSeconds-${uuid}`}>Seconds:&nbsp;</label>
              <input
                type="number"
                id={`durationSeconds-${uuid}`}
                name={`durationSeconds-${uuid}`}
                value={durationSeconds}
                onChange={setDurationSeconds}
                min="0"
              />
            </div>
          </div>
        </div>
      </>
    )
  );
}
Goal.propTypes = {
  goal: GoalPropType.isRequired,
  removeGoal: PropTypes.func.isRequired,
  updateGoal: PropTypes.func.isRequired,
};
