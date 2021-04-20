import React from 'react';
import { Link } from 'react-router-dom';

import { useAuth } from './Auth';

export default function NavBar() {
  const auth = useAuth();

  return (
    <header>
      <div className="logo">
        <Link to="/">
          <img
            src={`${process.env.PUBLIC_URL}/logo.svg`}
            className="brand_logo"
            alt="logo"
          />
          <h1 className="brand_name">WOD Board</h1>
        </Link>
      </div>
      <nav className="navbar">
        <ol className="crumbs">
          {auth.user ? (
            <>
              <li>
                <Link to="/profile">My Account</Link>
              </li>
              <li>
                <input
                  type="button"
                  onClick={() => auth.signOut()}
                  value="Sign Out"
                />
              </li>
            </>
          ) : (
            <>
              <li>
                <Link to="/">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/register">Register</Link>
              </li>
              <li>
                <Link to="/signin">Sign In</Link>
              </li>
            </>
          )}
        </ol>
      </nav>
    </header>
  );
}
