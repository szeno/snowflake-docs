Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# CAST , `::`

Converts a value of one data type into another data type. The semantics of CAST
are the same as the semantics of the corresponding TO\_ `datatype` conversion
functions. If the cast is not possible, an error is raised. For more details,
see the individual TO\_ `datatype` conversion functions. For more information
about data type conversion and the TO\_ `datatype` conversion
functions, see [Data type conversion](/sql-reference/data-type-conversion).

The `::` operator provides alternative syntax for CAST.

See also:
:   [TRY\_CAST](/sql-reference/functions/try_cast)

## Syntax

Copy code

```
CAST( <source_expr> AS <target_data_type> )
  [ RENAME FIELDS | ADD FIELDS ]

<source_expr> :: <target_data_type>
```

## Arguments

`source_expr`
:   Expression of any supported data type to be converted into a
    different data type.

`target_data_type`
:   The data type to which to convert the expression. If the data
    type supports additional properties, such as
    [precision and scale](/sql-reference/data-types-numeric#label-data-types-numeric-precision-and-scale)
    (for numbers/decimals), the properties can be included.

`RENAME FIELDS`
:   For [structured OBJECTs](/sql-reference/data-types-structured), specifies that you want to change the OBJECT to use
    different key-value pairs. The values in the original object are copied to the new key-value pairs in the order in which
    they appear.

    For an example, see [Example: Changing the key names in an OBJECT value](/sql-reference/data-types-structured#label-structured-types-casting-struct-struct-object-key-names).

`ADD FIELDS`
:   For [structured OBJECTs](/sql-reference/data-types-structured), specifies that you want to add key-value pairs to the
    OBJECT.

    For an example, see [Example: Adding keys to an OBJECT value](/sql-reference/data-types-structured#label-structured-types-casting-struct-struct-object-key-add).

    The values for the newly added keys will be set to NULL. If you want to assign a value to these keys, call the
    [OBJECT\_INSERT](/sql-reference/data-types-structured#label-structured-types-transform-object-insert) function instead.

## Usage notes

- If the scale is not sufficient to hold the input value, the function
  rounds the value.
- If the precision is not sufficient to hold the input value, the function
  raises an error.
- When numeric columns are explicitly cast to forms of the integer data type during a data unload to Parquet files, the data type of these
  columns in the Parquet files is INT. For more information, see [Explicitly convert numeric columns to Parquet data types](/user-guide/data-unload-considerations#label-converting-numeric-columns-to-parquet-data-types).
- Collation specifications aren’t retained when values are cast to
  [text string data types](/sql-reference/data-types-text#label-character-datatypes) (for example, VARCHAR and STRING). You can include collation
  specifications when you cast values (for example, `CAST(myvalue AS VARCHAR) COLLATE 'en-ai'`).
- When you use the `::` alternative syntax, you cannot specify the `RENAME FIELDS` or `ADD FIELDS` arguments.

## Examples

The CAST examples use the data in the following table:

Copy code

```
CREATE OR REPLACE TABLE test_data_type_conversion (
  varchar_value VARCHAR,
  number_value NUMBER(5, 4),
  timestamp_value TIMESTAMP);

INSERT INTO test_data_type_conversion VALUES (
  '9.8765',
  1.2345,
  '2024-05-09 14:32:29.135 -0700');

SELECT * FROM test_data_type_conversion;
```

```
+---------------+--------------+-------------------------+
| VARCHAR_VALUE | NUMBER_VALUE | TIMESTAMP_VALUE         |
|---------------+--------------+-------------------------|
| 9.8765        |       1.2345 | 2024-05-09 14:32:29.135 |
+---------------+--------------+-------------------------+
```

The examples use the [SYSTEM$TYPEOF](/sql-reference/functions/system_typeof) function to show the data type of the converted value.

Convert a string to a number with specified scale (2):

Copy code

```
SELECT CAST(varchar_value AS NUMBER(5,2)) AS varchar_to_number1,
       SYSTEM$TYPEOF(varchar_to_number1) AS data_type
  FROM test_data_type_conversion;
```

```
+--------------------+------------------+
| VARCHAR_TO_NUMBER1 | DATA_TYPE        |
|--------------------+------------------|
|               9.88 | NUMBER(5,2)[SB4] |
+--------------------+------------------+
```

Convert the same string to a number with scale 5, using
the `::` notation:

Copy code

```
SELECT varchar_value::NUMBER(6,5) AS varchar_to_number2,
       SYSTEM$TYPEOF(varchar_to_number2) AS data_type
  FROM test_data_type_conversion;
```

```
+--------------------+------------------+
| VARCHAR_TO_NUMBER2 | DATA_TYPE        |
|--------------------+------------------|
|            9.87650 | NUMBER(6,5)[SB4] |
+--------------------+------------------+
```

Convert a number to an integer. For an integer, precision and scale cannot be specified, so
the default is always NUMBER(38, 0).

Copy code

```
SELECT CAST(number_value AS INTEGER) AS number_to_integer,
       SYSTEM$TYPEOF(number_to_integer) AS data_type
  FROM test_data_type_conversion;
```

```
+-------------------+-------------------+
| NUMBER_TO_INTEGER | DATA_TYPE         |
|-------------------+-------------------|
|                 1 | NUMBER(38,0)[SB1] |
+-------------------+-------------------+
```

Convert a number to a string:

Copy code

```
SELECT CAST(number_value AS VARCHAR) AS number_to_varchar,
       SYSTEM$TYPEOF(number_to_varchar) AS data_type
  FROM test_data_type_conversion;
```

```
+-------------------+--------------+
| NUMBER_TO_VARCHAR | DATA_TYPE    |
|-------------------+--------------|
| 1.2345            | VARCHAR[LOB] |
+-------------------+--------------+
```

Convert a string to a VARCHAR value with a specified length:

Copy code

```
SELECT varchar_value,
       SYSTEM$TYPEOF(varchar_value) AS data_type_source,
       CAST(varchar_value AS VARCHAR(9)) AS converted_varchar,
       SYSTEM$TYPEOF(converted_varchar) AS data_type_converted
  FROM test_data_type_conversion;
```

```
+---------------+------------------------+-------------------+---------------------+
| VARCHAR_VALUE | DATA_TYPE_SOURCE       | CONVERTED_VARCHAR | DATA_TYPE_CONVERTED |
|---------------+------------------------+-------------------+---------------------|
| 9.8765        | VARCHAR(16777216)[LOB] | 9.8765            | VARCHAR(9)[LOB]     |
+---------------+------------------------+-------------------+---------------------+
```

If you are casting a value to the VARCHAR type with a specified length and the value exceeds that
length, an error is returned:

Copy code

```
SELECT CAST(varchar_value AS VARCHAR(4))
  FROM test_data_type_conversion;
```

```
100078 (22000): String '9.8765' is too long and would be truncated
```

Convert a timestamp to a date:

Copy code

```
SELECT CAST(timestamp_value AS DATE) AS timestamp_to_date,
       SYSTEM$TYPEOF(timestamp_to_date) AS data_type
  FROM test_data_type_conversion;
```

```
+-------------------+-----------+
| TIMESTAMP_TO_DATE | DATA_TYPE |
|-------------------+-----------|
| 2024-05-09        | DATE[SB4] |
+-------------------+-----------+
```
