import React from 'react';
import { NavLink, useRouteMatch } from 'react-router-dom';

export default function SideNav() {
  const { url } = useRouteMatch();
  return (
    <div>
      <nav className="navbar">
        <ol className="crumbs">
          <li>
            <NavLink exact to={`${url}`}>
              Home
            </NavLink>
          </li>
          <li>
            <NavLink exact to={`${url}/create-wod`}>
              Create a WOD
            </NavLink>
          </li>
        </ol>
      </nav>
    </div>
  );
}
