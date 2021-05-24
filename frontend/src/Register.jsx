import React from 'react';
import { Helmet } from 'react-helmet';
import {
  Link,
} from 'react-router-dom';

import { useAlert } from './Alert';
import { useApi } from './Api';
import { useAuth } from './Auth';
import { useInput } from './Utils';

export default function Register() {
  const auth = useAuth();
  const { api } = useApi();
  const { addAlert } = useAlert();

  const [email, setEmail] = useInput('');
  const [username, setUsername] = useInput('');
  const [password, setPassword] = useInput('');
  const [password2, setPassword2] = useInput('');
  const [firstName, setFirstName] = useInput('');
  const [lastName, setLastName] = useInput('');

  async function handleSubmit(event) {
    event.preventDefault();

    if (password !== password2) {
      addAlert({ message: 'Passwords don\'t match.', alertType: 'error' });
      return;
    }

    const formData = new FormData(event.target);

    const response = await api({
      method: 'post', data: formData, url: '/api/user/register/', silent: false,
    });

    if (response) {
      auth.signIn(response);
    }
  }

  return (
    <>
      <Helmet>
        <title>WOD Board - Register</title>
      </Helmet>
      <section id="register">
        <div className="subHeader">
          <h2 className="title">Register an account</h2>
          <p className="lead">Join our community for free!</p>
        </div>
        <div className="subContent">
          <form onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="email">Email*:&nbsp;</label>
              <input
                type="text"
                name="email"
                id="email"
                value={email}
                onChange={setEmail}
                required
              />
            </div>
            <div className="field">
              <label htmlFor="username">Username*:&nbsp;</label>
              <input
                type="text"
                name="username"
                id="username"
                value={username}
                onChange={setUsername}
                required
              />
            </div>
            <div className="group">
              <div className="field">
                <label htmlFor="firstName">First Name:&nbsp;</label>
                <input
                  type="text"
                  name="firstName"
                  id="firstName"
                  value={firstName}
                  onChange={setFirstName}
                />
              </div>
              <div className="field">
                <label htmlFor="lastName">Last Name:&nbsp;</label>
                <input
                  type="text"
                  name="lastName"
                  id="lastName"
                  value={lastName}
                  onChange={setLastName}
                />
              </div>
            </div>
            <div className="field">
              <label htmlFor="password">Password*:&nbsp;</label>
              <input
                type="password"
                name="password"
                id="password"
                value={password}
                onChange={setPassword}
                required
              />
            </div>
            <div className="field">
              <label htmlFor="password2">Verify Password*:&nbsp;</label>
              <input
                type="password"
                name="password2"
                id="password2"
                value={password2}
                onChange={setPassword2}
                required
              />
            </div>
            <p>All fields marked with * are required.</p>
            <input type="submit" value="Register" className="button primary" />
            <p>
              Have any account already? <Link to="/signin">Sign In</Link>{' '}
              now.
            </p>
          </form>
        </div>
      </section>
    </>
  );
}
