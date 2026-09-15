Categories:
:   [String & binary functions](/sql-reference/functions-string) (General) , [Table functions](/sql-reference/functions-table)

# STRTOK\_SPLIT\_TO\_TABLE

Tokenizes a string with the given set of delimiters and flattens the results into rows.

See also:
:   [STRTOK](/sql-reference/functions/strtok), [STRTOK\_TO\_ARRAY](/sql-reference/functions/strtok_to_array)

## Syntax

Copy code

```
STRTOK_SPLIT_TO_TABLE(<string> [,<delimiter_list>])
```

## Arguments

**Required:**

`string`
:   Text to be tokenized.

**Optional:**

`delimiter_list`
:   Optional set of delimiters. The default value is a single space character.

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
  FROM TABLE(STRTOK_SPLIT_TO_TABLE('a.b', '.')) AS table1
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
CREATE OR REPLACE TABLE splittable_strtok (v VARCHAR);
INSERT INTO splittable_strtok (v) VALUES ('a b'), ('cde'), ('f|g'), ('');
SELECT * FROM splittable_strtok;
```

```
+-----+
| V   |
|-----|
| a b |
| cde |
| f|g |
|     |
+-----+
```

You can use the [LATERAL](/sql-reference/constructs/join-lateral) keyword with the STRTOK\_SPLIT\_TO\_TABLE function
so that the function executes on each row of the `splittable_strtok` table as a correlated table:

Copy code

```
SELECT *
  FROM splittable_strtok, LATERAL STRTOK_SPLIT_TO_TABLE(splittable_strtok.v, ' ')
  ORDER BY SEQ, INDEX;
```

```
+-----+-----+-------+-------+
| V   | SEQ | INDEX | VALUE |
|-----+-----+-------+-------|
| a b |   1 |     1 | a     |
| a b |   1 |     2 | b     |
| cde |   2 |     1 | cde   |
| f|g |   3 |     1 | f|g   |
+-----+-----+-------+-------+
```

This example is the same as the preceding, except that it specifies multiple delimiters:

Copy code

```
SELECT *
  FROM splittable_strtok, LATERAL STRTOK_SPLIT_TO_TABLE(splittable_strtok.v, ' |')
  ORDER BY SEQ, INDEX;
```

```
+-----+-----+-------+-------+
| V   | SEQ | INDEX | VALUE |
|-----+-----+-------+-------|
| a b |   1 |     1 | a     |
| a b |   1 |     2 | b     |
| cde |   2 |     1 | cde   |
| f|g |   3 |     1 | f     |
| f|g |   3 |     2 | g     |
+-----+-----+-------+-------+
```

Create another table that contains authors in one column and some of their book titles in another column. In the table
data, the book titles might be separated by a comma or a semi-colon:

Copy code

```
CREATE OR REPLACE TABLE authors_books_test2 (author VARCHAR, titles VARCHAR);
INSERT INTO authors_books_test2 (author, titles) VALUES
  ('Nathaniel Hawthorne', 'The Scarlet Letter ; The House of the Seven Gables;The Blithedale Romance'),
  ('Herman Melville', 'Moby Dick,The Confidence-Man');
SELECT * FROM authors_books_test2;
```

```
+---------------------+---------------------------------------------------------------------------+
| AUTHOR              | TITLES                                                                    |
|---------------------+---------------------------------------------------------------------------|
| Nathaniel Hawthorne | The Scarlet Letter ; The House of the Seven Gables;The Blithedale Romance |
| Herman Melville     | Moby Dick,The Confidence-Man                                              |
+---------------------+---------------------------------------------------------------------------+
```

Use the LATERAL keyword and the SPLIT\_TO\_TABLE function to run a query that returns a separate row for each title.
In addition, use the [TRIM](/sql-reference/functions/trim) function to remove leading and trailing spaces from the titles. Note that the SELECT
list includes the fixed `value` column that is returned by the function:

Copy code

```
SELECT author, TRIM(value) AS title
  FROM authors_books_test2, LATERAL STRTOK_SPLIT_TO_TABLE(titles, ',;')
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
