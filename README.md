[![Coverage Status][coverage-badge]][coverage-link]

[coverage-link]: https://coveralls.io/github/GuillaumeOj/P13-WOD-Board?branch=main
[coverage-badge]: https://coveralls.io/repos/github/GuillaumeOj/P13-WOD-Board/badge.svg?branch=main

# Contents Page

- [I. Presentation](#i-presentation)
- [II. Requirements](#ii-requirements)
- [III. Run](#iii-run)
- [IV. Tests](#iv-tests)
- [V. To-Do List](#v-to-do-list)
- [VI. Credits](#vi-credits)

# I. Presentation
[⇧ *Top*](#contents-page)

This application is for the project 13 from [OpenClassrooms'](https://openclassrooms.com/fr/paths/68/projects/162/assignment) Python course.

The application is alive here => https://projet-13.ojardias.io

The roadmap of this project is available here: [Notion](https://www.notion.so/guillaumeoj/8c4537ce16a44754b703d0885754ec1f?v=8e9d19219c2c4c91ae945ff554e63453)

# II. Requirements
[⇧ *Top*](#contents-page)

For running this application you will need:
- [Python 3.9](https://www.python.org/)
- [Tox](https://tox.readthedocs.io)
- [PostgreSQL](https://www.postgresql.org)

Setup PostgreSQL with those parameters:
- User: wod_board
- Password: wod_board
- Databases:
  - wod_board_test (used for tests)
  - wod_board_dev (used for running the application)

# III. Run
[⇧ *Top*](#contents-page)

In a shell run:

```sh
tox -e start
```

Then visit:
- http://127.0.0.1:8000/docs for reading the back-end documentation

# IV. Tests
[⇧ *Top*](#contents-page)

Run tests by typing:

```sh
tox -e py39 [-- {optional-args}]
```

Run pep8 tests by typing:

```sh
tox -e pep8
```

# VI. Credits
[⇧ *Top*](#contents-page)
