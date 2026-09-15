Categories:
:   [Table functions](/sql-reference/functions-table) , [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Extraction)

# FLATTEN

Flattens (explodes) compound values into multiple rows.

FLATTEN is a table function that takes a VARIANT, OBJECT, or ARRAY column and produces a lateral view — an inline view that contains
correlations to other tables that precede it in the [FROM](/sql-reference/constructs/from) clause.

FLATTEN can be used to convert semi-structured data to a relational representation.

## Syntax

Copy code

```
FLATTEN( INPUT => <expr> [ , PATH => <constant_expr> ]
                         [ , OUTER => TRUE | FALSE ]
                         [ , RECURSIVE => TRUE | FALSE ]
                         [ , MODE => 'OBJECT' | 'ARRAY' | 'BOTH' ] )
```

## Arguments

**Required:**

`INPUT => expr`
:   The expression that will be flattened into rows. The expression must be of data type VARIANT, OBJECT, or ARRAY.

**Optional:**

`PATH => constant_expr`
:   The path to the element within a VARIANT data structure that needs to be flattened. Can be a zero-length string (that is, an empty path) if the
    outermost element is to be flattened.

    Default: Zero-length string (empty path)

`OUTER => TRUE | FALSE`
:   - If `FALSE`, any input rows that can’t be expanded, either because they can’t be accessed in the path or because they have zero fields or entries, are completely omitted from the output.
    - If `TRUE`, exactly one row is generated for zero-row expansions (with NULL in the KEY, INDEX, and VALUE columns).

    Default: `FALSE`

    Note

    A zero-row expansion of an empty compound displays NULL in the `THIS` output column, distinguishing it from an attempt to expand a non-existing or wrong kind of compound.

`RECURSIVE => TRUE | FALSE`
:   - If `FALSE`, only the element referenced by `PATH` is expanded.
    - If `TRUE`, the expansion is performed for all sub-elements recursively.

    Default: `FALSE`

`MODE => 'OBJECT' | 'ARRAY' | 'BOTH'`
:   Specifies whether only objects, arrays, or both should be flattened.

    Default: `BOTH`

## Output

The returned rows consist of a fixed set of columns:

```
+-----+------+------+-------+-------+------+
| SEQ |  KEY | PATH | INDEX | VALUE | THIS |
|-----+------+------+-------+-------+------|
```

SEQ:
:   A unique sequence number associated with the input record; the sequence is not guaranteed to be gap-free or ordered in any particular way.

KEY:
:   For maps or objects, this column contains the key to the exploded value.

PATH:
:   The path to the element within a data structure that needs to be flattened.

INDEX:
:   The index of the element, if it is an array; otherwise NULL.

VALUE:
:   The value of the element of the flattened array/object.

THIS:
:   The element being flattened (useful in recursive flattening).

Note

The columns of the original (correlated) table that was used as the source of data for FLATTEN are also accessible. If a single row from the original table resulted in multiple rows in the flattened view, the values in this input row are replicated to match the number of rows produced by FLATTEN.

## Usage notes

- For single-level arrays, `TABLE(FLATTEN(...))` and `LATERAL FLATTEN(...)` produce the same
  result. For nested data structures where you need to chain multiple FLATTEN calls, use
  [LATERAL](/sql-reference/constructs/join-lateral) so that each subsequent FLATTEN can
  reference the output of the previous one.
- For information about using this function with [structured types](/sql-reference/data-types-structured), see
  [Using the FLATTEN function with values of structured types](/sql-reference/data-types-structured#label-structured-types-working-flatten).

## Examples

See also [Example: Using a lateral join with the FLATTEN table function](/user-guide/lateral-join-using#label-lateral-flatten-example) and [Using FLATTEN to Filter the Results in a WHERE Clause](/user-guide/querying-semistructured#label-using-flatten-where-clause).

The following simple example flattens one record (note that the middle element of the array is missing):

Copy code

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('[1, ,77]'))) f;
```

```
+-----+------+------+-------+-------+------+
| SEQ |  KEY | PATH | INDEX | VALUE | THIS |
|-----+------+------+-------+-------+------|
|   1 | NULL | [0]  |     0 |     1 | [    |
|     |      |      |       |       |   1, |
|     |      |      |       |       |   ,  |
|     |      |      |       |       |   77 |
|     |      |      |       |       | ]    |
|   1 | NULL | [2]  |     2 |    77 | [    |
|     |      |      |       |       |   1, |
|     |      |      |       |       |   ,  |
|     |      |      |       |       |   77 |
|     |      |      |       |       | ]    |
+-----+------+------+-------+-------+------+
```

The next two queries show the effect of the PATH parameter:

Copy code

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('{"a":1, "b":[77,88]}'), OUTER => TRUE)) f;
```

