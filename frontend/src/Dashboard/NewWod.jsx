import React from 'react';
import { Helmet } from 'react-helmet';

export default function NewWod() {
  return (
    <>
      <Helmet>
        <title>WOD Board - My Dashboard</title>
      </Helmet>
      <div className="subContent">
        <h2 className="title">Create a new WOD</h2>
      </div>
    </>
  );
}
