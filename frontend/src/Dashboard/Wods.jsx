import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet';

import { useApi } from '../Api';
import { useAuth } from '../Auth';

export default function Wods() {
  const { user } = useAuth();
  const { api } = useApi();

  const [wods, setWods] = useState();

  useEffect(async () => {
    const response = await api({
      method: 'get', url: '/api/wod/wods', silent: false, user,
    });

    if (response) {
      setWods(response);
    }
  });
  return (
    <>
      <Helmet>
        <title>WOD Board - My WODS</title>
      </Helmet>
      <div className="subContent">
        <h2 className="title">My WODS</h2>
        <ul className="wodsList">
          {wods && wods.map((wod) => (
            <li key={`wod-${wod.id}`} className="wod">{wod.title}{wod.description ? ` - ${wod.description}` : ''}</li>
          ))}
        </ul>
      </div>
    </>
  );
}
