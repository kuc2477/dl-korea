from wtforms import (
    Form,
    StringField,
    IntegerField,
    BooleanField,
    FieldList,
    FormField,
)
from wtforms.validators import (
    URL,
    NumberRange,
    Length,
    Optional
)
from ..utils.form import abort_on_validation_fail


class BasePlanForm(Form):
    category = IntegerField('Category', [NumberRange(min=0)])
    load_unit = IntegerField('Load Unit', [NumberRange(min=0)])

    title = StringField('Title', [Length(min=2, max=50)])
    description = StringField('Description', [Length(min=5, max=500)])
    private = BooleanField('Private', [Optional()])
    active = BooleanField('Active', [Optional()])
    load_index = IntegerField('Load Index', [NumberRange(min=0)])
    objective_load = IntegerField('Objective Load', [NumberRange(min=0)])
    objective_daily_load = IntegerField('Objective Load', [NumberRange(min=0)])


class PlanCreationForm(BasePlanForm):
    pass


class PlanUpdateForm(BasePlanForm):
    pass


class BaseStageForm(Form):
    plan = IntegerField('Plan', [NumberRange(min=0)])
    title = StringField('Title', [Length(min=2, max=50)])
    load = IntegerField('Load', [NumberRange(min=0)])


class StageUpdateForm(BaseStageForm):
    pass
