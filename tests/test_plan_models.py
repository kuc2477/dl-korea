from datetime import datetime
from app.plans.models import Plan, Stage


def test_plan_attributes(plan):
    assert(plan.id)
    assert(plan.title)
    assert(plan.description)
    assert(hasattr(plan, 'private'))
    assert(hasattr(plan, 'active'))
    assert(plan.load_index)
    assert(plan.objective_load)
    assert(plan.objective_daily_load)
    assert(isinstance(plan.child_stage_ids, list))
    assert(plan.cron)
    assert(isinstance(plan.start_at, datetime))
    assert(plan.end_at is None or isinstance(plan.end_at, datetime))
    assert(isinstance(plan.created_at, datetime))
    assert(plan.updated_at is None or isinstance(plan.updated_at, datetime))


def test_plan_creation(session, user, category, unit):
    assert(not Plan.query.all())
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
    assert(p in session)


def test_plan_deletion(session, plan):
    assert(plan in session)
    session.delete(plan)
    session.commit()
    assert(plan not in session)


def test_stage_attributes(session, stage):
    assert(stage.id)
    assert(stage.title)
    assert(hasattr(stage, 'load'))
    assert(stage.user)
    assert(stage.category)
    assert(stage.load_unit)


def test_stage_creation(session, plan):
    assert(not Stage.query.all())
    s = Stage(plan=plan, title='test stage', load=5)
    session.add(s)
    session.commit()
    assert(s in session)


def test_stage_deletion(session, plan, stage):
    assert(stage in session)
    session.delete(stage)
    session.commit()
    assert(stage not in session)
