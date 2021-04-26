import axios from 'axios';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet';

import { useAlert } from '../Alert';
import { useInput } from '../Utils';

import Rounds from './WodComposer/Rounds';

dayjs.extend(utc);

export default function NewWod() {
  const { addAlert } = useAlert();

  const [description, setDescription] = useInput('');
  const [note, setNote] = useInput('');
  const [wodTypeId, setWodTypeId] = useState('');
  const [wodType, setWodType] = useState('');
  const [wodTypes, setWodTypes] = useState([]);

  const loadWodTypes = () => {
    axios
      .get('/api/wod/types')
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

  useEffect(() => {
    if (wodTypes.length === 0) {
      loadWodTypes();
    }
  });

  const selectWodType = (event) => {
    const typeName = event.target.value;
    if (typeName) {
      const typeId = wodTypes.find((type) => type.name === typeName).id;

      setWodType(typeName);
      setWodTypeId(typeId);
    } else {
      setWodType('');
      setWodTypeId('');
    }
    console.log(wodTypeId); // eslint-disable-line no-console
    console.log(wodType); // eslint-disable-line no-console
  };

  return (
    <>
      <Helmet>
        <title>WOD Board - My Dashboard</title>
      </Helmet>
      <div className="subContent">
        <h2 className="title">Create a new WOD</h2>
        <form>
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
            <select name="wodType" id="wodType" onChange={selectWodType}>
              <option value="" key="">
                -- Choose a type --
              </option>
              {wodTypes
                && wodTypes.map(({ name, id }) => (
                  <option value={name} key={id}>
                    {name}
                  </option>
                ))}
            </select>
          </div>
          <Rounds />
          <p>All fields marked with * are required.</p>
          <input type="submit" value="New WOD" className="button primary" />
        </form>
      </div>
    </>
  );
}
