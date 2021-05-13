import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { v4 as uuidV4 } from 'uuid';

import Goal from './Goal';

export default function Goals({ roundId }) {
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
      roundId,
      name: '',
      equipments: null,
      repetition: 0,
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
    const updatedGoals = [...goals];
    setGoals(updatedGoals.map((item) => ({ ...item, roundId })));
  }, [roundId]);

  return (
    <>
      <button className="button primary" type="button" onClick={addGoal}>
        Movement +
      </button>
      <div className="movements">
        {goals
            && goals.map((goal) => (
              <Goal key={goal.uuid} goal={goal} removeGoal={removeGoal} updateGoal={updatedGoal} />
            ))}
      </div>
    </>
  );
}
Goals.propTypes = {
  roundId: PropTypes.number,
};
Goals.defaultProps = {
  roundId: -1,
};