```
+-----+-----+------+-------+-------+-----------+
| SEQ | KEY | PATH | INDEX | VALUE | THIS      |
|-----+-----+------+-------+-------+-----------|
|     |     |      |       |       |   "a": 1, |
|     |     |      |       |       |   "b": [  |
|     |     |      |       |       |     77,   |
|     |     |      |       |       |     88    |
|     |     |      |       |       |   ]       |
|     |     |      |       |       | }         |
|   1 | b   | b    |  NULL | [     | {         |
|     |     |      |       |   77, |   "a": 1, |
|     |     |      |       |   88  |   "b": [  |
|     |     |      |       | ]     |     77,   |
|     |     |      |       |       |     88    |
|     |     |      |       |       |   ]       |
|     |     |      |       |       | }         |
+-----+-----+------+-------+-------+-----------+
```

Copy code

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('{"a":1, "b":[77,88]}'), PATH => 'b')) f;
```

```
+-----+------+------+-------+-------+-------+
| SEQ |  KEY | PATH | INDEX | VALUE | THIS  |
|-----+------+------+-------+-------+-------|
|   1 | NULL | b[0] |     0 |    77 | [     |
|     |      |      |       |       |   77, |
|     |      |      |       |       |   88  |
|     |      |      |       |       | ]     |
|   1 | NULL | b[1] |     1 |    88 | [     |
|     |      |      |       |       |   77, |
|     |      |      |       |       |   88  |
|     |      |      |       |       | ]     |
+-----+------+------+-------+-------+-------+
```

The next two queries show the effect of the OUTER parameter:

Copy code

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('[]'))) f;
```

```
+-----+-----+------+-------+-------+------+
| SEQ | KEY | PATH | INDEX | VALUE | THIS |
|-----+-----+------+-------+-------+------|
+-----+-----+------+-------+-------+------+
```

Copy code

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('[]'), OUTER => TRUE)) f;
```

```
+-----+------+------+-------+-------+------+
| SEQ |  KEY | PATH | INDEX | VALUE | THIS |
|-----+------+------+-------+-------+------|
|   1 | NULL |      |  NULL |  NULL | []   |
+-----+------+------+-------+-------+------+
```

The next two queries show the effect of the RECURSIVE parameter:

Copy code

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('{"a":1, "b":[77,88], "c": {"d":"X"}}'))) f;
```

```
+-----+-----+------+-------+------------+--------------+
| SEQ | KEY | PATH | INDEX | VALUE      | THIS         |
|-----+-----+------+-------+------------+--------------|
|   1 | a   | a    |  NULL | 1          | {            |
|     |     |      |       |            |   "a": 1,    |
|     |     |      |       |            |   "b": [     |
|     |     |      |       |            |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
|   1 | b   | b    |  NULL | [          | {            |
|     |     |      |       |   77,      |   "a": 1,    |
|     |     |      |       |   88       |   "b": [     |
|     |     |      |       | ]          |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
|   1 | c   | c    |  NULL | {          | {            |
|     |     |      |       |   "d": "X" |   "a": 1,    |
|     |     |      |       | }          |   "b": [     |
|     |     |      |       |            |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
+-----+-----+------+-------+------------+--------------+
```

Copy code

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('{"a":1, "b":[77,88], "c": {"d":"X"}}'),
                            RECURSIVE => TRUE )) f;
```

```
+-----+------+------+-------+------------+--------------+
| SEQ | KEY  | PATH | INDEX | VALUE      | THIS         |
|-----+------+------+-------+------------+--------------|
|   1 | a    | a    |  NULL | 1          | {            |
|     |      |      |       |            |   "a": 1,    |
|     |      |      |       |            |   "b": [     |
|     |      |      |       |            |     77,      |
|     |      |      |       |            |     88       |
|     |      |      |       |            |   ],         |
|     |      |      |       |            |   "c": {     |
|     |      |      |       |            |     "d": "X" |
|     |      |      |       |            |   }          |
|     |      |      |       |            | }            |
|   1 | b    | b    |  NULL | [          | {            |
|     |      |      |       |   77,      |   "a": 1,    |
|     |      |      |       |   88       |   "b": [     |
|     |      |      |       | ]          |     77,      |
|     |      |      |       |            |     88       |
|     |      |      |       |            |   ],         |
|     |      |      |       |            |   "c": {     |
|     |      |      |       |            |     "d": "X" |
|     |      |      |       |            |   }          |
|     |      |      |       |            | }            |
|   1 | NULL | b[0] |     0 | 77         | [            |
|     |      |      |       |            |   77,        |
|     |      |      |       |            |   88         |
|     |      |      |       |            | ]            |
|   1 | NULL | b[1] |     1 | 88         | [            |
|     |      |      |       |            |   77,        |
|     |      |      |       |            |   88         |
|     |      |      |       |            | ]            |
|   1 | c    | c    |  NULL | {          | {            |
|     |      |      |       |   "d": "X" |   "a": 1,    |
|     |      |      |       | }          |   "b": [     |
|     |      |      |       |            |     77,      |
|     |      |      |       |            |     88       |
|     |      |      |       |            |   ],         |
|     |      |      |       |            |   "c": {     |
|     |      |      |       |            |     "d": "X" |
|     |      |      |       |            |   }          |
|     |      |      |       |            | }            |
|   1 | d    | c.d  |  NULL | "X"        | {            |
|     |      |      |       |            |   "d": "X"   |
|     |      |      |       |            | }            |
+-----+------+------+-------+------------+--------------+
```

The following example shows the effect of the MODE parameter:

Copy code

```
SELECT * FROM TABLE(FLATTEN(INPUT => PARSE_JSON('{"a":1, "b":[77,88], "c": {"d":"X"}}'),
                            RECURSIVE => TRUE, MODE => 'OBJECT' )) f;
