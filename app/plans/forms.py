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
    Optional,
    DataRequired,
)
from .models import Plan
from ..utils.form import abort_on_validation_fail, RequiredIfNot
from ..exceptions import CronFormatError


class BasePlanForm(Form):
    category = StringField('Category', [DataRequired()])
    load_unit = StringField('Load Unit', [DataRequired()])

    private = BooleanField('Private', [Optional()])
    active = BooleanField('Active', [Optional()])

    title = StringField('Title', [DataRequired(), Length(min=2, max=50)])
    description = StringField('Description', [
        DataRequired(), Length(min=5, max=500)
    ])

    cron = StringField('Cron', [DataRequired()])
    start_at = DateTimeField('Start at', [DataRequired()])
    end_at = DateTimeField('End at', [
        RequiredIfNot(['total_load', 'daily_load'], use_and=False), Optional(),
    ])

    load_index = IntegerField('Load Index', [NumberRange(min=0)])
    total_load = IntegerField('Total Load', [
        RequiredIfNot(['daily_load', 'end_at'], use_and=False), Optional(),
        NumberRange(min=0)
    ])
    daily_load = IntegerField('Daily Load', [
        RequiredIfNot(['total_load', 'end_at'], use_and=False), Optional(),
        NumberRange(min=0)
    ])

    def validate_total_load(form, field):
        daily_load = form.daily_load.data
        cron = form.cron.data
        start_at = form.start_at.data
        end_at = form.end_at.data

        # validate only when necessity condition is met.
        if not (daily_load and cron and start_at and end_at):
            return

        try:
            given = field.data
            expected = Plan.get_total_load_from(
                daily_load=daily_load, cron=cron,
                start_at=start_at, end_at=end_at,
            )
            if given and given != expected:
                raise ValidationError(
                    'Inconsistent total load: expected {}, given {}'
                    .format(expected, given)
                )
        # validate only the field that the validator is responsible of.
        except CronFormatError:
            pass

    def validate_daily_load(form, field):
        total_load = form.total_load.data,
        cron = form.cron.data,
        start_at = form.start_at.data
        end_at = form.end_at.data

        # validate only when necessity condition is met.
        if not (total_load and cron and start_at and end_at):
            return

        try:
            given = field.data
            expected = Plan.get_daily_load_from(
                total_load=total_load, cron=cron,
                start_at=start_at, end_at=end_at,
            )
            if given and given != expected:
                raise ValidationError(
                    'Inconsistent daily load: expected {}, given {}'
                    .format(expected, given)
                )
        # validate only the field that the validator is responsible of.
        except CronFormatError:
            pass

    def validate_cron(form, field):
        try:
            croniter(field.data)
        except (ValueError, AttributeError):
            raise ValidationError(
                'Invalid cron format: given {}'
                .format(field.data)
            )

    def validate_end_at(form, field):
        total_load = form.total_load.data
        daily_load = form.daily_load.data
        cron = form.cron.data
        start_at = form.start_at.data

        # validate only when necessity condition is met.
        if not (total_load and daily_load and cron and start_at):
            return

        try:
            given = field.data
            expected = Plan.get_end_from(
                total_load=total_load,
                daily_load=daily_load,
                cron=cron, start_at=start_at
            )

            if given and given != expected:
                raise ValidationError(
                    'Inconsistent end: expected {}, given {}'
                    .format(expected, given)
                )
        # validate only the field that the validator is responsible of.
        except CronFormatError:
            pass


@abort_on_validation_fail
class PlanCreationForm(BasePlanForm):
    titles = FieldList(StringField('Stage Title', [Length(min=2, max=50)]))
    loads = FieldList(IntegerField('Stage Load', [NumberRange(min=0)]))

    def validate_titles(form, field):
        if (form.loads.data or field.data) and \
                len(form.loads.data) != len(field.data):
            raise ValidationError(
                'Length of titles and loads of plan stages' +
                'should be equal')

    def validate_loads(form, field):
        if (form.titles.data or field.data) and \
                len(form.titles.data) != len(field.data):
            raise ValidationError(
                'Length of titles and loads of plan stages' +
                'should be equal')


class PlanUpdateForm(BasePlanForm):
    pass


class BaseStageForm(Form):
    plan = IntegerField('Plan', [NumberRange(min=0)])
    title = StringField('Title', [Length(min=2, max=50)])
    load = IntegerField('Load', [NumberRange(min=0)])


class StageCreationForm(BaseStageForm):
    pass


class StageUpdateForm(BaseStageForm):
    pass
