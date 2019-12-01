# pyjsonschema
This project is based on jsonschema python library. The difference is that it doesn't aim in the performance but being a library that can be used anywhere without needing to specify the OS.

We aim to implement the entire https://json-schema.org specification. 

https://json-schema.org/understanding-json-schema/ gives an overview of the features expected for jsonschema validation.
And so far that has been our reference.

* JSON Schema Reference

  *  [ ]  Type-specific keywords
        *  [x]  string
        *  [x]  Length
        *  [ ]  Regular Expressions
        *  [x]  Format
  *  [ ]  Regular Expressions
        *  [ ]  Example
  *  [ ]  Numeric types
        *  [x]  integer
        *  [x]  number
        *  [x]  Multiples
        *  [x]  Range
  *  [ ]  object
        *  [x]  Properties
        *  [x]  Required Properties
        *  [ ]  Property names
        *  [ ]  Size
        *  [ ]  Dependencies
        *  [ ]  Pattern Properties
  *  [ ]  array
        *  [ ]  Items
        *  [ ]  Length
        *  [ ]  Uniqueness
  *  [x]  boolean
  *  [x]  null
  *  [ ]  Generic keywords
        *  [ ]  Annotations
        *  [ ]  Comments
        *  [x]  Enumerated values
        *  [ ]  Constant values
  *  [ ]  Media: string-encoding non-JSON data
        *  [ ]  contentMediaType
        *  [ ]  contentEncoding
        *  [ ]  Examples
  *  [ ]  Combining schemas
        *  [ ]  allOf
        *  [ ]  anyOf
        *  [ ]  oneOf
        *  [ ]  not
  *  [ ]  Applying subschemas conditionally
     *  [ ]  The $schema keyword
        *  [ ]  Advanced
*  [ ]  Structuring a complex schema
     *  [ ]  Reuse
        *  [ ]  Recursion
     *  [ ]  The $id property
        *  [ ]  Using $id with $ref
     *  [ ]  Extending