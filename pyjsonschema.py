class ValidationError(Exception):
    """Exception raised for errors from pyjsonschema.validate"""

    def __init__(self, message):
        self.message = message


def validate_required(instance, schema):
    if 'required' in schema:
        if len(schema['required']) > 0:
            for required in schema['required']:
                if required not in instance:
                    raise ValidationError("'{}' is a required property".format(required))


def json2py(tp):
    if type(tp) is list:
        return [t for x in tp for t in json2py(x)]
    return {
        "object": ["<class 'dict'>"],
        "number": ["<class 'int'>", "<class 'float'>"],
        "integer": ["<class 'int'>"],
        "string": ["<class 'str'>"],
        "array": ["<class 'list'>", "<class 'dict'>"],
        "boolean": ["<class 'bool'>"]
    }.get(tp, "Invalid type")


def validate(instance, schema):
    if type(instance) is list:
        for i in instance:
            validate(i, schema)
    else:
        validate_required(instance, schema)
        if 'type' in schema:
            if str(type(instance)) not in json2py(schema['type']):
                raise ValidationError("{} is not of type '{}'".format(instance, schema['type']))
            if schema['type'] in ['string']:
                if 'minLength' in schema:
                    if len(instance) < schema['minLength']:
                        raise ValidationError("{} length is smaller than {}".format(instance, schema['minLength']))
                if 'maxLength' in schema:
                    if len(instance) > schema['maxLength']:
                        raise ValidationError("{} length is bigger than {}".format(instance, schema['maxLength']))
            if schema['type'] in ['number', 'integer']:
                if 'multipleOf' in schema:
                    if instance % schema['multipleOf']:
                        raise ValidationError("{} should be multiple of {}".format(instance, schema['multipleOf']))
                if 'exclusiveMinimum' in schema:
                    if instance <= schema['exclusiveMinimum']:
                        raise ValidationError("{} should be bigger than {}".format(instance, schema['exclusiveMinimum']))
                if 'minimum' in schema:
                    if instance < schema['minimum']:
                        raise ValidationError("{} should be bigger than {}".format(instance, schema['minimum']))
                if 'exclusiveMaximum' in schema:
                    if instance >= schema['exclusiveMaximum']:
                        raise ValidationError("{} should be smaller than {}".format(instance, schema['exclusiveMaximum']))
                if 'maximum' in schema:
                    if instance > schema['maximum']:
                        raise ValidationError("{} should be smaller than {}".format(instance, schema['maximum']))
        if 'not' in schema:
            if instance in schema['not']['enum']:
                raise ValidationError("{} is not allowed for '{}'".format(instance, schema['not']))
        if 'properties' in schema:
            for key in schema['properties'].keys():
                validate(instance[key], schema['properties'][key])
