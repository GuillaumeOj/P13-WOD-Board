[![Mergify Status][mergify-badge]][mergify-link]
[![CI][ci-badge]][ci-link]
[![CD][cd-badge]][cd-link]
[![Coverage Status][coverage-badge]][coverage-link]
[![Code style: black][black-badge]][black-link]

[mergify-badge]: https://img.shields.io/endpoint.svg?url=https://gh.mergify.io/badges/GuillaumeOj/P11-AddAFeature&style=flat
[mergify-link]: https://mergify.io

[coverage-badge]: https://coveralls.io/repos/github/GuillaumeOj/P13-WOD-Board/badge.svg?branch=main
[coverage-link]: https://coveralls.io/github/GuillaumeOj/P13-WOD-Board?branch=main

[ci-badge]: https://github.com/GuillaumeOj/P13-WOD-Board/actions/workflows/ci.yml/badge.svg
[ci-link]: https://github.com/GuillaumeOj/P13-WOD-Board/actions/workflows/ci.yml

[cd-badge]: https://github.com/GuillaumeOj/P13-WOD-Board/actions/workflows/cd.yml/badge.svg
[cd-link]: https://github.com/GuillaumeOj/P13-WOD-Board/actions/workflows/cd.yml

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]: https://github.com/psf/black

# Presentation

This application is for the project 13 from [OpenClassrooms'](https://openclassrooms.com/fr/paths/68/projects/162/assignment) Python course.

The application is alive here => http://projet-13.ojardias.io

The roadmap of this project is available here: [Notion](https://www.notion.so/guillaumeoj/8c4537ce16a44754b703d0885754ec1f?v=8e9d19219c2c4c91ae945ff554e63453)

# Requirements

For running this application you will need:
- [Python 3.9](https://www.python.org/)
- [Tox](https://tox.readthedocs.io)
- [PostgreSQL](https://www.postgresql.org)
- [Yarn 1.22](https://yarnpkg.com/getting-started/install)

Setup PostgreSQL with those parameters:
- User: your choice
- Password: your choice too
- Databases:
  - `wod_board_test` (used for tests)
  - `wod_board_dev` (used for running the application)

# Env

Create a `.env` file in `/backend` based on `/backend/env-example`.

**NOTE**: Don't forget to replace `user` and `password` in `DATABASE_URL`

# Run

Start the backend application:

```sh
cd /backend
tox -e seed  # Populate the databe with user accounts and basic items
tox -e start # Run the backend application
```

Then visit:
- http://localhost:8500/api/docs for reading the back-end documentation


Start the frontend:
```sh
cd /frontend
yarn install # Only the first time
yarn start
```

Then visit:
- http://localhost:3000/

# Tests

In `/backend` type:

```sh
tox -e py39 [-- {optional-args}] # For python tests
tox -e pep8                      # For pep8
```
