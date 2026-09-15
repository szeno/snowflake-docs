Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# LEFT

Returns a leftmost substring of its input.

`LEFT(STR, N)` is equivalent to `SUBSTR(STR, 1, N)`.

See also:
:   [RIGHT](/sql-reference/functions/right) , [SUBSTR , SUBSTRING](/sql-reference/functions/substr)

## Syntax

Copy code

```
LEFT( <string_expr> , <length_expr> )
```

# Arguments

`string_expr`
:   An expression that evaluates to a VARCHAR or BINARY value.

`length_expr`
:   An expression that evaluates to an integer. It specifies:

    - The number of UTF-8 characters to return if the input is a VARCHAR value.
    - The number of bytes to return if the input is a BINARY value.

    Specify a length that is greater than or equal to zero. If the length is a negative number, the function returns an
    empty string.

## Returns

The data type of the returned value is the same as the data type of the `string_expr` (VARCHAR or BINARY).

If any of the inputs are NULL, NULL is returned.

## Usage notes

If `length_expr` is greater than the length of `expr`, then the function returns `expr`.

## Collation details

- Collation applies to VARCHAR inputs. Collation doesn’t apply if the input data type of the first parameter
  is BINARY.
- No impact. Although collation is accepted syntactically, collations don’t affect processing. For example,
  two-character and three-character letters in languages (for example, “dzs” in Hungarian or “ch” in Czech)
  are still counted as two or three characters (not one character) for the length argument.
- The collation of the result is the same as the collation of the input. This can be useful if the returned value is passed to another function as part of nested function calls.

## Examples

The following examples use the LEFT function.

### Basic example

Copy code

```
SELECT LEFT('ABCDEF', 3);
```

```
+-------------------+
| LEFT('ABCDEF', 3) |
|-------------------|
| ABC               |
+-------------------+
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

Use the [POSITION](/sql-reference/functions/position) function with the LEFT function to extract the username from email addresses.
This example finds the position of `@` in each string and subtracts one to return the username:

Copy code

```
SELECT cust_id,
       cust_email,
       LEFT(cust_email, POSITION('@' IN cust_email) - 1) AS username
  FROM customer_contact_example;
```

```
+---------+---------------------------------+---------------------+
| CUST_ID | CUST_EMAIL                      | USERNAME            |
|---------+---------------------------------+---------------------|
|       1 | some_text@example.com           | some_text           |
|       2 | some_other_text@example.org     | some_other_text     |
|       3 | some_different_text@example.net | some_different_text |
+---------+---------------------------------+---------------------+
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
       LEFT(cust_phone, 3) AS area_code
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

In the `activation_date` column in the table, the date is always in the format `YYYYMMDD`. Extract the year
from these strings:

Copy code

```
SELECT cust_id,
       activation_date,
       LEFT(activation_date, 4) AS year
  FROM customer_contact_example;
```

```
+---------+-----------------+------+
| CUST_ID | ACTIVATION_DATE | YEAR |
|---------+-----------------+------|
|       1 | 20210320        | 2021 |
|       2 | 20240509        | 2024 |
|       3 | 20191017        | 2019 |
+---------+-----------------+------+
```
