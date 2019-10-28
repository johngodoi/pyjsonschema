import unittest

import pyjsonschema


class TestPyJsonSchema(unittest.TestCase):

    def test_instance_fields_not_declared_at_schema(self):
        instance = {"name": "Eggs", "alias": "huevos"}
        schema = {"type": "object", "properties": {"price": {"type": "number"}, "name": {"type": "string"}, }, }
        pyjsonschema.validate(instance, schema)

    def test_instance_fields_less_than_schema(self):
        instance = {"name": "Eggs"}
        schema = {"type": "object", "properties": {"price": {"type": "number"}, "name": {"type": "string"}, }, }
        pyjsonschema.validate(instance, schema)

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
        else:
            self.fail("Price value is not a number")

    def test_number_type_validation(self):
        pyjsonschema.validate(2, {"type": "number"})
        pyjsonschema.validate(-38, {"type": "number"})
        pyjsonschema.validate(1.5, {"type": "number"})
        pyjsonschema.validate(-4.5, {"type": "number"})
        pyjsonschema.validate(1.0, {"type": "number", "multipleOf": 1.0})
        pyjsonschema.validate(1.5, {"type": "number", "minimum": 1.1})
        pyjsonschema.validate(1.1, {"type": "number", "minimum": 1.1})
        pyjsonschema.validate(1.5, {"type": "number", "exclusiveMinimum": 1.1})
        pyjsonschema.validate(2.4, {"type": "number", "maximum": 2.5})
        pyjsonschema.validate(2.5, {"type": "number", "maximum": 2.5})
        pyjsonschema.validate(2.4, {"type": "number", "exclusiveMaximum": 2.5})
        # FIXME this is a bug
        # with self.assertRaises(pyjsonschema.ValidationError):
        #   pyjsonschema.validate([], {"type": "number"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate({}, {"type": "number"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(True, {"type": "number"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(None, {"type": "number"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate("1.5", {"type": "number"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(1.5, {"type": "number", "multipleOf": 1.0})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(1.0, {"type": "number", "minimum": 1.1})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(1.0, {"type": "number", "exclusiveMinimum": 1.1})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(1.1, {"type": "number", "exclusiveMinimum": 1.1})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(2.6, {"type": "number", "maximum": 2.5})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(2.5, {"type": "number", "exclusiveMaximum": 2.5})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(2.6, {"type": "number", "exclusiveMaximum": 2.5})

    def test_integer_type_validation(self):
        pyjsonschema.validate(2, {"type": "integer"})
        pyjsonschema.validate(-38, {"type": "integer"})
        pyjsonschema.validate(40, {"type": "integer", "multipleOf": 4})
        pyjsonschema.validate(1, {"type": "integer", "minimum": 1})
        pyjsonschema.validate(11, {"type": "integer", "minimum": 1})
        pyjsonschema.validate(5, {"type": "integer", "exclusiveMinimum": 1})
        pyjsonschema.validate(4, {"type": "integer", "maximum": 5})
        pyjsonschema.validate(5, {"type": "integer", "maximum": 5})
        pyjsonschema.validate(4, {"type": "integer", "exclusiveMaximum": 5})
        # FIXME this is a bug
        # with self.assertRaises(pyjsonschema.ValidationError):
        #   pyjsonschema.validate([], {"type": "integer"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate({}, {"type": "integer"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(True, {"type": "integer"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(None, {"type": "integer"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate("1.5", {"type": "integer"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(1.5, {"type": "integer"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(-6.5, {"type": "integer"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(5, {"type": "integer", "multipleOf": 2})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(-1, {"type": "integer", "minimum": 0})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(0, {"type": "integer", "exclusiveMinimum": 0})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(1, {"type": "integer", "exclusiveMinimum": 1})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(6, {"type": "integer", "maximum": 5})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(5, {"type": "integer", "exclusiveMaximum": 5})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(6, {"type": "integer", "exclusiveMaximum": 5})

    def test_string_type_validation(self):
        pyjsonschema.validate("", {"type": "string"})
        pyjsonschema.validate("Déjà vu", {"type": "string"})
        pyjsonschema.validate("42", {"type": "string"})
        pyjsonschema.validate("hi", {"type": "string"})
        pyjsonschema.validate("hi", {"type": "string", "minLength": 2})
        pyjsonschema.validate("Hello, World", {"type": "string", "minLength": 2})
        pyjsonschema.validate("hi", {"type": "string", "maxLength": 5})
        pyjsonschema.validate("Hello", {"type": "string", "maxLength": 5})
        pyjsonschema.validate("Hello", {"type": "string", "minLength": 2, "maxLength": 5})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate({}, {"type": "string"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(42, {"type": "string"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(None, {"type": "string"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate("H", {"type": "string", "minLength": 2})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate("Hello, World", {"type": "string", "maxLength": 2})
        # FIXME this is a bug
        # with self.assertRaises(pyjsonschema.ValidationError):
        #     pyjsonschema.validate([], {"type": "string"})

    def test_boolean_type_validation(self):
        pyjsonschema.validate(False, {"type": "boolean"})
        pyjsonschema.validate(True, {"type": "boolean"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate("true", {"type": "boolean"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(0, {"type": "boolean"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(1, {"type": "boolean"})

    def test_multiple_types_validation(self):
        pyjsonschema.validate(42, {"type": ["number", "string"]})
        pyjsonschema.validate("Life, the universe, and everything", {"type": ["number", "string"]})
        # FIXME this is a bug
        # with self.assertRaises(pyjsonschema.ValidationError):
        #    pyjsonschema.validate(["Life", "the universe", "and everything"],{"type": ["number", "string"]})

    def test_null_type_validation(self):
        pyjsonschema.validate(None, {"type": "null"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(1, {"type": "null"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(1.2, {"type": "null"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate("foo", {"type": "null"})
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate({}, {"type": "null"})
        # FIXME this is a bug
        # with self.assertRaises(pyjsonschema.ValidationError):
        #     pyjsonschema.validate([], {"type": "null"})

    def test_successful_types_validation(self):
        pyjsonschema.validate({}, {"type": "object"})
        pyjsonschema.validate([], {"type": "array"})

    def test_failure_types_validation(self):
        with self.assertRaises(pyjsonschema.ValidationError):
            pyjsonschema.validate(True, {"type": "object"})
        # FIXME this is a bug
        # with self.assertRaises(pyjsonschema.ValidationError):
        #     pyjsonschema.validate({}, {"type": "array"})

    def test_product_validate(self):
        instance = {
            "productId": 1,
            "productName": "A green door",
            "price": 12.50,
            "free_ship": True,
            "tags": ["home", "green"]
        }
        pyjsonschema.validate(instance, {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://example.com/product.schema.json",
            "title": "Product",
            "description": "A product in the catalog",
            "type": "object"
        })

        pyjsonschema.validate(instance, {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://example.com/product.schema.json",
            "title": "Product",
            "description": "A product from Acme's catalog",
            "type": "object",
            "properties": {
                "productId": {
                    "description": "The unique identifier for a product",
                    "type": "integer"
                }
            },
            "required": ["productId"]
        })

        pyjsonschema.validate(instance, {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://example.com/product.schema.json",
            "title": "Product",
            "description": "A product from Acme's catalog",
            "type": "object",
            "properties": {
                "productId": {
                    "description": "The unique identifier for a product",
                    "type": "integer"
                },
                "productName": {
                    "description": "Name of the product",
                    "type": "string"
                }
            },
            "required": ["productId", "productName"]
        })

    def test_product_validate_price_min(self):
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://example.com/product.schema.json",
            "title": "Product",
            "description": "A product from Acme's catalog",
            "type": "object",
            "properties": {
                "productId": {
                    "description": "The unique identifier for a product",
                    "type": "integer"
                },
                "productName": {
                    "description": "Name of the product",
                    "type": "string"
                },
                "price": {
                    "description": "The price of the product",
                    "type": "number",
                    "exclusiveMinimum": 0
                }
            },
            "required": ["productId", "productName", "price"]
        }
        try:
            pyjsonschema.validate({
                "productId": 1,
                "productName": "A green door",
                "price": -1,
                "tags": ["home", "green"]
            }, schema)
        except pyjsonschema.ValidationError as ve:
            self.assertEqual('-1 should be bigger than 0', ve.message)
        else:
            self.fail('Price is not bigger than 0')
        try:
            pyjsonschema.validate({
                "productId": 1,
                "productName": "A green door",
                "price": 0,
                "tags": ["home", "green"]
            }, schema)
        except pyjsonschema.ValidationError as ve:
            self.assertEqual('0 should be bigger than 0', ve.message)
        else:
            self.fail('Price is not bigger than 0')

