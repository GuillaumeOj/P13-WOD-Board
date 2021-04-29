import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { v4 as uuidV4 } from 'uuid';

import { RoundPropType } from '../../Type';
import { useInput } from '../../Utils';

import Goal from './Goal';

export default function Round({ round, removeRound, updateRound }) {
  const { position, uuid, id } = round;

  const [repetition, setRepetition] = useInput(round.repetition);
  const [durationMinutes, setDurationMinutes] = useInput(round.durationMinutes);
  const [durationSeconds, setDurationSeconds] = useInput(round.durationSeconds);

  const [goals, setGoals] = useState([]);

  const removeGoal = (goalUuid) => {
    const updatedGoals = goals.filter((goal) => goal.uuid !== goalUuid);
    setGoals(updatedGoals);
  };

  const addGoal = () => {
    const updatedGoals = [...goals];
    updatedGoals.push({
      uuid: uuidV4(),
      id: 0,
      movementId: null,
      movement: null,
      roundId: null,
      name: '',
      equipments: null,
      repetition: 0,
      durationMinutes: 0,
      durationSeconds: 0,
    });

    setGoals(updatedGoals);
  };

  const updatedGoal = (goal) => {
    const updatedGoals = [...goals];

    if (goal) {
      setGoals(
        updatedGoals.map((item) => {
          if (item.uuid === goal.uuid) {
            return {
              ...item,
              name: goal.name,
              movementId: goal.movementId,
              repetition: goal.repetition,
              durationMinutes: goal.durationMinutes,
              durationSeconds: goal.durationSeconds,
            };
          }
          return item;
        }),
      );
    }
  };

  useEffect(() => {
    updateRound({
      uuid,
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
          <button className="button warning" type="button" onClick={() => removeRound(uuid)}>
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
        <button className="button primary" type="button" onClick={addGoal}>
          Movement +
        </button>
        <div className="movements">
          {goals
            && goals.map((goal) => (
              <Goal key={goal.uuid} goal={goal} removeGoal={removeGoal} updateGoal={updatedGoal} />
            ))}
        </div>
      </div>
    )
  );
}
Round.propTypes = {
  round: RoundPropType.isRequired,
  removeRound: PropTypes.func.isRequired,
  updateRound: PropTypes.func.isRequired,
};
