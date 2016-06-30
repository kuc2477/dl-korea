import pytest
from app.users.models import User
from app.plans.models import Plan, Stage
from app.categories.models import Category, Unit


@pytest.fixture(scope='function')
def category(request, session):
    c = Category(name='test category')
    session.add(c)
    session.commit()

    def teardown():
        session.delete(c)
        session.commit()

    request.addfinalizer(teardown)
    return c


@pytest.fixture(scope='function')
def unit(request, session, category):
    u = Unit(category=category, name='test unit', integer=True)

    def teardown():
        session.delete(u)
        session.commit()

    request.addfinalizer(teardown)
    return u


@pytest.fixture(scope='function')
def user(request, session):
    u = User(
        email='testemail@test.com',
        firstname='testfirstname',
        lastname='testlastname',
        password='testpassword'
    )
    session.add(u)
    session.commit()

    def teardown():
        session.delete(u)
        session.commit()

    request.addfinalizer(teardown)
    return u


@pytest.fixture(scope='function')
def plan(request, session, user, category, unit):
    p = Plan(
        user=user, category=category, load_unit=unit,
        title='test plan title',
        description='test plan description',
        objective_load=10,
        objective_daily_load=1,
        cron=None
    )
    session.add(p)
    session.commit()

    def teardown():
        session.delete(p)
        session.commit()

    request.addfinalizer(teardown)
    return p


@pytest.fixture(scope='function')
def stage(request, session, plan):
    s = Stage(plan=plan, title='test stage', load=5)
    session.add(s)
    session.commit()

    def teardown():
        session.delete(s)
        session.commit()

    request.addfinalizer(teardown)
    return s
