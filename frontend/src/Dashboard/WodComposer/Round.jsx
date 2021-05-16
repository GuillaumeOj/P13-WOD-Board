import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { RoundPropType } from '../../Type';
import { MinutesSecondsToSeconds, SecondsToMinutesSeconds } from '../../Utils';

import Goals from './Goals';

export default function Round({ round, removeRound, updateRound }) {
  const {
    uuid, position, wodId,
  } = round;

  const [id, setId] = useState();
  const [durationSeconds, setDurationSeconds] = useState(0);
  const [repetition, setRepetition] = useState(0);

  const [displayMinutes, setDisplayMinutes] = useState(0);
  const [displaySeconds, setDisplaySeconds] = useState(0);

  useEffect(() => {
    if (round.id) { setId(round.id); }
    if (round.repetition) { setRepetition(round.repetition); }
    if (round.durationSeconds) {
      const { minutes, seconds } = SecondsToMinutesSeconds(round.durationSeconds);
      if (minutes !== displayMinutes) { setDisplayMinutes(minutes); }
      if (seconds !== displaySeconds) { setDisplaySeconds(seconds); }
    }
  }, [round]);

  useEffect(() => {
    const { seconds } = MinutesSecondsToSeconds(displayMinutes, displaySeconds);
    if (seconds !== durationSeconds) { setDurationSeconds(seconds); }
  }, [displayMinutes, displaySeconds]);

  useEffect(() => {
    if (position && wodId) {
      updateRound({
        uuid,
        id,
        durationSeconds,
        repetition,
      });
    }
  }, [id, repetition, durationSeconds]);

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
