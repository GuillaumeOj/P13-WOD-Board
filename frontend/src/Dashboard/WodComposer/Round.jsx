import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { useAuth } from '../../Auth';
import { RoundPropType } from '../../Type';
import { MinutesSecondsToSeconds, SecondsToMinutesSeconds } from '../../Utils';

import Goals from './Goals';

export default function Round({ round, removeRound, updateRound }) {
  const { user } = useAuth();

  const { uuid, position, wodId } = round;

  const [id, setId] = useState();
  const [durationSeconds, setDurationSeconds] = useState(0);
  const [repetition, setRepetition] = useState(0);

  const [displayMinutes, setDisplayMinutes] = useState(0);
  const [displaySeconds, setDisplaySeconds] = useState(0);

  useEffect(() => {
    const { minutes, seconds } = SecondsToMinutesSeconds(durationSeconds);

    if (minutes !== displayMinutes) { setDisplayMinutes(minutes); }
    if (seconds !== displaySeconds) { setDisplaySeconds(seconds); }
  }, [durationSeconds]);

  useEffect(() => {
    const intMinutes = parseInt(displayMinutes, 10);
    const intSeconds = parseInt(displaySeconds, 10);
    const { seconds } = MinutesSecondsToSeconds(intMinutes, intSeconds);

    if (seconds !== durationSeconds) { setDurationSeconds(seconds); }
  }, [displayMinutes, displaySeconds]);

  useEffect(() => {
    updateRound({
      uuid,
      id,
      durationSeconds,
      repetition,
    });
  }, [id, repetition, durationSeconds]);

  useEffect(() => {
    if (position && wodId && user) {
      const config = { headers: { Authorization: `${user.token_type} ${user.access_token}` } };
      const data = {
        position, durationSeconds, repetition, wodId,
      };
      if (!id) {
        axios
          .post('/api/round/', data, config)
          .then((response) => setId(response.data.id));
      } else {
        axios
          .put(`/api/round/${id}`, data, config);
      }
    }
  }, [round]);

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
