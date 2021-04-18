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

The application is alive here => https://projet-13.ojardias.io

The roadmap of this project is available here: [Notion](https://www.notion.so/guillaumeoj/8c4537ce16a44754b703d0885754ec1f?v=8e9d19219c2c4c91ae945ff554e63453)

# Requirements

For running this application you will need:
- [Python 3.9](https://www.python.org/)
- [Tox](https://tox.readthedocs.io)
- [PostgreSQL](https://www.postgresql.org)

Setup PostgreSQL with those parameters:
- User: `wod_board`
- Password: `wod_board`
- Databases:
  - `wod_board_test` (used for tests)
  - `wod_board_dev` (used for running the application)

# Run

In a shell run:

```sh
tox -e start
```

Then visit:
- http://127.0.0.1:8000/docs for reading the back-end documentation

# Tests

Run tests by typing:

```sh
tox -e py39 [-- {optional-args}]
```

Run pep8 tests by typing:

```sh
tox -e pep8
```
