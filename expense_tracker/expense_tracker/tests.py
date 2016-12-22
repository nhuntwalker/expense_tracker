import pytest
import transaction

from pyramid import testing

from .models import (
    Expense,
    get_engine,
    get_session_factory,
    get_tm_session,
)
from .models.meta import Base

import faker
import random
import datetime


# set up a SQL DB for the entire testing session.
@pytest.fixture(scope="session")
def sqlengine(request):
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include(".models")
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()

    request.addfinalizer(teardown)
    return session

fake = faker.Faker()

CATEGORIES = [
    "rent",
    "utilities",
    "groceries",
    "food",
    "diapers",
    "car loan",
    "netflix",
    "booze",
    "therapist"
]
EXPENSES = [Expense(
    item=fake.company(),
    amount=random.random() * random.randint(0, 1000),
    paid_to=fake.name(),
    category=random.choice(CATEGORIES),
    date=datetime.datetime.now(),
    description=fake.text(100),
) for i in range(100)]


@pytest.fixture
def http_request(new_session):
    the_request = testing.DummyRequest()
    the_request.dbsession = new_session
    return the_request


def test_new_expenses_are_added(new_session):
    """New expenses get added to the database."""

    query = new_session.query(Expense).all()
    assert len(query) == len(EXPENSES)


def test_list_view_returns_empty_when_empty(http_request):
    from .views.default import list_view
    result = list_view(http_request)
    assert len(result["expenses"]) == 0


# @pytest.fixture
# def testapp():
#     from webtest import TestApp
#     from expense_tracker import main

#     app = main({}, **{"sqlalchemy.url": 'sqlite:///:memory:'})
#     return TestApp(app)


# def test_home_route_has_table(testapp):
#     """The home page has a table."""
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert len(html.find_all("table")) == 1
