import React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

import { DisplayAlerts } from './Alert';
import { useAuth } from './Auth';
import Dashboard from './Dashboard/Dashboard';
import Home from './Home';
import NavBar from './Nav';
import Register from './Register';
import SignIn from './SignIn';
import { NotFound } from './Utils';

function App() {
  const auth = useAuth();
  return (
    <div className="App">
      <NavBar />
      <DisplayAlerts />
      <div id="content">
        <Switch>
          <Route exact path="/">
            {auth.user ? <Redirect to="/dashboard" /> : <Home />}
          </Route>
          <Route path="/profile">
            <Home />
          </Route>
          <Route path="/register">
            {auth.user ? <Redirect to="/dashboard" /> : <Register />}
          </Route>
          <Route path="/signin">
            {auth.user ? <Redirect to="/dashboard" /> : <SignIn />}
          </Route>
          <Route path="/dashboard">
            {auth.user ? <Dashboard /> : <Redirect to="/" />}
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
