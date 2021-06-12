import React from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router-dom';

import { useApi } from './Api';
import { useAuth } from './Auth';
import { useInput } from './Utils';

export default function SignIn() {
  const { signIn } = useAuth();
  const { api } = useApi();

  const [email, setEmail] = useInput('');
  const [password, setPassword] = useInput('');

  async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    const response = await api({
      method: 'post', data: formData, url: '/api/user/token', silent: false,
    });

    if (response) {
      signIn(response);
    }
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
              Don&apos;t have any account?{' '}
              <Link to="/register">Register</Link> now.
            </p>
          </form>
        </div>
      </section>
    </>
  );
}
