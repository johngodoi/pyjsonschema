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


def json2py(t):
    if t == "object":
        return ["<class 'dict'>"]
    if t == "number":
        return ["<class 'int'>", "<class 'float'>"]
    if t == "string":
        return ["<class 'str'>"]
    if t == "array":
        return ["<class 'list'>", "<class 'dict'>"]


def validate(instance, schema):
    if type(instance) is list:
        for i in instance:
            validate(i, schema)
    else:
        validate_required(instance, schema)
        if 'type' in schema:
            if str(type(instance)) not in json2py(schema['type']):
                raise ValidationError("{} is not of type '{}'".format(instance, schema['type']))
        if 'not' in schema:
            if instance in schema['not']['enum']:
                raise ValidationError("{} is not allowed for '{}'".format(instance, schema['not']))
        if 'properties' in schema:
            for key in schema['properties'].keys():
                validate(instance[key], schema['properties'][key])
