from croniter import croniter
from wtforms import (
    Form,
    StringField,
    IntegerField,
    BooleanField,
    DateTimeField,
    FieldList,
    ValidationError
)
from wtforms.validators import (
    NumberRange,
    Length,
    Optional
)
from .models import Plan
from ..utils.form import abort_on_validation_fail


class BasePlanForm(Form):
    category = IntegerField('Category', [NumberRange(min=0)])
    load_unit = IntegerField('Load Unit', [NumberRange(min=0)])

    private = BooleanField('Private', [Optional()])
    active = BooleanField('Active', [Optional()])

    title = StringField('Title', [Length(min=2, max=50)])
    description = StringField('Description', [Length(min=5, max=500)])

    load_index = IntegerField('Load Index', [NumberRange(min=0)])
    total_load = IntegerField('Total Load', [NumberRange(min=0)])
    daily_load = IntegerField('Daily Load', [NumberRange(min=0)])

    cron = StringField('Cron')
    start_at = DateTimeField('Start at')
    end_at = DateTimeField('End at')

    def valid_total_load(form, field):
        given = field.data
        expected = Plan.get_total_load_from(
            daily_load=form.daily_load.data,
            cron=form.cron.data,
            start_at=form.start_at.data,
            end_at=form.end_at.data,
        )
        if given and given != expected:
            raise ValidationError('Inconsistent total load')

    def valid_daily_load(form, field):
        given = field.data
        expected = Plan.get_daily_load_from(
            total_load=form.total_load.data,
            cron=form.cron.data,
            start_at=form.start_at.data,
            end_at=form.end_at.data,
        )
        if given and given != expected:
            raise ValidationError('Inconsistent daily load')

    def valid_end_at(form, field):
        given = field.data
        expected = Plan.get_end_from(
            total_load=form.total_load.data,
            daily_load=form.daily_load.data,
            cron=form.cron.data,
            start_at=form.start_at.data,
        )
        if given and given != expected:
            raise ValidationError('Inconsistent end at')

    def valid_cron(form, field):
        try:
            croniter(field.data)
        except ValueError:
            raise ValidationError('Invalid cron format')


@abort_on_validation_fail
class PlanCreationForm(BasePlanForm):
    titles = FieldList(StringField('Stage Title', [Length(min=2, max=50)]))
    loads = FieldList(IntegerField('Stage Load', [NumberRange(min=0)]))

    def valid_titles(form, field):
        if len(form.loads.data) != len(field.data):
            raise ValidationError(
                'Length of titles and loads of plan stages' +
                'should be equal')

    def valid_loads(form, field):
        if len(form.titles.data) != len(field.data):
            raise ValidationError(
                'Length of titles and loads of plan stages' +
                'should be equal')


@abort_on_validation_fail
class PlanUpdateForm(BasePlanForm):
    pass


class BaseStageForm(Form):
    plan = IntegerField('Plan', [NumberRange(min=0)])
    title = StringField('Title', [Length(min=2, max=50)])
    load = IntegerField('Load', [NumberRange(min=0)])


@abort_on_validation_fail
class StageCreationForm(BaseStageForm):
    pass


@abort_on_validation_fail
class StageUpdateForm(BaseStageForm):
    pass
