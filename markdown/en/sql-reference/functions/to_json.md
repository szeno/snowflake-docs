Categories:
:   [Conversion functions](/sql-reference/functions-conversion) , [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# TO\_JSON

Converts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to a string containing the JSON representation of the value.

## Syntax

Copy code

```
TO_JSON( <expr> )
```

## Arguments

`expr`
:   An expression of type VARIANT that holds valid JSON information.

## Returns

Returns a value of type VARCHAR.

If the input is NULL, the function returns NULL.

## Usage notes

- If the input is NULL, the output is also NULL. If the input is a VARIANT that contains [JSON null](/user-guide/semistructured-considerations#label-variant-null),
  then the returned value is the string `"null"` (i.e. the word “null” surrounded by double quotes). See the example below.
- A JSON object (also called a “dictionary” or a “hash”) is an
  unordered set of key-value pairs. When TO\_JSON produces a
  string, the order of the key-value pairs in that string is not predictable.

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

The following examples use the TO\_JSON function.

### Inserting VARIANT values and converting them to strings with a query

Create and fill a table. The INSERT statement uses the PARSE\_JSON function to insert
a VARIANT value in the `v` column of the table.

Copy code

```
CREATE OR REPLACE TABLE jdemo1 (v VARIANT);
INSERT INTO jdemo1 SELECT PARSE_JSON('{"food":"bard"}');
```

Query the data and use the TO\_JSON function to convert the VARIANT value to a string.

Copy code

```
SELECT v, v:food, TO_JSON(v) FROM jdemo1;
```

```
+------------------+--------+-----------------+
| V                | V:FOOD | TO_JSON(V)      |
|------------------+--------+-----------------|
| {                | "bard" | {"food":"bard"} |
|   "food": "bard" |        |                 |
| }                |        |                 |
+------------------+--------+-----------------+
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
