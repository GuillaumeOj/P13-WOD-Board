import React from 'react';
import { Helmet } from 'react-helmet';
import {
  Switch, useRouteMatch,
} from 'react-router-dom';

import { PrivateRoute } from '../CustomRoute';

import SideNav from './SideNav';
import Wod from './WodComposer/Wod';
import Wods from './Wods';

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
          <PrivateRoute exact path={path}>
            <Wods />
          </PrivateRoute>
          <PrivateRoute path={`${path}/create-wod`}>
            <Wod />
          </PrivateRoute>
        </Switch>
      </section>
    </>
  );
}
