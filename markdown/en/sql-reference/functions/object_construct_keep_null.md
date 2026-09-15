Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# OBJECT\_CONSTRUCT\_KEEP\_NULL

Returns an [OBJECT](/sql-reference/data-types-semistructured) constructed from the arguments
that retains key-value pairs with NULL values.

See also:
:   [OBJECT\_CONSTRUCT](/sql-reference/functions/object_construct), [OBJECT\_CONSTRUCT\_KEEP\_NULL\_STRUCTURED](/sql-reference/functions/object_construct_keep_null_structured)

## Syntax

Copy code

```
OBJECT_CONSTRUCT_KEEP_NULL( [<key>, <value> [, <key>, <value> , ...]] )

OBJECT_CONSTRUCT_KEEP_NULL(*)
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

    For this function, the ILIKE and EXCLUDE keywords are valid only in a SELECT list or GROUP BY clause.

    For more information about the ILIKE and EXCLUDE keywords, see the “Parameters” section in [SELECT](/sql-reference/sql/select).

## Returns

The data type of the returned value is [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object).

## Usage notes

- If the key is NULL (that is, SQL NULL), the key-value pair is omitted from the resulting object. However,
  if the value is NULL, then the key-value pair is kept.
- The constructed object does not necessarily preserve the original order of the key-value pairs.

## Examples

This example shows the difference between OBJECT\_CONSTRUCT and OBJECT\_CONSTRUCT\_KEEP\_NULL:

Copy code

```
SELECT OBJECT_CONSTRUCT('key_1', 'one', 'key_2', NULL) AS WITHOUT_KEEP_NULL,
       OBJECT_CONSTRUCT_KEEP_NULL('key_1', 'one', 'key_2', NULL) AS KEEP_NULL_1,
       OBJECT_CONSTRUCT_KEEP_NULL('key_1', 'one', NULL, 'two') AS KEEP_NULL_2;
```

```
+-------------------+-------------------+------------------+
| WITHOUT_KEEP_NULL | KEEP_NULL_1       | KEEP_NULL_2      |
|-------------------+-------------------+------------------|
| {                 | {                 | {                |
|   "key_1": "one"  |   "key_1": "one", |   "key_1": "one" |
| }                 |   "key_2": null   | }                |
|                   | }                 |                  |
+-------------------+-------------------+------------------+
```

The following example also shows the difference between OBJECT\_CONSTRUCT and OBJECT\_CONSTRUCT\_KEEP\_NULL, but this example
uses a small table (which is shown prior to the query):

Copy code

```
CREATE TABLE demo_table_1_with_nulls (province VARCHAR, created_date DATE);
INSERT INTO demo_table_1_with_nulls (province, created_date) VALUES
  ('Manitoba', '2024-01-18'::DATE),
  ('British Columbia', NULL),
  ('Alberta', '2024-01-19'::DATE),
  (NULL, '2024-01-20'::DATE);
```

Copy code

```
SELECT *
  FROM demo_table_1_with_nulls
  ORDER BY province;
```

```
+------------------+--------------+
| PROVINCE         | CREATED_DATE |
|------------------+--------------|
| Alberta          | 2024-01-19   |
| British Columbia | NULL         |
| Manitoba         | 2024-01-18   |
| NULL             | 2024-01-20   |
+------------------+--------------+
```

Copy code

```
SELECT OBJECT_CONSTRUCT(*) AS oc,
       OBJECT_CONSTRUCT_KEEP_NULL(*) AS oc_keep_null
  FROM demo_table_1_with_nulls
  ORDER BY oc_keep_null['PROVINCE'];
```

```
+----------------------------------+----------------------------------+
| OC                               | OC_KEEP_NULL                     |
|----------------------------------+----------------------------------|
| {                                | {                                |
|   "CREATED_DATE": "2024-01-19",  |   "CREATED_DATE": "2024-01-19",  |
|   "PROVINCE": "Alberta"          |   "PROVINCE": "Alberta"          |
| }                                | }                                |
| {                                | {                                |
|   "PROVINCE": "British Columbia" |   "CREATED_DATE": null,          |
| }                                |   "PROVINCE": "British Columbia" |
|                                  | }                                |
| {                                | {                                |
|   "CREATED_DATE": "2024-01-18",  |   "CREATED_DATE": "2024-01-18",  |
|   "PROVINCE": "Manitoba"         |   "PROVINCE": "Manitoba"         |
| }                                | }                                |
| {                                | {                                |
|   "CREATED_DATE": "2024-01-20"   |   "CREATED_DATE": "2024-01-20",  |
| }                                |   "PROVINCE": null               |
|                                  | }                                |
+----------------------------------+----------------------------------+
```

For examples that use the closely related function OBJECT\_CONSTRUCT, see [OBJECT\_CONSTRUCT](/sql-reference/functions/object_construct).
