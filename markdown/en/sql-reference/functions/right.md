Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# RIGHT

Returns a rightmost substring of its input.

`RIGHT(STR, N)` is equivalent to `SUBSTR(STR, LENGTH(STR)-N+1, N)`.

See also:
:   [LEFT](/sql-reference/functions/left) , [SUBSTR , SUBSTRING](/sql-reference/functions/substr)

## Syntax

Copy code

```
RIGHT( <string_expr> , <length_expr> )
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

The following examples use the RIGHT function.

### Basic example

Copy code

```
SELECT RIGHT('ABCDEFG', 3);
```

```
+---------------------+
| RIGHT('ABCDEFG', 3) |
|---------------------|
| EFG                 |
+---------------------+
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

Use the [LENGTH](/sql-reference/functions/length) and [POSITION](/sql-reference/functions/position) functions with the RIGHT function to extract the domains from
email addresses. This example first finds the length of the input string and then subtracts the position
of `@` in each string to determine the length of the domain:

Copy code

```
SELECT cust_id,
       cust_email,
       RIGHT(cust_email, LENGTH(cust_email) - (POSITION('@' IN cust_email))) AS domain
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
the phone numbers without the area codes:

Copy code

```
SELECT cust_id,
       cust_phone,
       RIGHT(cust_phone, 8) AS phone_without_area_code
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

In the `activation_date` column in the table, the date is always in the format `YYYYMMDD`. Extract day from
these strings:

Copy code

```
SELECT cust_id,
       activation_date,
       RIGHT(activation_date, 2) AS day
  FROM customer_contact_example;
```

```
+---------+-----------------+-----+
| CUST_ID | ACTIVATION_DATE | DAY |
|---------+-----------------+-----|
|       1 | 20210320        | 20  |
|       2 | 20240509        | 09  |
|       3 | 20191017        | 17  |
+---------+-----------------+-----+
```
