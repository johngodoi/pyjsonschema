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

    def test_types_validation(self):
        pyjsonschema.validate(True, {"type": "boolean"})
        pyjsonschema.validate({}, {"type": "object"})
        pyjsonschema.validate(1.5, {"type": "number"})
        pyjsonschema.validate(5, {"type": "integer"})
        pyjsonschema.validate("hi", {"type": "string"})
        pyjsonschema.validate([], {"type": "array"})

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
            "required": [ "productId" ]
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
        with self.assertRaises(pyjsonschema.ValidationError) as context:
            pyjsonschema.validate({
                "productId": 1,
                "productName": "A green door",
                "price": -1,
                "tags": ["home", "green"]
            }, schema)
        self.assertEqual('-1 should be bigger than 0', context.exception.message)
        with self.assertRaises(pyjsonschema.ValidationError) as context:
            pyjsonschema.validate({
                "productId": 1,
                "productName": "A green door",
                "price": 0,
                "tags": ["home", "green"]
            }, schema)
        self.assertEqual('0 should be bigger than 0', context.exception.message)

