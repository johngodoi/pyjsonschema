"""
pyjsonschema.py is used to validate JSONs against a JSON Schema
"""

import re


class ValidationError(Exception):
    """Exception raised for errors from pyjsonschema.validate"""

    def __init__(self, message):
        self.message = message


def json2py(data_type):
    """
    Function to convert json data type to python data type
    """
    if type(data_type) is list:
        return [t for x in data_type for t in json2py(x)]  # flat_map
    return {
        "object": ["<class 'dict'>"],
        "number": ["<class 'int'>", "<class 'float'>"],
        "integer": ["<class 'int'>"],
        "string": ["<class 'str'>"],
        "array": ["<class 'list'>", "<class 'dict'>"],
        "null": ["<class 'NoneType'>"],
        "boolean": ["<class 'bool'>"]
    }.get(data_type, "Invalid type")


def validate(instance, schema):
    """
    Function to validate json schema
    """
    if type(instance) is list:
        for i in instance:
            validate(i, schema)
    else:
        for key in schema.keys():
            {
                'properties': check_properties,
                'not': check_not,
                'type': check_type,
                'required': check_required
            }.get(key, lambda ins, s: s)(instance, schema)


def check_properties(instance, schema):
    """
    Function to check properties from json schema
    """
    for key in schema['properties'].keys():
        if key in instance.keys():
            validate(instance[key], schema['properties'][key])


def check_not(instance, schema):
    """
    Function to check "not" tag from json schema
    """
    if instance in schema['not']['enum']:
        raise ValidationError("{} is not allowed for '{}'".format(instance, schema['not']))


def check_type(instance, schema):
    """
    Function to check data type from json schema
    """
    if str(type(instance)) not in json2py(schema['type']):
        raise ValidationError("{} is not of type '{}'".format(instance, schema['type']))
    check_string_type(instance, schema)
    check_number_type(instance, schema)


def check_required(instance, schema):
    """
    Function to check required fields from json schema
    """
    if len(schema['required']) > 0:
        for required in schema['required']:
            if required not in instance:
                raise ValidationError("'{}' is a required property".format(required))


def check_number_type(instance, schema):
    """
    Function to check number type from json schema
    """
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
    """
    Function to check string data type
    """
    if schema['type'] in ['string']:
        for key in schema.keys():
            check(({
                'minLength': lambda i, s, k: (len(i) < s[k], "{} length is smaller than {}".format(i, s[k])),
                'maxLength': lambda i, s, k: (len(i) > s[k], "{} length is bigger than {}".format(i, s[k])),
                'pattern': lambda i, s, k: (re.match(s[k], i) is None, "{} format is wrong".format(i, s[k]))
            }.get(key, contradiction)(instance, schema, key)))


def check(tpl):
    """
    Function to check tuple
    """
    if tpl[0]:
        raise ValidationError(tpl[1])


def contradiction(instance, schema, key):  # pylint: disable=unused-argument
    """
    Contradiction function
    """
    return False, ""
