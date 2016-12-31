# Expense Tracker
A simple Pyramid app for listing and displaying expenses.

**Authors**:

- Nicholas Hunt-Walker (nhuntwalker@gmail.com)
- the class of Code Fellows Python 401d5

## Routes:

- `/` - the home page and a listing of all expenses
- `/new-expense` - to create a new expense
- `/expense/{id:\d+}` - the page for an individual expense
- `/expense/{id:\d+}/edit` - for editing existing expenses
- `/expense/{cat:\w+}` - list all expenses by category

## Usage:

- Clone this repository to your local machine.

- Once downloaded, `cd` into the `expense_tracker` directory.

- Begin a new Virtual Environment with Python 3 and activate it.

- `cd` into the next `expense_tracker` directory. It should be at the same level of `setup.py`

- `pip install` this package as well as the `testing` set of extras.

## To Test

- If you have the `testing` extras installed, testing is simple. If you're in the same directory as `setup.py` type the following.

```bash
$ py.test expense_tracker
```