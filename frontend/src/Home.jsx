import React from 'react';
import { Helmet } from 'react-helmet';
import { Redirect, Link } from 'react-router-dom';

import { useAuth } from './Auth';

export default function Home() {
  const auth = useAuth();
  return (auth.user ? <Redirect to="/dashboard" /> : (
    <>
      <Helmet>
        <title>Welcome to WOD Board!</title>
      </Helmet>
      <section id="home">
        <div className="subHeader">
          <h2 className="title">Track your WODs</h2>
          <p className="lead">Train hard and log your performance!</p>
        </div>
        <div className="subContent">
          <div>
            <article>
              <h3>Leaderboard</h3>
              <p>Compare your level with your box&apos;s mates.</p>
            </article>
            <article>
              <h3>Progession</h3>
              <p>See your progression along the time.</p>
            </article>
          </div>
          <div>
            <article>
              <h3>Share</h3>
              <p>Share your performance with your friends.</p>
            </article>
            <article>
              <h3>It&apos;s free!</h3>
              <p>All the features are free!</p>
            </article>
          </div>
        </div>
        <div className="subscribe">
          <Link to="/register" className="button primary">
            Register
          </Link>
          <Link to="/signin" className="button">
            Sign In
          </Link>
        </div>
      </section>
    </>
  ));
}
