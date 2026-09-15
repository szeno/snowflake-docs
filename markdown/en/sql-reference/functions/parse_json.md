Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Parsing)

# PARSE\_JSON

Interprets an input string as a JSON document, producing a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value.

You can use the PARSE\_JSON function when you have input data in JSON format. This function can convert
data from JSON format to [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) or [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) data and store that
data directly in a VARIANT value. You can then analyze or manipulate the data.

By default, the function doesn’t allow duplicate keys in the JSON object, but you can set the
`'parameter'` argument to allow duplicate keys.

See also:
:   [TRY\_PARSE\_JSON](/sql-reference/functions/try_parse_json)

## Syntax

Copy code

```
PARSE_JSON( <expr> [ , '<parameter>' ] )
```

## Arguments

**Required:**

`expr`
:   An expression of string type (for example, VARCHAR) that holds valid JSON information.

**Optional:**

`'parameter'`
:   String constant that specifies the parameter used to search for matches. Supported values:

    | Parameter | Description |
    | --- | --- |
    | `d` | Allow duplicate keys in JSON objects. If a JSON object contains a duplicate key, the returned object has a single instance of that key with the last value specified for that key. |
    | `s` | Don’t allow duplicate keys in JSON objects (strict). This value is the default. |

    Expand

    Show lessSee more

## Returns

Returns a value of type VARIANT that contains a JSON document.

If the input is NULL, the function returns NULL.

This function doesn’t return a [structured type](/sql-reference/data-types-structured).

## Usage notes

- This function supports an input expression with a maximum size of 64 MB compressed.
- If the PARSE\_JSON function is called with an empty string, or with a string containing only whitespace characters, then
  the function returns NULL (rather than raising an error), even though an empty string isn’t valid JSON. This behavior allows
  processing to continue rather than aborting if some inputs are empty strings.
