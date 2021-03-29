import React from 'react';
import { Helmet } from 'react-helmet';
import { NavLink, Route, Switch } from 'react-router-dom';

import Home from './Home';
import Register from './Register';

function App() {
  return (
    <div className="App">
      <Helmet>
        <title>Welcome to WOD Board!</title>
      </Helmet>
      <header>
        <div className="logo">
          <NavLink to="/">
            <img
              src={`${process.env.PUBLIC_URL}logo.svg`}
              className="brand_logo"
              alt="logo"
            />
            <h1 className="brand_name">WOD Board</h1>
          </NavLink>
        </div>
        <nav className="navbar">
          <ol className="crumbs">
            <li>
              <NavLink to="/">Home</NavLink>
            </li>
            <li>
              <NavLink to="/register">Register</NavLink>
            </li>
            <li>
              <NavLink to="/signin">Sign In</NavLink>
            </li>
          </ol>
        </nav>
      </header>
      <div id="background" />
      <div id="content">
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route path="/register">
            <Register />
          </Route>
          <Route path="/signin">
            <Home />
          </Route>
        </Switch>
      </div>
    </div>
  );
}

export default App;
