import React from 'react';

function Register() {
  return (
    <>
      <section id="register">
        <div className="subHeader">
          <h2 className="title">Join Us!</h2>
          <p className="lead">Join our community for free!</p>
        </div>
        <div className="subContent">
          <form method="post" action="api/register">
            <div className="field">
              <label htmlFor="username">Username*:&nbsp;</label>
              <input type="text" name="username" id="username" required />
            </div>
            <div className="group">
              <div className="field">
                <label htmlFor="first_name">First Name:&nbsp;</label>
                <input type="text" name="first_name" id="first_name" />
              </div>
              <div className="field">
                <label htmlFor="last_name">Last Name:&nbsp;</label>
                <input type="text" name="last_name" id="last_name" />
              </div>
            </div>
            <div className="field">
              <label htmlFor="password">Password*:&nbsp;</label>
              <input type="password" name="password" id="password" required />
            </div>
            <p>All fields marked with * are required.</p>
            <input type="button" value="Register" className="button primary" />
          </form>
        </div>
      </section>
    </>
  );
}

export default Register;
