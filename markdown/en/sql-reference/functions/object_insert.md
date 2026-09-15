Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# OBJECT\_INSERT

Returns an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value consisting of the input OBJECT value with a new key-value pair inserted
(or an existing key updated with a new value).

## Syntax

Copy code

```
OBJECT_INSERT( <object> , <key> , <value> [ , <updateFlag> ] )
```

## Arguments

**Required:**

`object`
:   The source OBJECT value into which the new key-value pair is inserted or in which an existing key-value pair is updated.

`key`
:   The new key to be inserted into the OBJECT value or an existing key whose value is being updated. The specified key must
    be different from all existing keys in the OBJECT value, unless `updateFlag` is set to TRUE.

`value`
:   The value associated with the key.

**Optional:**

`updateFlag`
:   A Boolean flag that, when set to TRUE, specifies that the input value updates the value of an existing key in the
    OBJECT value, rather than inserting a new key-value pair.

    The default is FALSE.

## Returns

This function returns a value that has the OBJECT data type.

## Usage notes

- The function supports [JSON null](/user-guide/semistructured-considerations#label-variant-null) values, but not SQL NULL values or keys:

  - If `key` is any string other than NULL and `value` is a JSON null (for example, `PARSE_JSON('null')`),
    the key-value pair is inserted into the returned OBJECT value.
  - If either `key` or `value` is a SQL NULL, the key-value pair is omitted from the returned OBJECT value.
- If the optional `updateFlag` argument is set to TRUE, the existing input `key` is updated to the input `value`.
  If `updateFlag` is omitted or set to FALSE, calling this function with an input key that already exists in the OBJECT value results
  in an error.
- If the update flag is set to TRUE, but the corresponding key doesn’t already
  exist in the OBJECT value, then the key-value pair is added.
- For [structured OBJECT values](/sql-reference/data-types-structured):

  - For the arguments that are keys, you must specify constants.
  - When the `<updateFlag>` argument is FALSE (when you are inserting a new key-value pair):

    - If you specify a key that already exists in the OBJECT value, an error occurs.

      Copy code

      ```
      SELECT OBJECT_INSERT(
        {'city':'San Mateo','state':'CA'}::OBJECT(city VARCHAR,state VARCHAR),
        'city',
        'San Jose',
        false
      );
      ```

      ```
      093202 (23001): Function OBJECT_INSERT:
        expected structured object to not contain field city but it did.
      ```
    - The function returns a structured OBJECT value. The type of the OBJECT value includes the newly inserted key. For example, suppose that
      you add the `zipcode` key with the VARCHAR value `94402`:

      Copy code

      ```
      SELECT
        OBJECT_INSERT(
          {'city':'San Mateo','state':'CA'}::OBJECT(city VARCHAR,state VARCHAR),
          'zip_code',
          94402::VARCHAR,
          false
        ) AS new_object,
        SYSTEM$TYPEOF(new_object) AS type;
      ```

      ```
      +------------------------+---------------------------------------------------------------------+
      | NEW_OBJECT             | TYPE                                                                |
      |------------------------+---------------------------------------------------------------------|
      | {                      | OBJECT(city VARCHAR, state VARCHAR, zip_code VARCHAR NOT NULL)[LOB] |
      |   "city": "San Mateo", |                                                                     |
      |   "state": "CA",       |                                                                     |
      |   "zip_code": "94402"  |                                                                     |
      | }                      |                                                                     |
      +------------------------+---------------------------------------------------------------------+
      ```

      The type of the inserted value determines the type added to the OBJECT type definition. In this case, the value for
      `zipcode` is a value cast to a VARCHAR, so the type of `zipcode` is VARCHAR.
  - When the `<updateFlag>` argument is TRUE (when you are replacing an existing key-value pair):

    - If you specify a key that doesn’t exist in the OBJECT value, an error occurs.
    - The function returns a structured OBJECT value of the same type.
    - The type of the inserted value is [coerced](/sql-reference/data-types-structured#label-structured-types-casting-implicit) to the type of the existing key.

## Examples

The following examples call the OBJECT\_INSERT function:

- [Add and update key-value pairs](#add-and-update-key-value-pairs)
- [Add and update nested OBJECT values](#add-and-update-nested-object-values)

### Add and update key-value pairs

The examples use the following table:

Copy code

```
CREATE OR REPLACE TABLE object_insert_examples (object_column OBJECT);

INSERT INTO object_insert_examples (object_column)
  SELECT OBJECT_CONSTRUCT('a', 'value1', 'b', 'value2');

SELECT * FROM object_insert_examples;
```

```
+------------------+
| OBJECT_COLUMN    |
|------------------|
| {                |
|   "a": "value1", |
|   "b": "value2"  |
| }                |
+------------------+
```

#### Add a new key-value pair to an OBJECT value

Insert a third key-value pair into an OBJECT value that has two key-value pairs:

Copy code

```
UPDATE object_insert_examples
  SET object_column = OBJECT_INSERT(object_column, 'c', 'value3');

SELECT * FROM object_insert_examples;
```

```
+------------------+
| OBJECT_COLUMN    |
|------------------|
| {                |
|   "a": "value1", |
|   "b": "value2", |
|   "c": "value3"  |
| }                |
+------------------+
```

Insert two new key-value pairs into the OBJECT value, while omitting one key-value pair:

> - `d` consists of a JSON null value.
> - `e` consists of a SQL NULL value and is, therefore, omitted.
> - `f` consists of a string containing “null”.

Copy code

```
UPDATE object_insert_examples
  SET object_column = OBJECT_INSERT(object_column, 'd', PARSE_JSON('null'));

UPDATE object_insert_examples
  SET object_column = OBJECT_INSERT(object_column, 'e', NULL);

UPDATE object_insert_examples
  SET object_column = OBJECT_INSERT(object_column, 'f', 'null');

SELECT * FROM object_insert_examples;
```

```
+------------------+
| OBJECT_COLUMN    |
|------------------|
| {                |
|   "a": "value1", |
|   "b": "value2", |
|   "c": "value3", |
|   "d": null,     |
|   "f": "null"    |
| }                |
+------------------+
```

#### Update a key-value pair in an OBJECT value

Update an existing key-value pair (`"b": "value2"`) in the OBJECT value with a new value (`"valuex"`):

Copy code

```
UPDATE object_insert_examples
  SET object_column = OBJECT_INSERT(object_column, 'b', 'valuex', TRUE);

SELECT * FROM object_insert_examples;
```

```
+------------------+
| OBJECT_COLUMN    |
|------------------|
| {                |
|   "a": "value1", |
|   "b": "valuex", |
|   "c": "value3", |
|   "d": null,     |
|   "f": "null"    |
| }                |
+------------------+
```

### Add and update nested OBJECT values

The examples use the following table with nested OBJECT values:

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

#### Add new nested key-value pairs to the nested OBJECT values

The following example adds new nested key-value pairs to the nested OBJECT values in the table. It uses
a [CASE](/sql-reference/functions/case) expression to specify the added key-value pair for
each row:

Copy code

```
UPDATE sample_nested_object
  SET nested_object = OBJECT_INSERT(
    nested_object,
    'outer_key1',
     OBJECT_INSERT(
       nested_object:outer_key1,
       'inner_key1C',
       CASE
         WHEN id = 1 THEN 'added_value_1'
         WHEN id = 2 THEN 'added_value_2'
       END,
       TRUE
      ),
    TRUE);

SELECT * FROM sample_nested_object;
```

```
+----+------------------------------------+
| ID | NESTED_OBJECT                      |
|----+------------------------------------|
|  1 | {                                  |
|    |   "outer_key1": {                  |
|    |     "inner_key1A": "example1",     |
|    |     "inner_key1B": "example2",     |
|    |     "inner_key1C": "added_value_1" |
|    |   },                               |
|    |   "outer_key2": {                  |
|    |     "inner_key2": 5                |
|    |   }                                |
|    | }                                  |
|  2 | {                                  |
|    |   "outer_key1": {                  |
|    |     "inner_key1A": "example3",     |
|    |     "inner_key1B": "example4",     |
|    |     "inner_key1C": "added_value_2" |
|    |   },                               |
|    |   "outer_key2": {                  |
|    |     "inner_key2": 7                |
|    |   }                                |
|    | }                                  |
+----+------------------------------------+
```

#### Update key-value pairs in the nested OBJECT values

The following example updates nested key-value pairs in the OBJECT values in the table:

Copy code

```
UPDATE sample_nested_object
  SET nested_object = OBJECT_INSERT(
    nested_object,
    'outer_key2',
    OBJECT_INSERT(
      nested_object:outer_key2,
      'inner_key2',
      CASE
        WHEN id = 1 THEN 6
        WHEN id = 2 THEN 8
      END,
      TRUE),
    TRUE);

SELECT * FROM sample_nested_object;
```

```
+----+------------------------------------+
| ID | NESTED_OBJECT                      |
|----+------------------------------------|
|  1 | {                                  |
|    |   "outer_key1": {                  |
|    |     "inner_key1A": "example1",     |
|    |     "inner_key1B": "example2",     |
|    |     "inner_key1C": "added_value_1" |
|    |   },                               |
|    |   "outer_key2": {                  |
|    |     "inner_key2": 6                |
|    |   }                                |
|    | }                                  |
|  2 | {                                  |
|    |   "outer_key1": {                  |
|    |     "inner_key1A": "example3",     |
|    |     "inner_key1B": "example4",     |
|    |     "inner_key1C": "added_value_2" |
|    |   },                               |
|    |   "outer_key2": {                  |
|    |     "inner_key2": 8                |
|    |   }                                |
|    | }                                  |
+----+------------------------------------+
```
