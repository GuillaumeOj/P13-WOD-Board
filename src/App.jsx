import React from 'react';
import { Helmet } from 'react-helmet';
import { NavLink, Route, Switch } from 'react-router-dom';

import { useAuth } from './Auth';
import Home from './Home';
import Register from './Register';
import SignIn from './SignIn';
import { NotFound } from './Utils';

function App() {
  const auth = useAuth();
  return (
    <div className="App">
      <Helmet>
        <title>Welcome to WOD Board!</title>
      </Helmet>
      <header>
        <div className="logo">
          <NavLink exact to="/">
            <img src={`${process.env.PUBLIC_URL}logo.svg`} className="brand_logo" alt="logo" />
            <h1 className="brand_name">WOD Board</h1>
          </NavLink>
        </div>
        <nav className="navbar">
          <ol className="crumbs">
            <li>
              <NavLink exact to="/">
                Home
              </NavLink>
            </li>
            {auth.user ? (
              <>
                <li>
                  <NavLink to="/profile">My Account</NavLink>
                </li>
                <li>
                  <input type="button" onClick={() => auth.signOut()} value="Signout" />
                </li>
              </>
            ) : (
              <>
                <li>
                  <NavLink to="/register">Register</NavLink>
                </li>
                <li>
                  <NavLink to="/signin">Signin</NavLink>
                </li>
              </>
            )}
          </ol>
        </nav>
      </header>
      <div id="content">
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route path="/profile">
            <Home />
          </Route>
          <Route path="/register">
            <Register />
          </Route>
          <Route path="/signin">
            <SignIn />
          </Route>
          <Route path="*">
            <NotFound />
          </Route>
        </Switch>
      </div>
    </div>
  );
}

export default App;
