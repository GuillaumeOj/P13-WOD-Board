import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { v4 as uuidV4 } from 'uuid';

import Round from './Round';

export default function Rounds({ wodId }) {
  const [rounds, setRounds] = useState();

  const removeRound = (uuid) => {
    const updatedRounds = rounds.filter((item) => item.uuid !== uuid);

    setRounds(updatedRounds.map((item, index) => ({ ...item, position: index + 1 })));
  };

  const addRound = () => {
    const newRounds = [...rounds];
    const position = newRounds.length + 1;

    newRounds.push({
      uuid: uuidV4(),
      position,
      wodId,
    });

    setRounds(newRounds);
  };

  const updateRound = (round) => {
    const updatedRounds = [...rounds];

    if (round) {
      setRounds(
        updatedRounds.map((item) => {
          if (item.uuid === round.uuid) {
            return {
              ...item,
              id: round.id,
              durationSeconds: round.durationSeconds,
              repetition: round.repetition,
            };
          }
          return item;
        }),
      );
    }
  };

  useEffect(() => {
    if (wodId) {
      if (rounds) {
        const updatedRounds = [...rounds];
        setRounds(updatedRounds.map((round) => ({ ...round, wodId })));
      } else {
        axios
          .get(`/api/round/rounds/${wodId}`)
          .then((response) => setRounds(response.data));
      }
    }
  }, [wodId]);

  return (
    <div className="rounds">
      <button
        className="button primary"
        type="button"
        onClick={addRound}
        disabled={!wodId}
        title={(!wodId) ? 'Add a title first' : 'Add a new round'}
      >
        Round +
      </button>
      {rounds
        && rounds.map(
          (round) => round && (
          <Round
            key={round.uuid}
            round={round}
            removeRound={removeRound}
            updateRound={updateRound}
          />
          ),
        )}
    </div>
  );
}
Rounds.propTypes = {
  wodId: PropTypes.number,
};
Rounds.defaultProps = {
  wodId: null,
};
