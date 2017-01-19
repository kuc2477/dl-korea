from datetime import datetime
import pytest
from app.users.models import User


@pytest.fixture(scope='function')
def user(request, session):
    u = User(
        email='testemail@test.com',
        firstname='testfirstname',
        lastname='testlastname',
        password='testpassword',
        confirmed=True,
        confirmed_on=datetime.now(),
    )
    session.add(u)
    session.commit()

    def teardown():
        session.delete(u)
        session.commit()

    request.addfinalizer(teardown)
    return u
