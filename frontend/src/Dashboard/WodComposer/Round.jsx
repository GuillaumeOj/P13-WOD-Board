import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { RoundPropType } from '../../Type';
import { MinutesSecondsToSeconds, SecondsToMinutesSeconds } from '../../Utils';

import Goals from './Goals';

export default function Round({ round, removeRound, updateRound }) {
  const { uuid } = round;

  const [id, setId] = useState(round.id);
  const [position, setPosition] = useState(round.position);
  const [durationSeconds, setDurationSeconds] = useState(round.durationSeconds);
  const [repetition, setRepetition] = useState(round.repetition);
  const [wodId, setWodId] = useState(round.wodId);

  const [displayMinutes, setDisplayMinutes] = useState();
  const [displaySeconds, setDisplaySeconds] = useState();

  useEffect(() => {
    if (round.id !== id) { setId(round.id); }
    if (round.position !== position) { setPosition(round.position); }
    if (round.durationSeconds !== durationSeconds) { setDurationSeconds(round.durationSeconds); }
    if (round.repetition !== repetition) { setRepetition(round.repetition); }
    if (round.wodId !== wodId) { setWodId(round.wodId); }
  }, [round]);

  useEffect(() => {
    const { minutes, seconds } = SecondsToMinutesSeconds(durationSeconds);

    if (minutes !== displayMinutes) { setDisplayMinutes(minutes); }
    if (seconds !== displaySeconds) { setDisplaySeconds(seconds); }
  }, [durationSeconds]);

  useEffect(() => {
    const { seconds } = MinutesSecondsToSeconds(displayMinutes, displaySeconds);

    updateRound({
      uuid,
      id,
      position,
      durationSeconds: seconds,
      repetition,
      wodId,
    });
  }, [position, repetition, displayMinutes, displaySeconds]);

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
            <label htmlFor={`displayMinutes-${position}`}>Minutes:&nbsp;</label>
            <input
              type="number"
              id={`displayMinutes-${position}`}
              name={`displayMinutes-${position}`}
              value={displayMinutes}
              onChange={(event) => setDisplayMinutes(event.target.value)}
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
              onChange={(event) => setDisplaySeconds(event.target.value)}
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
