Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# NVL

If `expr1` is NULL, returns `expr2`, otherwise returns `expr1`.

Aliases:
:   [IFNULL](/sql-reference/functions/ifnull)

## Syntax

Copy code

```
NVL( <expr1> , <expr2> )
```

## Arguments

`expr1`
:   A general expression.

`expr2`
:   A general expression.

## Usage notes

- Snowflake performs [implicit conversion](/sql-reference/data-type-conversion#label-when-coercion-occurs) of arguments to make
  them compatible. For example, if one of the input expressions is a numeric type, the return type
  is also a numeric type. That is, `SELECT NVL('17', 1);` first converts the VARCHAR value `'17'`
  to the NUMBER value `17`, and then returns the first non-NULL value.

  When conversion isn’t possible, implicit conversion fails. For example, `SELECT NVL('foo', 1);`
  returns an error because the VARCHAR value `'foo'` can’t be converted to a NUMBER value.

  We recommend passing in arguments of the same type or explicitly converting arguments if needed.

- When implicit conversion converts a non-numeric value to a numeric value, the result is a value
  of type NUMBER(18,5).

  For numeric string arguments that aren’t constants, if NUMBER(18,5) isn’t sufficient to represent
  the numeric value, then [cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) the argument to a type that
  can represent the value.

- Either expression can include a `SELECT` statement containing set
  operators, such as `UNION`, `INTERSECT`, `EXCEPT`, and `MINUS`.
  When using set operators, make sure that data types are compatible. For
  details, see the [General usage notes](/sql-reference/operators-query#label-operators-query-general-usage-notes) in the
  [Set operators](/sql-reference/operators-query) topic.

## Collation details

- The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.
- The collation of the result of the function is the highest-[precedence](/sql-reference/collation#label-determining-the-collation-used-in-an-operation) collation of the inputs.

## Returns

Returns the data type of the returned expression.

If both expressions are NULL, returns NULL.

## Examples

Create a table that contains contact information for suppliers:

Copy code

```
CREATE TABLE IF NOT EXISTS suppliers (
  supplier_id INT PRIMARY KEY,
  supplier_name VARCHAR(30),
  phone_region_1 VARCHAR(15),
  phone_region_2 VARCHAR(15));
```

The table contains the phone number for each supplier in two different regions. The phone number can
be NULL for a region.

Insert values into the table:

Copy code

```
INSERT INTO suppliers(supplier_id, supplier_name, phone_region_1, phone_region_2)
  VALUES(1, 'Company_ABC', NULL, '555-01111'),
        (2, 'Company_DEF', '555-01222', NULL),
        (3, 'Company_HIJ', '555-01333', '555-01444'),
        (4, 'Company_KLM', NULL, NULL);
```

The following SELECT statement uses the NVL function to
retrieve the `phone_region_1` and `phone_region_2` values.

This example shows the following results for the NVL function:

- The `IF_REGION_1_NULL` column contains the value in `phone_region_1` or, if that value is NULL, the
  value in `phone_region_2`.
- The `IF_REGION_2_NULL` column contains the value in `phone_region_2` or, if that value is NULL, the
  value in `phone_region_1`.
- If both `phone_region_1` and `phone_region_2` are NULL, the function returns NULL.

Copy code

```
SELECT supplier_id,
       supplier_name,
       phone_region_1,
       phone_region_2,
       NVL(phone_region_1, phone_region_2) IF_REGION_1_NULL,
       NVL(phone_region_2, phone_region_1) IF_REGION_2_NULL
  FROM suppliers
  ORDER BY supplier_id;
```

```
+-------------+---------------+----------------+----------------+------------------+------------------+
| SUPPLIER_ID | SUPPLIER_NAME | PHONE_REGION_1 | PHONE_REGION_2 | IF_REGION_1_NULL | IF_REGION_2_NULL |
|-------------+---------------+----------------+----------------+------------------+------------------|
|           1 | Company_ABC   | NULL           | 555-01111      | 555-01111        | 555-01111        |
|           2 | Company_DEF   | 555-01222      | NULL           | 555-01222        | 555-01222        |
|           3 | Company_HIJ   | 555-01333      | 555-01444      | 555-01333        | 555-01444        |
|           4 | Company_KLM   | NULL           | NULL           | NULL             | NULL             |
+-------------+---------------+----------------+----------------+------------------+------------------+
```
