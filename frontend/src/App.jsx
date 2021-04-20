import React from 'react';
import { Route, Switch } from 'react-router-dom';

import { DisplayAlerts } from './Alert';
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
          <Route path="/dashboard">
            <Dashboard />
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
