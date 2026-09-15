Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# OBJECT\_CONSTRUCT

Returns an [OBJECT](/sql-reference/data-types-semistructured) constructed from the arguments.

See also:
:   [OBJECT\_CONSTRUCT\_KEEP\_NULL](/sql-reference/functions/object_construct_keep_null) , [OBJECT\_CONSTRUCT\_KEEP\_NULL\_STRUCTURED](/sql-reference/functions/object_construct_keep_null_structured)

## Syntax

Copy code

```
OBJECT_CONSTRUCT( [<key>, <value> [, <key>, <value> , ...]] )

OBJECT_CONSTRUCT(*)
```

## Arguments

`key`
:   The key in a key-value pair. Each key is a VARCHAR value.

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

    You can also specify the wildcard in an [object constant](/sql-reference/data-types-semistructured#label-object-constant).

    For this function, the ILIKE and EXCLUDE keywords are valid only in a SELECT list or GROUP BY clause.

    For more information about the ILIKE and EXCLUDE keywords, see the “Parameters” section in [SELECT](/sql-reference/sql/select).

## Returns

Returns a value of type [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object).

## Usage notes

- If the key or value is NULL — that is, SQL NULL — the key-value pair is
  omitted from the resulting object. A key-value pair consisting of a
  string that isn’t NULL as the key and a JSON null as the value — that is,
  `PARSE_JSON('NULL')` — isn’t omitted. For more information, see
  [NULL values](/user-guide/semistructured-considerations#label-variant-null).
- The constructed object does not necessarily preserve the original order of the key-value pairs.
- In many contexts, you can use an [OBJECT constant](/sql-reference/data-types-semistructured#label-object-constant) (also called an *OBJECT literal*) instead of
  the OBJECT\_CONSTRUCT function.

## Examples

The following examples call the OBJECT\_CONSTRUCT function:

- [Construct a simple object](#construct-a-simple-object)
- [Construct objects by using the wildcard (\*) character](#construct-objects-by-using-the-wildcard-character)
- [Construct objects by using a SQL NULL and a JSON null](#construct-objects-by-using-a-sql-null-and-a-json-null)
- [Construct objects by using expressions](#construct-objects-by-using-expressions)
- [Construct nested OBJECT values](#construct-nested-object-values)

### Construct a simple object

This example shows how to construct a simple object:

Copy code

```
SELECT OBJECT_CONSTRUCT('a', 1, 'b', 'BBBB', 'c', NULL);
```

```
+--------------------------------------------------+
| OBJECT_CONSTRUCT('A', 1, 'B', 'BBBB', 'C', NULL) |
|--------------------------------------------------|
| {                                                |
|   "a": 1,                                        |
|   "b": "BBBB"                                    |
| }                                                |
+--------------------------------------------------+
```

### Construct objects by using the wildcard (\*) character

This example uses the wildcard character (`*`) to get the attribute name and the value from the FROM clause:

Copy code

```
CREATE OR REPLACE TABLE demo_table_1 (province VARCHAR, created_date DATE);
INSERT INTO demo_table_1 (province, created_date) VALUES
  ('Manitoba', '2024-01-18'::DATE),
  ('Alberta', '2024-01-19'::DATE);
```

Copy code

```
SELECT province, created_date
  FROM demo_table_1
  ORDER BY province;
```

```
+----------+--------------+
| PROVINCE | CREATED_DATE |
|----------+--------------|
| Alberta  | 2024-01-19   |
| Manitoba | 2024-01-18   |
+----------+--------------+
```

Copy code

```
SELECT OBJECT_CONSTRUCT(*) AS oc
  FROM demo_table_1
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

This example uses `*` and includes the ILIKE keyword to filter the output:

Copy code

```
SELECT OBJECT_CONSTRUCT(* ILIKE 'prov%') AS oc
  FROM demo_table_1
  ORDER BY oc['PROVINCE'];
```

```
+--------------------------+
| OC                       |
|--------------------------|
| {                        |
|   "PROVINCE": "Alberta"  |
| }                        |
| {                        |
|   "PROVINCE": "Manitoba" |
| }                        |
+--------------------------+
```

This example uses `*` and includes the EXCLUDE keyword to filter the output:

Copy code

```
SELECT OBJECT_CONSTRUCT(* EXCLUDE province) AS oc
  FROM demo_table_1
  ORDER BY oc['PROVINCE'];
```

```
+--------------------------------+
| OC                             |
|--------------------------------|
| {                              |
|   "CREATED_DATE": "2024-01-18" |
| }                              |
| {                              |
|   "CREATED_DATE": "2024-01-19" |
| }                              |
+--------------------------------+
```

This example is equivalent to the previous example, but it uses an object constant instead of
the OBJECT\_CONSTRUCT function:

Copy code

```
SELECT {* EXCLUDE province} AS oc
  FROM demo_table_1
  ORDER BY oc['PROVINCE'];
```

```
+--------------------------------+
| OC                             |
|--------------------------------|
| {                              |
|   "CREATED_DATE": "2024-01-18" |
| }                              |
| {                              |
|   "CREATED_DATE": "2024-01-19" |
| }                              |
+--------------------------------+
```

This is another example using `*`. In this case, attribute names are not specified, so Snowflake
uses `COLUMN1`, `COLUMN2`, and so on:

Copy code

```
SELECT OBJECT_CONSTRUCT(*) FROM VALUES(1,'x'), (2,'y');
```

```
+---------------------+
| OBJECT_CONSTRUCT(*) |
|---------------------|
| {                   |
|   "COLUMN1": 1,     |
|   "COLUMN2": "x"    |
| }                   |
| {                   |
|   "COLUMN1": 2,     |
|   "COLUMN2": "y"    |
| }                   |
+---------------------+
```

### Construct objects by using a SQL NULL and a JSON null

This example constructs an object by using SQL NULL and the string `'null'`:

Copy code

```
SELECT OBJECT_CONSTRUCT(
  'Key_One', PARSE_JSON('NULL'),
  'Key_Two', NULL,
  'Key_Three', 'null') AS obj;
```

```
+-----------------------+
| OBJ                   |
|-----------------------|
| {                     |
|   "Key_One": null,    |
|   "Key_Three": "null" |
| }                     |
+-----------------------+
```

For more information, see [NULL values](/user-guide/semistructured-considerations#label-variant-null).

### Construct objects by using expressions

OBJECT\_CONSTRUCT supports expressions and queries to add, modify, or omit values from the JSON object.

Copy code

```
SELECT OBJECT_CONSTRUCT(
    'foo', 1234567,
    'dataset_size', (SELECT COUNT(*) FROM demo_table_1),
    'distinct_province', (SELECT COUNT(DISTINCT province) FROM demo_table_1),
    'created_date_seconds', EXTRACT(epoch_seconds, created_date)
  )  AS json_object
  FROM demo_table_1;
```

```
+---------------------------------------+
| JSON_OBJECT                           |
|---------------------------------------|
| {                                     |
|   "created_date_seconds": 1705536000, |
|   "dataset_size": 2,                  |
|   "distinct_province": 2,             |
|   "foo": 1234567                      |
| }                                     |
| {                                     |
|   "created_date_seconds": 1705622400, |
|   "dataset_size": 2,                  |
|   "distinct_province": 2,             |
|   "foo": 1234567                      |
| }                                     |
+---------------------------------------+
```

### Construct nested OBJECT values

The following example creates a table and inserts OBJECT values with two levels of nesting:

Copy code

```
CREATE OR REPLACE TABLE sample_nested_object (
  id INTEGER,
  nested_object OBJECT);

INSERT INTO sample_nested_object (id, nested_object)
  SELECT 1,
         OBJECT_CONSTRUCT(
           'outer_key1', OBJECT_CONSTRUCT('inner_key1A', 'example1', 'inner_key1B', 'example2'),
           'outer_key2', OBJECT_CONSTRUCT('inner_key2', 5)
         );

INSERT INTO sample_nested_object (id, nested_object)
  SELECT 2,
         OBJECT_CONSTRUCT(
           'outer_key1', OBJECT_CONSTRUCT('inner_key1A', 'example3', 'inner_key1B', 'example4'),
           'outer_key2', OBJECT_CONSTRUCT('inner_key2', 7)
         );

SELECT * FROM sample_nested_object;
```

```
+----+--------------------------------+
| ID | NESTED_OBJECT                  |
+----+--------------------------------+
| 1  | {                              |
|    |   "outer_key1": {              |
|    |     "inner_key1A": "example1", |
|    |     "inner_key1B": "example2"  |
|    |   },                           |
|    |   "outer_key2": {              |
|    |     "inner_key2": 5            |
|    |   }                            |
|    | }                              |
| 2  | {                              |
|    |   "outer_key1": {              |
|    |     "inner_key1A": "example3", |
|    |     "inner_key1B": "example4"  |
|    |   },                           |
|    |   "outer_key2": {              |
|    |     "inner_key2": 7            |
|    |   }                            |
|    | }                              |
+----+--------------------------------+
```
