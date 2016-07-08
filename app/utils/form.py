from collections import OrderedDict
from functools import (
    wraps,
    partial
)
from wtforms.validators import Required
from wtforms import ValidationError
from flask.ext.restful import abort


def abort_on_validation_fail(form_cls=None, code=400, detail=True):
    if not form_cls:
        return partial(abort_on_validation_fail, code=code, detail=detail)

    validate = form_cls.validate

    @wraps(validate)
    def wrapper(self, *args, **kwargs):
        if validate(self, *args, **kwargs):
            return True

        # if validation error details are not required, we will simply
        # abort the response
        if not detail:
            abort(code)
        # otherwise we will delegate response to the app's error handler
        # to respond with validation error details.
        else:
            ordered_errors = OrderedDict(self.errors)
            field_name, error_messages = ordered_errors.popitem(last=False)
            e = ValidationError('{}: {}'.format(field_name, error_messages[0]))
            e.code = code
            raise e

    form_cls.validate = wrapper
    return form_cls


class RequiredIf(Required):
    def __init__(self, other_field_names, use_and=True, *args, **kwargs):
        self.use_and = use_and
        self.other_field_names = other_field_names
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        condition_op = self._get_condition_op()
        condition_ok = condition_op([
            bool(field.data) for name, field in self._get_other_fields(form)
        ])

        # run validation conditionally
        if condition_ok:
            super(RequiredIf, self).__call__(form, field)

    def _get_condition_op(self):
        return all if self.use_and else any

    def _get_other_fields(self, form):
        # coerce given field name parameter into a list
        try:
            other_fields = [(n, form._fields.get(n)) for n in
                            self.other_field_names]
        except TypeError:
            other_fields = [(self.other_field_names,
                             form._fields.get(self.other_field_names))]

        # check field existence
        for name, field in other_fields:
            if field is None:
                raise ValueError('Field name {} not found'.format(name))

        return other_fields


class RequiredIfNot(RequiredIf):
    def __call__(self, form, field):
        condition_op = self._get_condition_op()
        condition_ok = condition_op([
            not bool(field.data) for name, field in
            self._get_other_fields(form)
        ])

        # run validation conditionally
        if condition_ok:
            super(RequiredIfNot, self).__call__(form, field)
