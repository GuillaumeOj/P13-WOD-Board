import React from 'react';

import useInput from './Utils';

function Register() {
  const [username, setUsername] = useInput('');
  const [password, setPassword] = useInput('');
  const [firstName, setFirstName] = useInput('');
  const [lastName, setLastName] = useInput('');

  function handleSubmit(event) {
    event.preventDefault();
  }

  return (
    <section id="register">
      <div className="subHeader">
        <h2 className="title">Join Us!</h2>
        <p className="lead">Join our community for free!</p>
      </div>
      <div className="subContent">
        <form onSubmit={handleSubmit}>
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
          <p>All fields marked with * are required.</p>
          <input type="submit" value="Register" className="button primary" />
        </form>
      </div>
    </section>
  );
}

export default Register;
