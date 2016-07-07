from collections import OrderedDict
from functools import (
    wraps,
    partial
)
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
