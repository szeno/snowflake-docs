Categories:
:   [Hash functions](/sql-reference/functions-hash-scalar)

# HASH

Returns a signed 64-bit hash value. Note that HASH never returns NULL, even for NULL inputs.

Possible uses for the HASH function include:

- Convert skewed data values to values that are likely to be more randomly or more evenly distributed.

  For example, you can hash a group of highly skewed values and generate a set of values that are more likely to be randomly distributed or evenly distributed.
- Put data in buckets. Because hashing can convert skewed data values to closer-to-evenly distributed values, you can use hashing to help take skewed values and
  create approximately evenly-sized buckets.

  If hashing alone is not sufficient to get the number of distinct buckets that you want, you can combine hashing with the [ROUND](/sql-reference/functions/round) or [WIDTH\_BUCKET](/sql-reference/functions/width_bucket)
  functions.

Note

HASH is a proprietary function that accepts a variable number of input expressions of arbitrary types and returns a signed value. It is not a
cryptographic hash function and should not be used as such.

Cryptographic hash functions have a few properties which this function does not, for example:

- The cryptographic hashing of a value cannot be inverted to find the original value.
- Given a value, it is infeasible to find another value with the same cryptographic hash.

For cryptographic purposes, use the SHA families of functions (in [String & binary functions](/sql-reference/functions-string)).

See also:
:   [HASH\_AGG](/sql-reference/functions/hash_agg)

## Syntax

Copy code

```
HASH( <expr> [ , <expr> ... ] )

HASH(*)
```

## Arguments

`expr`
:   The expression can be a general expression of any Snowflake data type.

`*`
:   Returns a single hashed value based on all columns in each record,
    including records with NULL values.

    When you pass a wildcard to the function, you can qualify the wildcard with the name or alias for the table.
    For example, to pass in all of the columns from the table named `mytable`, specify the following:

    Copy code

    ```
    (mytable.*)
    ```

    You can also use the ILIKE and EXCLUDE keywords for filtering:

    - ILIKE filters for column names that match the specified pattern. Only one
      pattern is allowed. For example:

      Copy code

      ```
      (* ILIKE 'col1%')
      ```
    - EXCLUDE filters out column names that don’t match the specified column or columns. For example:

      Copy code

      ```
      (* EXCLUDE col1)

      (* EXCLUDE (col1, col2))
      ```

    Qualifiers are valid when you use these keywords. The following example uses the ILIKE keyword to
    filter for all of the columns that match the pattern `col1%` in the table `mytable`:

    Copy code

    ```
    (mytable.* ILIKE 'col1%')
    ```

    The ILIKE and EXCLUDE keywords can’t be combined in a single function call.

    For this function, the ILIKE and EXCLUDE keywords are valid only in a SELECT list or GROUP BY clause.

    For more information about the ILIKE and EXCLUDE keywords, see the “Parameters” section in [SELECT](/sql-reference/sql/select).

## Returns

Returns a signed 64-bit value as NUMBER(19,0).

HASH never returns NULL, even for NULL inputs.

## Usage notes

- HASH is stable in the sense that it guarantees:

  - Any two values of type NUMBER that compare equally will hash to the same hash value, even if the
    respective types have different precision and/or scale.
  - Any two values of type FLOAT that can be converted to NUMBER(38, 0) without loss of precision will
    hash to the same value. For example, the following all return the same hash value:

    - `HASH(10::NUMBER(38,0))`
    - `HASH(10::NUMBER(5,3))`
    - `HASH(10::FLOAT)`
  - Any two values of type TIMESTAMP\_TZ that compare equally will hash to the same hash value, even if
    the timestamps are from different time zones.
  - This guarantee also applies to NUMBER, FLOAT, and TIMESTAMP\_TZ values within a VARIANT column.
  - Note that this guarantee does not apply to other combinations of types, even if implicit conversions exist
    between the types. For example, with overwhelming probability, the following will not return the same hash values
    even though `10 = '10'` after implicit conversion:

    - `HASH(10)`
    - `HASH('10')`
- `HASH(*)` means to create a single hashed value based on all columns in the row.
- Do not use HASH to create unique keys. HASH has a finite resolution of 64 bits, and is guaranteed to return
  non-unique values if more than 2^64 values are entered (e.g. for a table with more than 2^64 rows). In practice, if
  the input is on the order of 2^32 rows (approximately 4 billion rows) or more, the function is reasonably likely
  to return at least one duplicate value.

## Collation details

No impact.

- Two strings that are identical but have different collation specifications have the same hash value. In other words,
  only the string, not the collation specification, affects the hash value.
- Two strings that are different, but compare equal according to a collation, might have a different hash value. For
  example, two strings that are identical using punctuation-insensitive collation will normally have different hash
  values because only the string, not the collation specification, affects the hash value.

## Examples

Copy code

```
SELECT HASH(SEQ8()) FROM TABLE(GENERATOR(rowCount=>10));
```

```
+----------------------+
|         HASH(SEQ8()) |
|----------------------|
| -6076851061503311999 |
| -4730168494964875235 |
| -3690131753453205264 |
| -7287585996956442977 |
| -1285360004004520191 |
|  4801857165282451853 |
| -2112898194861233169 |
|  1885958945512144850 |
| -3994946021335987898 |
| -3559031545629922466 |
+----------------------+
```

Copy code

```
SELECT HASH(10), HASH(10::number(38,0)), HASH(10::number(5,3)), HASH(10::float);
```

```
+---------------------+------------------------+-----------------------+---------------------+
|            HASH(10) | HASH(10::NUMBER(38,0)) | HASH(10::NUMBER(5,3)) |     HASH(10::FLOAT) |
|---------------------+------------------------+-----------------------+---------------------|
| 1599627706822963068 |    1599627706822963068 |   1599627706822963068 | 1599627706822963068 |
+---------------------+------------------------+-----------------------+---------------------+
```

Copy code

```
SELECT HASH(10), HASH('10');
```

```
+---------------------+---------------------+
|            HASH(10) |          HASH('10') |
|---------------------+---------------------|
| 1599627706822963068 | 3622494980440108984 |
+---------------------+---------------------+
```

Copy code

```
SELECT HASH(null), HASH(null, null), HASH(null, null, null);
```

```
+---------------------+--------------------+------------------------+
|          HASH(NULL) |   HASH(NULL, NULL) | HASH(NULL, NULL, NULL) |
|---------------------+--------------------+------------------------|
| 8817975702393619368 | 953963258351104160 |    2941948363845684412 |
+---------------------+--------------------+------------------------+
```

The example below shows that even if the table contains multiple columns, `HASH(*)` returns a single value per row.

Copy code

```
CREATE TABLE orders (order_ID INTEGER, customer_ID INTEGER, order_date ...);

...

SELECT HASH(*) FROM orders LIMIT 10;
```

```
+-----------------------+
|        HASH(*)        |
|-----------------------|
|  -3527903796973745449 |
|  6296330861892871310  |
|  6918165900200317484  |
|  -2762842444336053314 |
|  -2340602249668223387 |
|  5248970923485160358  |
|  -5807737826218607124 |
|  428973568495579456   |
|  2583438210124219420  |
|  4041917286051184231  |
+ ----------------------+
```
