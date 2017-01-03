"""A short testing suite for the expense tracker."""


import pytest
import transaction

from pyramid import testing

from .models import Expense, get_tm_session
from .models.meta import Base

import faker
import random
import datetime


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:'}  # points to an in-memory database.
    config = testing.setUp(settings=settings)
    config.include('.models')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture()
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
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
    """Instantiate a fake HTTP Request, complete with a database session.

    This is a function-level fixture, so every new request will have a
    new database session.
    """
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    """Add a bunch of model instances to the database.

    Every test that includes this fixture will add new random expenses.
    """
    dummy_request.dbsession.add_all(EXPENSES)

# instantiate a Faker object for producing fake names, companies, and text.
FAKE = faker.Faker()

# create a list of categories with which I can organize my expenses.
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

# create a bunch of Expense model instances with randomized attributes and
# put them into a list that is globally available.
# this could also just be made into a fixture.
EXPENSES = [Expense(
    item=FAKE.company(),
    amount=random.random() * random.randint(0, 1000),
    paid_to=FAKE.name(),
    category=random.choice(CATEGORIES),
    date=datetime.datetime.now(),
    description=FAKE.text(100),
) for i in range(100)]


# ======== UNIT TESTS ==========

def test_new_expenses_are_added(db_session):
    """New expenses get added to the database."""
    db_session.add_all(EXPENSES)
    query = db_session.query(Expense).all()
    assert len(query) == len(EXPENSES)


def test_list_view_returns_empty_when_empty(dummy_request):
    """Test that the list view returns no objects in the expenses iterable."""
    from .views.default import list_view
    result = list_view(dummy_request)
    assert len(result["expenses"]) == 0


def test_list_view_returns_objects_when_exist(dummy_request, add_models):
    """Test that the list view does return objects when the DB is populated."""
    from .views.default import list_view
    result = list_view(dummy_request)
    assert len(result["expenses"]) == 100

# ======== FUNCTIONAL TESTS ===========


@pytest.fixture
def testapp():
    """Create an instance of webtests TestApp for testing routes.

    With the alchemy scaffold we need to add to our test application the
    setting for a database to be used for the models.
    We have to then set up the database by starting a database session.
    Finally we have to create all of the necessary tables that our app
    normally uses to function.

    The scope of the fixture is function-level, so every test will get a new
    test application.
    """
    from webtest import TestApp
    from expense_tracker import main

    app = main({}, **{"sqlalchemy.url": 'sqlite:///:memory:'})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture
def set_auth_credentials():
    """Make a username/password combo for testing."""
    import os
    from passlib.apps import custom_app_context as pwd_context

    os.environ["AUTH_USERNAME"] = "testme"
    os.environ["AUTH_PASSWORD"] = pwd_context.hash("foobar")


@pytest.fixture
def fill_the_db(testapp):
    """Fill the database with some model instances.

    Start a database session with the transaction manager and add all of the
    expenses. This will be done anew for every test.
    """
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(EXPENSES)


def test_home_route_has_table(testapp):
    """The home page has a table in the html."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("table")) == 1


def test_home_route_with_data_has_filled_table(testapp, fill_the_db):
    """When there's data in the database, the home page has some rows."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("tr")) == 101


def test_home_route_has_table2(testapp):
    """Without data the home page only has the header row in its table."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("tr")) == 1

# ======== TESTING WITH SECURITY ==========


def test_create_route_is_forbidden(testapp):
    """Any old user shouldn't be able to access the create view."""
    response = testapp.get("/new-expense", status=403)
    assert response.status_code == 403


def test_auth_app_can_see_create_route(set_auth_credentials, testapp):
    """A logged-in user should be able to access the create view."""
    response = testapp.post("/login", params={
        "username": "testme",
        "password": "foobar"
    })
    response = testapp.get("/new-expense")
    assert response.status_code == 200
