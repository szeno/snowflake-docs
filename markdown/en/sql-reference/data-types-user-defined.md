# User-defined types

You can define *user-defined types*, which are new data types that are based on existing
[Snowflake data types](/sql-reference-data-types). For example, suppose that you want to
define a column for the age of a person, and you want to restrict the values to include numbers with at
most three digits and no digits after the decimal point. You can define a data type named `age` that
corresponds to `NUMBER(3,0)`.

A user-defined type is a schema-level object that can be used in all of the places that types can be used, including
column definitions, function and procedure definitions, and cast expressions.

User-defined types can simplify schema maintenance and improve data quality. You can define a user-defined type
once, and then use it in multiple objects.

You can also use user-defined types to group related data fields into a single, logical column, instead of using
multiple columns or tables for the fields. For example, you can define a data type for addresses that is a
[structured OBJECT type](/sql-reference/data-types-structured#label-structured-types-specifying-object) with fields for the street address,
city, state, and ZIP Code.

## Privileges required for user-defined types

To create a user-defined type in a schema, you must use a role that has been granted the CREATE TYPE privilege on that schema.

For more information, see the [access control requirements for user-defined types](/user-guide/security-access-control-privileges#label-access-control-privileges-type).

## General usage notes for user-defined types

- To change the definition of a user-defined type, drop it and re-create it.

  If you change the definition of a user-defined type:

  - SQL statements that directly operate on table columns that use the type might
    return errors, including SELECT statements and DML statements. However, SQL statements that don’t directly operate on
    table columns that use the type run normally. For example, if a table contains a user-defined type column
    named `typed_column`, and a SELECT statement specifies other columns in its SELECT list, the SELECT statement runs
    normally. To correct the problem, you can revise the SQL statements to use the underlying Snowflake types.
  - Calls to functions and stored procedures that use the type return errors. To correct the problem,
    drop and re-create the functions and stored procedures.
- The [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column) command can change the data type of a column from a user-defined
  type to a compatible [Snowflake data type](/sql-reference-data-types), or from a Snowflake data type to a
  user-defined type.
- When you are constructing an object to insert into a column of a user-defined type by using the
  [OBJECT\_CONSTRUCT](/sql-reference/functions/object_construct) function or an [OBJECT constant](/sql-reference/data-types-semistructured#label-object-constant),
  cast the result to the user-defined type.

  For examples, see [Using a user-defined type for a table column](#label-user-defined-type-examples-table-column).
- When [set operators](/sql-reference/operators-query) (for example, UNION, INTERSECT, EXCEPT) or
  [conditional expression functions](/sql-reference/expressions-conditional) (for example, CASE, IFF, COALESCE, NVL, and so on)
  evaluate an expression that resolves to a value of a user-defined type, Snowflake determines a common type using the underlying
  base types of the operands. By default, the data type of the result is this base type. If you want the result to be a value of a
  user-defined type, explicitly cast the final expression to the user-defined type.

  The following rules apply when user-defined types are used in set operations or conditional expression functions:

  - User-defined types are distinct from their base types, but, in expression type resolution, they coerce to their base
    types to find a common type.
  - If the branches or operands resolve to a single Snowflake type (for example, VARCHAR or NUMBER), that is the result type.
  - To preserve a user-defined type or produce a result that is a value of a user-defined type,
    [cast](#label-user-defined-type-casting-explicit) the overall expression by
    using `CAST(expr AS {user-defined type})` or `expr::{user-defined type}`.
  - Incompatible base types (for example, VARCHAR and NUMBER) follow normal
    [coercion rules](/sql-reference/data-type-conversion). If no common base type exists, an error is returned.

  For examples, see [Using set operators and conditional expression functions with user-defined types](#label-user-defined-type-examples-set-operators-conditional-expression-functions).
- Using user-defined types and compatible Snowflake data types for function [overloading](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading)
  is allowed. That is, you can specify a user-defined type for a function argument type, and you can specify a compatible Snowflake
  data type for an argument type of a function with the same name.
- If a user-defined type is specified as the RETURN type of a SQL user-defined function (UDF) or Snowflake Scripting stored procedure,
  the return value must be explicitly cast to the user-defined type in the body of the UDF or stored procedure.
- When a user-defined type is used as an argument or return value for a UDF or procedure written in a language other
  than SQL (such as Python or Java), the user-defined type is treated the same as its base type.
- [Schema evolution](/user-guide/data-load-schema-evolution) isn’t supported for user-defined types.

## Casting user-defined types

User-defined types support [data type conversion](/sql-reference/data-type-conversion), including
both explicit casting and implicit casting (coercion):

- [Explicit casting to and from user-defined types](#label-user-defined-type-casting-explicit)
- [Coercion of user-defined types](#label-user-defined-type-coercion)

### Explicit casting to and from user-defined types

A user-defined type value can be cast to the same data types as values of its base type. For example,
create a user-defined type named `age` that is based on the NUMBER type:

Copy code

```
CREATE TYPE age AS NUMBER(3,0);
```

A value can be cast to a user-defined type if the value can be cast to the base type of the user-defined type.
For example, the value `10` can be cast to the NUMBER type, so you can cast the value to the `age` type:

Copy code

```
SELECT 10::age;
```

A user-defined type value can be cast to a different data type if the base type of the user-defined type can be
cast to that data type. For example, a NUMBER value can be cast to the VARCHAR type, so the value `10` of
user-defined type `age` can be cast to the VARCHAR type:

Copy code

```
SELECT 10::age::VARCHAR;
```

### Coercion of user-defined types

A user-defined type value coerces to its base type. Therefore, in all operations, it behaves the same as
its base type. For example, create a user-defined type named `age` that is based on the NUMBER type and
a table with two columns of type `age`:

Copy code

```
CREATE TYPE age AS NUMBER(3,0);

CREATE TABLE test_age_udf(a age, b age);
```

Insert values into the table:

Copy code

```
INSERT INTO test_age_udf VALUES (10, 20);
```

The following example performs an addition operation on the table values, and Snowflake coerces the `age` values to values
of type NUMBER to complete the operation. The example uses the [SYSTEM$TYPEOF](/sql-reference/functions/system_typeof) function to show
the data type of the result:

Copy code

```
SELECT a + b AS result,
       SYSTEM$TYPEOF(a + b) AS type
  FROM test_age_udf;
```

```
+--------+------------------+
| RESULT | TYPE             |
|--------+------------------|
|     30 | NUMBER(4,0)[SB1] |
+--------+------------------+
```

## Examples for user-defined data types

The following examples show you how to use user-defined types:

- [Using a user-defined type for a table column](#using-a-user-defined-type-for-a-table-column)
- [Using set operators and conditional expression functions with user-defined types](#using-set-operators-and-conditional-expression-functions-with-user-defined-types)

### Using a user-defined type for a table column

In the following example, you create a user-defined type named `address`, and then use the type in a table:

1. Create a user-defined type that is based on a [structured OBJECT type](/sql-reference/data-types-structured#label-structured-types-specifying-object)
   to store address information:

   Copy code

   ```
   CREATE TYPE address AS OBJECT(
     street VARCHAR(100),
     city VARCHAR(50),
     state_abbr CHAR(2),
     zip_code CHAR(10)
   );
   ```
2. Create a table that stores customer information, including the address:

   Copy code

   ```
   CREATE TABLE customers_udt_test (
     cust_id VARCHAR NOT NULL,
     cust_name VARCHAR(100),
     cust_address address
   );
   ```
3. Insert a row into the table, and specify the value for the `cust_address` column by casting an
   [OBJECT constant](/sql-reference/data-types-semistructured#label-object-constant) to the `address` type:

   Copy code

   ```
   INSERT INTO customers_udt_test (cust_id, cust_name, cust_address)
     SELECT
    '1000',
    'Example1 Inc',
    {
      'street': '101 Snow Street',
      'city': 'San Francisco',
      'state_abbr': 'CA',
      'zip_code': '94102'
    }::address;
   ```
4. Insert a row into the table, and specify the value for the `cust_address` column by calling the
   [OBJECT\_CONSTRUCT](/sql-reference/functions/object_construct) function and casting the return value to the `address`
   type:

   Copy code

   ```
   INSERT INTO customers_udt_test (cust_id, cust_name, cust_address)
     SELECT
    '1001',
    'Example2 Inc',
    OBJECT_CONSTRUCT(
      'street', '555 Polar Bear Street',
      'city', 'New York',
      'state_abbr', 'NY',
      'zip_code', '10001'
    )::address;
   ```
5. Insert a row into the table, and specify the value for the `cust_address` column by casting an OBJECT constant
   to the OBJECT type, which is the base type of the `address` type. It is usually easier to cast an OBJECT
   constant to the user-defined type, but this example shows that the OBJECT constant is coerced to the user-defined
   type:

   Copy code

   ```
   INSERT INTO customers_udt_test (cust_id, cust_name, cust_address)
     SELECT
    '1002',
    'Example3 Inc',
    {
      'street': '909 Flake Street',
      'city': 'Seattle',
      'state_abbr': 'WA',
      'zip_code': '98109'
    }::OBJECT(
         street VARCHAR(100),
         city VARCHAR(50),
         state_abbr CHAR(2),
         zip_code CHAR(10));
   ```
6. To show the inserted rows, query the table:

   Copy code

   ```
   SELECT * FROM customers_udt_test;
   ```

   ```
   +---------+--------------+--------------------------------------+
   | CUST_ID | CUST_NAME    | CUST_ADDRESS                         |
   |---------+--------------+--------------------------------------|
   | 1000    | Example1 Inc | {                                    |
   |         |              |   "street": "101 Snow Street",       |
   |         |              |   "city": "San Francisco",           |
   |         |              |   "state_abbr": "CA",                |
   |         |              |   "zip_code": "94102"                |
   |         |              | }                                    |
   | 1001    | Example2 Inc | {                                    |
   |         |              |   "street": "555 Polar Bear Street", |
   |         |              |   "city": "New York",                |
   |         |              |   "state_abbr": "NY",                |
   |         |              |   "zip_code": "10001"                |
   |         |              | }                                    |
   | 1002    | Example3 Inc | {                                    |
   |         |              |   "street": "909 Flake Street",      |
   |         |              |   "city": "Seattle",                 |
   |         |              |   "state_abbr": "WA",                |
   |         |              |   "zip_code": "98109"                |
   |         |              | }                                    |
   +---------+--------------+--------------------------------------+
   ```
7. Query the table, and use the colon operator to show only the `zip_code` values in the `address` data:

   Copy code

   ```
   SELECT cust_id,
       cust_name,
       cust_address:zip_code
     FROM customers_udt_test;
   ```

   ```
   +---------+--------------+-----------------------+
   | CUST_ID | CUST_NAME    | CUST_ADDRESS:ZIP_CODE |
   |---------+--------------+-----------------------|
   | 1000    | Example1 Inc | 94102                 |
   | 1001    | Example2 Inc | 10001                 |
   | 1002    | Example3 Inc | 98109                 |
   +---------+--------------+-----------------------+
   ```

### Using set operators and conditional expression functions with user-defined types

When [set operators](/sql-reference/operators-query) or [conditional expression functions](/sql-reference/expressions-conditional)
evaluate values of Snowflake types and user-defined types, the types must be compatible and coercible into a single type. The resulting
output is of the Snowflake base type, unless it is explicitly cast to a user-defined type. For more information, see
[General usage notes for user-defined types](#label-user-defined-type-usage-notes).

The examples in this section use set operators and conditional expressions with user-defined types.
First, create several user-defined types with various base types:

Copy code

```
CREATE TYPE us_zipcode AS VARCHAR;
CREATE TYPE uk_postcode AS VARCHAR;
CREATE TYPE positive_integer AS INTEGER;
CREATE TYPE positive_number AS NUMBER;
```

The following query calls the IFF function. The call evaluates a value of the `us_zipcode` user-defined
type and a value of a compatible Snowflake type. The query uses the [SYSTEM$TYPEOF](/sql-reference/functions/system_typeof) function to
show that the result is Snowflake base type VARCHAR:

Copy code

```
SELECT IFF(TRUE, '90210'::us_zipcode, '10006') AS result,
       SYSTEM$TYPEOF(IFF(TRUE, '90210'::us_zipcode, '10006')) AS type;
```

```
+--------+-------------------------+
| RESULT | TYPE                    |
|--------+-------------------------|
| 90210  | VARCHAR(134217728)[LOB] |
+--------+-------------------------+
```

The following query is the same as the previous query, but it casts the result to the `us_zipcode` user-defined type:

Copy code

```
SELECT IFF(TRUE, '90210'::us_zipcode, '10006')::us_zipcode AS result,
       SYSTEM$TYPEOF(IFF(TRUE, '90210'::us_zipcode, '10006')::us_zipcode) AS type;
```

```
+--------+-------------------------------+
| RESULT | TYPE                          |
|--------+-------------------------------|
| 90210  | MYDB.MYSCHEMA.US_ZIPCODE[LOB] |
+--------+-------------------------------+
```

The following query contains a CASE expression that evaluates different but compatible user-defined
types and returns a value of a Snowflake base type:

Copy code

```
SELECT CASE
         WHEN TRUE THEN 'SW1A 0AA'::uk_postcode
           ELSE '90210'::us_zipcode
         END AS result,
       SYSTEM$TYPEOF(CASE
         WHEN TRUE THEN 'SW1A 0AA'::uk_postcode
           ELSE '90210'::us_zipcode
         END) AS type;
```

```
+----------+-------------------------+
| RESULT   | TYPE                    |
|----------+-------------------------|
| SW1A 0AA | VARCHAR(134217728)[LOB] |
+----------+-------------------------+
```

The following query is the same as the previous query, but it casts the result to the `uk_postcode` user-defined type:

Copy code

```
SELECT CAST(CASE
         WHEN TRUE THEN 'SW1A 0AA'::uk_postcode
           ELSE '90210'::us_zipcode
         END AS uk_postcode) AS result,
       SYSTEM$TYPEOF(CAST(CASE
         WHEN TRUE THEN 'SW1A 0AA'::uk_postcode
           ELSE '90210'::us_zipcode
         END AS uk_postcode)) AS type;
```

```
+----------+--------------------------------------------+
| RESULT   | TYPE                                       |
|----------+--------------------------------------------|
| SW1A 0AA | MYDB.MYSCHEMA.UK_POSTCODE[LOB]             |
+----------+--------------------------------------------+
```

The following query contains a COALESCE expression that evaluates different but compatible user-defined
types and returns a value of a Snowflake base type:

Copy code

```
SELECT COALESCE(
         5::positive_integer,
         10::positive_number) AS result,
       SYSTEM$TYPEOF(COALESCE(
         5::positive_integer,
         10::positive_number)) AS type;
```

```
+--------+-------------------+
| RESULT | TYPE              |
|--------+-------------------|
|      5 | NUMBER(38,0)[SB1] |
+--------+-------------------+
```

The following query is the same as the previous query, but it casts the result to the `positive_number` user-defined type:

Copy code

```
SELECT CAST(COALESCE(
         5::positive_integer,
         10::positive_number
       ) AS positive_number) AS result,
       SYSTEM$TYPEOF(CAST(COALESCE(
         5::positive_integer,
         10::positive_number
       ) AS positive_number)) AS type;
```

```
+--------+------------------------------------+
| RESULT | TYPE                               |
|--------+------------------------------------|
|      5 | MYDB.MYSCHEMA.POSITIVE_NUMBER[SB1] |
+--------+------------------------------------+
```
