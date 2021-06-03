import { faGithub, faReact } from '@fortawesome/free-brands-svg-icons';
import { faSlash, faHeart, faBook } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React from 'react';

export default function Footer() {
  return (
    <footer className="footer">
      <p className="signature">
        Made by <a href="https://github.com/GuillaumeOj/" target="_blank" rel="noreferrer">GuillaumeOj</a> with <FontAwesomeIcon icon={faHeart} title="Heart" /> in France
      </p>
      <ul className="socials">
        <li key="github" className="social">
          <FontAwesomeIcon icon={faGithub} className="icon fontawesome" title="GitHub" />
          <a
            href="https://github.com/GuillaumeOj/P13-WOD-Board"
            className="socialLink"
            target="_blank"
            rel="noreferrer"
          >
            P13-WOD-Board
          </a>
        </li>
        <li key="separator-1" className="separator">
          <FontAwesomeIcon icon={faSlash} className="icon" rotation={90} />
        </li>
        <li key="react" className="social">
          <FontAwesomeIcon icon={faReact} className="icon fontawesome" title="ReactJS" />
          <a
            href="https://reactjs.org/"
            className="socialLink"
            target="_blank"
            rel="noreferrer"
          >
            ReactJS
          </a>
        </li>
        <li key="separator-2" className="separator">
          <FontAwesomeIcon icon={faSlash} className="icon" rotation={90} />
        </li>
        <li key="fastapi" className="social">
          <img src={`${process.env.PUBLIC_URL}/fastapi.svg`} alt="FastAPI's logo" className="icon" />
          <a
            href="https://fastapi.tiangolo.com/"
            className="socialLink"
            target="_blank"
            rel="noreferrer"
          >
            FastAPI
          </a>
        </li>
        <li key="separator-2" className="separator">
          <FontAwesomeIcon icon={faSlash} className="icon" rotation={90} />
        </li>
        <li key="fastapi" className="social">
          <FontAwesomeIcon icon={faBook} className="icon fontawesome" title="API Docs" />
          <a
            href="/api/docs"
            className="Documentation"
            target="_blank"
            rel="noreferrer"
          >
            Documentation
          </a>
        </li>

      </ul>
    </footer>
  );
}
