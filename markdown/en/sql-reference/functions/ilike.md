Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# [ NOT ] ILIKE

Performs a case-insensitive comparison to determine whether a string matches or does not match a specified pattern.
For case-sensitive matching, use LIKE instead.

LIKE, ILIKE, and RLIKE all perform similar operations. However, RLIKE uses POSIX ERE (Extended Regular Expression) syntax
instead of the SQL pattern syntax used by LIKE and ILIKE.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

See also:
:   [[ NOT ] LIKE](/sql-reference/functions/like) , [[ NOT ] RLIKE](/sql-reference/functions/rlike)

## Syntax

Copy code

```
<subject> [ NOT ] ILIKE <pattern> [ ESCAPE <escape> ]

ILIKE( <subject> , <pattern> [ , <escape> ] )
```

## Arguments

**Required:**

`subject`
:   Subject to match.

`pattern`
:   Pattern to match.

**Optional:**

`escape`
:   Character(s) inserted in front of a wildcard character to indicate that the wildcard should
    be interpreted as a regular character and not as a wildcard.

## Returns

Returns a BOOLEAN or NULL.

- When ILIKE is specified, the value is TRUE if there is a match. Otherwise, returns FALSE.
- When NOT ILIKE is specified, the value is TRUE if there is no match. Otherwise, returns FALSE.
- When either ILIKE or NOT ILIKE is specified, returns NULL if any argument is NULL.

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
  'SOMETHING%' ILIKE '%\\%%' ESCAPE '\\';
  ```

  For examples of using escape characters, see [the examples for ILIKE](#label-examples-for-ilike).
  For more examples of using escape characters, and in particular the backslash as an escape character,
  see [the examples for LIKE](/sql-reference/functions/like#label-examples-for-like).

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
CREATE OR REPLACE TABLE ilike_ex(name VARCHAR(20));
INSERT INTO ilike_ex VALUES
  ('John  Dddoe'),
  ('Joe   Doe'),
  ('John_down'),
  ('Joe down'),
  (null);
```

The following examples show the use of `ILIKE`, `NOT ILIKE`, and the wildcard
character `%`:

Copy code

```
SELECT *
  FROM ilike_ex
  WHERE name ILIKE '%j%h%do%'
  ORDER BY 1;
```

```
+-------------+
| NAME        |
|-------------|
| John  Dddoe |
| John_down   |
+-------------+
```

Copy code

```
SELECT *
  FROM ilike_ex
  WHERE name NOT ILIKE '%j%h%do%'
  ORDER BY 1;
```

```
+-----------+
| NAME      |
|-----------|
| Joe   Doe |
| Joe down  |
+-----------+
```

Copy code

```
SELECT *
  FROM ilike_ex
  WHERE name ILIKE '%j%h%^_do%' ESCAPE '^'
  ORDER BY 1;
```

```
+-----------+
| NAME      |
|-----------|
| John_down |
+-----------+
```
