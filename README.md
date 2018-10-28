# Expense Tracker

[![Build Status](https://travis-ci.org/nhuntwalker/expense_tracker.svg?branch=master)](https://travis-ci.org/nhuntwalker/expense_tracker)
[![Coverage Status](https://coveralls.io/repos/github/nhuntwalker/expense_tracker/badge.svg?branch=master)](https://coveralls.io/github/nhuntwalker/expense_tracker?branch=master)

A simple Pyramid app for listing and displaying expenses.

**Author**: Nicholas Hunt-Walker (nhuntwalker@gmail.com)

## Routes

- `/` - the home page and a listing of all expenses
- `/expense` - to create a new expense
- `/expense/{id:\d+}` - the page for an individual expense
- `/expense/{id:\d+}/edit` - for editing existing expenses
- `/expense/{id:\d+}/delete` - delete an existing expense
- `/expense/{category:\w+}` - list all expenses by category
- `/api/v1/expense` - JSON list of all existing expenses
- `/login` - log the user in
- `/logout` - log the user out

## Set Up and Installation

- Clone this repository to your machine.
- Once downloaded, `cd` into the `expense_tracker` directory.
- Begin a new virtual environment with Python 3 and activate it.
- `cd` into the next `expense_tracker` directory. You should land at the same level of `setup.py`
- `pip install -e .[testing]` this package as well as the set of extras into your environment.

### In Development

- `$ initialize_db development.ini` to initialize the database, populating with random models.
- `$ pserve development.ini --reload` to serve the application on `http://localhost:6543`

### In Production

- TBD

## To Test

- If you have the `testing` extras installed, testing is simple. If you're in the same directory as `setup.py` type the following:

```
$ py.test expense_tracker
```