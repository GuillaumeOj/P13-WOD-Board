import React, { useEffect, useState } from 'react';

import { v4 as uuidV4 } from 'uuid';

import { WodPropType } from '../../Type';

import Round from './Round';

export default function Rounds({ wod }) {
  const [rounds, setRounds] = useState([]);

  const removeRound = (uuid) => {
    const updatedRounds = rounds.filter((item) => item.uuid !== uuid);

    setRounds(updatedRounds.map((item, index) => ({ ...item, position: index + 1 })));
  };

  const addRound = () => {
    const newRounds = [...rounds];
    const position = newRounds.length + 1;

    newRounds.push({
      uuid: uuidV4(),
      id: 0,
      position,
      repetition: 0,
      durationMinutes: 0,
      durationSeconds: 0,
      wodId: wod.id,
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
              repetition: round.repetition,
              durationMinutes: round.durationMinutes,
              durationSeconds: round.durationSeconds,
            };
          }
          return item;
        }),
      );
    }
  };

  useEffect(() => {
    const updatedRounds = [...rounds];
    setRounds(updatedRounds.map((item) => ({ ...item, wodId: wod.id })));
  }, [wod]);

  return (
    <div className="rounds">
      <button className="button primary" type="button" onClick={addRound}>
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
  wod: WodPropType.isRequired,
};
