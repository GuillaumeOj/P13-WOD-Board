import axios from 'axios';
import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

import { useAuth } from './Auth';
import { useInput, Alert } from './Utils';

export default function SignIn() {
  const auth = useAuth();
  const [email, setEmail] = useInput('');
  const [password, setPassword] = useInput('');

  const [alert, setAlert] = useState({ content: '', type: '' });

  async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    axios
      .post('/api/user/token', formData)
      .then((response) => {
        setAlert({ content: 'You are now logged in!', type: 'success' });
        auth.signIn(response.data);
      })
      .catch((error) => {
        if (error.response) {
          setAlert({ content: error.response.data.detail, type: 'error' });
        } else if (error.message) {
          setAlert({ content: error.message, type: 'error' });
        } else {
          setAlert({
            content: 'An error occured, please try again or contact an administrator.',
            type: 'error',
          });
        }
      });
  }

  return (
    <section id="signIn">
      <div className="subHeader">
        <h2 className="title">Sign In!</h2>
      </div>
      <div className="subContent">
        <form onSubmit={handleSubmit}>
          <Alert message={alert.content} type={alert.type} />
          <div className="field">
            <label htmlFor="username">Email:&nbsp;</label>
            {/* The field is named username
            because we use the 'email' as an 'username' */}
            <input
              type="text"
              name="username"
              id="username"
              value={email}
              onChange={setEmail}
              required
            />
          </div>
          <div className="field">
            <label htmlFor="password">Password:&nbsp;</label>
            <input
              type="password"
              name="password"
              id="password"
              value={password}
              onChange={setPassword}
              required
            />
          </div>
          <input type="submit" value="Sign In" className="button primary" />
          <p>
            Don&apos;t have any account? <NavLink to="/register">Register</NavLink> now.
          </p>
        </form>
      </div>
    </section>
  );
}
