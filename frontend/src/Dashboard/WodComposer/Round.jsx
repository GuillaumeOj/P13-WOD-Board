import PropTypes from 'prop-types';
import React from 'react';

import { useInput } from '../../Utils';

export default function Round(props) {
  const { position, removeRound } = props;

  const [repetition, setRepetition] = useInput(0);
  const [duration, setDuration] = useInput('');

  return (
    <div>
      <div className="lead">
        <p>{`Round number ${position}`}</p>
        <button className="button warning" type="button" onClick={() => removeRound({ position })}>X</button>
      </div>
      <div className="group border">
        <div className="field">
          <label htmlFor={`repetitionRound-${position}`}>Repetition:&nbsp;</label>
          <input type="number" id={`repetitionRound-${position}`} name={`repetitionRound-${position}`} value={repetition} onChange={setRepetition} min="0" />
        </div>
        <div className="field">
          <label htmlFor={`durationRound-${position}`}>Duration:&nbsp;</label>
          <input type="time" id={`durationRound-${position}`} name={`durationRound-${position}`} value={duration} onChange={setDuration} />
        </div>
      </div>
    </div>
  );
}
Round.propTypes = {
  position: PropTypes.number.isRequired,
  removeRound: PropTypes.func.isRequired,
};
