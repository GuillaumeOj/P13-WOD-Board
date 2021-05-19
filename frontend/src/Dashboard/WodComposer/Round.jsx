import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { RoundPropType } from '../../Type';
import { MinutesSecondsToSeconds, SecondsToMinutesSeconds } from '../../Utils';

import Goals from './Goals';

export default function Round({ round, removeRound, updateRound }) {
  const { id, position, wodId } = round;

  const [repetition, setRepetition] = useState(0);
  const [displayMinutes, setDisplayMinutes] = useState(0);
  const [displaySeconds, setDisplaySeconds] = useState(0);

  useEffect(() => {
    if (round.repetition) { setRepetition(round.repetition); }
    if (round.durationSeconds) {
      const { minutes, seconds } = SecondsToMinutesSeconds(round.durationSeconds);
      if (minutes !== displayMinutes) { setDisplayMinutes(minutes); }
      if (seconds !== displaySeconds) { setDisplaySeconds(seconds); }
    }
  }, [round]);

  useEffect(() => {
    if (id) {
      const { seconds } = MinutesSecondsToSeconds(displayMinutes, displaySeconds);
      updateRound({
        id,
        position,
        durationSeconds: seconds,
        repetition,
        wodId,
      });
    }
  }, [id, repetition, displayMinutes, displaySeconds, wodId]);

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
            <label htmlFor={`repetition-${position}`}>Repetition:&nbsp;</label>
            <input
              type="number"
              id={`repetition-${position}`}
              name={`repetition-${position}`}
              value={repetition}
              onChange={(event) => setRepetition(parseInt(event.target.value, 10))}
              min="0"
            />
          </div>
          <div className="field">
            <label htmlFor={`displayMinutes-${position}`}>Minutes:&nbsp;</label>
            <input
              type="number"
              id={`displayMinutes-${position}`}
              name={`displayMinutes-${position}`}
              value={displayMinutes}
              onChange={(event) => setDisplayMinutes(parseInt(event.target.value, 10))}
              min="0"
            />
          </div>
          <div className="field">
            <label htmlFor={`displaySeconds-${position}`}>Seconds:&nbsp;</label>
            <input
              type="number"
              id={`displaySeconds-${position}`}
              name={`displaySeconds-${position}`}
              value={displaySeconds}
              onChange={(event) => setDisplaySeconds(parseInt(event.target.value, 10))}
              min="0"
            />
          </div>
        </div>
        <Goals roundId={id} />
      </div>
    )
  );
}
Round.propTypes = {
  round: RoundPropType.isRequired,
  removeRound: PropTypes.func.isRequired,
  updateRound: PropTypes.func.isRequired,
};
