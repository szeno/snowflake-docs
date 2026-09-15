Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# FORMAT\_STRING\_TEMPLATE

Formats a string by substituting placeholders with values, providing type-aware string interpolation.

This function enables templated string construction with typed formatting specifications, similar to formatted string literals in other programming languages.

See also:
:   [CONCAT , ||](/sql-reference/functions/concat), [CONCAT\_WS](/sql-reference/functions/concat_ws)

## Syntax

Copy code

```
FORMAT_STRING_TEMPLATE( <template_string> , <value1> [ , <value2> ... ] )
```

## Arguments

`template_string`
:   A string containing placeholders that are replaced with formatted values. Placeholders use curly braces `{}` with optional format specifications.

`value1 [ , value2 ... ]`
:   One or more values to substitute into the template string. Values are matched to placeholders in order.

    The function supports full type handling for numeric, string, date, and other Snowflake data types.

## Returns

Returns a VARCHAR containing the formatted string with all placeholders replaced by the corresponding values.

## Usage notes

- Placeholders in the template string use curly braces `{}` and are replaced by the corresponding arguments in order.
- Format specifications within placeholders control how values are formatted (for example, number precision, padding, alignment).
- The locale flag `{:L}` is not supported and will cause an error if used.
- If the number of placeholders does not match the number of provided values, the function returns an error.

## Examples

Basic string interpolation:

Copy code

```
SELECT FORMAT_STRING_TEMPLATE('Hello, {}!', 'World');
```

```
+------------------------------------------------+
| FORMAT_STRING_TEMPLATE('HELLO, {}!', 'WORLD')  |
|------------------------------------------------|
| Hello, World!                                  |
+------------------------------------------------+
```

Format multiple values:

Copy code

```
SELECT FORMAT_STRING_TEMPLATE('{} has {} apples', 'Alice', 5);
```

```
+--------------------------------------------------------+
| FORMAT_STRING_TEMPLATE('{} HAS {} APPLES', 'ALICE', 5) |
|--------------------------------------------------------|
| Alice has 5 apples                                     |
+--------------------------------------------------------+
```

Format numbers with precision:

Copy code

```
SELECT FORMAT_STRING_TEMPLATE('Pi is approximately {:.2f}', 3.14159);
```

```
+--------------------------------------------------------------------+
| FORMAT_STRING_TEMPLATE('PI IS APPROXIMATELY {:.2F}', 3.14159)     |
|--------------------------------------------------------------------|
| Pi is approximately 3.14                                           |
+--------------------------------------------------------------------+
```

Use with table data:

Copy code

```
CREATE OR REPLACE TABLE products (name VARCHAR, price NUMBER(10,2), quantity NUMBER);
INSERT INTO products VALUES
  ('Widget', 19.99, 100),
  ('Gadget', 49.95, 50);

SELECT FORMAT_STRING_TEMPLATE('Product: {} - Price: ${:.2f} - Stock: {}', name, price, quantity) AS product_info
  FROM products;
```

```
+----------------------------------------------------+
| PRODUCT_INFO                                       |
|----------------------------------------------------|
| Product: Widget - Price: $19.99 - Stock: 100      |
| Product: Gadget - Price: $49.95 - Stock: 50       |
+----------------------------------------------------+
```
