Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Extraction)

# JSON\_EXTRACT\_PATH\_TEXT

Parses the first argument as a JSON string and returns the value of the element pointed to by the path in the second
argument. This is equivalent to `TO_VARCHAR(GET_PATH(PARSE_JSON(JSON), PATH))`

## Syntax

Copy code

```
JSON_EXTRACT_PATH_TEXT( <column_identifier> , '<path_name>' )
```

## Arguments

`column_identifier`
:   The name of the column with the data that you want to extract.

`path_name`
:   A string that contains the path to the element that you want to extract.

## Returns

The data type of the returned value is VARCHAR.

## Usage notes

- The function returns NULL if the path name does not correspond to any element.
- The path name syntax is standard JavaScript notation; it consists of a concatenation of field names (identifiers)
  preceded by periods (e.g. `.`) and index operators (e.g. `[<index>]`):

  - The first field name does not require the leading period to be specified.
  - The index values in the index operators can be non-negative integers (for arrays) or single or
    double-quoted string literals (for object fields).

  For more details, see [Querying Semi-structured Data](/user-guide/querying-semistructured).
- To maintain syntactic consistency, the path notation also supports SQL-style double-quoted identifiers, and use of
  `:` as path separators.

## Examples

Create a table and insert values:

> Copy code
>
> ```
> CREATE TABLE demo1 (id INTEGER, json_data VARCHAR);
> INSERT INTO demo1 SELECT
>    1, '{"level_1_key": "level_1_value"}';
> INSERT INTO demo1 SELECT
>    2, '{"level_1_key": {"level_2_key": "level_2_value"}}';
> INSERT INTO demo1 SELECT
>    3, '{"level_1_key": {"level_2_key": ["zero", "one", "two"]}}';
> ```

Use JSON\_EXTRACT\_PATH\_TEXT to extract a value from a simple 1-level string:

> Copy code
>
> ```
> SELECT 
>         TO_VARCHAR(GET_PATH(PARSE_JSON(json_data), 'level_1_key')) 
>             AS OLD_WAY,
>         JSON_EXTRACT_PATH_TEXT(json_data, 'level_1_key')
>             AS JSON_EXTRACT_PATH_TEXT
>     FROM demo1
>     ORDER BY id;
> +--------------------------------------+--------------------------------------+
> | OLD_WAY                              | JSON_EXTRACT_PATH_TEXT               |
> |--------------------------------------+--------------------------------------|
> | level_1_value                        | level_1_value                        |
> | {"level_2_key":"level_2_value"}      | {"level_2_key":"level_2_value"}      |
> | {"level_2_key":["zero","one","two"]} | {"level_2_key":["zero","one","two"]} |
> +--------------------------------------+--------------------------------------+
> ```

Use JSON\_EXTRACT\_PATH\_TEXT to extract a value from a 2-level string using a 2-level path:

> Copy code
>
> ```
> SELECT 
>         TO_VARCHAR(GET_PATH(PARSE_JSON(json_data), 'level_1_key.level_2_key'))
>             AS OLD_WAY,
>         JSON_EXTRACT_PATH_TEXT(json_data, 'level_1_key.level_2_key')
>             AS JSON_EXTRACT_PATH_TEXT
>     FROM demo1
>     ORDER BY id;
> +----------------------+------------------------+
> | OLD_WAY              | JSON_EXTRACT_PATH_TEXT |
> |----------------------+------------------------|
> | NULL                 | NULL                   |
> | level_2_value        | level_2_value          |
> | ["zero","one","two"] | ["zero","one","two"]   |
> +----------------------+------------------------+
> ```

This example contains an array:

> Copy code
>
> ```
> SELECT 
>       TO_VARCHAR(GET_PATH(PARSE_JSON(json_data), 'level_1_key.level_2_key[1]'))
>           AS OLD_WAY,
>       JSON_EXTRACT_PATH_TEXT(json_data, 'level_1_key.level_2_key[1]')
>           AS JSON_EXTRACT_PATH_TEXT
>     FROM demo1
>     ORDER BY id;
> +---------+------------------------+
> | OLD_WAY | JSON_EXTRACT_PATH_TEXT |
> |---------+------------------------|
> | NULL    | NULL                   |
> | NULL    | NULL                   |
> | one     | one                    |
> +---------+------------------------+
> ```
