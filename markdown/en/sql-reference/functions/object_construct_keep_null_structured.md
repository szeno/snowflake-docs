Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# OBJECT\_CONSTRUCT\_KEEP\_NULL\_STRUCTURED

Returns a [structured OBJECT](/sql-reference/data-types-structured) constructed from the arguments that retains
key-value pairs with NULL values.

Unlike [OBJECT\_CONSTRUCT\_KEEP\_NULL](/sql-reference/functions/object_construct_keep_null), which returns a semi-structured OBJECT, this function
always returns a structured `OBJECT(<key> <type>, ...)` value.

See also:
:   [OBJECT\_CONSTRUCT](/sql-reference/functions/object_construct), [OBJECT\_CONSTRUCT\_KEEP\_NULL](/sql-reference/functions/object_construct_keep_null)

## Syntax

Copy code

```
OBJECT_CONSTRUCT_KEEP_NULL_STRUCTURED( <key>, <value> [ , <key>, <value> , ... ] )

OBJECT_CONSTRUCT_KEEP_NULL_STRUCTURED(*)
```

## Arguments

`key`
:   The key in a key-value pair. Each key must be a non-empty constant VARCHAR value.

`value`
:   The value that is associated with the key. The value can be any data type.

`*`
:   When invoked with an asterisk (wildcard), the OBJECT value is constructed from the
    specified data using the attribute names as keys and the associated values as values.
    See the examples below.

    When you pass a wildcard to the function, you can qualify the wildcard with the name or alias for the table.
    For example, to pass in all of the columns from the table named `mytable`, specify the following:

    Copy code

    ```
    (mytable.*)
    ```

    You can also use the ILIKE and EXCLUDE keywords for filtering:

    - ILIKE filters for column names that match the specified pattern. Only one
      pattern is allowed. For example:

      Copy code

      ```
      (* ILIKE 'col1%')
      ```
    - EXCLUDE filters out column names that don’t match the specified column or columns. For example:

      Copy code

      ```
      (* EXCLUDE col1)

      (* EXCLUDE (col1, col2))
      ```

    Qualifiers are valid when you use these keywords. The following example uses the ILIKE keyword to
    filter for all of the columns that match the pattern `col1%` in the table `mytable`:

    Copy code

    ```
    (mytable.* ILIKE 'col1%')
    ```

    The ILIKE and EXCLUDE keywords can’t be combined in a single function call.

    For this function, the ILIKE and EXCLUDE keywords are valid only in a SELECT list or GROUP BY clause.

    For more information about the ILIKE and EXCLUDE keywords, see the “Parameters” section in [SELECT](/sql-reference/sql/select).

## Returns

Returns a [structured OBJECT](/sql-reference/data-types-structured) whose fields are the specified keys and whose
field types are the types of the associated values.

## Usage notes

- You must specify an even number of arguments (one or more key-value pairs). Specifying an odd number of arguments
  returns an error.
- Each key must be a non-empty constant VARCHAR value. A key that is NULL, empty, not a constant, or not a VARCHAR
  value returns an error.
- The keys must be unique. Specifying a duplicate key returns an error.
- If a value is NULL, the key-value pair is kept. A value that is an untyped NULL literal returns an error because
  the field type can’t be determined. To keep a NULL value, cast the value to a specific type (for example,
  `NULL::VARCHAR`).
- This function always returns a structured OBJECT, even when none of the input values are structured types.
- To construct a semi-structured OBJECT that retains key-value pairs with NULL values, use
  [OBJECT\_CONSTRUCT\_KEEP\_NULL](/sql-reference/functions/object_construct_keep_null).

## Examples

Construct a structured object, retaining the key-value pair with a NULL value:

Copy code

```
SELECT OBJECT_CONSTRUCT_KEEP_NULL_STRUCTURED('a', 1, 'b', NULL::VARCHAR) AS structured_object;
```

```
+-------------------+
| STRUCTURED_OBJECT |
|-------------------|
| {                 |
|   "a": 1,         |
|   "b": null       |
| }                 |
+-------------------+
```

Use the wildcard character (`*`) to construct a structured object from the columns of a table:

Copy code

```
CREATE OR REPLACE TABLE demo_table_structured (province VARCHAR, created_date DATE);
INSERT INTO demo_table_structured (province, created_date) VALUES
  ('Manitoba', '2024-01-18'::DATE),
  ('Alberta', '2024-01-19'::DATE);
```

Copy code

```
SELECT OBJECT_CONSTRUCT_KEEP_NULL_STRUCTURED(*) AS oc
  FROM demo_table_structured
  ORDER BY oc['PROVINCE'];
```

```
+---------------------------------+
| OC                              |
|---------------------------------|
| {                               |
|   "CREATED_DATE": "2024-01-19", |
|   "PROVINCE": "Alberta"         |
| }                               |
| {                               |
|   "CREATED_DATE": "2024-01-18", |
|   "PROVINCE": "Manitoba"        |
| }                               |
+---------------------------------+
```
