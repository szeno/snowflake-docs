# Configure a catalog integration for files in object storage

Create a catalog integration for Apache Iceberg™ table files or Delta Lake table files in object storage.

After you create a catalog integration, you can [create an Iceberg table](/user-guide/tables-iceberg-create#label-tables-iceberg-create-catalog-int).

## Iceberg files

Create a catalog integration for Iceberg metadata that’s in an external cloud storage location
by setting `OBJECT_STORE` as the `CATALOG_SOURCE` value and `ICEBERG` as the `TABLE_FORMAT`.

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION icebergCatalogInt
  CATALOG_SOURCE = OBJECT_STORE
  TABLE_FORMAT = ICEBERG
  ENABLED = TRUE;
```

## Delta Lake table files

This integration is part of **Delta Direct** in Snowflake: you use it together with
[CREATE ICEBERG TABLE (Delta files in object storage)](/sql-reference/sql/create-iceberg-table-delta) so that Snowflake
can read Delta Lake tables in your bucket and optionally generate Iceberg metadata.

Create a catalog integration for Iceberg tables based on
Delta table files by setting `OBJECT_STORE` as the `CATALOG_SOURCE` value and `DELTA` as the `TABLE_FORMAT`.

- `CATALOG_SOURCE = OBJECT_STORE`
- `TABLE_FORMAT = DELTA`

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION delta_catalog_integration
  CATALOG_SOURCE = OBJECT_STORE
  TABLE_FORMAT = DELTA
  ENABLED = TRUE;
```

Note

Snowflake doesn’t support creating Iceberg tables from Delta table definitions in other catalogs such as Databricks Unity Catalog or AWS Glue Data Catalog.
