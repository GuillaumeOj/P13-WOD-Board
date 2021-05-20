import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { GoalPropType } from '../../Type';
import { MinutesSecondsToSeconds, SecondsToMinutesSeconds } from '../../Utils';

import Movement from './Movement';

export default function Goal({
  goal, removeGoal, updateGoal,
}) {
  const { uuid } = goal;

  const [id, setId] = useState(goal.id);
  const [movementId, setMovementId] = useState(goal.movementId);
  const [repetition, setRepetition] = useState(goal.repetition);
  const [displayMinutes, setDisplayMinutes] = useState(0);
  const [displaySeconds, setDisplaySeconds] = useState(0);

  useEffect(() => {
    if (goal.id && goal.id !== id) {
      setId(goal.id);
    }
    if (goal.durationSeconds) {
      const { minutes, seconds } = SecondsToMinutesSeconds(goal.durationSeconds);
      if (minutes !== displayMinutes) { setDisplayMinutes(minutes); }
      if (seconds !== displaySeconds) { setDisplaySeconds(seconds); }
    }
  }, [goal]);

  useEffect(() => {
    const { seconds } = MinutesSecondsToSeconds(displayMinutes, displaySeconds);
    if (uuid && movementId) {
      updateGoal({
        uuid,
        id,
        movementId,
        repetition,
        durationSeconds: seconds,
      });
    }
  }, [movementId, repetition, displayMinutes, displaySeconds]);

  return (
    goal && (
      <>
        <hr className="divider" />
        <div className="goal">
          <Movement
            uuid={uuid}
            movementId={movementId}
            setMovementId={setMovementId}
            removeGoal={removeGoal}
          />
          <div className="group">
            <div className="field">
              <label htmlFor={`repetitionGoal-${uuid}`}>Repetition:&nbsp;</label>
              <input
                type="number"
                id={`repetitionGoal-${uuid}`}
                name={`repetitionGoal-${uuid}`}
                value={repetition}
                onChange={(event) => setRepetition(parseInt(event.target.value, 10))}
                min="0"
              />
            </div>
            <div className="field">
              <label htmlFor={`minutesGoal-${uuid}`}>Minutes:&nbsp;</label>
              <input
                type="number"
                id={`minutesGoal-${uuid}`}
                name={`minutesGoal-${uuid}`}
                value={displayMinutes}
                onChange={(event) => setDisplayMinutes(parseInt(event.target.value, 10))}
                min="0"
              />
            </div>
            <div className="field">
              <label htmlFor={`secondsGoal-${uuid}`}>Seconds:&nbsp;</label>
              <input
                type="number"
                id={`secondsGoal-${uuid}`}
                name={`secondsGoal-${uuid}`}
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
  goal: GoalPropType.isRequired,
  removeGoal: PropTypes.func.isRequired,
  updateGoal: PropTypes.func.isRequired,
};
