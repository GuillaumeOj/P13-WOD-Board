import React, { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';

import { useAuth } from './Auth';

export default function NavBar() {
  const [home, setHome] = useState('/');
  const auth = useAuth();

  useEffect(() => {
    setHome(auth.user ? '/dashboard' : '/');
  }, [auth.user]);

  return (
    <header>
      <div className="logo">
        <NavLink exact to={home}>
          <img
            src={`${process.env.PUBLIC_URL}/logo.svg`}
            className="brand_logo"
            alt="logo"
          />
          <h1 className="brand_name">WOD Board</h1>
        </NavLink>
      </div>
      <nav className="navbar">
        <ol className="crumbs">
          <li>
            <NavLink exact to={home}>
              Home
            </NavLink>
          </li>
          {auth.user ? (
            <>
              <li>
                <NavLink to="/profile">My Account</NavLink>
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
                <NavLink to="/register">Register</NavLink>
              </li>
              <li>
                <NavLink to="/signin">Sign In</NavLink>
              </li>
            </>
          )}
        </ol>
      </nav>
    </header>
  );
}
