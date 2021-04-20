import React from 'react';
import { Link, useRouteMatch } from 'react-router-dom';

export default function SideNav() {
  const { url } = useRouteMatch();

  return (
    <div>
      <nav className="navbar">
        <ol className="crumbs">
          <li>
            <Link to={url}>Home</Link>
          </li>
          <li>
            <Link to={`${url}/create-wod`}>Create a WOD</Link>
          </li>
        </ol>
      </nav>
    </div>
  );
}
