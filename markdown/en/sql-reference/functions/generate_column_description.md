Categories:
:   [Metadata functions](/sql-reference/functions-metadata)

# GENERATE\_COLUMN\_DESCRIPTION

Generates a list of columns from a set of staged files that contain semi-structured data using the
[INFER\_SCHEMA](/sql-reference/functions/infer_schema) function output.

The output from this function can be used as input when manually creating a table, external table, Apache Iceberg™ table, or view (using the appropriate
[CREATE <object>](/sql-reference/sql/create) command) based on the column definitions of the staged files.

Alternatively, the [CREATE TABLE](/sql-reference/sql/create-table) or [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) command with the USING TEMPLATE clause can be used to create a new table with the
column definitions derived from the same INFER\_SCHEMA function output.

## Syntax

Copy code

```
GENERATE_COLUMN_DESCRIPTION( <expr> , '<string>' )
```

## Arguments

`expr`
:   Output of the INFER\_SCHEMA function formatted as an array.

`'string'`
:   Type of object that could be created from the column list. The appropriate formatting for this type is applied to the output.

    Possible values are `table`, `external_table`, or `view`.

## Returns

The function returns the list of columns in a set of staged files, which can be
used as input when creating an object of the type identified in the second argument.

## Examples

Detect, format, and output the set of column definitions in a set of Parquet files staged in the `mystage` stage. The output columns are
formatted for creating a table.

This example builds on an example in the [INFER\_SCHEMA](/sql-reference/functions/infer_schema) topic:

Copy code

```
-- Create a file format that sets the file type as Parquet.
CREATE FILE FORMAT my_parquet_format
  TYPE = parquet;

-- Query the GENERATE_COLUMN_DESCRIPTION function.
SELECT GENERATE_COLUMN_DESCRIPTION(ARRAY_AGG(OBJECT_CONSTRUCT(*)), 'table') AS COLUMNS
  FROM TABLE (
    INFER_SCHEMA(
      LOCATION=>'@mystage',
      FILE_FORMAT=>'my_parquet_format'
    )
  );

+--------------------+
| COLUMN_DESCRIPTION |
|--------------------|
| "country" VARIANT, |
| "continent" TEXT   |
+--------------------+

-- The function output can be used to define the columns in a table.
CREATE TABLE mytable ("country" VARIANT, "continent" TEXT);
```

Same as the previous example, but generates a set of columns formatted for creating an external table:

Copy code

```
-- Query the GENERATE_COLUMN_DESCRIPTION function.
SELECT GENERATE_COLUMN_DESCRIPTION(ARRAY_AGG(OBJECT_CONSTRUCT(*)), 'external_table') AS COLUMNS
  FROM TABLE (
    INFER_SCHEMA(
      LOCATION=>'@mystage',
      FILE_FORMAT=>'my_parquet_format'
    )
  );

+---------------------------------------------+
| COLUMN_DESCRIPTION                          |
|---------------------------------------------|
| "country" VARIANT AS ($1:country::VARIANT), |
| "continent" TEXT AS ($1:continent::TEXT)    |
+---------------------------------------------+
```

Same as the previous examples, but generates a set of columns formatted for creating an Iceberg table:

Copy code

```
-- Create a file format that sets the file type as Parquet.
CREATE OR REPLACE FILE FORMAT my_parquet_format
  TYPE = PARQUET
  USE_VECTORIZED_SCANNER = TRUE;

-- Query the GENERATE_COLUMN_DESCRIPTION function.
SELECT GENERATE_COLUMN_DESCRIPTION(ARRAY_AGG(OBJECT_CONSTRUCT(*)), 'table') AS COLUMNS
  FROM TABLE (
    INFER_SCHEMA(
      LOCATION=>'@my_int_stage',
      FILE_FORMAT=>'my_parquet_format',
      KIND => 'ICEBERG'
    )
  );

+---------------------------------------------+
| COLUMN_DESCRIPTION                          |
|---------------------------------------------|
| "id" INT NOT NULL,                          |
| "custnum" INT NOT NULL                      |
+---------------------------------------------+
```

Same as the previous examples, but generates a set of columns formatted for creating a view:

Copy code

```
-- Query the GENERATE_COLUMN_DESCRIPTION function.
SELECT GENERATE_COLUMN_DESCRIPTION(ARRAY_AGG(OBJECT_CONSTRUCT(*)), 'view') AS COLUMNS
  FROM TABLE (
    INFER_SCHEMA(
      LOCATION=>'@mystage',
      FILE_FORMAT=>'my_parquet_format'
    )
  );

+--------------------+
| COLUMN_DESCRIPTION |
|--------------------|
| "country" ,        |
| "continent"        |
+--------------------+
```

Note

Using `*` for `ARRAY_AGG(OBJECT_CONSTRUCT())` might result in an error if the returned result is larger
than 128 MB. Avoid using `*` for larger result sets, and only use the required columns, `COLUMN NAME`,
`TYPE`, and `NULLABLE`, for the query. You can include the optional column `ORDER_ID` when using
`WITHIN GROUP (ORDER BY order_id)`.
