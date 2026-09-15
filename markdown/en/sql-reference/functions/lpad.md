Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# LPAD

Left-pads a string with characters from another string, or left-pads a binary value with bytes from another binary value.

The argument (`base`) is left-padded to length `length_expr` with characters/bytes from the `pad` argument.

See also:
:   [RPAD](/sql-reference/functions/rpad)

## Syntax

Copy code

```
LPAD( <base>, <length_expr> [, <pad>] )
```

# Arguments

`base`
:   A VARCHAR or BINARY value.

`length_expr`
:   An expression that evaluates to an integer. It specifies:

    - The number of UTF-8 characters to return if the input is VARCHAR.
    - The number of bytes to return if the input is BINARY.

`pad`
:   A VARCHAR or BINARY value. The type must match the data type of the `base` argument.
    Characters (or bytes) from this argument are used to pad the `base`.

## Returns

The data type of the returned value is the same as the data type of the `base` input value (VARCHAR or BINARY).

## Usage notes

- If the `base` argument is longer than `length_expr`, it is truncated to length `length_expr`.
- The `pad` argument can be multiple characters/bytes long. The `pad`
  argument is repeated in the result until the desired length (`length_expr`) is
  reached, truncating any superfluous characters/bytes in the `pad` argument.
  If the `pad` argument is empty, no padding is inserted, but the result is
  still truncated to length `length_expr`.
- When `base` is a string, the default `pad` string is `' '` (a single blank space). When
  `base` is a binary value, the `pad` argument must be provided explicitly.

## Collation details

- Collation applies to VARCHAR inputs. Collation doesn’t apply if the input data type of the first argument
  is BINARY.
- No impact.
  Although collation is accepted syntactically, collations have no impact on processing. For example, languages with
  two-character and three-character letters (for example, “dzs” in Hungarian, “ch” in Czech) still count
  those as two or three characters (not one character) for the length argument.
- The collation of the result is the same as the collation of the input. This can be useful if the returned value is passed to another function as part of nested function calls.
- Currently, Snowflake allows the `base` and `pad` arguments to have different collation specifiers.
  However, the individual collation specifiers can’t both be retained because the returned value has only one
  collation specifier. Snowflake recommends that you avoid using `pad` strings that have a different
  collation from the `base` string.

## Examples

The LPAD function can pad a string with characters on the left so that the values conform to a
specific format. The following example assumes that the `id` values in a column should be eight
characters long and padded with zeros on the left to meet this standard.

Create a table with an `id` column and insert values:

Copy code

```
CREATE OR REPLACE TABLE demo_lpad_ids (id VARCHAR);

INSERT INTO demo_lpad_ids VALUES
  ('5'),
  ('50'),
  ('500');
```

Run a query using the LPAD function so that values in the output meet the standard:

Copy code

```
SELECT id, LPAD(id, 8, '0') AS padded_ids
  FROM demo_lpad_ids;
```

```
+-----+------------+
| ID  | PADDED_IDS |
|-----+------------|
| 5   | 00000005   |
| 50  | 00000050   |
| 500 | 00000500   |
+-----+------------+
```

The following additional examples use the LPAD function to pad VARCHAR and BINARY data on the left.

Create and fill a table:

Copy code

```
CREATE OR REPLACE TABLE padding_example (v VARCHAR, b BINARY);

INSERT INTO padding_example (v, b)
  SELECT
    'Hi',
    HEX_ENCODE('Hi');

INSERT INTO padding_example (v, b)
  SELECT
    '-123.00',
    HEX_ENCODE('-123.00');

INSERT INTO padding_example (v, b)
  SELECT
    'Twelve Dollars',
    TO_BINARY(HEX_ENCODE('Twelve Dollars'), 'HEX');
```

Query the table to show the data:

Copy code

```
SELECT * FROM padding_example;
```

```
+----------------+------------------------------+
| V              | B                            |
|----------------+------------------------------|
| Hi             | 4869                         |
| -123.00        | 2D3132332E3030               |
| Twelve Dollars | 5477656C766520446F6C6C617273 |
+----------------+------------------------------+
```

This example demonstrates left-padding of VARCHAR values using the LPAD function, with the
results limited to 10 characters:

Copy code

```
SELECT v,
       LPAD(v, 10, ' ') AS pad_with_blank,
       LPAD(v, 10, '$') AS pad_with_dollar_sign
  FROM padding_example
  ORDER BY v;
```

```
+----------------+----------------+----------------------+
| V              | PAD_WITH_BLANK | PAD_WITH_DOLLAR_SIGN |
|----------------+----------------+----------------------|
| -123.00        |    -123.00     | $$$-123.00           |
| Hi             |         Hi     | $$$$$$$$Hi           |
| Twelve Dollars | Twelve Dol     | Twelve Dol           |
+----------------+----------------+----------------------+
```

This example demonstrates left-padding of BINARY values using the LPAD function, with the
results limited to 10 bytes:

Copy code

```
SELECT b,
       LPAD(b, 10, TO_BINARY(HEX_ENCODE(' '))) AS pad_with_blank,
       LPAD(b, 10, TO_BINARY(HEX_ENCODE('$'))) AS pad_with_dollar_sign
  FROM padding_example
  ORDER BY b;
```

```
+------------------------------+----------------------+----------------------+
| B                            | PAD_WITH_BLANK       | PAD_WITH_DOLLAR_SIGN |
|------------------------------+----------------------+----------------------|
| 2D3132332E3030               | 2020202D3132332E3030 | 2424242D3132332E3030 |
| 4869                         | 20202020202020204869 | 24242424242424244869 |
| 5477656C766520446F6C6C617273 | 5477656C766520446F6C | 5477656C766520446F6C |
+------------------------------+----------------------+----------------------+
```

This example shows left-padding when multiple characters are used and when
the padding isn’t an even multiple of the length of the multi-character
string used for padding:

Copy code

```
SELECT LPAD('123.50', 19, '*_');
```

```
+--------------------------+
| LPAD('123.50', 19, '*_') |
|--------------------------|
| *_*_*_*_*_*_*123.50      |
+--------------------------+
```

The output shows that 19 characters were returned, and the last `*` character doesn’t have
an accompanying `_` character.
