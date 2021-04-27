import React, { useState } from 'react';

import { v4 as uuidV4 } from 'uuid';

import Round from './Round';

export default function Rounds() {
  const [rounds, setRounds] = useState([]);

  const removeRound = (id) => {
    const updatedRounds = rounds.filter((item) => item.id !== id);

    setRounds(updatedRounds.map((item, index) => ({ ...item, position: index + 1 })));
  };

  const addRound = () => {
    const newRounds = [...rounds];
    const position = newRounds.length + 1;

    newRounds.push({
      id: uuidV4(),
      position,
      repetition: 0,
      durationMinutes: 0,
      durationSeconds: 0,
    });

    setRounds(newRounds);
  };

  const updateRound = (round) => {
    const updatedRounds = [...rounds];

    if (round) {
      setRounds(
        updatedRounds.map((item) => {
          if (item.id === round.id) {
            return {
              ...item,
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

  return (
    <div className="rounds">
      <button className="button primary" type="button" onClick={addRound}>
        Round +
      </button>
      {rounds
        && rounds.map((round) => (
          <Round key={round.id} round={round} removeRound={removeRound} updateRound={updateRound} />
        ))}
    </div>
  );
}
