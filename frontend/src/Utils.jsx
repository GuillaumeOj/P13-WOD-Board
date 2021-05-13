import React, { useState } from 'react';

export function useInput(initialValue) {
  const [value, setValue] = useState(initialValue);

  function handleChange(event) {
    setValue(event.target.value);
  }

  return [value, handleChange];
}

export function NotFound() {
  return (
    <section id="notFound">
      <div className="subHeader">
        <h2 className="title">Oops!</h2>
        <p className="lead">The page you are looking for doesn&apos;t exist.</p>
      </div>
    </section>
  );
}

export function SecondsToMinutesSeconds(value) {
  let seconds = value;
  let minutes = 0;

  if (seconds < 60) {
    return { minutes, seconds };
  }

  minutes = (seconds - (seconds % 60)) / 60;
  seconds %= 60;
  return { minutes, seconds };
}

export function MinutesSecondsToSeconds(minutes, seconds) {
  const result = seconds + minutes * 60;

  return { seconds: result };
}
