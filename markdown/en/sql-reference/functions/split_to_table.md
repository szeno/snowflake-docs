Categories:
:   [String & binary functions](/sql-reference/functions-string) (General) , [Table functions](/sql-reference/functions-table)

# SPLIT\_TO\_TABLE

This table function splits a string (based on a specified delimiter) and flattens the results into rows.

See also:
:   [SPLIT](/sql-reference/functions/split)

## Syntax

Copy code

```
SPLIT_TO_TABLE(<string>, <delimiter>)
```

## Arguments

`string`
:   Text to be split.

`delimiter`
:   Text to split the string by.

## Output

This function returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| SEQ | NUMBER | A unique sequence number associated with the input record. The sequence is not guaranteed to be gap-free or ordered. in any particular way. |
| INDEX | NUMBER | The one-based index of the element. |
| VALUE | VARCHAR | The value of the element of the flattened array. |

Expand

Show lessSee more

Note

The query can also access the columns of the original (correlated) table that served as the source of data for this function. If a single row
from the original table resulted in multiple rows in the flattened view, the values in this input row are replicated to match the number of
rows produced by this function.

## Examples

Here is a simple example on constant input.

Copy code

```
SELECT table1.value
  FROM TABLE(SPLIT_TO_TABLE('a.b', '.')) AS table1
  ORDER BY table1.value;
```

```
+-------+
| VALUE |
|-------|
| a     |
| b     |
+-------+
```

Create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE splittable (v VARCHAR);
INSERT INTO splittable (v) VALUES ('a.b.c'), ('d'), ('');
SELECT * FROM splittable;
```

```
+-------+
| V     |
|-------|
| a.b.c |
| d     |
|       |
+-------+
```

You can use the [LATERAL](/sql-reference/constructs/join-lateral) keyword with the SPLIT\_TO\_TABLE function
so that the function executes on each row of the `splittable` table as a correlated table:

Copy code

```
SELECT *
  FROM splittable, LATERAL SPLIT_TO_TABLE(splittable.v, '.')
  ORDER BY SEQ, INDEX;
```

```
+-------+-----+-------+-------+
| V     | SEQ | INDEX | VALUE |
|-------+-----+-------+-------|
| a.b.c |   1 |     1 | a     |
| a.b.c |   1 |     2 | b     |
| a.b.c |   1 |     3 | c     |
| d     |   2 |     1 | d     |
|       |   3 |     1 |       |
+-------+-----+-------+-------+
```

Create another table that contains authors in one column and some of their book titles in another column, separated
by commas:

Copy code

```
CREATE OR REPLACE TABLE authors_books_test (author VARCHAR, titles VARCHAR);
INSERT INTO authors_books_test (author, titles) VALUES
  ('Nathaniel Hawthorne', 'The Scarlet Letter , The House of the Seven Gables,The Blithedale Romance'),
  ('Herman Melville', 'Moby Dick,The Confidence-Man');
SELECT * FROM authors_books_test;
```

```
+---------------------+---------------------------------------------------------------------------+
| AUTHOR              | TITLES                                                                    |
|---------------------+---------------------------------------------------------------------------|
| Nathaniel Hawthorne | The Scarlet Letter , The House of the Seven Gables,The Blithedale Romance |
| Herman Melville     | Moby Dick,The Confidence-Man                                              |
+---------------------+---------------------------------------------------------------------------+
```

Use the LATERAL keyword and the SPLIT\_TO\_TABLE function to run a query that returns a separate row for each title.
In addition, use the [TRIM](/sql-reference/functions/trim) function to remove leading and trailing spaces from the titles. Note that the
SELECT list includes the fixed `value` column that is returned by the function:

Copy code

```
SELECT author, TRIM(value) AS title
  FROM authors_books_test, LATERAL SPLIT_TO_TABLE(titles, ',')
  ORDER BY author;
```

```
+---------------------+-------------------------------+
| AUTHOR              | TITLE                         |
|---------------------+-------------------------------|
| Herman Melville     | Moby Dick                     |
| Herman Melville     | The Confidence-Man            |
| Nathaniel Hawthorne | The Scarlet Letter            |
| Nathaniel Hawthorne | The House of the Seven Gables |
| Nathaniel Hawthorne | The Blithedale Romance        |
+---------------------+-------------------------------+
```