```

```
+-----+-----+------+-------+------------+--------------+
| SEQ | KEY | PATH | INDEX | VALUE      | THIS         |
|-----+-----+------+-------+------------+--------------|
|   1 | a   | a    |  NULL | 1          | {            |
|     |     |      |       |            |   "a": 1,    |
|     |     |      |       |            |   "b": [     |
|     |     |      |       |            |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
|   1 | b   | b    |  NULL | [          | {            |
|     |     |      |       |   77,      |   "a": 1,    |
|     |     |      |       |   88       |   "b": [     |
|     |     |      |       | ]          |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
|   1 | c   | c    |  NULL | {          | {            |
|     |     |      |       |   "d": "X" |   "a": 1,    |
|     |     |      |       | }          |   "b": [     |
|     |     |      |       |            |     77,      |
|     |     |      |       |            |     88       |
|     |     |      |       |            |   ],         |
|     |     |      |       |            |   "c": {     |
|     |     |      |       |            |     "d": "X" |
|     |     |      |       |            |   }          |
|     |     |      |       |            | }            |
|   1 | d   | c.d  |  NULL | "X"        | {            |
|     |     |      |       |            |   "d": "X"   |
|     |     |      |       |            | }            |
+-----+-----+------+-------+------------+--------------+
```

The following example explodes an array that is nested within another array. Create the following table:

Copy code

```
CREATE OR REPLACE TABLE persons AS
  SELECT column1 AS id, PARSE_JSON(column2) as c
    FROM values
      (12712555,
       '{ name:  { first: "John", last: "Smith"},
         contact: [
         { business:[
           { type: "phone", content:"555-1234" },
           { type: "email", content:"j.smith@example.com" } ] } ] }'),
      (98127771,
       '{ name:  { first: "Jane", last: "Doe"},
         contact: [
         { business:[
           { type: "phone", content:"555-1236" },
           { type: "email", content:"j.doe@example.com" } ] } ] }') v;
```

The following query uses multiple LATERAL FLATTEN calls. LATERAL is required here because the second
FLATTEN references the output of the first (`f.value:business`) call. Without LATERAL, the second FLATTEN
could not access columns from the first call.

Copy code

```
SELECT id as "ID",
    f.value AS "Contact",
    f1.value:type AS "Type",
    f1.value:content AS "Details"
  FROM persons p,
    LATERAL FLATTEN(INPUT => p.c, PATH => 'contact') f,
    LATERAL FLATTEN(INPUT => f.value:business) f1;
```

```
+----------+-----------------------------------------+---------+-----------------------+
|       ID | Contact                                 | Type    | Details               |
|----------+-----------------------------------------+---------+-----------------------|
| 12712555 | {                                       | "phone" | "555-1234"            |
|          |   "business": [                         |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "555-1234",            |         |                       |
|          |       "type": "phone"                   |         |                       |
|          |     },                                  |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "j.smith@example.com", |         |                       |
|          |       "type": "email"                   |         |                       |
|          |     }                                   |         |                       |
|          |   ]                                     |         |                       |
|          | }                                       |         |                       |
| 12712555 | {                                       | "email" | "j.smith@example.com" |
|          |   "business": [                         |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "555-1234",            |         |                       |
|          |       "type": "phone"                   |         |                       |
|          |     },                                  |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "j.smith@example.com", |         |                       |
|          |       "type": "email"                   |         |                       |
|          |     }                                   |         |                       |
|          |   ]                                     |         |                       |
|          | }                                       |         |                       |
| 98127771 | {                                       | "phone" | "555-1236"            |
|          |   "business": [                         |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "555-1236",            |         |                       |
|          |       "type": "phone"                   |         |                       |
|          |     },                                  |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "j.doe@example.com",   |         |                       |
|          |       "type": "email"                   |         |                       |
|          |     }                                   |         |                       |
|          |   ]                                     |         |                       |
|          | }                                       |         |                       |
| 98127771 | {                                       | "email" | "j.doe@example.com"   |
|          |   "business": [                         |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "555-1236",            |         |                       |
|          |       "type": "phone"                   |         |                       |
|          |     },                                  |         |                       |
|          |     {                                   |         |                       |
|          |       "content": "j.doe@example.com",   |         |                       |
|          |       "type": "email"                   |         |                       |
|          |     }                                   |         |                       |
|          |   ]                                     |         |                       |
|          | }                                       |         |                       |
+----------+-----------------------------------------+---------+-----------------------+
```
