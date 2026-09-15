Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# SUBSTR , SUBSTRING

Returns the portion of the [string or binary](/sql-reference/data-types-text) value
from `base_expr`, starting from the character/byte specified by `start_expr`,
with optionally limited length.

These functions are synonymous.

See also:
:   [LEFT](/sql-reference/functions/left) , [RIGHT](/sql-reference/functions/right)

## Syntax

Copy code

```
SUBSTR( <base_expr>, <start_expr> [ , <length_expr> ] )

SUBSTRING( <base_expr>, <start_expr> [ , <length_expr> ] )
```

## Arguments

`base_expr`
:   An expression that evaluates to a VARCHAR or BINARY value.

`start_expr`
:   An expression that evaluates to an integer. It specifies the offset from which the substring starts. The offset is measured in:

    - The number of UTF-8 characters if the input is a VARCHAR value.
    - The number of bytes if the input is a BINARY value.

    The start position is 1-based, not 0-based. For example, `SUBSTR('abc', 1, 1)` returns `a`, not `b`.

`length_expr`
:   An expression that evaluates to an integer. It specifies:

    - The number of UTF-8 characters to return if the input is VARCHAR.
    - The number of bytes to return if the input is BINARY.

    Specify a length that is greater than or equal to zero. If the length is a negative number, the function returns an
    empty string.

## Returns

The data type of the returned value is the same as the data type of the `base_expr` (VARCHAR or BINARY).

If any of the inputs are NULL, NULL is returned.

## Usage notes

- If `length_expr` is specified, up to `length_expr` characters/bytes are
  returned. If `length_expr` isn’t specified, all the characters until the end of the string or
  binary value are returned.
- The values in `start_expr` start from 1:
  - If 0 is specified, it is treated as 1.
  - If a negative value is specified, the starting position is computed as
    the `start_expr` characters/bytes from the end of the string or binary
    value. If the position is outside of the range of a string or binary
    value, an empty value is returned.

## Collation details

- Collation applies to VARCHAR inputs. Collation doesn’t apply if the input data type of the first parameter
  is BINARY.
- No impact. Although collation is accepted syntactically, collations don’t affect processing. For example,
  two-character and three-character letters in languages (for example, “dzs” in Hungarian or “ch” in Czech)
  are still counted as two or three characters (not one character) for the length argument.
- The collation of the result is the same as the collation of the input. This can be useful if the returned value is passed to another function as part of nested function calls.

## Examples

The following examples use the SUBSTR function.

### Basic example

The following example uses the SUBSTR function to return the portion of the string that starts at the
ninth character and limits the length of the returned value to three characters:

Copy code

```
SELECT SUBSTR('testing 1 2 3', 9, 3);
```

```
+-------------------------------+
| SUBSTR('TESTING 1 2 3', 9, 3) |
|-------------------------------|
| 1 2                           |
+-------------------------------+
```

### Specifying different start and length values

The following example shows the substrings returned for the same `base_expr` when different
values are specified for `start_expr` and `length_expr`:

Copy code

```
CREATE OR REPLACE TABLE test_substr (
    base_value VARCHAR,
    start_value INT,
    length_value INT)
  AS SELECT
    column1,
    column2,
    column3
  FROM
    VALUES
      ('mystring', -1, 3),
      ('mystring', -3, 3),
      ('mystring', -3, 7),
      ('mystring', -5, 3),
      ('mystring', -7, 3),
      ('mystring', 0, 3),
      ('mystring', 0, 7),
      ('mystring', 1, 3),
      ('mystring', 1, 7),
      ('mystring', 3, 3),
      ('mystring', 3, 7),
      ('mystring', 5, 3),
      ('mystring', 5, 7),
      ('mystring', 7, 3),
      ('mystring', NULL, 3),
      ('mystring', 3, NULL);

SELECT base_value,
       start_value,
       length_value,
       SUBSTR(base_value, start_value, length_value) AS substring
  FROM test_substr;
```

```
+------------+-------------+--------------+-----------+
| BASE_VALUE | START_VALUE | LENGTH_VALUE | SUBSTRING |
|------------+-------------+--------------+-----------|
| mystring   |          -1 |            3 | g         |
| mystring   |          -3 |            3 | ing       |
| mystring   |          -3 |            7 | ing       |
| mystring   |          -5 |            3 | tri       |
| mystring   |          -7 |            3 | yst       |
| mystring   |           0 |            3 | mys       |
| mystring   |           0 |            7 | mystrin   |
| mystring   |           1 |            3 | mys       |
| mystring   |           1 |            7 | mystrin   |
| mystring   |           3 |            3 | str       |
| mystring   |           3 |            7 | string    |
| mystring   |           5 |            3 | rin       |
| mystring   |           5 |            7 | ring      |
| mystring   |           7 |            3 | ng        |
| mystring   |        NULL |            3 | NULL      |
| mystring   |           3 |         NULL | NULL      |
+------------+-------------+--------------+-----------+
```

