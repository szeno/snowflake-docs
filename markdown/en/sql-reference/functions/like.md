Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# [ NOT ] LIKE

Performs a case-sensitive comparison to determine whether a string matches or does not match a specified pattern.
For case-insensitive matching, use ILIKE instead.

LIKE, ILIKE, and RLIKE all perform similar operations. However, RLIKE uses POSIX ERE (Extended Regular Expression) syntax
instead of the SQL pattern syntax used by LIKE and ILIKE.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

See also:
:   [[ NOT ] ILIKE](/sql-reference/functions/ilike) , [[ NOT ] RLIKE](/sql-reference/functions/rlike) , [LIKE ALL](/sql-reference/functions/like_all), [LIKE ANY](/sql-reference/functions/like_any)

## Syntax

Copy code

```
<subject> [ NOT ] LIKE <pattern> [ ESCAPE <escape> ]

LIKE( <subject> , <pattern> [ , <escape> ] )
```

## Arguments

**Required:**

`subject`
:   Subject to match. This is typically a VARCHAR, although some other data
    types can be used.

`pattern`
:   Pattern to match. This is typically a VARCHAR, although some other data
    types can be used.

**Optional:**

`escape`
:   Character(s) inserted in front of a wildcard character to indicate that the wildcard should
    be interpreted as a regular character and not as a wildcard.

## Returns

Returns a BOOLEAN or NULL.

- When LIKE is specified, the value is TRUE if there is a match. Otherwise, returns FALSE.
- When NOT LIKE is specified, the value is TRUE if there is no match. Otherwise, returns FALSE.
- When either LIKE or NOT LIKE is specified, returns NULL if any argument is NULL.

## Usage notes

- To include single quotes or other special characters in pattern matching, you can use a
  [backslash escape sequence](/sql-reference/data-types-text#label-single-quoted-string-constants-escape-sequences).
- NULL does not match NULL. In other words, if the subject is NULL and the pattern is NULL,
  that is not considered a match.
- SQL wildcards are supported in `pattern`:

  - An underscore (`_`) matches any single character.
  - A percent sign (`%`) matches any sequence of zero or more characters.
- Wildcards in `pattern` include newline characters (`n`) in `subject` as matches.
- Pattern matching covers the entire string. To match a sequence anywhere within a string, start and end the pattern with `%`.
- There is no default escape character.

- If you use the backslash as an escape character, then you must escape the backslash in both the
  expression and the ESCAPE clause. For example, the following command specifies that the escape character is
  the backslash, and then uses that escape character to search for `%` as a literal (without the escape character,
  the `%` would be treated as a wildcard):

  Copy code

  ```
  'SOMETHING%' LIKE '%\\%%' ESCAPE '\\';
  ```

  For examples of using escape characters, and in particular the backslash as an escape character, see
  [Examples](#label-examples-for-like).

- If you require more complex pattern matching than this function supports, you can use a
  [regular expression function](/sql-reference/functions-regexp) instead.

# Collation details

Only the `upper`, `lower`, and `trim` collation specifications are supported. Combinations with `upper`,
`lower`, and `trim` are also supported (for example, `upper-trim` and `lower-trim`), except for locale
combinations (for example, `en-upper`).

## Examples

Create a table that contains some strings:

Copy code

```
CREATE OR REPLACE TABLE like_ex(name VARCHAR(20));
INSERT INTO like_ex VALUES
  ('John  Dddoe'),
  ('John \'alias\' Doe'),
  ('Joe   Doe'),
  ('John_down'),
  ('Joe down'),
  ('Elaine'),
  (''),    -- empty string
  (null);
```

The following examples show the use of `LIKE`, `NOT LIKE`, and the wildcard
character `%`:

Copy code

```
SELECT name
  FROM like_ex
  WHERE name LIKE '%Jo%oe%'
  ORDER BY name;
```

```
+------------------+
| NAME             |
|------------------|
| Joe   Doe        |
| John  Dddoe      |
| John 'alias' Doe |
+------------------+
```

Copy code

```
SELECT name
  FROM like_ex
  WHERE name NOT LIKE '%Jo%oe%'
  ORDER BY name;
```

```
+-----------+
| NAME      |
|-----------|
|           |
| Elaine    |
| Joe down  |
| John_down |
+-----------+
```

Copy code

```
SELECT name
  FROM like_ex
  WHERE name NOT LIKE 'John%'
  ORDER BY name;
```

```
+-----------+
| NAME      |
|-----------|
|           |
| Elaine    |
| Joe   Doe |
| Joe down  |
+-----------+
```

Copy code

```
SELECT name
  FROM like_ex
  WHERE name NOT LIKE ''
  ORDER BY name;
```

```
+------------------+
| NAME             |
|------------------|
| Elaine           |
| Joe   Doe        |
| Joe down         |
| John  Dddoe      |
| John 'alias' Doe |
| John_down        |
+------------------+
```

The following example uses a backslash to escape a single quote so that it can be found in pattern matching:

Copy code

```
SELECT name
  FROM like_ex
  WHERE name LIKE '%\'%'
  ORDER BY name;
```

```
+------------------+
| NAME             |
|------------------|
| John 'alias' Doe |
+------------------+
```

The following examples use an ESCAPE clause:

Copy code

```
SELECT name
  FROM like_ex
  WHERE name LIKE '%J%h%^_do%' ESCAPE '^'
  ORDER BY name;
```

```
+-----------+
| NAME      |
|-----------|
| John_down |
+-----------+
```

Insert more rows into the `like_ex` table:

Copy code

```
INSERT INTO like_ex (name) VALUES
  ('100 times'),
  ('1000 times'),
  ('100%');
```

Without the escape character, the percent sign (`%`) is treated as a wildcard:

Copy code

```
SELECT * FROM like_ex WHERE name LIKE '100%'
  ORDER BY 1;
```

```
+------------+
| NAME       |
|------------|
| 100 times  |
| 100%       |
| 1000 times |
+------------+
```

With the escape character, the percent sign (`%`) is treated as a literal:

Copy code

```
SELECT * FROM like_ex WHERE name LIKE '100^%' ESCAPE '^'
  ORDER BY 1;
```

```
+------+
| NAME |
|------|
| 100% |
+------+
```

The following example uses an ESCAPE clause in which the backslash is the escape character. Note that the backslash
itself must be escaped in both the ESCAPE clause and in the expression:

Copy code

```
SELECT * FROM like_ex WHERE name LIKE '100\\%' ESCAPE '\\'
  ORDER BY 1;
```

```
+------+
| NAME |
|------|
| 100% |
+------+
```
