Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Parsing)

# TRY\_PARSE\_JSON

A special version of [PARSE\_JSON](/sql-reference/functions/parse_json) that
returns a NULL value if an error occurs during parsing.

## Syntax

Copy code

```
TRY_PARSE_JSON( <expr> [ , '<parameter>' ] )
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

If the input is NULL or if an error occurs during parsing, the function returns NULL.

This function doesn’t return a [structured type](/sql-reference/data-types-structured).

## Usage notes

See [PARSE\_JSON](/sql-reference/functions/parse_json) for the usage notes.

## Examples

This shows an example of storing different types of data in a VARIANT column by calling TRY\_PARSE\_JSON to parse
strings that contain values that can be parsed as JSON:

Create and fill a table.

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE vartab (ID INTEGER, v VARCHAR);

INSERT INTO vartab (id, v) VALUES
  (1, '[-1, 12, 289, 2188, FALSE,]'),
  (2, '{ "x" : "abc", "y" : FALSE, "z": 10} '),
  (3, '{ "bad" : "json", "missing" : TRUE, "close_brace": 10 ');
```

Query the data, using TRY\_PARSE\_JSON. Note that the value for the third line is NULL. If the query used
PARSE\_JSON rather than TRY\_PARSE\_JSON, it would fail.

Copy code

```
SELECT ID, TRY_PARSE_JSON(v)
  FROM vartab
  ORDER BY ID;
```

```
+----+-------------------+
| ID | TRY_PARSE_JSON(V) |
|----+-------------------|
|  1 | [                 |
|    |   -1,             |
|    |   12,             |
|    |   289,            |
|    |   2188,           |
|    |   false,          |
|    |   undefined       |
|    | ]                 |
|  2 | {                 |
|    |   "x": "abc",     |
|    |   "y": false,     |
|    |   "z": 10         |
|    | }                 |
|  3 | NULL              |
+----+-------------------+
```

See [PARSE\_JSON](/sql-reference/functions/parse_json) for more examples.