- If the input is NULL, the output is also NULL. However, if the input string is `'null'`, then it is interpreted as a
  [JSON null](/user-guide/semistructured-considerations#label-variant-null) value so that the result isn’t SQL NULL, but instead a valid VARIANT value containing `null`.
  See the example below.
- When parsing decimal numbers, PARSE\_JSON attempts to preserve the exactness of the representation by treating 123.45 as NUMBER(5,2),
  not as a DOUBLE value. However, numbers that use scientific notation (for example, 1.2345e+02), or numbers that cannot be stored as fixed-point
  decimals due to range or scale limitations, are stored as DOUBLE values. Because JSON does not represent values such as TIMESTAMP, DATE,
  TIME, or BINARY natively, these values must be represented as strings.
- In JSON, an object (also called a “dictionary” or a “hash”) is an unordered set of
  key-value pairs.

- TO\_JSON and PARSE\_JSON are (almost) converse or reciprocal functions.

  - The PARSE\_JSON function takes a string as input and returns a JSON-compatible [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant).
  - The TO\_JSON function takes a JSON-compatible VARIANT and returns a string.

  The following is (conceptually) true if X is a string containing valid JSON:

  > `X = TO_JSON(PARSE_JSON(X));`

  For example, the following is (conceptually) true:

  > `'{"pi":3.14,"e":2.71}' = TO_JSON(PARSE_JSON('{"pi":3.14,"e":2.71}'))`

  However, the functions are not perfectly reciprocal because:

  - Empty strings, and strings with only whitespace, are not handled reciprocally. For example, the return value of
    `PARSE_JSON('')` is NULL, but the return value of `TO_JSON(NULL)` is NULL, not the reciprocal `''`.
  - The order of the key-value pairs in the string produced by TO\_JSON is not predictable.
  - The string produced by TO\_JSON can have less whitespace than the string passed to PARSE\_JSON.

  For example, the following are equivalent JSON, but not equivalent strings:

  - `{"pi": 3.14, "e": 2.71}`
  - `{"e":2.71,"pi":3.14}`

## Examples

The following examples use the PARSE\_JSON function.

### Storing values of different data types in a VARIANT column

This example stores different types of data in a VARIANT column by calling PARSE\_JSON to parse strings.

Create and fill a table. The INSERT statement uses PARSE\_JSON to insert VARIANT values in the `v` column
of the table.

Copy code

```
CREATE OR REPLACE TABLE vartab (n NUMBER(2), v VARIANT);

INSERT INTO vartab
  SELECT column1 AS n, PARSE_JSON(column2) AS v
    FROM VALUES (1, 'null'),
                (2, null),
                (3, 'true'),
                (4, '-17'),
                (5, '123.12'),
                (6, '1.912e2'),
                (7, '"Om ara pa ca na dhih"  '),
                (8, '[-1, 12, 289, 2188, false,]'),
                (9, '{ "x" : "abc", "y" : false, "z": 10} ')
       AS vals;
```

Query the data. The query uses the [TYPEOF](/sql-reference/functions/typeof) function to show the data types of
the values stored in the VARIANT values.

Copy code

```
SELECT n, v, TYPEOF(v)
  FROM vartab
  ORDER BY n;
```

```
+---+------------------------+------------+
| N | V                      | TYPEOF(V)  |
|---+------------------------+------------|
| 1 | null                   | NULL_VALUE |
| 2 | NULL                   | NULL       |
| 3 | true                   | BOOLEAN    |
| 4 | -17                    | INTEGER    |
| 5 | 123.12                 | DECIMAL    |
| 6 | 1.912000000000000e+02  | DOUBLE     |
| 7 | "Om ara pa ca na dhih" | VARCHAR    |
| 8 | [                      | ARRAY      |
|   |   -1,                  |            |
|   |   12,                  |            |
|   |   289,                 |            |
|   |   2188,                |            |
|   |   false,               |            |
|   |   undefined            |            |
|   | ]                      |            |
| 9 | {                      | OBJECT     |
|   |   "x": "abc",          |            |
|   |   "y": false,          |            |
|   |   "z": 10              |            |
|   | }                      |            |
+---+------------------------+------------+
```

### Insert a JSON object with duplicate keys in a VARIANT value

Try to insert a JSON object with duplicate keys in a VARIANT value:

Copy code

```
INSERT INTO vartab
SELECT column1 AS n, PARSE_JSON(column2) AS v
  FROM VALUES (10, '{ "a" : "123", "b" : "456", "a": "789"} ')
     AS vals;
```

An error is returned because duplicate keys aren’t allowed by default:

```
100069 (22P02): Error parsing JSON: duplicate object attribute "a", pos 31
```

Insert a JSON object with duplicate keys in a VARIANT value, and specify the `d` parameter to allow
duplicates:

Copy code

```
INSERT INTO vartab
SELECT column1 AS n, PARSE_JSON(column2, 'd') AS v
  FROM VALUES (10, '{ "a" : "123", "b" : "456", "a": "789"} ')
     AS vals;
```

```
+-------------------------+
| number of rows inserted |
|-------------------------|
|                       1 |
+-------------------------+
```

A query on the table shows that only the value of the last duplicate key was inserted:

Copy code

```
SELECT v
  FROM vartab
  WHERE n = 10;
```

```
+---------------+
| V             |
|---------------|
| {             |
|   "a": "789", |
|   "b": "456"  |
| }             |
+---------------+
```

# Handling NULL values with the PARSE\_JSON and TO\_JSON functions

The following example shows how PARSE\_JSON and TO\_JSON handle NULL values:

Copy code

```
SELECT TO_JSON(NULL), TO_JSON('null'::VARIANT),
       PARSE_JSON(NULL), PARSE_JSON('null');
```

```
+---------------+--------------------------+------------------+--------------------+
| TO_JSON(NULL) | TO_JSON('NULL'::VARIANT) | PARSE_JSON(NULL) | PARSE_JSON('NULL') |
|---------------+--------------------------+------------------+--------------------|
| NULL          | "null"                   | NULL             | null               |
+---------------+--------------------------+------------------+--------------------+
```

## Comparing PARSE\_JSON and TO\_JSON

The following examples demonstrate the relationship between the PARSE\_JSON and TO\_JSON functions.

This example creates a table with a VARCHAR column and a VARIANT column. The INSERT statement inserts
a VARCHAR value, and the UPDATE statement generates a JSON value that corresponds with that VARCHAR value.

Copy code

```
CREATE OR REPLACE TABLE jdemo2 (
  varchar1 VARCHAR,
  variant1 VARIANT);

INSERT INTO jdemo2 (varchar1) VALUES ('{"PI":3.14}');

UPDATE jdemo2 SET variant1 = PARSE_JSON(varchar1);
```

This query shows that TO\_JSON and PARSE\_JSON are conceptually reciprocal functions:

Copy code

```
SELECT varchar1,
       PARSE_JSON(varchar1),
       variant1,
       TO_JSON(variant1),
       PARSE_JSON(varchar1) = variant1,
       TO_JSON(variant1) = varchar1
  FROM jdemo2;
```

```
+-------------+----------------------+--------------+-------------------+---------------------------------+------------------------------+
| VARCHAR1    | PARSE_JSON(VARCHAR1) | VARIANT1     | TO_JSON(VARIANT1) | PARSE_JSON(VARCHAR1) = VARIANT1 | TO_JSON(VARIANT1) = VARCHAR1 |
|-------------+----------------------+--------------+-------------------+---------------------------------+------------------------------|
| {"PI":3.14} | {                    | {            | {"PI":3.14}       | True                            | True                         |
|             |   "PI": 3.14         |   "PI": 3.14 |                   |                                 |                              |
|             | }                    | }            |                   |                                 |                              |
+-------------+----------------------+--------------+-------------------+---------------------------------+------------------------------+
```

However, the functions are not exactly reciprocal. Differences in whitespace or in the order of key-value
pairs can prevent the output from matching the input. For example:

Copy code

```
SELECT TO_JSON(PARSE_JSON('{"b":1,"a":2}')),
       TO_JSON(PARSE_JSON('{"b":1,"a":2}')) = '{"b":1,"a":2}',
       TO_JSON(PARSE_JSON('{"b":1,"a":2}')) = '{"a":2,"b":1}';
```

```
+--------------------------------------+--------------------------------------------------------+--------------------------------------------------------+
| TO_JSON(PARSE_JSON('{"B":1,"A":2}')) | TO_JSON(PARSE_JSON('{"B":1,"A":2}')) = '{"B":1,"A":2}' | TO_JSON(PARSE_JSON('{"B":1,"A":2}')) = '{"A":2,"B":1}' |
|--------------------------------------+--------------------------------------------------------+--------------------------------------------------------|
| {"a":2,"b":1}                        | False                                                  | True                                                   |
+--------------------------------------+--------------------------------------------------------+--------------------------------------------------------+
```

### Comparing PARSE\_JSON and TO\_VARIANT

Although both the PARSE\_JSON function and the [TO\_VARIANT](/sql-reference/functions/to_variant) function can take a string and return
a VARIANT value, they are not equivalent. The following example creates a table with two VARIANT
columns. Then, it uses PARSE\_JSON to insert a value into one column and TO\_VARIANT to
insert a value into the other column.

Copy code

```
CREATE OR REPLACE TABLE jdemo3 (
  variant1 VARIANT,
  variant2 VARIANT);

INSERT INTO jdemo3 (variant1, variant2)
  SELECT
    PARSE_JSON('{"PI":3.14}'),
    TO_VARIANT('{"PI":3.14}');
```

The query below shows that the functions returned VARIANT values that
store values of different data types.

Copy code

```
SELECT variant1,
       TYPEOF(variant1),
       variant2,
       TYPEOF(variant2),
       variant1 = variant2
  FROM jdemo3;
```

```
+--------------+------------------+-----------------+------------------+---------------------+
| VARIANT1     | TYPEOF(VARIANT1) | VARIANT2        | TYPEOF(VARIANT2) | VARIANT1 = VARIANT2 |
|--------------+------------------+-----------------+------------------+---------------------|
| {            | OBJECT           | "{\"PI\":3.14}" | VARCHAR          | False               |
|   "PI": 3.14 |                  |                 |                  |                     |
| }            |                  |                 |                  |                     |
+--------------+------------------+-----------------+------------------+---------------------+
```
