import axios from 'axios';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { useAuth } from '../../Auth';

import Round from './Round';

export default function Rounds({ wodId }) {
  const { user } = useAuth();

  const [rounds, setRounds] = useState();

  const getRounds = () => {
    axios
      .get(`/api/round/rounds/${wodId}`)
      .then((response) => {
        if (response.data) {
          setRounds(
            response.data.map((item, index) => (
              { ...item, position: index + 1 }
            )),
          );
        }
      });
  };

  const removeRound = (id) => {
    if (id && user) {
      const config = { headers: { Authorization: `${user.token_type} ${user.access_token}` } };
      axios
        .delete(`/api/round/${id}`, config)
        .then(() => getRounds());
    }
  };

  const addRound = () => {
    const position = rounds.length + 1;

    if (wodId && user) {
      const config = { headers: { Authorization: `${user.token_type} ${user.access_token}` } };
      const payload = {
        position,
        durationSeconds: 0,
        repetition: 0,
        wodId,
      };
      axios
        .post('/api/round/', payload, config)
        .then(() => getRounds());
    }
  };

  const updateRound = (round) => {
    if (round.id) {
      const config = { headers: { Authorization: `${user.token_type} ${user.access_token}` } };
      const payload = {
        position: round.position,
        durationSeconds: round.durationSeconds,
        repetition: round.repetition,
        wodId,
      };
      axios
        .put(`/api/round/${round.id}`, payload, config)
        .then(() => getRounds());
    }
  };

  useEffect(() => {
    if (wodId) {
      if (rounds) {
        const updatedRounds = [...rounds];
        setRounds(updatedRounds.map((round) => ({ ...round, wodId })));
      } else {
        getRounds();
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
          (round) => round.id && (
          <Round
            key={round.id}
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
