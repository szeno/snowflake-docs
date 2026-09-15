# Redshift - System catalog tables

Note

This is a work in progress.

## Description

> The system catalogs store schema metadata, such as information about tables and columns. System catalog tables have a PG prefix.
>
> The standard PostgreSQL catalog tables are accessible to Amazon Redshift users. ([Redshift SQL Language reference System catalog tables](https://docs.aws.amazon.com/redshift/latest/dg/c_intro_catalog_views.html)).

The following table outlines how references to SQL functions defined in the `pg_catalog` in Redshift are transformed.

## Mapping of SQL functions from the `pg_catalog`

| Redshift | Snowflake |
| --- | --- |
| pg\_catalog.row\_number() | [row\_number()](https://docs.snowflake.com/en/sql-reference/functions/row_number) |
| pg\_catalog.replace() | [replace()](https://docs.snowflake.com/en/sql-reference/functions/replace) |
| pg\_catalog.lead() | [lead()](https://docs.snowflake.com/en/sql-reference/functions/lead) |
