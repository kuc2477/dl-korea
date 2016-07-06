def serialize(data, schema_cls, **kwargs):
    try:
        iter(data)
        many = True
    except TypeError:
        many = False

    schema = schema_cls(many=many, **kwargs)
    return schema.dump(data).data
