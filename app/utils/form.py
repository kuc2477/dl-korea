from functools import (
    wraps,
    partial
)
from flask.ext.restful import abort


def abort_on_validation_fail(form_cls=None, code=400):
    if not form_cls:
        return partial(abort_on_validation_fail, code=code)

    validate = form_cls.validate

    @wraps(validate)
    def wrapper(self, *args, **kwargs):
        if not validate(self, *args, **kwargs):
            abort(code)
        else:
            return True

    form_cls.validate = wrapper
    return form_cls