### Returning substrings for email, phone, and date strings

The following examples return substrings for customer information in a table.

Create the table and insert data:

Copy code

```
CREATE OR REPLACE TABLE customer_contact_example (
    cust_id INT,
    cust_email VARCHAR,
    cust_phone VARCHAR,
    activation_date VARCHAR)
  AS SELECT
    column1,
    column2,
    column3,
    column4
  FROM
    VALUES
      (1, 'some_text@example.com', '800-555-0100', '20210320'),
      (2, 'some_other_text@example.org', '800-555-0101', '20240509'),
      (3, 'some_different_text@example.net', '800-555-0102', '20191017');

SELECT * from customer_contact_example;
```

```
+---------+---------------------------------+--------------+-----------------+
| CUST_ID | CUST_EMAIL                      | CUST_PHONE   | ACTIVATION_DATE |
|---------+---------------------------------+--------------+-----------------|
|       1 | some_text@example.com           | 800-555-0100 | 20210320        |
|       2 | some_other_text@example.org     | 800-555-0101 | 20240509        |
|       3 | some_different_text@example.net | 800-555-0102 | 20191017        |
+---------+---------------------------------+--------------+-----------------+
```

Use the [POSITION](/sql-reference/functions/position) function with the SUBSTR function to extract the domains from email addresses.
This example finds the position of `@` in each string and starts from the next character by adding
one:

Copy code

```
SELECT cust_id,
       cust_email,
       SUBSTR(cust_email, POSITION('@' IN cust_email) + 1) AS domain
  FROM customer_contact_example;
```

```
+---------+---------------------------------+-------------+
| CUST_ID | CUST_EMAIL                      | DOMAIN      |
|---------+---------------------------------+-------------|
|       1 | some_text@example.com           | example.com |
|       2 | some_other_text@example.org     | example.org |
|       3 | some_different_text@example.net | example.net |
+---------+---------------------------------+-------------+
```

Tip

You can use the POSITION function to find the position of other characters, such as an empty
character (`' '`) or an underscore (`_`).

In the `cust_phone` column in the table, the area code is always the first three characters. Extract
the area code from phone numbers:

Copy code

```
SELECT cust_id,
       cust_phone,
       SUBSTR(cust_phone, 1, 3) AS area_code
  FROM customer_contact_example;
```

```
+---------+--------------+-----------+
| CUST_ID | CUST_PHONE   | AREA_CODE |
|---------+--------------+-----------|
|       1 | 800-555-0100 | 800       |
|       2 | 800-555-0101 | 800       |
|       3 | 800-555-0102 | 800       |
+---------+--------------+-----------+
```

Remove the area code from phone numbers:

Copy code

```
SELECT cust_id,
       cust_phone,
       SUBSTR(cust_phone, 5) AS phone_without_area_code
  FROM customer_contact_example;
```

```
+---------+--------------+-------------------------+
| CUST_ID | CUST_PHONE   | PHONE_WITHOUT_AREA_CODE |
|---------+--------------+-------------------------|
|       1 | 800-555-0100 | 555-0100                |
|       2 | 800-555-0101 | 555-0101                |
|       3 | 800-555-0102 | 555-0102                |
+---------+--------------+-------------------------+
```

In the `activation_date` column in the table, the date is always in the format `YYYYMMDD`. Extract the year,
month, and day from these strings:

Copy code

```
SELECT cust_id,
       activation_date,
       SUBSTR(activation_date, 1, 4) AS year,
       SUBSTR(activation_date, 5, 2) AS month,
       SUBSTR(activation_date, 7, 2) AS day
  FROM customer_contact_example;
```

```
+---------+-----------------+------+-------+-----+
| CUST_ID | ACTIVATION_DATE | YEAR | MONTH | DAY |
|---------+-----------------+------+-------+-----|
|       1 | 20210320        | 2021 | 03    | 20  |
|       2 | 20240509        | 2024 | 05    | 09  |
|       3 | 20191017        | 2019 | 10    | 17  |
+---------+-----------------+------+-------+-----+
```
