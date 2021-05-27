import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet';
import { useHistory } from 'react-router-dom';

import { useAlert } from '../../Alert';
import { useApi } from '../../Api';
import { useAuth } from '../../Auth';

import Rounds from './Rounds';
import WodType from './WodType';

dayjs.extend(utc);

export default function Wod() {
  const history = useHistory();
  const { api } = useApi();
  const { user, userId } = useAuth();
  const { addAlert } = useAlert();

  const [id, setId] = useState();
  const [title, setTitle] = useState();
  const [description, setDescription] = useState();
  const date = dayjs.utc().format();
  const [wodTypeId, setWodTypeId] = useState();
  const [authorId, setAuthorId] = useState();
  const [isComplete, setIsComplete] = useState(false);

  const [wod, setWod] = useState();

  useEffect(async () => {
    const response = await api({
      method: 'get', url: '/api/wod/incomplete', silent: true, user,
    });

    if (response) {
      if (response.id) { setId(response.id); }
      if (response.title) { setTitle(response.title); }
      if (response.description) { setDescription(response.description); }
      if (response.wodTypeId) { setWodTypeId(response.wodTypeId); }
    }
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

  useEffect(async () => {
    if (wod && wod.title && user) {
      if (!id) {
        const response = await api({
          method: 'post', url: '/api/wod/', data: wod, user, silent: true,
        });

        if (response) {
          setId(response.id);
        }
      } else {
        const response = await api({
          method: 'put', url: `/api/wod/${id}`, data: wod, user, silent: false,
        });

        if (response && isComplete) {
          addAlert({ message: 'WOD saved!', alertType: 'success' });
          history.replace('/');
        }
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
