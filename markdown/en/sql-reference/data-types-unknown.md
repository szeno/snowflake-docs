# UNKNOWN data type

This topic describes the UNKNOWN data type.

## UNKNOWN

The UNKNOWN data type is an [Apache Iceberg™ v3](https://iceberg.apache.org/spec/#primitive-types)
primitive type. Use it to define a column or field whose type isn’t known yet.

An UNKNOWN column or field has the following characteristics:

- It has no physical storage in the underlying Parquet data files.
- It always reads as `NULL` for every row.
- It’s always nullable. You can’t apply a `NOT NULL` constraint.
- You can’t write a value to it.

The UNKNOWN type is only supported in [Apache Iceberg tables](/user-guide/tables-iceberg)
(both Snowflake-managed and externally managed) that use Iceberg format version 3 (`ICEBERG_VERSION = 3`).
It isn’t supported in standard Snowflake tables.

### Specifying an UNKNOWN column or field

To define an UNKNOWN column, use the `UNKNOWN` keyword as the column type in a
`CREATE ICEBERG TABLE` statement:

Copy code

```
CREATE ICEBERG TABLE my_iceberg_table (c1 INT, c2 UNKNOWN, c3 INT)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 'my_iceberg_table'
  ICEBERG_VERSION = 3;
```

You can also use UNKNOWN as a field type inside a structured [OBJECT](/sql-reference/data-types-structured#label-structured-types-specifying-object):

Copy code

```
CREATE ICEBERG TABLE my_iceberg_table (c1 INT, c2 OBJECT(f1 INT, f2 UNKNOWN, f3 INT))
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 'my_iceberg_table'
  ICEBERG_VERSION = 3;
```

UNKNOWN isn’t supported as the element type of an [ARRAY](/sql-reference/data-types-structured#label-structured-types-specifying-array)
or as the key or value type of a [MAP](/sql-reference/data-types-structured#label-structured-types-specifying-map). The
following definitions are rejected:

Copy code

```
ARRAY(UNKNOWN)
MAP(UNKNOWN, VARCHAR)
MAP(VARCHAR, UNKNOWN)
```

## Reading UNKNOWN columns and fields

Because an UNKNOWN column has no storage, it always returns `NULL`:

Copy code

```
SELECT c1, c2, c3 FROM my_iceberg_table;
```

```
+----+------+----+
| C1 | C2   | C3 |
|----+------+----|
|  1 | NULL | 10 |
|  2 | NULL | 20 |
+----+------+----+
```

When you read a structured OBJECT that contains an UNKNOWN field, the field is present in the
result and its value is `NULL`. For example, reading a column defined as
`OBJECT(f1 INT, f2 UNKNOWN, f3 INT)` returns:

```
{
  "f1": 1,
  "f2": null,
  "f3": 3
}
```

Aggregate functions treat an UNKNOWN column as `NULL`:

- `COUNT(*)` counts all rows.
- `COUNT(<unknown_column>)` returns `0`.
- `MIN`, `MAX`, `SUM`, and `AVG` return `NULL`.
- `GROUP BY` on an UNKNOWN column groups all rows into a single `NULL` group.

### Extracting an UNKNOWN field with path syntax

Extracting an UNKNOWN field from a structured OBJECT with [path notation](/sql-reference/data-types-structured)
(for example, `my_object_column:my_unknown_field`) returns `NULL`, because the field has no stored
value.

## Writing to UNKNOWN columns and fields

You can’t write a value to an UNKNOWN column or field. They always remain `NULL`. How you write
to a table that contains UNKNOWN depends on whether UNKNOWN is a top-level column or a field inside
a structured OBJECT.

### Top-level UNKNOWN columns

`INSERT`, `UPDATE`, and `MERGE` operations that target an UNKNOWN column directly fail with an
error. Omit UNKNOWN columns from the column list when you write rows. The remaining columns are
populated as usual:

Copy code

```
INSERT INTO my_iceberg_table (c1, c3) VALUES (1, 10);
```

### UNKNOWN fields inside structured objects

To write to a structured OBJECT column that contains UNKNOWN fields, supply a source object that
includes only the non-UNKNOWN fields, with matching field names, order, and coercible types. The
UNKNOWN fields are stored as `NULL` automatically. For example, given a column defined as
`c2 OBJECT(f1 INT, f2 UNKNOWN, f3 INT)`:

Copy code

```
INSERT INTO my_iceberg_table (c2)
  SELECT OBJECT_CONSTRUCT('f1', 1, 'f3', 3)::OBJECT(f1 INT, f3 INT);

UPDATE my_iceberg_table
  SET c2 = OBJECT_CONSTRUCT('f1', 10, 'f3', 30)::OBJECT(f1 INT, f3 INT);
```

Supplying a source object that adds an extra field or uses a field name that doesn’t match the
target schema results in an error.

## Loading and unloading data

When you load data with [COPY INTO <table>](/sql-reference/sql/copy-into-table) into an Iceberg
table that has UNKNOWN columns or fields, the source file must omit those columns and fields,
because they have no physical storage. After loading, the UNKNOWN columns and fields read back as
`NULL`. For example, when loading into a table defined as `t (a INT, b STRING, c UUID, u UNKNOWN)`,
provide values only for `a`, `b`, and `c`; `u` reads back as `NULL`.

When you unload data with [COPY INTO <location>](/sql-reference/sql/copy-into-location), an
UNKNOWN column is exported as `NULL`.

## Evolving an UNKNOWN column

You can evolve an UNKNOWN column to any primitive type through schema evolution:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table ALTER COLUMN c2 SET DATA TYPE INT;
```

You can’t evolve an UNKNOWN column directly to a structured type (ARRAY, OBJECT, or MAP).

## CREATE TABLE AS SELECT and query results

When you use [CREATE TABLE <table> AS SELECT](/sql-reference/sql/create-table) with a query that
selects a top-level UNKNOWN column, the type of the resulting column depends on the target table:

- If the target is an Iceberg v3 table, the UNKNOWN column is preserved as UNKNOWN.
- If the target is a standard Snowflake table, which can’t store UNKNOWN, the UNKNOWN column is
  converted to a nullable VARCHAR column that contains `NULL`. A top-level UNKNOWN column is also
  reported as VARCHAR in the result metadata.

You can’t use CREATE TABLE AS SELECT with a query that selects a structured type column (ARRAY,
OBJECT, or MAP) that contains UNKNOWN fields. This operation returns an error.

## Examples for the UNKNOWN data type

Create a managed Iceberg table with an UNKNOWN column, insert rows, and read the column back as `NULL`:

Copy code

```
CREATE ICEBERG TABLE t (c1 INT, c2 UNKNOWN, c3 INT)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 't'
  ICEBERG_VERSION = 3;

INSERT INTO t (c1, c3) VALUES (1, 10), (2, 20);

SELECT * FROM t;
```

```
+----+------+----+
| C1 | C2   | C3 |
|----+------+----|
|  1 | NULL | 10 |
|  2 | NULL | 20 |
+----+------+----+
```

Later, promote the UNKNOWN column to a concrete type:

Copy code

```
ALTER ICEBERG TABLE t ALTER COLUMN c2 SET DATA TYPE VARCHAR;
```

## Limitations for the UNKNOWN data type

- UNKNOWN is supported only in Iceberg tables that use `ICEBERG_VERSION = 3`. It isn’t supported in
  standard Snowflake tables.
- An UNKNOWN column or field is always nullable and can’t take a `NOT NULL` constraint.
- You can’t write a value to an UNKNOWN column or field.
- UNKNOWN isn’t allowed as an ARRAY element type or a MAP key or value type.
- You can evolve an UNKNOWN column to a primitive type only, not to a structured type.
- UNKNOWN isn’t supported in user-defined functions (UDFs), user-defined table functions (UDTFs),
  or stored procedures.
