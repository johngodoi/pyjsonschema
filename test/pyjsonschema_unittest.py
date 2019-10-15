import unittest

import pyjsonschema


class TestPyJsonSchema(unittest.TestCase):

    def test_simple_success(self):
        instance = {"name": "Eggs", "price": 34.99}
        schema = {"type": "object", "properties": {"price": {"type": "number"}, "name": {"type": "string"}, }, }
        pyjsonschema.validate(instance, schema)

    def test_simple_failure(self):
        instance = {"name": "Eggs", "price": "Invalid"}
        schema = {"type": "object", "properties": {"price": {"type": "number"}, "name": {"type": "string"}, }, }
        try:
            pyjsonschema.validate(instance, schema)
        except pyjsonschema.ValidationError as ve:
            self.assertEqual("Invalid is not of type 'number'", ve.message)


