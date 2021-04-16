import axios from 'axios';
import React from 'react';
import { Helmet } from 'react-helmet';
import { NavLink } from 'react-router-dom';

import { useAlert } from './Alert';
import { useInput } from './Utils';

function Register() {
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
      addAlert({ message: 'Passwords don&apos;t match.', alertType: 'error' });
      return;
    }

    const formData = new FormData();
    formData.append('email', email);
    formData.append('username', username);
    formData.append('password', password);
    formData.append('first_name', firstName);
    formData.append('last_name', lastName);

    axios
      .post('/api/user/register', formData)
      .then(() => {
        addAlert({ message: 'You are now registered!', alertType: 'success' });
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
              <label htmlFor="username">Email*:&nbsp;</label>
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
              <label htmlFor="username2">Username*:&nbsp;</label>
              <input
                type="text"
                name="username2"
                id="username2"
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
              Have any account already? <NavLink to="/signin">Sign In</NavLink>{' '}
              now.
            </p>
          </form>
        </div>
      </section>
    </>
  );
}

export default Register;
