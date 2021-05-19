import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { GoalPropType } from '../../Type';
import { MinutesSecondsToSeconds, SecondsToMinutesSeconds } from '../../Utils';

import Movement from './Movement';

export default function Goal({
  index, goal, removeGoal, updateGoal,
}) {
  const { id } = goal;

  const [movementId, setMovementId] = useState();
  const [repetition, setRepetition] = useState(0);
  const [displayMinutes, setDisplayMinutes] = useState(0);
  const [displaySeconds, setDisplaySeconds] = useState(0);

  const updateMovement = (value) => {
    if (value) {
      setMovementId(value);
    }
  };

  useEffect(() => {
    if (goal.movementId) { setRepetition(goal.movementId); }
    if (goal.repetition) { setRepetition(goal.repetition); }
    if (goal.durationSeconds) {
      const { minutes, seconds } = SecondsToMinutesSeconds(goal.durationSeconds);
      if (minutes !== displayMinutes) { setDisplayMinutes(minutes); }
      if (seconds !== displaySeconds) { setDisplaySeconds(seconds); }
    }
  }, [goal]);

  useEffect(() => {
    const { seconds } = MinutesSecondsToSeconds(displayMinutes, displaySeconds);
    updateGoal({
      id,
      movementId,
      repetition,
      durationSeconds: seconds,
    });
  }, [movementId, repetition, displayMinutes, displaySeconds]);

  return (
    goal && (
      <>
        <hr className="divider" />
        <div className="goal">
          <Movement
            index={index}
            movementId={movementId}
            updateMovement={updateMovement}
            removeGoal={removeGoal}
          />
          <div className="group">
            <div className="field">
              <label htmlFor={`repetitionGoal-${index}`}>Repetition:&nbsp;</label>
              <input
                type="number"
                id={`repetitionGoal-${index}`}
                name={`repetitionGoal-${index}`}
                value={repetition}
                onChange={(event) => setRepetition(parseInt(event.target.value, 10))}
                min="0"
              />
            </div>
            <div className="field">
              <label htmlFor={`minutesGoal-${index}`}>Minutes:&nbsp;</label>
              <input
                type="number"
                id={`minutesGoal-${index}`}
                name={`minutesGoal-${index}`}
                value={displayMinutes}
                onChange={(event) => setDisplayMinutes(parseInt(event.target.value, 10))}
                min="0"
              />
            </div>
            <div className="field">
              <label htmlFor={`secondsGoal-${index}`}>Seconds:&nbsp;</label>
              <input
                type="number"
                id={`secondsGoal-${index}`}
                name={`secondsGoal-${index}`}
                value={displaySeconds}
                onChange={(event) => setDisplaySeconds(parseInt(event.target.value, 10))}
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
  index: PropTypes.number.isRequired,
  goal: GoalPropType.isRequired,
  removeGoal: PropTypes.func.isRequired,
  updateGoal: PropTypes.func.isRequired,
};
