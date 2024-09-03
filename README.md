### Hexlet tests and linter status:
[![Actions Status](https://github.com/AnastasiaTimoshe/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AnastasiaTimoshe/python-project-52/actions)

### Hexlet tests and linter status:
#[![Maintainability]()]()

#[![Test Coverage]()]()

# Task manager



Task Manager is a program that makes project management easier. But at the same time, you can use such software not only for project work, but also for everyday tasks. The task manager helps to check the effectiveness of employees, as well as set tasks and monitor their implementation.



This project was build using these tools:
1. python
2. poetry
3. flake8

It will be comfortable to use this application with these commands:
- to install: `pip install --user `
- to assemble package : `make build`
- to prepare your database : `make migrate`
- to run app : `make start`
- to run pytest : `make test`
- to run linter : `make lint`

To use the app properly you'll need to provide it with $DATABASE_URL (variable for connecting to the database) and $SECRET_KEY (your secret key formed Django) vars.