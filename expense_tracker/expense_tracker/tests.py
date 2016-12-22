import pytest
import transaction

from pyramid import testing

from .models import Expense, get_tm_session
from .models.meta import Base

import faker
import random
import datetime


@pytest.yield_fixture(scope="session")
def configuration():
    settings = {'sqlalchemy.url': 'sqlite:///:memory:'}
    config = testing.setUp(settings=settings)
    config.include('.models')
    yield config
    testing.tearDown()


@pytest.fixture()
def db_session(configuration, request):
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    dummy_request.dbsession.add_all(EXPENSES)

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


# ======== UNIT TESTS ==========

def test_new_expenses_are_added(db_session):
    """New expenses get added to the database."""
    db_session.add_all(EXPENSES)
    query = db_session.query(Expense).all()
    assert len(query) == len(EXPENSES)


def test_list_view_returns_empty_when_empty(dummy_request, add_models):
    from .views.default import list_view
    result = list_view(dummy_request)
    assert len(result["expenses"]) == 100

# ======== FUNCTIONAL TESTS ===========


@pytest.fixture
def testapp():
    from webtest import TestApp
    from expense_tracker import main

    app = main({}, **{"sqlalchemy.url": 'sqlite:///:memory:'})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(EXPENSES)


def test_home_route_has_table(testapp):
    """The home page has a table."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("table")) == 1


def test_home_route_with_data_has_filled_table(testapp, fill_the_db):
    """When there's data in the database, the home page has rows."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("tr")) == 101


def test_home_route_has_table2(testapp):
    """The home page has a table with no rows."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("tr")) == 1

