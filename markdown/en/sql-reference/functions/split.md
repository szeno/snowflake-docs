Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# SPLIT

Splits a given string with a given separator and returns the result in an array of strings.

Contiguous split strings in the source string, or the presence of a split string at the beginning
or end of the source string, results in an empty string in the output. An empty separator string results
in an array containing only the source string. If either parameter is a NULL, a NULL is returned.

You can use functions and constructs that operate on [arrays](/sql-reference/data-types-semistructured#label-data-type-array) on the result,
such as [FLATTEN](/sql-reference/functions/flatten), [ARRAY\_SIZE](/sql-reference/functions/array_size), and [access by index position](/sql-reference/data-types-semistructured#label-accessing-array-by-index).

See also:
:   [SPLIT\_PART](/sql-reference/functions/split_part)

## Syntax

Copy code

```
SPLIT(<string>, <separator>)
```

## Arguments

`string`
:   Text to be split into parts.

`separator`
:   Text to split string by.

## Returns

The data type of the returned value is ARRAY.

## Collation details

This function doesn’t support the following collation specifications:

- `pi` (punctuation-insensitive).
- `cs-ai` (case-sensitive, accent-insensitive).

The values in the output array don’t include a collation specification and therefore don’t support further
collation operations.

## Examples

Split the localhost IP address `127.0.0.1` into an array consisting of each of the four parts:

Copy code

```
SELECT SPLIT('127.0.0.1', '.');
```

```
+-------------------------+
| SPLIT('127.0.0.1', '.') |
|-------------------------|
| [                       |
|   "127",                |
|   "0",                  |
|   "0",                  |
|   "1"                   |
| ]                       |
+-------------------------+
```

Access the first element in the returned array by index position:

Copy code

```
SELECT SPLIT('127.0.0.1', '.')[0];
```

```
+----------------------------+
| SPLIT('127.0.0.1', '.')[0] |
|----------------------------|
| "127"                      |
+----------------------------+
```

Split a string that contains vertical lines as separators, which returns output
that contains empty strings:

Copy code

```
SELECT SPLIT('%a%|', '|');
```

```
+--------------------+
| SPLIT('|A||', '|') |
|--------------------|
| [                  |
|   "",              |
|   "a",             |
|   "",              |
|   ""               |
| ]                  |
+--------------------+
```

Use the result of SPLIT to generate multiple records from a single string using the LATERAL FLATTEN construct.
[FLATTEN](/sql-reference/functions/flatten) is a table function that takes a VARIANT, OBJECT, or ARRAY column and produces a lateral view
(that is, an inline view that contains correlation referring to other tables that precede it in the FROM clause):

Copy code

```
CREATE TABLE split_test_names(first_name VARCHAR, children VARCHAR);

INSERT INTO split_test_names values
  ('Mark', 'Marky,Mike,Maria'),
  ('John', 'Johnny,Jane');

SELECT * FROM split_test_names;
```

```
+------------+------------------+
| FIRST_NAME | CHILDREN         |
|------------+------------------|
| Mark       | Marky,Mike,Maria |
| John       | Johnny,Jane      |
+------------+------------------+
```

Copy code

```
SELECT first_name, C.value::STRING AS childname
  FROM split_test_names,
    LATERAL FLATTEN(INPUT=>SPLIT(children, ',')) C;
```

```
+------------+-----------+
| FIRST_NAME | CHILDNAME |
|------------+-----------|
| Mark       | Marky     |
| Mark       | Mike      |
| Mark       | Maria     |
| John       | Johnny    |
| John       | Jane      |
+------------+-----------+
```
