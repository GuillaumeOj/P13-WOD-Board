import React from 'react';
import { NavLink } from 'react-router-dom';

import { TokenPropType } from './Type';

function Home({ user }) {
  return (
    <>
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
        {user && user.access_token ? (
          ''
        ) : (
          <div className="subscribe">
            <NavLink to="/register" className="button primary">
              Register
            </NavLink>
            <NavLink to="/signin" className="button">
              Sign In
            </NavLink>
          </div>
        )}
      </section>
    </>
  );
}

Home.propTypes = {
  user: TokenPropType,
};

Home.defaultProps = {
  user: '',
};

export default Home;
