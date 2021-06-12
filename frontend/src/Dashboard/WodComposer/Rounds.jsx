import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';

import { useApi } from '../../Api';
import { useAuth } from '../../Auth';

import Round from './Round';

export default function Rounds({ wodId }) {
  const { user } = useAuth();
  const { api } = useApi();

  const [rounds, setRounds] = useState();

  const getRounds = async () => {
    const response = await api({
      method: 'get', url: `/api/round/rounds/${wodId}`, silent: true, user,
    });

    if (response) {
      setRounds(
        response.map((item, index) => (
          { ...item, position: index + 1 }
        )),
      );
    }
  };

  const removeRound = async (id) => {
    if (id && user) {
      const response = await api({
        method: 'delete', url: `/api/round/${id}`, silent: true, user,
      });

      if (response) {
        getRounds();
      }
    }
  };

  const addRound = async () => {
    if (wodId && user) {
      const position = rounds.length + 1;
      const data = {
        position,
        durationSeconds: 0,
        repetition: 0,
        wodId,
      };

      const response = await api({
        method: 'post', url: '/api/round', data, silent: true, user,
      });

      if (response) {
        getRounds();
      }
    }
  };

  const updateRound = async (round) => {
    if (round.id) {
      const data = {
        position: round.position,
        durationSeconds: round.durationSeconds,
        repetition: round.repetition,
        wodId,
      };

      const response = await api({
        method: 'put', url: `/api/round/${round.id}`, data, silent: true, user,
      });

      if (response) {
        getRounds();
      }
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
