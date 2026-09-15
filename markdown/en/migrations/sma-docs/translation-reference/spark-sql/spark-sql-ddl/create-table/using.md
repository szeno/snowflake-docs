description:
:   Who is USING who?

# Snowpark Migration Accelerator: Using

## Description

The USING command in Spark specifies which file format should be used when creating a table. Common formats include CSV, JSON, and AVRO. For more detailed information about the Create Table USING command, refer to the [Databricks documentation](https://docs.databricks.com/en/archive/spark-sql-2.x-language-manual/create-table.html).

## Syntax

Copy code

```
CREATE TABLE [IF NOT EXISTS] [db_name.]table_name
  [(col_name1 col_type1 [COMMENT col_comment1], ...)]
  USING data_source
  [OPTIONS (key1 [ = ] val1, key2 [ = ] val2, ...)]
  [PARTITIONED BY (col_name1, col_name2, ...)]
  [CLUSTERED BY (col_name3, col_name4, ...) INTO num_buckets BUCKETS]
  [LOCATION path]
  [COMMENT table_comment]
  [TBLPROPERTIES (key1 [ = ] val1, key2 [ = ] val2, ...)]
  [AS select_statement]
```

## Sample source patterns

The `USING` data source statement is not supported in Snowflake. During migration, this statement will be commented out and marked with an Error, Warning, and Issue (EWI) message indicating that it is unsupported.

### Sample data

Copy code

```
CREATE TABLE table1
(
id INTEGER
) USING DELTA;
```

Copy code

```
CREATE TABLE table1
(
id INTEGER
) /*** MSC-WARNING - MSCEWI# - SNOWFLAKE DOES NOT SUPPORT USING STATEMENT ***/
-- USING DELTA;
```

## Known Issues

Snowflake does not support the USING data source clause in SQL statements.

## Related EWIs

- Snowflake does not support the USING statement in SQL queries.
