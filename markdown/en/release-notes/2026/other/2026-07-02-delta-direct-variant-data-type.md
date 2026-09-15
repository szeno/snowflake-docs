# Jul 2, 2026: VARIANT data type on Delta Direct tables (*General availability*)

With this release, Snowflake supports the VARIANT data type on Iceberg tables created from Delta table files in object storage (Delta Direct).

When your Delta tables include `variant` columns, Snowflake maps them to the Snowflake VARIANT data type. You can query semi-structured data using VARIANT functions and dot or bracket notation. Delta Direct tables are read-only in Snowflake.

For supported type mappings, see [Delta data types](/user-guide/tables-iceberg-data-types#label-tables-iceberg-delta-source-data-types).
