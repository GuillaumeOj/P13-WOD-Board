import React from 'react';
import { Helmet } from 'react-helmet';
import { useRouteMatch, Switch, Route } from 'react-router-dom';

import NewWod from './NewWod';
import SideNav from './SideNav';

export default function Dashboard() {
  const { path } = useRouteMatch();
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

          <Route exact path={`${path}/create-wod`}>
            <NewWod />
          </Route>
        </Switch>
      </section>
    </>
  );
}
