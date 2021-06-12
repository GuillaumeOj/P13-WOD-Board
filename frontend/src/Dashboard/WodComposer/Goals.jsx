import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';

import { useApi } from '../../Api';

import { useAuth } from '../../Auth';

import Goal from './Goal';

export default function Goals({ roundId }) {
  const { user } = useAuth();
  const { api } = useApi();

  const [goals, setGoals] = useState([]);

  const getGoals = async () => {
    const response = await api({
      method: 'get', url: `/api/goal/goals/${roundId}`, silent: true, user,
    });

    if (response) {
      setGoals(response.map((goal) => ({ ...goal, uuid: uuidv4() })));
    }
  };

  const removeGoal = async (uuid) => {
    const updatedGoals = [...goals];
    const goalToDelete = updatedGoals.find((goal) => goal.uuid === uuid);

    updatedGoals.splice(updatedGoals.findIndex((goal) => goal.uuid === uuid), 1);

    if (goalToDelete && goalToDelete.id) {
      if (user) {
        const response = await api({
          method: 'delete', url: `/api/goal/${goalToDelete.id}`, silent: true, user,
        });

        if (response) {
          setGoals(updatedGoals);
        }
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

  const updateGoal = async (goal) => {
    if (user && goal.uuid && goal.movementId && roundId) {
      const updatedGoals = [...goals];
      const data = {
        movementId: goal.movementId,
        roundId,
        repetition: goal.repetition,
        durationSeconds: goal.durationSeconds,
      };

      if (goal.id) {
        const response = await api({
          method: 'put', url: `/api/goal/${goal.id}`, data, silent: true, user,
        });

        if (response) {
          setGoals(updatedGoals.map((item) => {
            if (item.uuid === goal.uuid) {
              return { ...response, uuid: goal.uuid };
            }
            return item;
          }));
        }
      } else {
        const response = await api({
          method: 'post', url: '/api/goal', data, silent: true, user,
        });

        if (response) {
          setGoals(updatedGoals.map((item) => {
            if (item.uuid === goal.uuid) {
              return { ...response, uuid: goal.uuid };
            }
            return item;
          }));
        }
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
