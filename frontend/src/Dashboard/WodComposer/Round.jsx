import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { v4 as uuidV4 } from 'uuid';

import { RoundPropType } from '../../Type';
import { useInput } from '../../Utils';

import Movement from './Movement';

export default function Round({ round, removeRound, updateRound }) {
  const { position, id } = round;

  const [repetition, setRepetition] = useInput(round.repetition);
  const [durationMinutes, setDurationMinutes] = useInput(round.durationMinutes);
  const [durationSeconds, setDurationSeconds] = useInput(round.durationSeconds);

  const [movements, setMovements] = useState([]);

  const removeMovement = (movementId) => {
    const updatedMovements = movements.filter((item) => item.id !== movementId);
    setMovements(updatedMovements);
  };

  const addMovement = () => {
    const newMovements = [...movements];
    newMovements.push({
      id: uuidV4(),
      movementId: null,
      roundId: null,
      name: '',
      repetition: 0,
      durationMinutes: 0,
      durationSeconds: 0,
    });

    setMovements(newMovements);
  };

  const updateMovement = (movement) => {
    const updatedMovements = [...movements];

    if (movement) {
      setMovements(
        updatedMovements.map((item) => {
          if (item.id === movement.id) {
            return {
              ...item,
              name: movement.name,
              movementId: movement.movementId,
              repetition: movement.repetition,
              durationMinutes: movement.durationMinutes,
              durationSeconds: movement.durationSeconds,
            };
          }
          return item;
        }),
      );
    }
  };

  useEffect(() => {
    updateRound({
      id,
      repetition: parseInt(repetition, 10),
      durationMinutes: parseInt(durationMinutes, 10),
      durationSeconds: parseInt(durationSeconds, 10),
    });
  }, [repetition, durationMinutes, durationSeconds]);

  return (
    round && (
      <div className="round">
        <div className="lead">
          <p>{`Round number ${position}`}</p>
          <button className="button warning" type="button" onClick={() => removeRound(id)}>
            X
          </button>
        </div>
        <div className="group">
          <div className="field">
            <label htmlFor={`repetitionRound-${position}`}>Repetition:&nbsp;</label>
            <input
              type="number"
              id={`repetition-${position}`}
              name={`repetition-${position}`}
              value={repetition}
              onChange={setRepetition}
              min="0"
            />
          </div>
          <div className="field">
            <label htmlFor={`durationMinutes-${position}`}>Minutes:&nbsp;</label>
            <input
              type="number"
              id={`durationMinutes-${position}`}
              name={`durationMinutes-${position}`}
              value={durationMinutes}
              onChange={setDurationMinutes}
              min="0"
            />
          </div>
          <div className="field">
            <label htmlFor={`durationSeconds-${position}`}>Seconds:&nbsp;</label>
            <input
              type="number"
              id={`durationSeconds-${position}`}
              name={`durationSeconds-${position}`}
              value={durationSeconds}
              onChange={setDurationSeconds}
              min="0"
            />
          </div>
        </div>
        <button className="button primary" type="button" onClick={addMovement}>
          Movement +
        </button>
        {movements
          && movements.map((movement) => (
            <Movement
              key={movement.id}
              movement={movement}
              removeMovement={removeMovement}
              updateMovement={updateMovement}
            />
          ))}
      </div>
    )
  );
}
Round.propTypes = {
  round: RoundPropType.isRequired,
  removeRound: PropTypes.func.isRequired,
  updateRound: PropTypes.func.isRequired,
};
