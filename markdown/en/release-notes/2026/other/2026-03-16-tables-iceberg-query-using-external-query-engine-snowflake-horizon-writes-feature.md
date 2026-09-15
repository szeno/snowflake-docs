# Mar 16, 2026: Apache Iceberg™ tables: Write support by using an external query engine (*Preview*)

You can now write to Snowflake-managed Apache Iceberg™ tables by using any
external query engine that supports the open Iceberg REST protocol, such as Apache Spark™. To ensure this interoperability with
external engines, [Apache Polaris™ (incubating)](https://github.com/apache/polaris) is integrated into Horizon Catalog. You can write to
these tables in a Snowflake account by using a single Horizon Catalog endpoint and you can use your existing users, roles, policies,
and authentication in Snowflake.

For more information, see [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).
