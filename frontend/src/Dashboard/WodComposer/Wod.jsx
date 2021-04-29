import axios from 'axios';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet';
import { Prompt } from 'react-router-dom';

import { useAlert } from '../../Alert';
import { useInput } from '../../Utils';

import Rounds from './Rounds';

dayjs.extend(utc);

export default function Wod() {
  const { addAlert } = useAlert();

  const date = dayjs.utc().format();

  const [id, setId] = useState(0);
  const [description, setDescription] = useInput('');
  const [note, setNote] = useInput('');
  const [wodType, setWodType] = useState({ id: 0, name: '' });
  const [wodTypes, setWodTypes] = useState([]);
  const [isBlocking, setIsBlocking] = useState(true);
  const [wod, setWod] = useState();

  const searchWodType = (name) => {
    axios
      .get(`/api/wod/types/${name}`)
      .then((response) => setWodTypes(response.data))
      .catch((error) => {
        if (error) {
          if (error.response) {
            if (error.response.data) {
              const { detail } = error.response.data;

              if (typeof detail === 'string') {
                addAlert({ message: detail, alertType: 'error' });
              } else {
                detail.map((item) => addAlert({ message: item.msg, alertType: 'error' }));
              }
            }
          } else {
            addAlert({
              message: 'Impossible to retrieve WOD types',
              alertType: 'error',
            });
          }
        }
      });
  };

  const selectWodType = (event) => {
    const previousWodType = { ...wodType };
    const typeName = event.target.value;
    if (typeName) {
      searchWodType(typeName);
      setWodType({ ...previousWodType, name: typeName });
    } else {
      setWodTypes([]);
      setWodType({ ...previousWodType, name: typeName });
    }
  };

  const updateWod = () => {
    const updatedWod = {
      id,
      date,
      description,
      note,
      wodTypeId: wodType.id,
      wodType,
    };
    setWod(updatedWod);
  };

  useEffect(() => {
    updateWod();
  }, [date, id, description, note, wodType]);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (id === 0) {
      setId(1);
    }
    updateWod();
    setIsBlocking(false);
  };

  return wod ? (
    <>
      <Helmet>
        <title>WOD Board - My Dashboard</title>
      </Helmet>
      <div className="subContent">
        <h2 className="title">Create a new WOD</h2>
        <form onSubmit={handleSubmit}>
          <Prompt when={isBlocking} message="Are you sure you want to leave the form?" />
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
          <div className="field">
            <label htmlFor="wodType">Type of WOD*:&nbsp;</label>
            <input name="wodType" id="wodType" value={wodType.name} onChange={selectWodType} />
            <div className="completion">
              {wodTypes && (
                <div className="types">
                  {wodTypes.map((item) => (
                    <button
                      className="button type"
                      type="button"
                      key={item.id}
                      value={item.name}
                      onClick={() => {
                        setWodType({ id: item.id, name: item.name });
                        setWodTypes([]);
                      }}
                    >
                      {item.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
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
