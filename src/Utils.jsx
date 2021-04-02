import React, { useState } from 'react';

function useInput(initialValue) {
  const [value, setValue] = useState(initialValue);

  function handleChange(event) {
    setValue(event.target.value);
  }

  return [value, handleChange];
}

export default useInput;
export function NotFound() {
  return (
    <section id="notFound">
      <div className="subHeader">
        <h2 className="title">Oops!</h2>
        <p className="lead">It seems the page you are looking for doesn&apos;t exist.</p>
      </div>
    </section>
  );
}
