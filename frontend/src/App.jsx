import React from 'react';
import { Route, Switch } from 'react-router-dom';

import { DisplayAlerts } from './Alert';
import { AnonymRoute, PrivateRoute } from './CustomRoute';
import Dashboard from './Dashboard/Dashboard';
import Home from './Home';
import NavBar from './Nav';
import Register from './Register';
import SignIn from './SignIn';
import { NotFound } from './Utils';

function App() {
  return (
    <div className="App">
      <NavBar />
      <DisplayAlerts />
      <div id="content">
        <Switch>
          <AnonymRoute exact path="/">
            <Home />
          </AnonymRoute>
          <PrivateRoute path="/profile">
            <Home />
          </PrivateRoute>
          <AnonymRoute path="/register">
            <Register />
          </AnonymRoute>
          <AnonymRoute path="/signin">
            <SignIn />
          </AnonymRoute>
          <PrivateRoute path="/dashboard">
            <Dashboard />
          </PrivateRoute>
          <Route path="*">
            <NotFound />
          </Route>
        </Switch>
      </div>
    </div>
  );
}

export default App;
