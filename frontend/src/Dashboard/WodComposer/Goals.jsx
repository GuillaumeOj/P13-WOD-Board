import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { useAuth } from '../../Auth';

import Goal from './Goal';

export default function Goals({ roundId }) {
  const { user } = useAuth();

  const [goals, setGoals] = useState([]);

  const getGoals = () => {
    axios
      .get(`/api/goal/goals/${roundId}`)
      .then((response) => {
        if (response.data) {
          setGoals(response.data);
        }
      });
  };

  const removeGoal = (index) => {
    const updatedGoals = [...goals];
    const itemToDelete = updatedGoals[index];

    if (itemToDelete.id) {
      if (user) {
        const config = { headers: { Authorization: `${user.token_type} ${user.access_token}` } };
        axios
          .delete(`/api/goal/${itemToDelete.id}`, config)
          .then(() => getGoals());
      }
    } else {
      updatedGoals.splice(index, 1);
      setGoals(updatedGoals);
    }
  };

  const addGoal = () => {
    if (roundId && user) {
      const updatedGoals = [...goals];
      updatedGoals.push({
        roundId,
        repetition: 0,
        durationSeconds: 0,
      });
      setGoals(updatedGoals);
    }
  };

  const updateGoal = (goal) => {
    if (user) {
      const config = { headers: { Authorization: `${user.token_type} ${user.access_token}` } };
      const payload = {
        movementId: goal.movementId,
        roundId,
        repetition: goal.repetition,
        durationSeconds: goal.durationSeconds,
      };
      if (goal.id && goal.movementId) {
        axios
          .put(`/api/goal/${goal.id}`, payload, config)
          .then(() => getGoals());
      } else if (!goal.id && goal.movementId) {
        axios
          .post('/api/goal/', payload, config)
          .then(() => getGoals());
      }
    }
  };

  useEffect(() => {
    if (roundId) {
      getGoals();
    }
  }, []);

  useEffect(() => {
    if (roundId) {
      if (goals) {
        const updatedGoals = [...goals];
        setGoals(updatedGoals.map((goal) => ({ ...goal, roundId })));
      } else {
        getGoals();
      }
    }
  }, [roundId]);

  return (
    <>
      <button className="button primary" type="button" onClick={addGoal}>
        Movement +
      </button>
      <div className="goals">
        {goals
            && goals.map((goal, index) => (
              <Goal
                key={`goal-${index.toString()}`}
                index={index}
                goal={goal}
                removeGoal={removeGoal}
                updateGoal={updateGoal}
              />
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
