import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';

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
          setGoals(response.data.map((goal) => ({ ...goal, uuid: uuidv4() })));
        }
      });
  };

  const removeGoal = (uuid) => {
    const updatedGoals = [...goals];
    const goalToDelete = updatedGoals.find((goal) => goal.uuid === uuid);

    updatedGoals.splice(updatedGoals.findIndex((goal) => goal.uuid === uuid), 1);

    if (goalToDelete && goalToDelete.id) {
      if (user) {
        const config = { headers: { Authorization: `${user.token_type} ${user.access_token}` } };
        axios
          .delete(`/api/goal/${goalToDelete.id}`, config)
          .then(() => {
            setGoals(updatedGoals);
          });
      }
    } else {
      setGoals(updatedGoals);
    }
  };

  const addGoal = () => {
    if (roundId && user) {
      const updatedGoals = [...goals];
      updatedGoals.push({
        uuid: uuidv4(),
        id: null,
        roundId,
        repetition: 0,
        durationSeconds: 0,
      });
      setGoals(updatedGoals);
    }
  };

  const updateGoal = (goal) => {
    if (user && goal.uuid && goal.movementId && roundId) {
      const updatedGoals = [...goals];
      const config = { headers: { Authorization: `${user.token_type} ${user.access_token}` } };
      const payload = {
        movementId: goal.movementId,
        roundId,
        repetition: goal.repetition,
        durationSeconds: goal.durationSeconds,
      };

      if (goal.id) {
        axios
          .put(`/api/goal/${goal.id}`, payload, config)
          .then((response) => {
            setGoals(updatedGoals.map((item) => {
              if (item.uuid === goal.uuid) {
                return { ...response.data, uuid: goal.uuid };
              }
              return item;
            }));
          });
      } else {
        axios
          .post('/api/goal/', payload, config)
          .then((response) => {
            setGoals(updatedGoals.map((item) => {
              if (item.uuid === goal.uuid) {
                return { ...response.data, uuid: goal.uuid };
              }
              return item;
            }));
          });
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
            && goals.map((goal) => (
              goal.uuid && (
              <Goal
                key={goal.uuid}
                goal={goal}
                removeGoal={removeGoal}
                updateGoal={updateGoal}
              />
              )
            ))}
      </div>
    </>
  );
}
Goals.propTypes = {
  roundId: PropTypes.number.isRequired,
};
