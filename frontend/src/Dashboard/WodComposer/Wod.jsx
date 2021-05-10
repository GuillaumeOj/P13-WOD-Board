import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet';

import { useInput } from '../../Utils';

import Rounds from './Rounds';
import WodType from './WodType';

dayjs.extend(utc);

export default function Wod() {
  const [id, setId] = useState(0);
  const [description, setDescription] = useInput('');
  const [note, setNote] = useInput('');
  const date = dayjs.utc().format();

  const [wod, setWod] = useState();

  const updateWod = () => {
    const updatedWod = {
      id,
      description,
      note,
      date,
    };
    setWod(updatedWod);
  };

  useEffect(() => {
    updateWod();
  }, [date, id, description, note]);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (id === 0) {
      setId(1);
    }
    updateWod();
  };

  return wod ? (
    <>
      <Helmet>
        <title>WOD Board - My Dashboard</title>
      </Helmet>
      <div className="subContent">
        <h2 className="title">Create a new WOD</h2>
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="description">Description:&nbsp;</label>
            <input
              type="text"
              name="description"
              id="description"
              value={description}
              onChange={setDescription}
            />
          </div>
          <div className="field">
            <label htmlFor="note">Note:&nbsp;</label>
            <input type="text" name="note" id="note" value={note} onChange={setNote} />
          </div>
          <WodType />
          <Rounds wod={wod} />
          <p>All fields marked with * are required.</p>
          <input type="submit" value="New WOD" className="button primary" />
        </form>
      </div>
    </>
  ) : (
    ''
  );
}
