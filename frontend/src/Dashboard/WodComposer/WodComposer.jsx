import React, { useState } from 'react';

import Round from './Round';

export default function WodComposer() {
  const [rounds, setRounds] = useState([]);
  const [nextPosition, setNextPosition] = useState(1);

  const addRound = () => {
    const updatedRounds = [...rounds];

    updatedRounds.push(nextPosition);
    setRounds(updatedRounds);
    setNextPosition(nextPosition + 1);
  };

  const removeRound = ({ position }) => {
    const updatedRounds = rounds.filter((round) => round !== position);
    setRounds(updatedRounds);
  };

  return (
    <div className="roundArea">
      <button className="button primary" type="button" onClick={addRound}>Add a Round +</button>
      {rounds && rounds.map((position) => (
        <Round key={`round-${position.toString()}`} position={position} removeRound={removeRound} />
      ))}
    </div>
  );
}
