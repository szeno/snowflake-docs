# Vertica - Predicates

## ALL & ANY array expressions

### Description

An expression used to **evaluate and compare** each element of an array against a specified expression. ([Vertica Language Reference ANY & ALL (array)](https://docs.vertica.com/23.4.x/en/sql-reference/language-elements/predicates/any-and-all/))

### Grammar Syntax

Copy code

```
:force:
expression operator ANY (array expression)
expression operator ALL (array expression)
```

To support this expression the `<> ALL` is translated to `NOT IN` and the `= ANY` to `IN`

### Sample Source Patterns

#### Input Code:

Copy code

```
SELECT some_column <> ALL (ARRAY[1, 2, 3])
FROM some_table;

SELECT *
FROM someTable
WHERE column_name = ANY (ARRAY[1, 2, 3]);
```

#### Output Code:

Copy code

```
SELECT some_column NOT IN (1, 2, 3)
FROM some_table;

SELECT *
 FROM someTable
 WHERE column_name IN (1, 2, 3);
```

#### Known Issues

There are no known issues

#### Related EWIs

There are no related EWIs.

## LIKE

LIKE Predicate

### Description

> Retrieves rows where a string expression—typically a column—matches the specified pattern or, if qualified by ANY or ALL, set of patterns ([Vertica SQL Language Reference Like Predicate](https://docs.vertica.com/23.4.x/en/sql-reference/language-elements/predicates/like/))

### Grammar Syntax

Copy code

```
 string-expression [ NOT ] { LIKE | ILIKE | LIKEB | ILIKEB }
   { pattern | { ANY | SOME | ALL } ( pattern,... ) } [ ESCAPE 'char' ]
```

#### Vertica Substitute symbols

| Symbol | Vertica Equivalent | Snowflake Equivalent |
| --- | --- | --- |
| ~~ | LIKE | LIKE |
| ~# | LIKEB | LIKE |
| ~~\* | ILIKE | ILIKE |
| ~#\* | ILIKEB | ILIKE |
| !~~ | NOT LIKE | NOT LIKE |
| !~# | NOT LIKEB | NOT LIKE |
| !~~\* | NOT ILIKE | NOT ILIKE |
| !~#\* | NOT ILIKEB | NOT ILIKE |

Expand

Show lessSee more

In Vertica, the default escape character is the backslash (`\`). Snowflake doesn’t have a default escape character. The `ESCAPE` clause will be automatically added when needed.

It’s important to know that Snowflake requires the backslash to be escaped (`\\`) when you use it as an escape character within both the expression and the `ESCAPE` clause. This means you’ll need two backslashes to represent a single literal backslash escape character in Snowflake queries. This is handled by automatically escaping the backslash for you.

### Sample Source Patterns

Note

:class: tip
This syntax is fully supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

#### Vertica

Copy code

```
 SELECT path_name
FROM file_paths
WHERE path_name ~~ '/report/sales_2025_q_.csv';

-- Find a path containing the literal '50%'
SELECT path_name
FROM file_paths
WHERE path_name LIKE '%50\%%';

-- Find a path starting with 'C:\'
SELECT path_name
FROM file_paths
WHERE path_name ILIKEB 'C:\\%' ESCAPE'\';
```

#### Snowflake

Copy code

```
SELECT path_name
FROM file_paths
WHERE path_name LIKE '/report/sales_2025_q_.csv';

-- Find a path containing the literal '50%'
SELECT path_name
FROM file_paths
WHERE path_name LIKE '%50\\%%' ESCAPE'\\';

-- Find a path starting with 'C:\'
SELECT path_name
FROM file_paths
WHERE path_name ILIKE 'C:\\\\%' ESCAPE'\\';
```

#### Known Issues

While most backslash patterns are handled, some **complex expressions** may still cause **query failures**. We recommend reviewing complex patterns to prevent these issues.

#### Related EWIs

There are no related EWIs.
