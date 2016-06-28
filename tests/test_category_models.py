from app.categories.models import Category, Unit


def test_category_attributes(category):
    assert(category.id)
    assert(category.name)


def test_category_creation(session):
    assert(not Category.query.all())
    c = Category(name='test name')
    session.add(c)
    session.commit()
    assert(c in session)


def test_category_deletion(session, category):
    assert(category in session)
    session.delete(category)
    session.commit()
    assert(category not in session)


def test_unit_attributes(unit):
    assert(unit.id)
    assert(unit.name)
    assert(unit.category)
    assert(hasattr(unit, 'integer'))


def test_unit_creation(session, category):
    assert(not Unit.query.all())
    u = Unit(category=category, name='test unit')
    session.add(u)
    session.commit()
    assert(u in session)


def test_unit_deletion(session, unit):
    assert(unit in session)
    session.delete(unit)
    session.commit()
    assert(unit not in session)
