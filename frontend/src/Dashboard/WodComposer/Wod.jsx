import axios from 'axios';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet';

import { useAlert } from '../../Alert';
import { useAuth } from '../../Auth';

import Rounds from './Rounds';
import WodType from './WodType';

dayjs.extend(utc);

export default function Wod() {
  const { user, userId } = useAuth();
  const { addAlert } = useAlert();

  const [id, setId] = useState();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const date = dayjs.utc().format();
  const [wodTypeId, setWodTypeId] = useState();
  const [authorId, setAuthorId] = useState();
  const [isComplete, setIsComplete] = useState(false);

  const [wod, setWod] = useState();

  useEffect(() => {
    const config = { headers: { Authorization: `${user.token_type} ${user.access_token}` } };
    axios.get('/api/wod/incomplete', config)
      .then((response) => {
        if (response.data) {
          const values = response.data;
          if (values) {
            if (values.id) { setId(values.id); }
            if (values.title) { setTitle(values.title); }
            if (values.description) { setDescription(values.description); }
            if (values.wodTypeId) { setWodTypeId(values.wodTypeId); }
          }
        }
      });
  }, []);

  useEffect(() => {
    setAuthorId(userId);
  }, [user]);

  useEffect(() => {
    const updatedWod = {
      id,
      title,
      description,
      date,
      wodTypeId,
      authorId,
      isComplete,
    };
    setWod(updatedWod);
  }, [date, id, description, title, wodTypeId, authorId, isComplete]);

  useEffect(() => {
    const config = { headers: { Authorization: `${user.token_type} ${user.access_token}` } };
    if (title && user) {
      if (!id) {
        axios.post('/api/wod/', wod, config)
          .then((response) => setId(response.data.id));
      } else {
        axios.put(`/api/wod/${id}`, wod, config)
          .then(() => (isComplete ? addAlert('WOD saved!', 'success') : ''));
      }
    }
  }, [wod]);

  const handleSubmit = (event) => {
    event.preventDefault();
    setIsComplete(true);
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
            <label htmlFor="title">Title*:&nbsp;</label>
            <input
              type="text"
              name="title"
              id="title"
              value={title}
              onChange={(event) => { setTitle(event.target.value); }}
              required
              placeholder="Murph, Cindy, etc."
            />
          </div>
          <div className="field">
            <label htmlFor="description">Description:&nbsp;</label>
            <input
              type="text"
              name="description"
              id="description"
              value={description}
              onChange={(event) => { setDescription(event.target.value); }}
              placeholder="Murph Day!"
            />
          </div>
          <WodType wodTypeId={wodTypeId} setWodTypeId={setWodTypeId} />
          <Rounds wodId={id} />
          <p>All fields marked with * are required.</p>
          <input type="submit" value="New WOD" className="button primary" />
        </form>
      </div>
    </>
  ) : (
    ''
  );
}
