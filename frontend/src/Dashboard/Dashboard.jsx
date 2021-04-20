import React from 'react';
import { Helmet } from 'react-helmet';
import {
  Redirect, Route, Switch, useLocation, useRouteMatch,
} from 'react-router-dom';

import { useAuth } from '../Auth';

import NewWod from './NewWod';
import SideNav from './SideNav';

export default function Dashboard() {
  const { path } = useRouteMatch();
  const location = useLocation();
  const auth = useAuth();

  if (!auth.user) {
    return <Redirect to="/signin" from={location.state} />;
  }

  return (
    <>
      <Helmet>
        <title>WOD Board - My Dashboard</title>
      </Helmet>
      <section id="dashboard">
        <SideNav />
        <Switch>
          <Route exact path={path}>
            <div className="subContent">
              <h2 className="title">Welcome to your Dashboard</h2>
            </div>
          </Route>
          <Route path={`${path}/create-wod`}>
            <NewWod />
          </Route>
        </Switch>
      </section>
    </>
  );
}
