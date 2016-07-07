from datetime import datetime


def coerce_datetime(maybe_datetime):
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

    if maybe_datetime is None or isinstance(maybe_datetime, datetime):
        return maybe_datetime
    elif isinstance(maybe_datetime, str):
        return datetime.strptime(maybe_datetime, DATETIME_FORMAT)
    else:
        raise TypeError('Invalid datetime argument: {}'.format(maybe_datetime))
