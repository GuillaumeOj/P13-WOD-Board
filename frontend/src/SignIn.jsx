import axios from 'axios';
import React from 'react';
import { Helmet } from 'react-helmet';
import {
  Link, Redirect, useLocation,
} from 'react-router-dom';

import { useAlert } from './Alert';
import { useAuth } from './Auth';
import { useInput } from './Utils';

export default function SignIn() {
  const location = useLocation();
  const auth = useAuth();
  const { addAlert } = useAlert();

  const [email, setEmail] = useInput('');
  const [password, setPassword] = useInput('');

  const { from } = location.state || { from: { pathname: '/' } };

  async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    axios
      .post('/api/user/token', formData)
      .then((response) => {
        auth.signIn(response.data);
        addAlert({ message: 'You are now logged in!', alertType: 'success' });
      })
      .catch((error) => {
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
          addAlert({ message: 'Something went wrong', alertType: 'error' });
        }
      });
  }

  if (auth.user) {
    return <Redirect to={from.pathname} />;
  }

  return (
    <>
      <Helmet>
        <title>WOD Board - Sign In</title>
      </Helmet>
      <section id="signIn">
        <div className="subHeader">
          <h2 className="title">Sign In!</h2>
        </div>
        <div className="subContent">
          <form onSubmit={handleSubmit}>
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
            <input type="submit" onClick={handleSubmit} value="Sign In" className="button primary" />
            <p>
              Don&apos;t have any account?{' '}
              <Link to="/register">Register</Link> now.
            </p>
          </form>
        </div>
      </section>
    </>
  );
}
