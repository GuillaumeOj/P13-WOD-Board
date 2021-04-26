import PropTypes from 'prop-types';
import React, { useEffect } from 'react';

import { RoundPropType } from '../../Type';
import { useInput } from '../../Utils';

export default function Round({ round, removeRound, updateRound }) {
  const { position, id } = round;

  const [repetition, setRepetition] = useInput(round.repetition);
  const [durationMinutes, setDurationMinutes] = useInput(round.durationMinutes);
  const [durationSeconds, setDurationSeconds] = useInput(round.durationSeconds);

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
      </div>
    )
  );
}
Round.propTypes = {
  round: RoundPropType.isRequired,
  removeRound: PropTypes.func.isRequired,
  updateRound: PropTypes.func.isRequired,
};
