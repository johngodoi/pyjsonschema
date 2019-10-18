class ValidationError(Exception):
    """Exception raised for errors from pyjsonschema.validate"""

    def __init__(self, message):
        self.message = message


def json2py(tp):
    if type(tp) is list:
        return [t for x in tp for t in json2py(x)]
    return {
        "object": ["<class 'dict'>"],
        "number": ["<class 'int'>", "<class 'float'>"],
        "integer": ["<class 'int'>"],
        "string": ["<class 'str'>"],
        "array": ["<class 'list'>", "<class 'dict'>"],
        "null": ["<class 'NoneType'>"],
        "boolean": ["<class 'bool'>"]
    }.get(tp, "Invalid type")


def validate(instance, schema):
    if type(instance) is list:
        for i in instance:
            validate(i, schema)
    else:
        check_required(instance, schema)
        check_type(instance, schema)
        check_not(instance, schema)
        check_properties(instance, schema)


def check_properties(instance, schema):
    if 'properties' in schema:
        for key in schema['properties'].keys():
            validate(instance[key], schema['properties'][key])


def check_not(instance, schema):
    if 'not' in schema:
        if instance in schema['not']['enum']:
            raise ValidationError("{} is not allowed for '{}'".format(instance, schema['not']))


def check_type(instance, schema):
    if 'type' in schema:
        if str(type(instance)) not in json2py(schema['type']):
            raise ValidationError("{} is not of type '{}'".format(instance, schema['type']))
        check_string_type(instance, schema)
        check_number_type(instance, schema)


def check_number_type(instance, schema):
    if schema['type'] in ['number', 'integer']:
        for key in schema.keys():
            check(({
                'multipleOf': lambda i, s, k: (i % s[k], "{} should be multiple of {}".format(i, s[k])),
                'exclusiveMinimum': lambda i, s, k: (i <= s[k], "{} should be bigger than {}".format(i, s[k])),
                'minimum': lambda i, s, k: (i < s[k], "{} should be bigger than {}".format(i, s[k])),
                'exclusiveMaximum': lambda i, s, k: (i >= s[k], "{} should be smaller than {}".format(i, s[k])),
                'maximum': lambda i, s, k: (i > s[k], "{} should be smaller than {}".format(i, s[k]))
            }.get(key, contradiction)(instance, schema, key)))


def check_string_type(instance, schema):
    if schema['type'] in ['string']:
        for key in schema.keys():
            check(({
                'minLength': lambda i, s, k: (len(i) < s[k],"{} length is smaller than {}".format(i, s[k])),
                'maxLength': lambda i, s, k: (len(i) > s[k],"{} length is bigger than {}".format(i, s[k]))
            }.get(key, contradiction)(instance, schema, key)))


def check_required(instance, schema):
    if 'required' in schema:
        if len(schema['required']) > 0:
            for required in schema['required']:
                if required not in instance:
                    raise ValidationError("'{}' is a required property".format(required))


def check(tpl):
    if tpl[0]:
        raise ValidationError(tpl[1])


def contradiction(instance, schema, key):
    return False, ""
