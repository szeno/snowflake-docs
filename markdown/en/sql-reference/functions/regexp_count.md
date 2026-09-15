Categories:
:   [String functions (regular expressions)](/sql-reference/functions-regexp)

# REGEXP\_COUNT

Returns the number of times that a [pattern](/sql-reference/functions-regexp) occurs in a string.

## Syntax

Copy code

```
REGEXP_COUNT( <subject> ,
              <pattern>
                [ , <position>
                  [ , <parameters> ]
                ]
)
```

## Arguments

**Required:**

`subject`
:   The string to search for matches.

`pattern`
:   Pattern to match.

    For guidelines on specifying patterns, see [String functions (regular expressions)](/sql-reference/functions-regexp).

**Optional:**

`position`
:   Number of characters from the beginning of the string where the function starts searching for matches.
    The value must be a positive integer.

    Default: `1` (the search for a match starts at the first character on the left)

`parameters`
> String of one or more characters that specifies the parameters used for searching for matches. Supported values:
>
> | Parameter | Description |
> | --- | --- |
> | `c` | Case-sensitive matching |
> | `i` | Case-insensitive matching |
> | `m` | Multi-line mode |
> | `e` | Extract submatches |
> | `s` | Single-line mode POSIX wildcard character `.` matches `\n` |
>
> Expand
>
> Show lessSee more
>
> Default: `c`
>
> For more information, see [Specifying the parameters for the regular expression](/sql-reference/functions-regexp#label-regexp-parameters-argument).

## Returns

Returns a value of type NUMBER. Returns NULL if any argument is NULL.

## Usage notes

See the [General usage notes](/sql-reference/functions-regexp#label-regexp-general-usage-notes) for regular expression functions.

## Collation details

When the [2026\_04 BCR bundle](/release-notes/bcr-bundles/2026_04/bcr-2314)
is enabled, the function accepts arguments with a collation specification. The
collation has no effect on pattern matching: matching is always case-sensitive
unless you pass the `i` flag in the `parameters` argument.

## Examples

The following example counts occurrences of the word `was`. You can use the `\b` metacharacter to indicate
a word boundary. In the following example, matching begins at the first character in the string `w` and
ends at the last character in the string `s`, and so doesn’t match words that contain the string (such
as `washing`):

Copy code

```
SELECT REGEXP_COUNT('It was the best of times, it was the worst of times',
                    '\\bwas\\b',
                    1) AS result;
```

```
+--------+
| RESULT |
|--------|
|      2 |
+--------+
```

The following example uses the `i` parameter for case-insensitive matching of the character `e`:

Copy code

```
SELECT REGEXP_COUNT('Excelence', 'e', 1, 'i') AS e_in_excelence;
```

```
+----------------+
| E_IN_EXCELENCE |
|----------------|
|              4 |
+----------------+
```

The following example illustrates overlapping occurrences. Create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE overlap (id NUMBER, a STRING);
INSERT INTO overlap VALUES (1,',abc,def,ghi,jkl,');
INSERT INTO overlap VALUES (2,',abc,,def,,ghi,,jkl,');

SELECT * FROM overlap;
```

```
+----+----------------------+
| ID | A                    |
|----+----------------------|
|  1 | ,abc,def,ghi,jkl,    |
|  2 | ,abc,,def,,ghi,,jkl, |
+----+----------------------+
```

Run a query that uses REGEXP\_COUNT to count the number of times that the following pattern
is found in each row: a punctuation mark followed by digits and letters, followed by a
punctuation mark.

Copy code

```
SELECT id,
       REGEXP_COUNT(a,
                    '[[:punct:]][[:alnum:]]+[[:punct:]]',
                    1,
                    'i') AS result
  FROM overlap;
```

```
+----+--------+
| ID | RESULT |
|----+--------|
|  1 |      2 |
|  2 |      4 |
+----+--------+
```

The remaining examples use the data in the following table:

Copy code

```
CREATE OR REPLACE TABLE regexp_count_demo (dt DATE, messages VARCHAR);

INSERT INTO regexp_count_demo (dt, messages) VALUES
  ('10-AUG-2025','ER-6842,LG-230,LG-150,ER-3379,ER-6210'),
  ('11-AUG-2025','LG-272,LG-605,LG-683,ER-5577'),
  ('12-AUG-2025','ER-2207,LG-551,LG-826,ER-6842');

SELECT * FROM regexp_count_demo;
```

```
+------------+---------------------------------------+
| DT         | MESSAGES                              |
|------------+---------------------------------------|
| 2025-08-10 | ER-6842,LG-230,LG-150,ER-3379,ER-6210 |
| 2025-08-11 | LG-272,LG-605,LG-683,ER-5577          |
| 2025-08-12 | ER-2207,LG-551,LG-826,ER-6842         |
+------------+---------------------------------------+
```

The following query returns the total number of messages for each day by searching for the delimiter (`,`) and
adding one to the total:

Copy code

```
SELECT dt,
       REGEXP_COUNT(messages, ',') + 1 AS message_count
  FROM regexp_count_demo;
```

```
+------------+---------------+
| DT         | MESSAGE_COUNT |
|------------+---------------|
| 2025-08-10 |             5 |
| 2025-08-11 |             4 |
| 2025-08-12 |             4 |
+------------+---------------+
```

Assume that errors always begin with `ER` followed by a hyphen and a four-digit number. The following
query counts the number of errors for each day:

Copy code

```
SELECT dt,
       REGEXP_COUNT(messages, '\\bER-[0-9]{4}') AS number_of_errors
  FROM regexp_count_demo;
```

```
+------------+------------------+
| DT         | NUMBER_OF_ERRORS |
|------------+------------------|
| 2025-08-10 |                3 |
| 2025-08-11 |                1 |
| 2025-08-12 |                2 |
+------------+------------------+
```
